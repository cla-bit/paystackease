"""
Wrapper for Paystack Transfer Control APIs

The Transfers Control API allows you manage settings of your transfers.
"""

from paystackease._base import PayStackBaseClientAPI
from paystackease._utils import Response


class TransferControlClientAPI(PayStackBaseClientAPI):
    """
    Paystack Transfers Control API
    Reference: https://paystack.com/docs/api/transfer-control/
    """

    def check_balance(self) -> Response:
        """
        Get the available balance

        :return: The response from the API
        :rtype: Response object
        """
        return self._get_request("/balance")

    def fetch_balance_ledger(self) -> Response:
        """
        Fetch all pay-ins and pay-outs that occurred on your integration

        :return: The response from the API
        :rtype: Response object
        """
        return self._get_request("/balance/ledger")

    def resend_otp(self, transfer_code: str, reason: str) -> Response:
        """
        Generates a new OTP and sends to customer in the event
        they are having trouble receiving one.

        :param: transfer_code: The code of the transfer to finalize
        :param: reason: Either resend_otp or transfer as the value of this field

        :return: The response from the API
        :rtype: Response object
        """
        data = {"transfer_code": transfer_code, "reason": reason}
        return self._post_request("/transfer/resend_otp", data=data)

    def disable_otp(self) -> Response:
        """
        This is used in the event that you want to be able to
         complete transfers programmatically without use of OTPs

        :return: The response from the API
        :rtype: Response object
        """
        return self._post_request("/transfer/disable_otp")

    def finalize_disable_otp(self, otp: str) -> Response:
        """
        Finalize the request to disable OTP on your transfers.

        :param: otp: The OTP sent to the business phone to verify disabling of OTP

        :return: The response from the API
        :rtype: Response object
        """
        data = {"otp": otp}
        return self._post_request("/transfer/disable_otp_finalize", data=data)

    def enable_otp(self) -> Response:
        """
        This is used in the event that you want to stop
        being able to complete transfers programmatically with use of OTPs

        :return: The response from the API
        :rtype: Response object
        """
        return self._post_request("/transfer/enable_otp")
