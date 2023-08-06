import logging
from dataclasses import dataclass
from uuid import UUID, uuid4

from starlette.datastructures import Headers
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from asgi_correlation_id.context import correlation_id

logger = logging.getLogger('asgi_correlation_id')


def is_valid_uuid(uuid_: str) -> bool:
    """
    Check whether a string is a uuid.
    """
    try:
        return bool(UUID(uuid_, version=4))
    except ValueError:
        return False


@dataclass()
class CorrelationIdMiddleware:
    app: ASGIApp
    uuid_length: int = 32
    validate_guid: bool = True
    correlation_id_header_name: str = 'Correlation-ID'

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)

        header_value = Headers(scope=scope).get(self.correlation_id_header_name.lower())

        if not header_value or (self.validate_guid and not is_valid_uuid(header_value)):
            logger.warning('Generating new UUID after receiving invalid header value: %s', header_value)
            correlation_id.set(uuid4().hex[: self.uuid_length])
        else:
            correlation_id.set(header_value[: self.uuid_length])

        async def handle_outgoing_request(message: Message) -> None:
            if message['type'] == 'http.response.start':
                headers = {k.decode(): v.decode() for (k, v) in message['headers']}
                headers[self.correlation_id_header_name] = correlation_id.get()
                headers['Access-Control-Expose-Headers'] = self.correlation_id_header_name
                response_headers = Headers(headers=headers)
                message['headers'] = response_headers.raw

            await send(message)

        return await self.app(scope, receive, handle_outgoing_request)
