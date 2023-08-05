from dataclasses import dataclass
from typing import Any

from energytt_platform.api import Endpoint, Context
from energytt_platform.models.auth import InternalToken


class EmptyEndpoint(Endpoint):
    """
    Empty endpoints should always return status 200 and empty body.
    """
    def handle_request(self):
        pass


class EndpointReturnsGeneric(Endpoint):
    """
    Generic endpoint that returns whatever is passed to it's constructor.
    """
    def __init__(self, response: Any):
        self.response = response

    def handle_request(self) -> Any:
        return self.response


class EndpointRaisesGeneric(Endpoint):
    """
    Generic endpoint that raises whatever is passed to it's constructor.
    """
    def __init__(self, response: Any):
        self.response = response

    def handle_request(self) -> Any:
        raise self.response


class EndpointRequiresRequestModel(Endpoint):
    """
    Endpoint that requires an instance of a request model.

    Expected behaviour:
        - The model should be formatted as JSON body
        - "Content-Type" header should be 'application/json'
    """

    @dataclass
    class Request:
        something: str

    def handle_request(self, request: Request):
        return self.Response(
            success=True,
            something='something',
        )


class EndpointReturnsResponseModel(Endpoint):
    """
    Endpoint that returns body as an instance of a response model.

    Expected behaviour:
        - The model should be formatted as JSON body
        - "Content-Type" header should be 'application/json'
    """

    @dataclass
    class Response:
        success: bool
        something: str

    def handle_request(self) -> Response:
        return self.Response(
            success=True,
            something='something',
        )


class EndpointWithRequestAndResponseModels(Endpoint):
    """
    Endpoint that takes a request model, and returns body
    as an instance of a response model.

    Expected behaviour:
        - The model should be formatted as JSON body
        - Content-Type header should be 'application/json'
    """

    @dataclass
    class Request:
        something: str

    @dataclass
    class Response:
        success: bool
        something: str

    def handle_request(self, request: Request) -> Response:
        return self.Response(
            success=True,
            something=request.something,
        )


class EndpointRequiresContextReturnsToken(Endpoint):
    """
    Endpoint that returns context.token as JSON (unmodified).

    Expected behaviour:
        - The token is JSON encoded without mutation
    """

    @dataclass
    class Response:
        token: InternalToken

    def handle_request(self, context: Context) -> Response:
        return self.Response(token=context.token)
