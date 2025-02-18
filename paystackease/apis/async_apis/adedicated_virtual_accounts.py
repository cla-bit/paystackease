"""
Wrapper for Asynchronous Paystack Dedicated Virtual Account API

The Dedicated Virtual Account API enables Nigerian merchants to manage unique payment accounts of their customers.
"""

from datetime import date
from typing import Optional, Union

from paystackease.src import AsyncRequestAPI, PayStackResponse
from paystackease.helpers import Currency, CustomerDetails, dvd_endpoint, convert_to_string


class AsyncDedicatedVirtualAccountClientAPI(AsyncRequestAPI):
    """
    Paystack Dedicated Virtual Account API
    Reference: https://paystack.com/docs/api/dedicated-virtual-account/

    note::
        Ensure Dedicated NUBAN is available for your business. Contact Paystack Support
    """

    async def create_virtual_account(
            self,
            customer_id_or_code: str,
            preferred_bank: Optional[Union[str, None]] = None,
            subaccount: Optional[Union[str, None]] = None,
            split_code: Optional[Union[str, None]] = None,
            customer: Optional[CustomerDetails] = None,
    ) -> PayStackResponse:
        """
        Create a dedicated virtual account for existing customers.
        Currently, support Wema Bank and Titan Paystack.

        :param: customer_id_or_code: The customer's ID or Code
        :param: preferred_bank: Preferred bank slug for the virtual account. Eg: "wema-bank"

        note::

             currently support Wema Bank and Titan Paystack.

        :param: subaccount: Subaccount code of the account you want to split the transaction.
        :param: split_code: Split code
        :param: first_name: First name of the customer
        :param: last_name: Last name of the customer
        :param: phone: Phone number of the customer

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        data = {
            "customer": customer_id_or_code,
            "preferred_bank": preferred_bank,
            "subaccount": subaccount,
            "split_code": split_code,
            **(customer.model_dump(exclude={"middle_name"}) if customer else {})
        }
        return await self._post_request(dvd_endpoint, data=data)

    async def assign_dedicated_virtual_account(
            self,
            email: str,
            customer: CustomerDetails,
            preferred_bank: str,
            country: str,
            account_number: Optional[Union[str, None]] = None,
            bvn: Optional[Union[str, None]] = None,
            bank_code: Optional[Union[str, None]] = None,
            subaccount: Optional[Union[str, None]] = None,
            split_code: Optional[Union[str, None]] = None,
    ) -> PayStackResponse:
        """
        create a customer, validate the customer, and assign a DVA to the customer

        :param: email: The email associated with the customer.
        :param: first_name: The first name of the customer.
        :param: last_name: The last name of the customer.
        :param: phone: The phone number of the customer.
        :param: preferred_bank: Preferred bank slug for the virtual account. Eg: "wema-bank"

        note::

             currently support Wema Bank and Titan Paystack.

        :param: country: The country of the customer. 2-letter country code of identification issuer

        note::

             currently accepts NG only.

        :param: account_number: The account number of the customer
        :param: bvn: The Bank Verification Number
        :param: bank_code: The bank code of the customer
        :param: subaccount: Subaccount code of the account you want to split the transaction.
        :param: split_code: Split code

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        data = {
            "email": email,
            **(customer.model_dump(exclude={"middle_name"}) if customer else {}),
            "preferred_bank": preferred_bank,
            "country": country,
            "account_number": account_number,
            "bvn": bvn,
            "bank_code": bank_code,
            "subaccount": subaccount,
            "split_code": split_code,
        }
        return await self._post_request(dvd_endpoint, data=data)

    async def list_dedicated_account(
            self,
            active: Optional[Union[bool, None]] = True,
            currency: Optional[Union[Currency, None]] = None,
            provider_slug: Optional[Union[str, None]] = None,
            bank_id: Optional[Union[str, None]] = None,
            customer_id: Optional[Union[str, None]] = None,
    ) -> PayStackResponse:
        """
        List dedicated accounts

        :param: active: Shows the status of the dedicated virtual account
        :param: currency: Currency of the dedicated virtual account
        :param: provider_slug: Provider slug in lowercase eg: wema-bank
        :param: bank_id: Bank ID of the dedicated virtual account eg: 035
        :param: customer_id: Customer ID of the dedicated virtual account

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        # convert date to string
        active = convert_to_string(active)

        params = {
            "active": active,
            "currency": currency,
            "provider_slug": provider_slug,
            "bank_id": bank_id,
            "customer": customer_id,
        }
        return await self._get_request(dvd_endpoint, params=params)

    async def fetch_dedicated_account(self, dedicated_account_id: int) -> PayStackResponse:
        """
        Get details of a dedicated virtual account

        :param: dedicated_account_id: Dedicated account ID

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        return await self._get_request(f"{dvd_endpoint}{dedicated_account_id}")

    async def requery_dedicated_account(
            self,
            account_number: Optional[Union[str, None]] = None,
            provider_slug: Optional[Union[str, None]] = None,
            date_transfer: Optional[Union[date, None]] = None,
    ) -> PayStackResponse:
        """
        Requery a dedicated virtual account for new transactions

        :param: account_number: Virtual Account number to requery
        :param: provider_slug: Provider slug in lowercase eg: wema-bank
        :param: date_transfer: Date of when the transfer was made

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """

        # convert date to string
        date_transfer = convert_to_string(date_transfer)

        params = {
            "account_number": account_number,
            "provider_slug": provider_slug,
            "date": date_transfer,
        }
        return await self._get_request(f"{dvd_endpoint}requery", params=params)

    async def deactivate_dedicated_account(self, dedicated_account_id: int) -> PayStackResponse:
        """
        Deactivate a dedicated virtual account

        :param: dedicated_account_id: Dedicated account ID

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        return await self._delete_request(f"{dvd_endpoint}{dedicated_account_id}")

    async def split_dedicated_account(
            self,
            customer_id_or_code: str,
            subaccount: Optional[Union[str, None]] = None,
            split_code: Optional[Union[str, None]] = None,
            preferred_bank: Optional[Union[str, None]] = None,
    ) -> PayStackResponse:
        """
        Split a dedicated virtual account transaction with one or more accounts

        :param: customer_id_or_code: Customer's ID or Code
        :param: subaccount: Subaccount code of the account you want to split the transaction
        :param: split_code: Split code
        :param: preferred_bank: Preferred bank for the virtual account

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        data = {
            "customer": customer_id_or_code,
            "preferred_bank": preferred_bank,
            "subaccount": subaccount,
            "split_code": split_code,
        }
        return await self._post_request(f"{dvd_endpoint}split", data=data)

    async def remove_split_dedicated_account(self, account_number: str) -> PayStackResponse:
        """
        Remove a split dedicated virtual account

        :param: account_number: the account number of the dedicated virtual account

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        data = {
            "account_number": account_number,
        }
        return await self._delete_request(f"{dvd_endpoint}split", data=data)

    async def fetch_bank_providers(self) -> PayStackResponse:
        """
        Fetch bank providers

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        return await self._get_request(f"{dvd_endpoint}available_providers")
