class Contract:
    """Open contract with the associate id and the total debit balance of all
    open overdue operations.

    Attributes:
        id: the account holder identifier.
        debt: the total debit balance of all operations.
    """
    def __init__(self, id_: int, debt: float) -> None:
        self.id = id_
        self.debt = debt

    def __str__(self) -> str:
        return 'id={}, debt={}'.format(self.id, self.debt)
