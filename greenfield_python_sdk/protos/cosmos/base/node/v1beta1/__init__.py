# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: cosmos/base/node/v1beta1/query.proto
# plugin: python-betterproto
# This file has been @generated
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Optional

import betterproto
import grpclib
from betterproto.grpc.grpclib_server import ServiceBase

if TYPE_CHECKING:
    import grpclib.server
    from betterproto.grpc.grpclib_client import MetadataLike
    from grpclib.metadata import Deadline


@dataclass(eq=False, repr=False)
class ConfigRequest(betterproto.Message):
    """ConfigRequest defines the request structure for the Config gRPC query."""

    pass


@dataclass(eq=False, repr=False)
class ConfigResponse(betterproto.Message):
    """ConfigResponse defines the response structure for the Config gRPC query."""

    minimum_gas_price: str = betterproto.string_field(1)


class ServiceStub(betterproto.ServiceStub):
    async def config(
        self,
        config_request: "ConfigRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ConfigResponse":
        return await self._unary_unary(
            "/cosmos.base.node.v1beta1.Service/Config",
            config_request,
            ConfigResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class ServiceBase(ServiceBase):
    async def config(self, config_request: "ConfigRequest") -> "ConfigResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_config(self, stream: "grpclib.server.Stream[ConfigRequest, ConfigResponse]") -> None:
        request = await stream.recv_message()
        response = await self.config(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/cosmos.base.node.v1beta1.Service/Config": grpclib.const.Handler(
                self.__rpc_config,
                grpclib.const.Cardinality.UNARY_UNARY,
                ConfigRequest,
                ConfigResponse,
            ),
        }
