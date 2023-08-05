from evmosproto.cosmos.base.v1beta1.coin_pb2 import Coin
from evmosproto.cosmos.tx.signing.v1beta1.signing_pb2 import SIGN_MODE_DIRECT
from evmosproto.cosmos.tx.v1beta1.tx_pb2 import AuthInfo
from evmosproto.cosmos.tx.v1beta1.tx_pb2 import Fee
from evmosproto.cosmos.tx.v1beta1.tx_pb2 import ModeInfo
from evmosproto.cosmos.tx.v1beta1.tx_pb2 import SignDoc
from evmosproto.cosmos.tx.v1beta1.tx_pb2 import SignerInfo
from evmosproto.cosmos.tx.v1beta1.tx_pb2 import TxBody
from evmosproto.cosmos.tx.v1beta1.tx_pb2 import TxRaw
from evmosproto.ethermint.crypto.v1.ethsecp256k1.keys_pb2 import PubKey
from evmosproto.google.protobuf.any_pb2 import Any
from evmoswallet.eth.ethereum import sha3_256
from google.protobuf.message import Message

from evmosgrpc.builder import TransactionBuilder
from evmosgrpc.constants import CHAIN_ID
from evmosgrpc.constants import DENOM
from evmosgrpc.constants import FEE
from evmosgrpc.constants import GAS_LIMIT
from evmosgrpc.constants import MEMO


class Transaction:
    def create_body_bytes(self, msg: Message):
        body = TxBody()
        any = Any()
        any.Pack(msg, type_url_prefix='/')
        body.messages.append(any)
        body.memo = MEMO
        self.body = body

    def create_fee(self):
        coin = Coin()
        coin.denom = DENOM
        coin.amount = FEE
        fee = Fee()
        fee.amount.append(coin)
        fee.gas_limit = int(GAS_LIMIT)
        self.fee = fee

    def create_signer_info(self):
        signer_info = SignerInfo()
        pub_key = PubKey()
        pub_key.key = self.builder.wallet.public_key
        public_key = Any()
        public_key.Pack(pub_key, type_url_prefix='/')
        signer_info.public_key.CopyFrom(public_key)

        a = ModeInfo()
        single = ModeInfo.Single()
        single.mode = SIGN_MODE_DIRECT
        a.single.CopyFrom(single)
        signer_info.mode_info.CopyFrom(a)
        signer_info.sequence = int(self.builder.sequence)

        self.signer_info = signer_info

    def create_auth_info_bytes(self):
        auth_info = AuthInfo()
        auth_info.signer_infos.append(self.signer_info)
        auth_info.fee.CopyFrom(self.fee)
        self.info = auth_info

    def create_signatures(self):
        doc = SignDoc()
        doc.body_bytes = self.body.SerializeToString()
        doc.auth_info_bytes = self.info.SerializeToString()
        doc.chain_id = CHAIN_ID
        doc.account_number = int(self.builder.account_number)
        to_sign = doc.SerializeToString()
        to_sign = sha3_256(to_sign).digest()
        self.signature = self.builder.wallet.sign(to_sign)

    def create_tx_raw(self):
        tx = TxRaw()
        tx.body_bytes = self.body.SerializeToString()
        tx.auth_info_bytes = self.info.SerializeToString()
        tx.signatures.append(self.signature)
        return tx

    def generate_tx(self, builder: TransactionBuilder, msg: Message):
        self.builder = builder
        self.create_body_bytes(msg)
        self.create_fee()
        self.create_signer_info()
        self.create_auth_info_bytes()
        self.create_signatures()
        return self.create_tx_raw()
