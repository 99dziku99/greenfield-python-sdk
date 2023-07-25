from grpclib.client import Channel

from greenfield_python_sdk.protos.greenfield.permission import QueryParamsRequest, QueryParamsResponse, QueryStub


class Permission:
    def __init__(self, channel: Channel):
        self.query_stub = QueryStub(channel)

    async def get_params(self) -> QueryParamsResponse:
        request = QueryParamsRequest()
        response = await self.query_stub.params(request)
        return response
