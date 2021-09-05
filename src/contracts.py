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


class Contracts:
    @staticmethod
    def get_top_n_open_contracts(open_contracts: list[Contract],
                                 renegotiated_contracts: list[int],
                                 top_n: int) -> list[int]:
        """Returns the ids of the top_n greatest debtor contracts which are not
        renegotiated.

        Args:
            open_contracts: a list of Contract objects.
            renegotiated_contracts: a list with the ids of Contracts which are
             renegotiated.
            top_n: the number of Contract ids to be returned.

        Returns:
            A list with Contract ids of the top_n greatest debtors.

        Raises:
            NegativeTopNError: If top_n is negative.
        """

        if top_n < 0:
            raise NegativeTopNError('top_n must be greater than 0.')

        open_contracts.sort(key=lambda contract: contract.debt, reverse=True)
        return [contract.id for contract in open_contracts if
                contract.id not in renegotiated_contracts][:top_n]


class NegativeTopNError(Exception):
    pass
