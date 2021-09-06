from unittest import TestCase

from src.contracts import Contracts, Contract, NegativeTopNError


class GetTopNOpenContractsTest(TestCase):
    """Tests for get_top_n_open_contracts method."""

    def test_get_top_n_open_contracts(self):
        open_contracts = [
            Contract(3, 3.3),
            Contract(1, 1.1),
            Contract(5, 5.5),
            Contract(2, 2.2),
            Contract(4, 4.4),
        ]
        renegotiated = [4, 2]
        top_n = 3

        actual_open_contracts = Contracts.get_top_n_open_contracts(
            open_contracts, renegotiated, top_n,
        )

        expected_open_contracts = [5, 3, 1]
        self.assertEqual(actual_open_contracts, expected_open_contracts)

    def test_get_top_n_open_contracts_with_negative_n(self):
        open_contracts = [
            Contract(3, 3.3),
            Contract(1, 1.1),
            Contract(5, 5.5),
            Contract(2, 2.2),
            Contract(4, 4.4),
        ]
        renegotiated = [3]
        top_n = -3

        with self.assertRaises(NegativeTopNError):
            Contracts.get_top_n_open_contracts(
                open_contracts, renegotiated, top_n,
            )

    def test_get_top_n_open_contracts_with_n_equal_to_zero(self):
        open_contracts = [
            Contract(3, 3.3),
            Contract(1, 1.1),
            Contract(5, 5.5),
            Contract(2, 2.2),
            Contract(4, 4.4),
        ]
        renegotiated = [4, 2]
        top_n = 0

        actual_open_contracts = Contracts.get_top_n_open_contracts(
            open_contracts, renegotiated, top_n,
        )

        expected_open_contracts = []
        self.assertEqual(actual_open_contracts, expected_open_contracts)

    def test_get_top_n_open_contracts_with_n_greater_than_list_length(self):
        open_contracts = [
            Contract(3, 3.3),
            Contract(1, 1.1),
            Contract(5, 5.5),
            Contract(2, 2.2),
            Contract(4, 4.4),
        ]
        renegotiated = [4, 2]
        top_n = 10

        actual_open_contracts = Contracts.get_top_n_open_contracts(
            open_contracts, renegotiated, top_n,
        )

        expected_open_contracts = [5, 3, 1]
        self.assertEqual(actual_open_contracts, expected_open_contracts)

    def test_get_top_n_open_contracts_with_ordered_debts(self):
        open_contracts = [
            Contract(3, 1.1),
            Contract(1, 2.2),
            Contract(5, 3.3),
            Contract(2, 4.4),
            Contract(4, 5.5),
        ]
        renegotiated = [1, 2]
        top_n = 3

        actual_open_contracts = Contracts.get_top_n_open_contracts(
            open_contracts, renegotiated, top_n,
        )

        expected_open_contracts = [4, 5, 3]
        self.assertEqual(actual_open_contracts, expected_open_contracts)

    def test_get_top_n_open_contracts_with_reverse_ordered_debts(self):
        open_contracts = [
            Contract(4, 5.5),
            Contract(2, 4.4),
            Contract(5, 3.3),
            Contract(1, 2.2),
            Contract(3, 1.1),
        ]
        renegotiated = [1, 4]
        top_n = 3

        actual_open_contracts = Contracts.get_top_n_open_contracts(
            open_contracts, renegotiated, top_n,
        )

        expected_open_contracts = [2, 5, 3]
        self.assertEqual(actual_open_contracts, expected_open_contracts)

    def test_get_top_n_open_contracts_with_empty_contracts_list(self):
        open_contracts = []
        renegotiated = [1, 4]
        top_n = 3

        actual_open_contracts = Contracts.get_top_n_open_contracts(
            open_contracts, renegotiated, top_n,
        )

        expected_open_contracts = []
        self.assertEqual(actual_open_contracts, expected_open_contracts)

    def test_get_top_n_open_contracts_with_empty_renegotiated_list(self):
        open_contracts = [
            Contract(4, 5.5),
            Contract(2, 4.4),
            Contract(5, 3.3),
            Contract(1, 2.2),
            Contract(3, 1.1),
        ]
        renegotiated = []
        top_n = 3

        actual_open_contracts = Contracts.get_top_n_open_contracts(
            open_contracts, renegotiated, top_n,
        )

        expected_open_contracts = [4, 2, 5]
        self.assertEqual(actual_open_contracts, expected_open_contracts)


class ContractTest(TestCase):
    def test_str_representation(self):
        id_ = 1
        debt = 1.1
        contract = Contract(id_, debt)
        expected_str = f'id={id_}, debt={debt}'
        self.assertEqual(expected_str, str(contract))
