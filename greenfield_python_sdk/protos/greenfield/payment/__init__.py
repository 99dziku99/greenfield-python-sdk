# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: greenfield/payment/auto_settle_record.proto, greenfield/payment/base.proto, greenfield/payment/events.proto, greenfield/payment/genesis.proto, greenfield/payment/params.proto, greenfield/payment/payment_account.proto, greenfield/payment/payment_account_count.proto, greenfield/payment/query.proto, greenfield/payment/stream_record.proto, greenfield/payment/tx.proto
# plugin: python-betterproto
# This file has been @generated
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional

import betterproto
import grpclib
from betterproto.grpc.grpclib_server import ServiceBase

from ...cosmos.base.query import v1beta1 as __cosmos_base_query_v1_beta1__

if TYPE_CHECKING:
    import grpclib.server
    from betterproto.grpc.grpclib_client import MetadataLike
    from grpclib.metadata import Deadline


class StreamAccountStatus(betterproto.Enum):
    """StreamAccountStatus defines the status of a stream account"""

    STREAM_ACCOUNT_STATUS_ACTIVE = 0
    """STREAM_ACCOUNT_STATUS_ACTIVE defines the active status of a stream account."""

    STREAM_ACCOUNT_STATUS_FROZEN = 1
    """
    STREAM_ACCOUNT_STATUS_FROZEN defines the frozen status of a stream account.
    A frozen stream account cannot be used as payment address for buckets.
    It can be unfrozen by depositing more BNB to the stream account.
    """


class FeePreviewType(betterproto.Enum):
    FEE_PREVIEW_TYPE_PRELOCKED_FEE = 0
    FEE_PREVIEW_TYPE_UNLOCKED_FEE = 1


@dataclass(eq=False, repr=False)
class AutoSettleRecord(betterproto.Message):
    """
    AutoSettleRecord is the record keeps the auto settle information.
    The EndBlocker of payment module will scan the list of AutoSettleRecord
    and settle the stream account if the timestamp is less than the current time.
    """

    timestamp: int = betterproto.int64_field(1)
    """timestamp is the unix timestamp when the stream account will be settled."""

    addr: str = betterproto.string_field(2)
    """A stream account address"""


@dataclass(eq=False, repr=False)
class OutFlow(betterproto.Message):
    """
    OutFlow defines the accumulative outflow stream rate in BNB
    from a stream account to a Storage Provider
    """

    to_address: str = betterproto.string_field(1)
    """stream account address who receives the flow, usually SP(service provider)"""

    rate: str = betterproto.string_field(2)
    """flow rate"""


@dataclass(eq=False, repr=False)
class StreamRecord(betterproto.Message):
    """Stream Payment Record of a stream account"""

    account: str = betterproto.string_field(1)
    """account address"""

    crud_timestamp: int = betterproto.int64_field(2)
    """latest update timestamp of the stream record"""

    netflow_rate: str = betterproto.string_field(3)
    """
    The per-second rate that an account's balance is changing.
    It is the sum of the account's inbound and outbound flow rates.
    """

    static_balance: str = betterproto.string_field(4)
    """The balance of the stream account at the latest CRUD timestamp."""

    buffer_balance: str = betterproto.string_field(5)
    """
    reserved balance of the stream account
    If the netflow rate is negative, the reserved balance is `netflow_rate *
    reserve_time`
    """

    lock_balance: str = betterproto.string_field(6)
    """
    the locked balance of the stream account after it puts a new object and before the
    object is sealed
    """

    status: "StreamAccountStatus" = betterproto.enum_field(7)
    """the status of the stream account"""

    settle_timestamp: int = betterproto.int64_field(8)
    """the unix timestamp when the stream account will be settled"""

    out_flows: List["OutFlow"] = betterproto.message_field(9)
    """the accumulated outflow rates of the stream account"""


@dataclass(eq=False, repr=False)
class EventPaymentAccountUpdate(betterproto.Message):
    addr: str = betterproto.string_field(1)
    """address of the payment account"""

    owner: str = betterproto.string_field(2)
    """owner address of the payment account"""

    refundable: bool = betterproto.bool_field(3)
    """whether the payment account is refundable"""


@dataclass(eq=False, repr=False)
class EventStreamRecordUpdate(betterproto.Message):
    """Stream Payment Record of a stream account"""

    account: str = betterproto.string_field(1)
    """account address"""

    crud_timestamp: int = betterproto.int64_field(2)
    """latest update timestamp of the stream record"""

    netflow_rate: str = betterproto.string_field(3)
    """
    The per-second rate that an account's balance is changing.
    It is the sum of the account's inbound and outbound flow rates.
    """

    static_balance: str = betterproto.string_field(4)
    """The balance of the stream account at the latest CRUD timestamp."""

    buffer_balance: str = betterproto.string_field(5)
    """
    reserved balance of the stream account
    If the netflow rate is negative, the reserved balance is `netflow_rate *
    reserve_time`
    """

    lock_balance: str = betterproto.string_field(6)
    """
    the locked balance of the stream account after it puts a new object and before the
    object is sealed
    """

    status: "StreamAccountStatus" = betterproto.enum_field(7)
    """the status of the stream account"""

    settle_timestamp: int = betterproto.int64_field(8)
    """the unix timestamp when the stream account will be settled"""

    out_flows: List["OutFlow"] = betterproto.message_field(9)
    """the accumulated outflow rates of the stream account"""


@dataclass(eq=False, repr=False)
class EventForceSettle(betterproto.Message):
    """
    EventForceSettle may be emitted on all Msgs and EndBlocker when a payment account's
    balance or net outflow rate is changed
    """

    addr: str = betterproto.string_field(1)
    """address of the payment account"""

    settled_balance: str = betterproto.string_field(2)
    """
    left balance of the payment account after force settlement
    if the balance is positive, it will go to the governance stream account
    if the balance is negative, it's the debt of the system, which will be paid by the
    governance stream account
    """


@dataclass(eq=False, repr=False)
class EventDeposit(betterproto.Message):
    from_: str = betterproto.string_field(1)
    """from is the the address of the account to deposit from"""

    to: str = betterproto.string_field(2)
    """to is the address of the stream account to deposit to"""

    amount: str = betterproto.string_field(3)
    """amount is the amount to deposit"""


@dataclass(eq=False, repr=False)
class EventWithdraw(betterproto.Message):
    to: str = betterproto.string_field(1)
    """to the address of the receive account"""

    from_: str = betterproto.string_field(2)
    """from is the address of the stream account to withdraw from"""

    amount: str = betterproto.string_field(3)
    """amount is the amount to withdraw"""


@dataclass(eq=False, repr=False)
class EventFeePreview(betterproto.Message):
    """
    emit when upload/cancel/delete object, used for frontend to preview the fee changed
    only emit in tx simulation
    """

    account: str = betterproto.string_field(1)
    fee_preview_type: "FeePreviewType" = betterproto.enum_field(2)
    amount: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class Params(betterproto.Message):
    """Params defines the parameters for the module."""

    reserve_time: int = betterproto.uint64_field(1)
    """
    Time duration which the buffer balance need to be reserved for NetOutFlow e.g. 6
    month
    """

    payment_account_count_limit: int = betterproto.uint64_field(2)
    """The maximum number of payment accounts that can be created by one user"""

    forced_settle_time: int = betterproto.uint64_field(3)
    """
    Time duration threshold of forced settlement.
    If dynamic balance is less than NetOutFlowRate * forcedSettleTime, the account can
    be forced settled.
    """

    max_auto_force_settle_num: int = betterproto.uint64_field(4)
    """the maximum number of accounts that will be forced settled in one block"""

    fee_denom: str = betterproto.string_field(5)
    """The denom of fee charged in payment module"""

    validator_tax_rate: str = betterproto.string_field(6)
    """
    The tax rate to pay for validators in storage payment. The default value is 1%(0.01)
    """


@dataclass(eq=False, repr=False)
class PaymentAccount(betterproto.Message):
    """PaymentAccount defines a payment account"""

    addr: str = betterproto.string_field(1)
    """the address of the payment account"""

    owner: str = betterproto.string_field(2)
    """the owner address of the payment account"""

    refundable: bool = betterproto.bool_field(3)
    """whether the payment account is refundable"""


@dataclass(eq=False, repr=False)
class PaymentAccountCount(betterproto.Message):
    """
    PaymentAccountCount defines the state struct which stores the number of payment
    accounts for an account
    """

    owner: str = betterproto.string_field(1)
    """owner is the account address"""

    count: int = betterproto.uint64_field(2)
    """count is the number of payment accounts for the account"""


@dataclass(eq=False, repr=False)
class GenesisState(betterproto.Message):
    """GenesisState defines the payment module's genesis state."""

    params: "Params" = betterproto.message_field(1)
    stream_record_list: List["StreamRecord"] = betterproto.message_field(2)
    payment_account_count_list: List["PaymentAccountCount"] = betterproto.message_field(3)
    payment_account_list: List["PaymentAccount"] = betterproto.message_field(4)
    auto_settle_record_list: List["AutoSettleRecord"] = betterproto.message_field(5)


@dataclass(eq=False, repr=False)
class QueryParamsRequest(betterproto.Message):
    """QueryParamsRequest is request type for the Query/Params RPC method."""

    pass


@dataclass(eq=False, repr=False)
class QueryParamsResponse(betterproto.Message):
    """QueryParamsResponse is response type for the Query/Params RPC method."""

    params: "Params" = betterproto.message_field(1)
    """params holds all the parameters of this module."""


@dataclass(eq=False, repr=False)
class QueryGetStreamRecordRequest(betterproto.Message):
    account: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class QueryGetStreamRecordResponse(betterproto.Message):
    stream_record: "StreamRecord" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class QueryAllStreamRecordRequest(betterproto.Message):
    pagination: "__cosmos_base_query_v1_beta1__.PageRequest" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class QueryAllStreamRecordResponse(betterproto.Message):
    stream_record: List["StreamRecord"] = betterproto.message_field(1)
    pagination: "__cosmos_base_query_v1_beta1__.PageResponse" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class QueryGetPaymentAccountCountRequest(betterproto.Message):
    owner: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class QueryGetPaymentAccountCountResponse(betterproto.Message):
    payment_account_count: "PaymentAccountCount" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class QueryAllPaymentAccountCountRequest(betterproto.Message):
    pagination: "__cosmos_base_query_v1_beta1__.PageRequest" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class QueryAllPaymentAccountCountResponse(betterproto.Message):
    payment_account_count: List["PaymentAccountCount"] = betterproto.message_field(1)
    pagination: "__cosmos_base_query_v1_beta1__.PageResponse" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class QueryGetPaymentAccountRequest(betterproto.Message):
    addr: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class QueryGetPaymentAccountResponse(betterproto.Message):
    payment_account: "PaymentAccount" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class QueryAllPaymentAccountRequest(betterproto.Message):
    pagination: "__cosmos_base_query_v1_beta1__.PageRequest" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class QueryAllPaymentAccountResponse(betterproto.Message):
    payment_account: List["PaymentAccount"] = betterproto.message_field(1)
    pagination: "__cosmos_base_query_v1_beta1__.PageResponse" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class QueryDynamicBalanceRequest(betterproto.Message):
    account: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class QueryDynamicBalanceResponse(betterproto.Message):
    dynamic_balance: str = betterproto.string_field(1)
    """dynamic balance is static balance + flowDelta"""

    stream_record: "StreamRecord" = betterproto.message_field(2)
    """
    the stream record of the given account, if it does not exist, it will be default
    values
    """

    current_timestamp: int = betterproto.int64_field(3)
    """the timestamp of the current block"""

    bank_balance: str = betterproto.string_field(4)
    """bank_balance is the BNB balance of the bank module"""

    available_balance: str = betterproto.string_field(5)
    """available_balance is bank balance + static balance"""

    locked_fee: str = betterproto.string_field(6)
    """locked_fee is buffer balance + locked balance"""

    change_rate: str = betterproto.string_field(7)
    """change_rate is the netflow rate of the given account"""


@dataclass(eq=False, repr=False)
class QueryGetPaymentAccountsByOwnerRequest(betterproto.Message):
    owner: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class QueryGetPaymentAccountsByOwnerResponse(betterproto.Message):
    payment_accounts: List[str] = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class QueryAllAutoSettleRecordRequest(betterproto.Message):
    pagination: "__cosmos_base_query_v1_beta1__.PageRequest" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class QueryAllAutoSettleRecordResponse(betterproto.Message):
    auto_settle_record: List["AutoSettleRecord"] = betterproto.message_field(1)
    pagination: "__cosmos_base_query_v1_beta1__.PageResponse" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class MsgUpdateParams(betterproto.Message):
    """MsgUpdateParams is the Msg/UpdateParams request type."""

    authority: str = betterproto.string_field(1)
    """
    authority is the address that controls the module (defaults to x/gov unless
    overwritten).
    """

    params: "Params" = betterproto.message_field(2)
    """
    params defines the x/payment parameters to update.
    NOTE: All parameters must be supplied.
    """


@dataclass(eq=False, repr=False)
class MsgUpdateParamsResponse(betterproto.Message):
    """
    MsgUpdateParamsResponse defines the response structure for executing a
    MsgUpdateParams message.
    """

    pass


@dataclass(eq=False, repr=False)
class MsgCreatePaymentAccount(betterproto.Message):
    creator: str = betterproto.string_field(1)
    """creator is the address of the stream account that created the payment account"""


@dataclass(eq=False, repr=False)
class MsgCreatePaymentAccountResponse(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class MsgDeposit(betterproto.Message):
    creator: str = betterproto.string_field(1)
    """
    creator is the message signer for MsgDeposit and the address of the account to
    deposit from
    """

    to: str = betterproto.string_field(2)
    """to is the address of the account to deposit to"""

    amount: str = betterproto.string_field(3)
    """amount is the amount to deposit"""


@dataclass(eq=False, repr=False)
class MsgDepositResponse(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class MsgWithdraw(betterproto.Message):
    creator: str = betterproto.string_field(1)
    """
    creator is the message signer for MsgWithdraw and the address of the receive account
    """

    from_: str = betterproto.string_field(2)
    """from is the address of the account to withdraw from"""

    amount: str = betterproto.string_field(3)
    """amount is the amount to withdraw"""


@dataclass(eq=False, repr=False)
class MsgWithdrawResponse(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class MsgDisableRefund(betterproto.Message):
    owner: str = betterproto.string_field(1)
    """
    owner is the message signer for MsgDisableRefund and the address of the payment
    account owner
    """

    addr: str = betterproto.string_field(2)
    """addr is the address of the payment account to disable refund"""


@dataclass(eq=False, repr=False)
class MsgDisableRefundResponse(betterproto.Message):
    pass


class QueryStub(betterproto.ServiceStub):
    async def params(
        self,
        query_params_request: "QueryParamsRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "QueryParamsResponse":
        return await self._unary_unary(
            "/greenfield.payment.Query/Params",
            query_params_request,
            QueryParamsResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def stream_record(
        self,
        query_get_stream_record_request: "QueryGetStreamRecordRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "QueryGetStreamRecordResponse":
        return await self._unary_unary(
            "/greenfield.payment.Query/StreamRecord",
            query_get_stream_record_request,
            QueryGetStreamRecordResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def stream_record_all(
        self,
        query_all_stream_record_request: "QueryAllStreamRecordRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "QueryAllStreamRecordResponse":
        return await self._unary_unary(
            "/greenfield.payment.Query/StreamRecordAll",
            query_all_stream_record_request,
            QueryAllStreamRecordResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def payment_account_count(
        self,
        query_get_payment_account_count_request: "QueryGetPaymentAccountCountRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "QueryGetPaymentAccountCountResponse":
        return await self._unary_unary(
            "/greenfield.payment.Query/PaymentAccountCount",
            query_get_payment_account_count_request,
            QueryGetPaymentAccountCountResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def payment_account_count_all(
        self,
        query_all_payment_account_count_request: "QueryAllPaymentAccountCountRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "QueryAllPaymentAccountCountResponse":
        return await self._unary_unary(
            "/greenfield.payment.Query/PaymentAccountCountAll",
            query_all_payment_account_count_request,
            QueryAllPaymentAccountCountResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def payment_account(
        self,
        query_get_payment_account_request: "QueryGetPaymentAccountRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "QueryGetPaymentAccountResponse":
        return await self._unary_unary(
            "/greenfield.payment.Query/PaymentAccount",
            query_get_payment_account_request,
            QueryGetPaymentAccountResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def payment_account_all(
        self,
        query_all_payment_account_request: "QueryAllPaymentAccountRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "QueryAllPaymentAccountResponse":
        return await self._unary_unary(
            "/greenfield.payment.Query/PaymentAccountAll",
            query_all_payment_account_request,
            QueryAllPaymentAccountResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def dynamic_balance(
        self,
        query_dynamic_balance_request: "QueryDynamicBalanceRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "QueryDynamicBalanceResponse":
        return await self._unary_unary(
            "/greenfield.payment.Query/DynamicBalance",
            query_dynamic_balance_request,
            QueryDynamicBalanceResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def get_payment_accounts_by_owner(
        self,
        query_get_payment_accounts_by_owner_request: "QueryGetPaymentAccountsByOwnerRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "QueryGetPaymentAccountsByOwnerResponse":
        return await self._unary_unary(
            "/greenfield.payment.Query/GetPaymentAccountsByOwner",
            query_get_payment_accounts_by_owner_request,
            QueryGetPaymentAccountsByOwnerResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def auto_settle_record_all(
        self,
        query_all_auto_settle_record_request: "QueryAllAutoSettleRecordRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "QueryAllAutoSettleRecordResponse":
        return await self._unary_unary(
            "/greenfield.payment.Query/AutoSettleRecordAll",
            query_all_auto_settle_record_request,
            QueryAllAutoSettleRecordResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class MsgStub(betterproto.ServiceStub):
    async def update_params(
        self,
        msg_update_params: "MsgUpdateParams",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "MsgUpdateParamsResponse":
        return await self._unary_unary(
            "/greenfield.payment.Msg/UpdateParams",
            msg_update_params,
            MsgUpdateParamsResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def create_payment_account(
        self,
        msg_create_payment_account: "MsgCreatePaymentAccount",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "MsgCreatePaymentAccountResponse":
        return await self._unary_unary(
            "/greenfield.payment.Msg/CreatePaymentAccount",
            msg_create_payment_account,
            MsgCreatePaymentAccountResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def deposit(
        self,
        msg_deposit: "MsgDeposit",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "MsgDepositResponse":
        return await self._unary_unary(
            "/greenfield.payment.Msg/Deposit",
            msg_deposit,
            MsgDepositResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def withdraw(
        self,
        msg_withdraw: "MsgWithdraw",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "MsgWithdrawResponse":
        return await self._unary_unary(
            "/greenfield.payment.Msg/Withdraw",
            msg_withdraw,
            MsgWithdrawResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def disable_refund(
        self,
        msg_disable_refund: "MsgDisableRefund",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "MsgDisableRefundResponse":
        return await self._unary_unary(
            "/greenfield.payment.Msg/DisableRefund",
            msg_disable_refund,
            MsgDisableRefundResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class QueryBase(ServiceBase):
    async def params(self, query_params_request: "QueryParamsRequest") -> "QueryParamsResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def stream_record(
        self, query_get_stream_record_request: "QueryGetStreamRecordRequest"
    ) -> "QueryGetStreamRecordResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def stream_record_all(
        self, query_all_stream_record_request: "QueryAllStreamRecordRequest"
    ) -> "QueryAllStreamRecordResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def payment_account_count(
        self,
        query_get_payment_account_count_request: "QueryGetPaymentAccountCountRequest",
    ) -> "QueryGetPaymentAccountCountResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def payment_account_count_all(
        self,
        query_all_payment_account_count_request: "QueryAllPaymentAccountCountRequest",
    ) -> "QueryAllPaymentAccountCountResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def payment_account(
        self, query_get_payment_account_request: "QueryGetPaymentAccountRequest"
    ) -> "QueryGetPaymentAccountResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def payment_account_all(
        self, query_all_payment_account_request: "QueryAllPaymentAccountRequest"
    ) -> "QueryAllPaymentAccountResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def dynamic_balance(
        self, query_dynamic_balance_request: "QueryDynamicBalanceRequest"
    ) -> "QueryDynamicBalanceResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_payment_accounts_by_owner(
        self,
        query_get_payment_accounts_by_owner_request: "QueryGetPaymentAccountsByOwnerRequest",
    ) -> "QueryGetPaymentAccountsByOwnerResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def auto_settle_record_all(
        self, query_all_auto_settle_record_request: "QueryAllAutoSettleRecordRequest"
    ) -> "QueryAllAutoSettleRecordResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_params(self, stream: "grpclib.server.Stream[QueryParamsRequest, QueryParamsResponse]") -> None:
        request = await stream.recv_message()
        response = await self.params(request)
        await stream.send_message(response)

    async def __rpc_stream_record(
        self,
        stream: "grpclib.server.Stream[QueryGetStreamRecordRequest, QueryGetStreamRecordResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.stream_record(request)
        await stream.send_message(response)

    async def __rpc_stream_record_all(
        self,
        stream: "grpclib.server.Stream[QueryAllStreamRecordRequest, QueryAllStreamRecordResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.stream_record_all(request)
        await stream.send_message(response)

    async def __rpc_payment_account_count(
        self,
        stream: "grpclib.server.Stream[QueryGetPaymentAccountCountRequest, QueryGetPaymentAccountCountResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.payment_account_count(request)
        await stream.send_message(response)

    async def __rpc_payment_account_count_all(
        self,
        stream: "grpclib.server.Stream[QueryAllPaymentAccountCountRequest, QueryAllPaymentAccountCountResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.payment_account_count_all(request)
        await stream.send_message(response)

    async def __rpc_payment_account(
        self,
        stream: "grpclib.server.Stream[QueryGetPaymentAccountRequest, QueryGetPaymentAccountResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.payment_account(request)
        await stream.send_message(response)

    async def __rpc_payment_account_all(
        self,
        stream: "grpclib.server.Stream[QueryAllPaymentAccountRequest, QueryAllPaymentAccountResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.payment_account_all(request)
        await stream.send_message(response)

    async def __rpc_dynamic_balance(
        self,
        stream: "grpclib.server.Stream[QueryDynamicBalanceRequest, QueryDynamicBalanceResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.dynamic_balance(request)
        await stream.send_message(response)

    async def __rpc_get_payment_accounts_by_owner(
        self,
        stream: "grpclib.server.Stream[QueryGetPaymentAccountsByOwnerRequest, QueryGetPaymentAccountsByOwnerResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_payment_accounts_by_owner(request)
        await stream.send_message(response)

    async def __rpc_auto_settle_record_all(
        self,
        stream: "grpclib.server.Stream[QueryAllAutoSettleRecordRequest, QueryAllAutoSettleRecordResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.auto_settle_record_all(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/greenfield.payment.Query/Params": grpclib.const.Handler(
                self.__rpc_params,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryParamsRequest,
                QueryParamsResponse,
            ),
            "/greenfield.payment.Query/StreamRecord": grpclib.const.Handler(
                self.__rpc_stream_record,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryGetStreamRecordRequest,
                QueryGetStreamRecordResponse,
            ),
            "/greenfield.payment.Query/StreamRecordAll": grpclib.const.Handler(
                self.__rpc_stream_record_all,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryAllStreamRecordRequest,
                QueryAllStreamRecordResponse,
            ),
            "/greenfield.payment.Query/PaymentAccountCount": grpclib.const.Handler(
                self.__rpc_payment_account_count,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryGetPaymentAccountCountRequest,
                QueryGetPaymentAccountCountResponse,
            ),
            "/greenfield.payment.Query/PaymentAccountCountAll": grpclib.const.Handler(
                self.__rpc_payment_account_count_all,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryAllPaymentAccountCountRequest,
                QueryAllPaymentAccountCountResponse,
            ),
            "/greenfield.payment.Query/PaymentAccount": grpclib.const.Handler(
                self.__rpc_payment_account,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryGetPaymentAccountRequest,
                QueryGetPaymentAccountResponse,
            ),
            "/greenfield.payment.Query/PaymentAccountAll": grpclib.const.Handler(
                self.__rpc_payment_account_all,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryAllPaymentAccountRequest,
                QueryAllPaymentAccountResponse,
            ),
            "/greenfield.payment.Query/DynamicBalance": grpclib.const.Handler(
                self.__rpc_dynamic_balance,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryDynamicBalanceRequest,
                QueryDynamicBalanceResponse,
            ),
            "/greenfield.payment.Query/GetPaymentAccountsByOwner": grpclib.const.Handler(
                self.__rpc_get_payment_accounts_by_owner,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryGetPaymentAccountsByOwnerRequest,
                QueryGetPaymentAccountsByOwnerResponse,
            ),
            "/greenfield.payment.Query/AutoSettleRecordAll": grpclib.const.Handler(
                self.__rpc_auto_settle_record_all,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryAllAutoSettleRecordRequest,
                QueryAllAutoSettleRecordResponse,
            ),
        }


class MsgBase(ServiceBase):
    async def update_params(self, msg_update_params: "MsgUpdateParams") -> "MsgUpdateParamsResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def create_payment_account(
        self, msg_create_payment_account: "MsgCreatePaymentAccount"
    ) -> "MsgCreatePaymentAccountResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def deposit(self, msg_deposit: "MsgDeposit") -> "MsgDepositResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def withdraw(self, msg_withdraw: "MsgWithdraw") -> "MsgWithdrawResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def disable_refund(self, msg_disable_refund: "MsgDisableRefund") -> "MsgDisableRefundResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_update_params(
        self, stream: "grpclib.server.Stream[MsgUpdateParams, MsgUpdateParamsResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.update_params(request)
        await stream.send_message(response)

    async def __rpc_create_payment_account(
        self,
        stream: "grpclib.server.Stream[MsgCreatePaymentAccount, MsgCreatePaymentAccountResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.create_payment_account(request)
        await stream.send_message(response)

    async def __rpc_deposit(self, stream: "grpclib.server.Stream[MsgDeposit, MsgDepositResponse]") -> None:
        request = await stream.recv_message()
        response = await self.deposit(request)
        await stream.send_message(response)

    async def __rpc_withdraw(self, stream: "grpclib.server.Stream[MsgWithdraw, MsgWithdrawResponse]") -> None:
        request = await stream.recv_message()
        response = await self.withdraw(request)
        await stream.send_message(response)

    async def __rpc_disable_refund(
        self,
        stream: "grpclib.server.Stream[MsgDisableRefund, MsgDisableRefundResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.disable_refund(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/greenfield.payment.Msg/UpdateParams": grpclib.const.Handler(
                self.__rpc_update_params,
                grpclib.const.Cardinality.UNARY_UNARY,
                MsgUpdateParams,
                MsgUpdateParamsResponse,
            ),
            "/greenfield.payment.Msg/CreatePaymentAccount": grpclib.const.Handler(
                self.__rpc_create_payment_account,
                grpclib.const.Cardinality.UNARY_UNARY,
                MsgCreatePaymentAccount,
                MsgCreatePaymentAccountResponse,
            ),
            "/greenfield.payment.Msg/Deposit": grpclib.const.Handler(
                self.__rpc_deposit,
                grpclib.const.Cardinality.UNARY_UNARY,
                MsgDeposit,
                MsgDepositResponse,
            ),
            "/greenfield.payment.Msg/Withdraw": grpclib.const.Handler(
                self.__rpc_withdraw,
                grpclib.const.Cardinality.UNARY_UNARY,
                MsgWithdraw,
                MsgWithdrawResponse,
            ),
            "/greenfield.payment.Msg/DisableRefund": grpclib.const.Handler(
                self.__rpc_disable_refund,
                grpclib.const.Cardinality.UNARY_UNARY,
                MsgDisableRefund,
                MsgDisableRefundResponse,
            ),
        }
