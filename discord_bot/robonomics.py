from robonomicsinterface import Account, RWS, Launch
from substrateinterface import KeypairType
import typing as tp
import json

from .config.config import RWS_OWNER_SEED, ROBOT_ADDRESS
from .utils import to_thread, encrypt_message_for_devices
from .ipfs import IPFSPinner
from .robonomics_helpers.subscription import Subscription, DatalogSubscription, TransferSubscription


class Robonomics:
    def __init__(self):
        self.rws_owner_account: Account = Account(RWS_OWNER_SEED, crypto_type=KeypairType.ED25519)
        self.rws_owner_address: str = self.rws_owner_account.get_address()
        self.robot_address: str = ROBOT_ADDRESS
        self.devices_list: tp.List[str] = []
        self.current_subscription: tp.Optional[Subscription] = None

    async def add_to_rws(self, address: str) -> None:
        new_devices_list = self.devices_list.copy()
        new_devices_list.append(address)
        await self._set_devices(new_devices_list)

    async def clear_rws_devices(self) -> None:
        await self._set_devices([])

    async def send_start_command_to_robot(self, seed: str) -> None:
        encrypted_seed = self._encrypt_message(seed)
        ipfs_hash = await IPFSPinner().pin(encrypted_seed)
        await self._send_launch(ipfs_hash)

    def wait_for_transfer(self, sender_seed: str, callback: tp.Callable) -> tp.Callable:
        sender_address = self._get_address_for_seed(sender_seed)
        self.current_subscription = TransferSubscription(callback, sender_address)
        self.current_subscription.subscribe()
        return self._cancel_subscription
    
    def wait_for_datalog(self, callback: tp.Callable) -> tp.Callable:
        self.current_subscription = DatalogSubscription(callback, self.robot_address)
        self.current_subscription.subscribe()
        return self._cancel_subscription

    @to_thread
    def _update_local_devices_list(self) -> None:
        rws = RWS(self.rws_owner_account)
        devices_list = rws.get_devices()
        if self.rws_owner_address in devices_list:
            devices_list.remove(self.rws_owner_address)
        self.devices_list = devices_list

    @to_thread
    def _set_devices(self, devices_list: tp.List[str]) -> None:
        rws = RWS(self.rws_owner_account, rws_sub_owner=self.rws_owner_address)
        rws.set_devices(devices_list)
        self.devices_list = devices_list

    def _encrypt_message(self, message: tp.Union[tp.Dict, str]) -> tp.Dict[str, str]:
        if isinstance(message, dict):
            message = json.dumps(message)
        encrypted_json = encrypt_message_for_devices(message, self.rws_owner_account.keypair, [self.robot_address])
        return encrypted_json
    
    @to_thread
    def _send_launch(self, ipfs_hash: str) -> None:
        launch = Launch(self.rws_owner_account, rws_sub_owner=self.rws_owner_address)
        launch.launch(self.robot_address, ipfs_hash)

    def _cancel_subscription(self) -> None:
        self.current_subscription.close()
        self.current_subscription = None

    def _get_address_for_seed(self, seed: str) -> str:
        acc = Account(seed, crypto_type=KeypairType.ED25519)
        return acc.get_address()



