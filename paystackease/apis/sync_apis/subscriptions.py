"""
Wrapper for Paystack Subscriptions API

The Subscriptions API allows you to create and manage recurring payment on your integration.
"""

from datetime import date
from typing import Optional, Union

from paystackease.src import PayStackResponse, SyncRequestAPI
from paystackease.helpers import subscription_endpoint, convert_to_string, PageModel


class SubscriptionClientAPI(SyncRequestAPI):
    """
    Paystack Subscription API
    Reference: https://paystack.com/docs/api/subscription/
    """

    def create_subscription(
            self,
            customer: str,
            plan_code: str,
            authorization: str,
            start_date: Optional[Union[date, None]] = None,
    ) -> PayStackResponse:
        """
        Create a subscription

        :param: customer: Email or Code of the customer
        :param: plan_code: Code of the plan
        :param: authorization: Code of the authorization
        :param: start_date: Start date of the subscription

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """

        # convert date to string
        start_date = convert_to_string(start_date)

        data = {
            "customer": customer,
            "plan": plan_code,
            "authorization": authorization,
            "start_date": start_date,
        }
        return self._post_request(subscription_endpoint, data=data)

    def list_subscriptions(
            self,
            page_model: Optional[PageModel] = None,
            customer: Optional[Union[int, None]] = None,
            plan_code: Optional[Union[int, None]] = None,
    ) -> PayStackResponse:
        """
        List all the subscriptions

        :param: per_page: Number of records to return per page.
        :param: page: THe number to return
        :param: customer:
        :param: plan_code:

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        params = {
            **page_model.model_dump(by_alias=True, exclude_none=True),
            "customer": customer,
            "plan": plan_code,
        }
        return self._get_request(subscription_endpoint, params=params)

    def fetch_subscription(self, id_or_code: str) -> PayStackResponse:
        """
        Get details of a subscription

        :param: id_or_code: ID or Code of the subscription

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        return self._get_request(f"{subscription_endpoint}{id_or_code}")

    def enable_subscription(self, subscription_code: str, token: str) -> PayStackResponse:
        """
        Enable a subscription

        :param: subscription_code: Code of the subscription
        :param: token: Email token of the customer

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        data = {"code": subscription_code, "token": token}
        return self._post_request(f"{subscription_endpoint}enable", data=data)

    def disable_subscription(self, subscription_code: str, token: str) -> PayStackResponse:
        """
        Disable a subscription

        :param: subscription_code: Code of the subscription
        :param: token: Email token of the customer

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        data = {"code": subscription_code, "token": token}
        return self._post_request(f"{subscription_endpoint}disable", data=data)

    def generate_update_subscription(self, subscription_code: str) -> PayStackResponse:
        """
        Generate a link for updating the card on subscription

        :param: subscription_code: Code of the subscription

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        return self._post_request(f"{subscription_endpoint}{subscription_code}/manage/link")

    def send_update_subscription_link(self, subscription_code: str) -> PayStackResponse:
        """
        Email a customer a link for updating the card on their subscription

        :param: subscription_code: Code of the subscription

        :return: The PayStackResponse from the API
        :rtype: PayStackResponse object
        """
        return self._post_request(f"{subscription_endpoint}{subscription_code}/manage/email")
