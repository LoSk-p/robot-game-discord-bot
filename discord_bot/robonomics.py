import json
import typing as tp

from robonomicsinterface import RWS, Account, Launch
from substrateinterface import KeypairType
from tenacity import retry, stop_after_attempt, wait_fixed

from .config.config import ROBOT_ADDRESS, RWS_OWNER_SEED
from .ipfs import IPFSPinner
from .logger import get_logger
from .robonomics_helpers.subscription import DatalogSubscription, TransferSubscription
from .utils import encrypt_message_for_devices, to_thread

logger = get_logger(__name__)


class Robonomics:
    def __init__(self):
        self.rws_owner_account: Account = Account(
            RWS_OWNER_SEED, crypto_type=KeypairType.ED25519
        )
        self.rws_owner_address: str = self.rws_owner_account.get_address()
        self.robot_address: str = ROBOT_ADDRESS
        self.devices_list: tp.List[str] = []

    async def set_new_rws_devices_list(self, new_devices_list: tp.List[str]) -> None:
        logger.info(f"Start setting new RWS devices list: {new_devices_list}")
        self.devices_list = new_devices_list
        await self._set_devices(new_devices_list)

    async def clear_rws_devices(self) -> None:
        logger.info("Start to clesr RWS devices")
        await self._set_devices([])

    async def send_start_command_to_robot(self, seed: str) -> None:
        logger.info(f"Start sending start command to robot with seed: {seed}")
        encrypted_seed = self._encrypt_message(seed)
        logger.info(f"Encrypted command: {encrypted_seed}")
        ipfs_hash = await IPFSPinner().pin(encrypted_seed)
        await self._send_launch(ipfs_hash)
        logger.info("Start command to robot was sent")

    def wait_for_transfer(self, sender_seed: str, callback: tp.Callable) -> tp.Callable:
        sender_address = self._get_address_for_seed(sender_seed)
        logger.info(f"Start waiting for transfer from {sender_address}")
        current_subscription = TransferSubscription(callback, sender_address)
        current_subscription.subscribe()

    def wait_for_datalog(self, callback: tp.Callable) -> tp.Callable:
        logger.info("Start waiting for datalog")
        current_subscription = DatalogSubscription(callback, self.robot_address)
        current_subscription.subscribe()

    @to_thread
    @retry(wait=wait_fixed(5), stop=stop_after_attempt(5))
    def _set_devices(self, devices_list: tp.List[str]) -> None:
        if self.rws_owner_address not in devices_list:
            devices_list.append(self.rws_owner_address)
        logger.info(f"Start setting new devices list {devices_list}")
        rws = RWS(self.rws_owner_account, rws_sub_owner=self.rws_owner_address)
        rws.set_devices(devices_list)
        self.devices_list = devices_list
        logger.info(f"New devices list was successfuly set {devices_list}")

    def _encrypt_message(self, message: tp.Union[tp.Dict, str]) -> tp.Dict[str, str]:
        if isinstance(message, dict):
            message = json.dumps(message)
        encrypted_json = encrypt_message_for_devices(
            message, self.rws_owner_account.keypair, [self.robot_address]
        )
        return encrypted_json

    @to_thread
    @retry(wait=wait_fixed(5), stop=stop_after_attempt(5))
    def _send_launch(self, ipfs_hash: str) -> None:
        logger.info(f"Start sending launch with ipfs hash {ipfs_hash}")
        launch = Launch(self.rws_owner_account, rws_sub_owner=self.rws_owner_address)
        launch.launch(self.robot_address, ipfs_hash)
        logger.info(f"Launch with ipfs hash {ipfs_hash} was sent")

    def _get_address_for_seed(self, seed: str) -> str:
        acc = Account(seed, crypto_type=KeypairType.ED25519)
        return acc.get_address()
