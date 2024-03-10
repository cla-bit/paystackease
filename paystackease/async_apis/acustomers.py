"""
Wrapper for Asynchronous Paystack Customers API.

The Customers API allows you to create and manage customers on your integration.
"""

from datetime import date

from typing import Optional, Dict, Any
from paystackease.abase import AsyncPayStackBaseClientAPI


class AsyncCustomerClientAPI(AsyncPayStackBaseClientAPI):
    """
    Paystack Customer API
    Reference: https://paystack.com/docs/api/customer/
    """

    async def create_customer(
            self,
            email: str,
            first_name: str,
            last_name: str,
            phone: str,
            metadata: Optional[Dict[str, Any]] = None
    ) -> dict:
        """
        Create a customer

        :param: email: The email associated with the customer.
        :param: first_name: The first name of the customer.
        :param: last_name: The last name of the customer.
        :param: phone: The phone number of the customer.
        :param: metadata: The metadata of the customer in JSON format.
                            (Set key as: {"custom_fields": [{ "label": "First Name", "value": "John" }] })

        :return: The response from the API
        :rtype: dict
        """
        data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "metadata": metadata,
        }
        return await self._post_request("/customer", data=data)

    async def validate_customer(
            self,
            email_or_code: str,
            first_name: str,
            last_name: str,
            account_type: str,
            country: str,
            bank_code: str,
            account_number: str,
            bvn: str,
            customer_id_num: Optional[str] = None,
            middle_name: Optional[str] = None
    ) -> dict:
        """
        Validate a customer's identity

        :param: email_or_code: The email or code of the customer.
        :param: first_name: The first name of the customer.
        :param: last_name: The last name of the customer.
        :param: middle_name: The middle name of the customer.
        :param: account_type: The type of account. Only bank_account is currently supported.
        :param: customer_id_num: The customer identification number
        :param: country: The country of the customer. 2-letter country code of identification issuer
        :param: bvn: The Bank Verification Number
        :param: bank_code: The bank code of the customer
        :param: account_number: The account number of the customer

        :return: The response from the API
        :rtype: dict
        """
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "middle_name": middle_name,
            "type": account_type,
            "value": customer_id_num,
            "country": country,
            "bvn": bvn,
            "bank_code": bank_code,
            "account_number": account_number,
        }
        return await self._post_request(f"customer/{email_or_code}/identification", data=data)

    async def whitelist_blacklist_customer(
            self, email_or_code: str, risk_action: Optional[str] = None
    ) -> dict:
        """
        Whitelist or blacklist a customer

        :param: email_or_code: The code or email of the customer.
        :param: risk_action: The action to take on the customer. value: RiskAction.value.value = "allow" pr "deny"

        :return: The response from the API
        :rtype: dict
        """
        data = {"customer": email_or_code, "risk_action": risk_action}
        return await self._post_request("/customer/set_risk_action", data=data)

    async def deactivate_authorization(self, authorization_code: str) -> dict:
        """
        Deactivate an authorization when the card needs to be forgotten

        :param: authorization_code: The authorization code to be deactivated.

        :return: The response from the API
        :rtype: dict
        """
        data = {"authorization_code": authorization_code}
        return await self._post_request("/customer/deactivate_authorization", data=data)

    async def update_customer(
            self,
            customer_code: str,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            phone: Optional[str] = None,
            metadata: Optional[Dict[str, Any]] = None
    ) -> dict:
        """
        Update a customer

        :param: customer_code: The code of the customer.
        :param: first_name: The first name of the customer.
        :param: last_name: The last name of the customer.
        :param: phone: The phone number of the customer.
        :param: metadata: The metadata of the customer in JSON format. {"key1": "value1", "key2": "value2"}

        :return: The response from the API
        :rtype: dict
        """
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "metadata": metadata,
        }
        return await self._put_request(f"/customer/{customer_code}", data=data)

    async def fetch_customer(self, email_or_code: str) -> dict:
        """
        Fetch details of a specific customer

        :param: email_or_code: The email or code of the customer.

        :return: The response from the API
        :rtype: dict
        """
        return await self._get_request(f"/customer/{email_or_code}")

    async def list_customers(
            self,
            per_page: Optional[int] = None,
            page: Optional[int] = None,
            from_date: Optional[date] = None,
            to_date: Optional[date] = None,
    ) -> dict:
        """
        List all customers

        :param: per_page: The number of records to return.
        :param: page: The page number to return.
        :param: from_date: The date to start returning customers from
        :param: to_date: The date to stop returning customers from

        :return: The response from the API
        :rtype: dict
        """

        # convert date  to string
        from_date = self._convert_to_string(from_date)
        to_date = self._convert_to_string(to_date)

        params = {"perPage": per_page, "page": page, "from": from_date, "to": to_date}
        return await self._get_request("/customer", params=params)
