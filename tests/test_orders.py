from unittest import TestCase

from src.orders import Orders, MaxTravelAmountLimitExceededError, \
    NegativeOrZeroRequestAmountError


class OrdersTest(TestCase):
    """Tests for combine_orders method."""

    def test_combine_orders(self):
        requests = [80, 30, 90, 15, 10, 5, 70]
        n_max = 100

        min_travels = Orders().combine_orders(requests, n_max)

        expected_travels = 4
        self.assertEqual(expected_travels, min_travels)

    def test_combine_orders_requests_limit_per_travel(self):
        max_requests_per_travel = Orders.MAX_REQUESTS_PER_TRAVEL
        requests = [10] * (max_requests_per_travel + 1)
        n_max = 10 * (max_requests_per_travel + 1)

        min_travels = Orders().combine_orders(requests, n_max)

        expected_travels = 2
        self.assertEqual(expected_travels, min_travels)

    def test_combine_orders_with_amount_greater_than_travel_limit(self):
        requests = [70, 30, 110]
        n_max = 100

        with self.assertRaises(MaxTravelAmountLimitExceededError):
            Orders().combine_orders(requests, n_max)

    def test_combine_orders_with_negative_request_amount(self):
        requests = [70, -30, 10]
        n_max = 100

        with self.assertRaises(NegativeOrZeroRequestAmountError):
            Orders().combine_orders(requests, n_max)

    def test_combine_orders_with_zero_request_amount(self):
        requests = [70, 0, 10]
        n_max = 100

        with self.assertRaises(NegativeOrZeroRequestAmountError):
            Orders().combine_orders(requests, n_max)
