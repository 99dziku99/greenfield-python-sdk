import binascii
from datetime import datetime, timedelta
from typing import Optional, Tuple

from betterproto.lib.google.protobuf import Any as AnyMessage

from greenfield_python_sdk.blockchain_client import BlockchainClient
from greenfield_python_sdk.greenfield.account import Account
from greenfield_python_sdk.greenfield.basic import Basic
from greenfield_python_sdk.models.eip712_messages.proposal.proposal_url import PROPOSAL
from greenfield_python_sdk.models.eip712_messages.staking.staking_url import (
    CREATE_VALIDATOR,
    PUBKEY,
    STAKE_AUTHORIZATION,
)
from greenfield_python_sdk.protos.cosmos.authz.v1beta1 import Grant, MsgGrant
from greenfield_python_sdk.protos.cosmos.base.v1beta1 import Coin
from greenfield_python_sdk.protos.cosmos.crypto.ed25519 import PubKey
from greenfield_python_sdk.protos.cosmos.gov.v1 import MsgSubmitProposal
from greenfield_python_sdk.protos.cosmos.slashing.v1beta1 import MsgImpeach, MsgUnjail
from greenfield_python_sdk.protos.cosmos.staking.v1beta1 import (
    AuthorizationType,
    CommissionRates,
    Description,
    MsgBeginRedelegate,
    MsgCancelUnbondingDelegation,
    MsgCreateValidator,
    MsgDelegate,
    MsgEditValidator,
    MsgUndelegate,
    QueryValidatorsRequest,
    QueryValidatorsResponse,
    StakeAuthorization,
    StakeAuthorizationValidators,
)
from greenfield_python_sdk.protos.cosmos.tx.v1beta1 import GetTxRequest
from greenfield_python_sdk.storage_client import StorageClient


class Validator:
    blockchain_client: BlockchainClient
    storage_client: StorageClient
    basic: Basic
    account: Account

    def __init__(self, blockchain_client, storage_client, basic, account):
        self.blockchain_client = blockchain_client
        self.storage_client = storage_client
        self.basic = basic
        self.account = account

    async def list_validators(self, status: Optional[str] = None) -> QueryValidatorsResponse:
        request = QueryValidatorsRequest(status=status)
        return await self.blockchain_client.cosmos.staking.get_validators(request)

    async def create_validator(
        self,
        description: Description,
        commission: CommissionRates,
        min_self_delegation_amount: str,
        validator_address: str,
        ed25519_pub_key: bytes,
        delegator_address: str,
        relayer_address: str,
        challenger_address: str,
        bls_key: str,
        proposal_deposit_amount: str,
        proposal_title: str,
        proposal_summary: str,
        proposal_meta_data: str,
    ) -> Tuple[str, str]:
        gov_account = await self.account.get_module_account_by_name("gov")
        pubkey = AnyMessage(type_url=PUBKEY, value=bytes(PubKey(key=binascii.unhexlify(ed25519_pub_key))))
        value = Coin(denom="BNB", amount=proposal_deposit_amount)
        message = MsgCreateValidator(
            description=description,
            commission=commission,
            min_self_delegation=min_self_delegation_amount,
            delegator_address=delegator_address,
            validator_address=validator_address,
            pubkey=pubkey,
            value=value,
            from_=gov_account.base_account.address,
            relayer_address=relayer_address,
            challenger_address=challenger_address,
            bls_key=bls_key,
        )

        wrapped_message = AnyMessage(type_url=CREATE_VALIDATOR, value=bytes(message))
        msg_submit_proposal = MsgSubmitProposal(
            initial_deposit=[Coin(denom="BNB", amount=str(proposal_deposit_amount))],
            proposer=self.storage_client.key_manager.address,
            metadata=proposal_meta_data,
            title=proposal_title,
            summary=proposal_summary,
            messages=[wrapped_message],
        )

        hash = await self.blockchain_client.broadcast_message(
            message=msg_submit_proposal,
            type_url=PROPOSAL,
        )
        await self.basic.wait_for_tx(hash)

        request = GetTxRequest(hash=hash)
        resp = await self.blockchain_client.cosmos.tx.get_tx(request)

        for logs in resp.tx_response.logs:
            for events in logs.events:
                for attributes in events.attributes:
                    if attributes.key == "proposal_id":
                        proposal_id = int(attributes.value)
                        return proposal_id, hash
        raise Exception("Proposal ID not found")

    async def edit_validator(
        self,
        description: Description,
        rate: str,
        min_self_delegation: str,
        relayer_address: str,
        challenger_address: str,
        bls_key: str,
    ) -> str:
        message = MsgEditValidator(
            description=description,
            validator_address=self.storage_client.key_manager.address,
            commission_rate=rate,
            min_self_delegation=min_self_delegation,
            relayer_address=relayer_address,
            challenger_address=challenger_address,
            bls_key=bls_key,
        )
        hash = await self.blockchain_client.broadcast_message(
            message=message,
            type_url="/cosmos.staking.v1beta1.MsgEditValidator",
        )

        return hash

    async def delegate_validator(self, validator_address: str, amount: str) -> str:
        message = MsgDelegate(
            delegator_address=self.storage_client.key_manager.address,
            validator_address=validator_address,
            amount=Coin(denom="BNB", amount=amount),
        )
        hash = await self.blockchain_client.broadcast_message(
            message=message,
            type_url="/cosmos.staking.v1beta1.MsgDelegate",
        )

        return hash

    async def begin_redelegate(self, validator_src_address: str, validator_dest_address: str, amount: str) -> str:
        message = MsgBeginRedelegate(
            delegator_address=self.storage_client.key_manager.address,
            validator_src_address=validator_src_address,
            validator_dst_address=validator_dest_address,
            amount=Coin(denom="BNB", amount=amount),
        )
        hash = await self.blockchain_client.broadcast_message(
            message=message,
            type_url="/cosmos.staking.v1beta1.MsgBeginRedelegate",
        )

        return hash

    async def undelegate(self, validator_address: str, amount: str) -> str:
        message = MsgUndelegate(
            delegator_address=self.storage_client.key_manager.address,
            validator_address=validator_address,
            amount=Coin(denom="BNB", amount=amount),
        )
        hash = await self.blockchain_client.broadcast_message(
            message=message,
            type_url="/cosmos.staking.v1beta1.MsgUndelegate",
        )

        return hash

    async def cancel_unbonding_delegation(self, validator_address: str, creation_height: int, amount: str) -> str:
        message = MsgCancelUnbondingDelegation(
            delegator_address=self.storage_client.key_manager.address,
            validator_address=validator_address,
            creation_height=creation_height,
            amount=Coin(denom="BNB", amount=amount),
        )
        hash = await self.blockchain_client.broadcast_message(
            message=message,
            type_url="/cosmos.staking.v1beta1.MsgCancelUnbondingDelegation",
        )

        return hash

    async def grant_delegation_for_validator(self, delegation_amount: Optional[str] = None) -> str:
        gov_account = await self.account.get_module_account_by_name("gov")

        authorization = StakeAuthorization(
            allow_list=StakeAuthorizationValidators(address=[self.storage_client.key_manager.address]),
            max_tokens=Coin(denom="BNB", amount=delegation_amount) if delegation_amount else None,
            authorization_type=1,
        )
        wrapped_authorization = AnyMessage(type_url=STAKE_AUTHORIZATION, value=bytes(authorization))
        grant = Grant(
            authorization=wrapped_authorization,
        )
        message = MsgGrant(
            granter=self.storage_client.key_manager.address,
            grantee=gov_account.base_account.address,
            grant=grant,
        )

        hash = await self.blockchain_client.broadcast_message(
            message=message,
            type_url="/cosmos.authz.v1beta1.MsgGrant",
        )

        return hash

    async def unjail_validator(self) -> str:
        message = MsgUnjail(
            validator_addr=self.storage_client.key_manager.address,
        )
        hash = await self.blockchain_client.broadcast_message(
            message=message,
            type_url="/cosmos.slashing.v1beta1.MsgUnjail",
        )

        return hash

    async def impeach_validator(self, validator_address: str) -> str:
        message = MsgImpeach(
            from_=self.storage_client.key_manager.address,
            validator_address=validator_address,
        )
        hash = await self.blockchain_client.broadcast_message(
            message=message,
            type_url="/cosmos.slashing.v1beta1.MsgImpeach",
        )

        return hash
