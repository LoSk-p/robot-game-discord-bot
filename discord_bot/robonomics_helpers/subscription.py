import abc
import typing as tp
from robonomicsinterface import Subscriber, SubEvent, Account

from .transaction_format import TransferData, DatalogData

class Subscription(abc.ABC):
    def __init__(self, callback: tp.Callable, sub_event: SubEvent) -> None:
        self.callback = callback
        self.sub_event = sub_event
        self.subscriber = None

    def subscribe(self) -> None:
        self.subscriber = Subscriber(Account(), self.sub_event, self._subscription_handler)

    def close(self) -> None:
        if self.subscriber is not None:
            self.subscriber.cancel()

    @abc.abstractmethod
    def _subscription_handler(self, data: tp.Tuple[str, int]) -> None: pass

class TransferSubscription(Subscription):
    def __init__(self, callback: tp.Callable, sender: str) -> None:
        super().__init__(callback, SubEvent.Transfer)
        self.sender = sender

    def _subscription_handler(self, data: tp.Tuple[str | int]) -> None:
        transfer_data = TransferData(data)
        if transfer_data.sender == self.sender:
            print(f"{transfer_data.amount} XRT was sent from {self.sender} to {transfer_data.receiver}")
            self.callback(transfer_data.receiver)

class DatalogSubscription(Subscription):
    def __init__(self, callback: tp.Callable, robot_aadress: str) -> None:
        super().__init__(callback, SubEvent.NewRecord)
        self.robot_address = robot_aadress

    def _subscription_handler(self, data: tp.Tuple[str | int]) -> None:
        datalog_data = DatalogData(data)
        if datalog_data.sender == self.robot_address:
            print("Datalog was sent from Robot account")
            self.callback()