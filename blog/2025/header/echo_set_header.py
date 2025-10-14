from email import message_from_bytes


class EchoSetHeaderSend:
    def __init__(self, send, headers):
        self._send = send
        self._headers = headers

    async def __call__(self, message):
        if message["type"] == "http.response.start":
            message["headers"] = [
                *message.get("headers", ()),
                *self._headers,
            ]
        await self._send(message)


def _generate_echo_headers(scope, echo_set_header):
    for name, value in scope["headers"]:
        if name.decode().lower() == echo_set_header:
            try:
                (header,) = message_from_bytes(value).items()
                echo_name, echo_value = header
                yield echo_name.encode(), echo_value.encode()
            except ValueError:
                pass  # if we can't find a single header, we move on


class EchoSetHeader:
    def __init__(self, app, echo_set_header="x-echo-set-header"):
        self._app = app
        self._echo_set_header = echo_set_header.lower()

    async def __call__(self, scope, receive, send) -> None:
        echo_send = send
        if scope["type"] == "http":
            echo_send = EchoSetHeaderSend(
                send, _generate_echo_headers(scope, self._echo_set_header)
            )
        await self._app(scope, receive, echo_send)
