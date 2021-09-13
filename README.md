# bank-services
This project contains utility classes for processing account holder open contracts and physical money requests made by branches.

## 1. Contracts module
This module contains a method that allows the bank to find the greatest debtors who haven't renegotiated their debts yet.

The module contains two classes:
1. _Contract_
2. _Contracts_

The _Contract_ class represents the total debit balance for all open operations of an associate.

On the Contracts class, the _get_top_n_open_contracts_ method receives three parameters:
- _open_contracts_: a list containing _Contract_ objects.
- _renegotiated_contracts_: a list of integers, representing contract ids of associates who have already renegotiated their debts.
- _top_n_: an integer with the number of debtors the method must return.

The method returns a list of integers containing the top_n debtor ids, ordered by debit balance in descending order. A debtor contract is any open contract that is not renegotiated.

## 2. Orders module
This module contains a method that allows the bank to find the minimum number of security van travels needed to attend to money requests made by close branches, in order to save resources.

The _combine_orders_ method on the _Orders_ class receives two parameters:
- _requests_: a list of integers with the amount of money requested by each branch.
- _n_max_: an integer with the maximum amount of money a travel can transport.

The method returns the minimum number of travels required to fulfill all the money requests made by branches.
This method is intended for combining requests of branches that are close to each other, so all requests are considered to be from close branches on every method call.

For security reasons, there is a limit on how many requests a single travel can combine. This limit can be configured on the MAX_REQUESTS_PER_TRAVEL class variable. By default, the limit is set to 2.

## Project requirements
- Python ≥ 3.9.4

## Project setup
To create a python virtual environment:
```console
$ python3.9 -m venv venv
```
To activate the virtual environment:
```console
$ source venv/bin/activate
```
To install project dependencies:
```console
(venv) $ pip install -r requirements.txt
```

## Running the tests
To run all tests:
```console
$ python -m unittest
```
To run a specific test method:
```console
$ python -m unittest tests.<module_name>.<class_name>.<method_name>
```
To run test coverage:
```console
$ coverage run -m unittest
```
To show coverage report:
```console
$ coverage report
```

## Development
TODO:
- _contract-service_: this service will manage the associate contracts.
- _renegotiation-service_: this service will manage contract renegotiation.
- _debtor-service_: this service will manage debtor contracts.
- _order-service_: this service will manage physical money requests from branches.
