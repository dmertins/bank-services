class Orders:
    MAX_REQUESTS_PER_TRAVEL = 2

    def combine_orders(self, requests: list[int], n_max: int) -> int:
        """Return the minimum number of travels to fulfill the money requests
        made by close branches.
        The maximum allowed requests per travel is limited by the
        MAX_REQUESTS_PER_TRAVEL class variable.

        Args:
            requests: a list of integers containing the amount requested by each
             branch.

            n_max: maximum amount allowed for each travel.

        Returns:
            The minimum number of travels.

        Raises:
            MaxTravelAmountLimitExceededError: If a request amount exceeds
             n_max.
            NegativeOrZeroRequestAmountError: If a request amount is
             non-positive integer.
        """
        max_requests_per_travel = self.MAX_REQUESTS_PER_TRAVEL
        number_of_travels = 0

        requests.sort(reverse=True)

        while requests:
            validate_amount(requests[0], n_max)

            travel_amount = requests.pop(0)
            number_of_travels += 1
            requests_in_travel = 1

            for amount in requests.copy():
                validate_amount(amount, n_max)

                if (travel_amount == n_max or
                        requests_in_travel == max_requests_per_travel):
                    break

                if travel_amount + amount <= n_max:
                    travel_amount += amount
                    requests.remove(amount)
                    requests_in_travel += 1

        return number_of_travels


def validate_amount(amount: int, limit: int) -> None:
    if amount > limit:
        msg = (f'Request amount exceeds max allowed limit: '
               f'limit={limit}.')
        raise MaxTravelAmountLimitExceededError(msg)

    if amount <= 0:
        msg = f'Request amount must be positive (amount={amount}.)'
        raise NegativeOrZeroRequestAmountError(msg)


class ValidationError(Exception):
    """Validation exceptions base class."""
    pass


class MaxTravelAmountLimitExceededError(ValidationError):
    """Request amount exceeds max allowed limit per travel."""
    pass


class NegativeOrZeroRequestAmountError(ValidationError):
    """Request amount is less than or equal to zero."""
    pass
