from google.auth import transport
import google.cloud.logging
import google.auth
import threading
import time, os, random
import google.oauth2.id_token
from google.cloud.logging_v2.resource import Resource

from uuid import uuid4
from falcon import Request, Response
import re

SERVICE = os.getenv('SERVICE', 'python')
PROJECT_ID = os.getenv('PROJECT_ID', 'santoid-dev')

client = google.cloud.logging.Client()
logger = client.logger(SERVICE)

_TRACE_CONTEXT_HEADER_NAME = "x-cloud-trace-context"
_TRACE_CONTEXT_HEADER_FORMAT = r"(?P<trace_id>[0-9a-f]{32})\/(?P<span_id>[\d]{1,20});o=(?P<trace_flags>\d+)"
_TRACE_CONTEXT_HEADER_RE = re.compile(_TRACE_CONTEXT_HEADER_FORMAT)

RESOURCE = Resource(
    type="cloud_run_revision",
    labels = {
        "configuration_name": SERVICE,
        "project_id": PROJECT_ID,
        "service_name": SERVICE
    }
)


def generate_token(service_url) -> str:
    """
    Genarate id token for authentication service to service using container Service account
    """
    auth_req = transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, service_url)

    return id_token


def get_default_headers(service_url):
    """
    Generate Dictionary header with Authentication param and X-Cloud-Trace-Context param
    for continuous tracing
    """
    return {
        u'Authorization': u'Bearer {id_token}'.format(id_token=generate_token(service_url)),
        u'X-Cloud-Trace-Context': u'{}'.format(logging.get_trace_context()),
    }


class _Context:
    def __init__(self):
        self._thread_local = threading.local()

    @property
    def trace_id(self):
        return getattr(self._thread_local, 'trace_id', None)

    @property
    def trace(self):
        return getattr(self._thread_local, 'trace', None)

    @property
    def span_id(self):
        return getattr(self._thread_local, 'span_id', None)

    @property
    def trace_flags(self):
        return getattr(self._thread_local, 'trace_flags', None)

    @property
    def x_cloud_trace_context(self):
        return getattr(self._thread_local, 'x_cloud_trace_context', None)

    @property
    def endpoint_api_userinfo(self):
        return getattr(self._thread_local, 'endpoint_api_userinfo', None)

    @trace_id.setter
    def trace_id(self, value):
        self._thread_local.trace_id = value

    @trace.setter
    def trace(self, value):
        self._thread_local.trace = value

    @span_id.setter
    def span_id(self, value):
        self._thread_local.span_id = value

    @trace_flags.setter
    def trace_flags(self, value):
        self._thread_local.trace_flags = value

    @x_cloud_trace_context.setter
    def x_cloud_trace_context(self, value):
        self._thread_local.x_cloud_trace_context = value
    
    @endpoint_api_userinfo.setter
    def trace_context(self, value):
        self._thread_local.endpoint_api_userinfo = value


ctx = _Context


def set_request_id(request: Request, response: Response):
    cloud_trace_context = request.get_header('X-CLOUD-TRACE-CONTEXT', None)

    if not cloud_trace_context:
        ctx.trace_id = str(uuid4())
        ctx.span_id = str(random.randint(1000000000000000000, 9999999999999999999))
        ctx.trace_flags = 'o=1'

        ctx.x_cloud_trace_context = \
            f'{ctx.trace_id}/{ctx.span_id};{ctx.trace_flags}'
    else:
        match = re.fullmatch(_TRACE_CONTEXT_HEADER_RE, cloud_trace_context)
        ctx.trace_id = match.group("trace_id")
        ctx.span_id = match.group("span_id")
        ctx.trace_flags = match.group("trace_flags")
    
    ctx.x_cloud_trace_context = cloud_trace_context

    ctx.endpoint_api_userinfo = request.get_header('X-ENDPOINT-API-USERINFO', None)

    request.context.x_cloud_trace_context = cloud_trace_context
    request.context.trace_id = ctx.trace_id
    request.context.span_id = ctx.span_id
    request.context.trace = f"projects/{PROJECT_ID}/traces/{ctx.x_cloud_trace_context}"

    response.set_header('X-CLOUD-TRACE-CONTEXT', cloud_trace_context)
    return


class LogMiddleware(object):

    def process_request(self, request:Request, response:Response):

        set_request_id(request, response)

        host = request.host

        logger.log_struct({"message": f"request stated by {host} to service {SERVICE if SERVICE else 'unknown'}"},
            trace=request.context.trace,
            span_id=request.context.span_id,
            severity="INFO",
            http_request={
                "requestMethod": request.method,
                "requestUrl": request.url,
                "userAgent": request.headers.get('user-agent')
            },
            resource=RESOURCE,
        )


class logging():
    @staticmethod
    def get_trace() -> str:
        if ctx.trace:
            return ctx.trace

        ctx.trace_id = str(uuid4())
        ctx.span_id = str(random.randint(1000000000000000000, 9999999999999999999))
        ctx.trace_flags = 'o=1'

        ctx.x_cloud_trace_context = \
            f'{ctx.trace_id}/{ctx.span_id};{ctx.trace_flags}'
        ctx.trace = f"projects/{PROJECT_ID}/traces/{ctx.trace_id}"
        return ctx.trace

    @staticmethod
    def get_span_id() -> str:
        if ctx.span_id:
            return ctx.span_id
        return str(random.randint(1000000000000000000, 9999999999999999999))

    @staticmethod
    def get_trace_context() -> str:
        return ctx.trace_context

    @staticmethod
    def get_auth_token(service_url: str) -> str:
        return generate_token(service_url)

    @staticmethod
    def get_auth_header(service_url:str) -> dict:
        return (get_default_headers(service_url), ctx.endpoint_api_userinfo)

    @staticmethod
    def info(message: dict):
        logger.log_struct(message, trace=logging.get_trace(), span_id=logging.get_span_id(), resource=RESOURCE, severity="INFO")

    @staticmethod
    def warning(message: dict):
        logger.log_struct(message, trace=logging.get_trace(), span_id=logging.get_span_id(), resource=RESOURCE, severity="WARNING")

    @staticmethod
    def error(message: dict):
        logger.log_struct(message, trace=logging.get_trace(), span_id=logging.get_span_id(), resource=RESOURCE, severity="ERROR")

    @staticmethod
    def critical(message: dict):
        logger.log_struct(message, trace=logging.get_trace(), span_id=logging.get_span_id(), resource=RESOURCE, severity="CRITICAL")

    @staticmethod
    def alert(message: dict):
        logger.log_struct(message, trace=logging.get_trace(), span_id=logging.get_span_id(), resource=RESOURCE, severity="ALERT")

    @staticmethod
    def emergency(message: dict):
        logger.log_struct(message, trace=logging.get_trace(), span_id=logging.get_span_id(), resource=RESOURCE, severity="EMERGENCY")

    @staticmethod
    def debug(message: dict):
        logger.log_struct(message, trace=logging.get_trace(), span_id=logging.get_span_id(), resource=RESOURCE, severity="DEBUG")

    @staticmethod
    def default(message: dict):
        logger.log_struct(message, trace=logging.get_trace(), severity="DEFAULT")

    @staticmethod
    def request(message: dict,
                http_request: dict,
                log_name: str = f"projects/{PROJECT_ID}/logs/santodigital.com.br%2Frequests",
                severity: str = "DEFAULT"):
        logger.log_struct(message,
                          http_request=http_request,
                          trace=logging.get_trace(),
                          span_id=logging.get_span_id(),
                          resource=RESOURCE,
                          severity=severity,
                          log_name=log_name)