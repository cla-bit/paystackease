"""
Wrapper for Paystack SubAccounts API

The Subaccounts API allows you to create and manage subaccounts on your integration.
Subaccounts can be used to split payment between two accounts (your main account and a subaccount).
"""

from datetime import date
from typing import Optional, Dict, List, Any, Union

from paystackease.src import PayStackResponse, SyncRequestAPI
from paystackease.helpers import SettlementSchedule, subaccount_endpoint, CustomMetaData, convert_to_string, PageModel, \
    DatePageModel


class SubAccountClientAPI(SyncRequestAPI):
    """
    Paystack SubAccount API
    Reference: https://paystack.com/docs/api/subaccount/
    """

    def create_subaccount(
            self,
            business_name: str,
            settlement_bank: str,
            account_number: str,
            percentage_charge: float,
            description: str,
            primary_contact_email: Optional[Union[str, None]] = None,
            primary_contact_name: Optional[Union[str, None]] = None,
            primary_contact_phone: Optional[Union[str, None]] = None,
            metadata: Optional[CustomMetaData] = None,
    ) -> PayStackResponse:
        """
        Create a subaccount

        :param: business_name: The business name of the subaccount.
        :param: settlement_bank: Bank Code for the bank
        :param: account_number: The account number of the subaccount.
        :param: percentage_charge: The percentage charge receives from each payment made to the subaccount
        :param: description: The description of the subaccount.
        :param: primary_contact_email: A contact email for the subaccount
        :param: primary_contact_name: A name for the contact person for this subaccount
        :param: primary_contact_phone: A phone number to call for this subaccount
        :param: metadata: Stringified JSON object. {"custom_fields": [{"name": "value"}]}

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        data = {
            "business_name": business_name,
            "settlement_bank": settlement_bank,
            "account_number": account_number,
            "percentage_charge": percentage_charge,
            "description": description,
            "primary_contact_email": primary_contact_email,
            "primary_contact_name": primary_contact_name,
            "primary_contact_phone": primary_contact_phone,
            **(metadata.model_dump() if metadata else {})
        }
        return self._post_request(subaccount_endpoint, data=data)

    def update_subaccount(
            self,
            id_or_code: str,
            business_name: str,
            settlement_bank: str,
            account_number: str,
            active: Optional[Union[bool, None]] = True,
            percentage_charge: Optional[Union[float, None]] = None,
            description: Optional[Union[str, None]] = None,
            primary_contact_email: Optional[Union[str, None]] = None,
            primary_contact_name: Optional[Union[str, None]] = None,
            primary_contact_phone: Optional[Union[str, None]] = None,
            settlement_schedule: Optional[Union[SettlementSchedule, None]] = SettlementSchedule.AUTO.value,
            metadata: Optional[CustomMetaData] = None,
    ) -> PayStackResponse:
        """
        Update a subaccount

        :param: id_or_code: The id or code of the subaccount.
        :param: business_name: The business name of the subaccount.
        :param: settlement_bank: The settlement bank of the subaccount.
        :param: account_number
        :param: active: [ True or False ]
        :param: percentage_charge
        :param: description
        :param: primary_contact_email
        :param: primary_contact_name
        :param: primary_contact_phone
        :param: settlement_schedule: Values: [ auto, weekly, `monthly`, `manual` ].

        note::
            Auto means payout is T+1
            Manual means payout to the subaccount should only be made when requested. Defaults to auto

        :param: metadata: Stringified JSON object. {"custom_fields": [{"name": "value"}]}

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """

        # convert bool to string
        active = convert_to_string(active)

        data = {
            "business_name": business_name,
            "settlement_bank": settlement_bank,
            "account_number": account_number,
            "active": active,
            "percentage_charge": percentage_charge,
            "description": description,
            "primary_contact_email": primary_contact_email,
            "primary_contact_name": primary_contact_name,
            "primary_contact_phone": primary_contact_phone,
            "settlement_schedule": settlement_schedule,
            **(metadata.model_dump() if metadata else {})
        }
        return self._put_request(f"{subaccount_endpoint}{id_or_code}", data=data)

    def list_subaccounts(
            self,
            page_model: Optional[PageModel] = None,
            date_page: Optional[DatePageModel] = None,
    ) -> PayStackResponse:
        """
        List all subaccounts

        :param: per_page: The number of records to return per page.
        :param: page: The number to retrieve.
        :param: from_date:
        :param: to_date:

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        params = {
            **page_model.model_dump(by_alias=True, exclude_none=True),
            **date_page.model_dump(by_alias=True, exclude_none=True),
        }
        return self._get_request(subaccount_endpoint, params=params)

    def fetch_subaccount(self, id_or_code: str) -> PayStackResponse:
        """
        Fetch details of a specific subaccount

        :param: id_or_code: The id or code of the subaccount.

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        return self._get_request(f"{subaccount_endpoint}{id_or_code}")
