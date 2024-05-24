import typing as tp


class DatalogData:
    def __init__(self, data: tp.List):
        self.sender: str = data[0]
        self.timestamp: float = data[1] / 1000
        self.data: str = data[2]


class TransferData:
    def __init__(self, data: tp.List):
        self.sender: str = data["from"]
        self.receiver: str = data["to"]
        self.amount: float = data["amount"] / (10**9)
