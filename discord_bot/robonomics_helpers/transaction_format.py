import typing as tp

class DatalogData:
    def __init__(self, data: tp.List[str, int]):
        self.sender: str = data[0]
        self.timestamp: float = data[1]/1000
        self.data: str = data[2]

class TransferData:
    def __init__(self, data: tp.List[str, int]):
        self.sender: str = data[0]
        self.receiver: str = data[1]
        self.amount: float = data[2]/(10**6)