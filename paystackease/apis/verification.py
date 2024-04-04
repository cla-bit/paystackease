"""
Wrapper for Paystack Verification APIs
\
The Verification API allows you to perform KYC processes.
"""
from requests import Response
from paystackease._base import PayStackBaseClientAPI


class VerificationClientAPI(PayStackBaseClientAPI):
    """
    Paystack Verification API
    Reference: https://paystack.com/docs/api/verification/
    """

    def resolve_account(self, account_number: str, bank_code: str) -> Response:
        """
        Confirm an account belongs to the right customer.
        This feature is available to business in Nigeria and Ghana.

        :param: account_number: The account number to verify
        :param: bank_code: The bank code to verify

        :return: The response from the API
        :rtype: Response object
        """
        params = {"account_number": account_number, "bank_code": bank_code}
        return self._get_request("/bank/resolve", params=params)

    def validate_account(
            self,
            account_name: str,
            account_number: str,
            account_type: str,
            bank_code: str,
            country_code: str,
            document_type: str,
            document_number: str,
    ) -> Response:
        """
        Confirm the authenticity of a customer's account number before sending money.
        This feature is only available to businesses in South Africa.

        :param: account_name: The account name to validate: first and last name
        :param: account_number: The account number to validate
        :param: account_type: The account type to validate: personal or business
        :param: bank_code: The bank code to validate
        :param: country_code: The country code to validate
        :param: document_type: The customer's mode of identity:
                                identityNumber, passportNumber or businessRegistrationNumber
        :param: document_number: The customer's document number

        :return: The response from the API
        :rtype: Response object
        """
        data = {
            "account_name": account_name,
            "account_number": account_number,
            "account_type": account_type,
            "bank_code": bank_code,
            "country_code": country_code,
            "document_type": document_type,
            "document_number": document_number,
        }
        return self._post_request("/bank/validate", data=data)

    def resolve_card_bin(self, bin_code: str) -> Response:
        """
        Resolve a card BIN

        :param: bin_code: First 6 characters of card

        :return: The response from the API
        :rtype: Response object
        """
        return self._get_request(f"/decision/bin/{bin_code}")
