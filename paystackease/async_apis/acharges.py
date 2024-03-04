""" Wrapper for Asynchronous Paystack Charges API.
The Charge API allows you to configure payment channel of your choice when initiating a payment.
"""

from typing import Optional, Dict
from paystackease.abase import AsyncPayStackBaseClientAPI


class AsyncChargesClientAPI(AsyncPayStackBaseClientAPI):
    """Paystack Charges API
    Reference: https://paystack.com/docs/api/charge/
    """

    async def create_charge(
        self,
        email: str,
        amount: int,
        bank: Optional[Dict[str, str]] = None,
        bank_transfer: Optional[Dict[str, str]] = None,
        qr: Optional[Dict[str, str]] = None,
        authorization_code: Optional[str] = None,
        pin: Optional[int] = None,
        reference: Optional[str] = None,
        ussd: Optional[Dict[str, str]] = None,
        mobile_money: Optional[Dict[str, str]] = None,
        device_id: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> dict:
        """Create a charge
        :param email
        :param amount
        :param bank (don't send if charging an authorization code). Pass {code, account_number} as keys
        :param bank_transfer. Pass {account_expires_at} as key and a datetime iso format as value
        :param qr. Pass {provider} as key
        :param authorization_code (don't send if charging a bank account)
        :param pin (send with a non-reusable authorization code)
        :param reference
        :param ussd (don't send if charging an authorization code, bank or card). Pass {type} as key
        :param mobile_money (don't send if charging an authorization code, bank or card. Only in Ghana and Kenya).
        Pass {phone, provider} as keys and a {phone_number, MobileMoney.value.value} as value
        :param device_id
        :param metadata A JSON object, which is passed as-is to your integration API

        :return: The response from the API
        :rtype: dict
        """
        data = {
            "email": email,
            "amount": amount,
            "bank": bank,
            "bank_transfer": bank_transfer,
            "qr": qr,
            "authorization_code": authorization_code,
            "pin": pin,
            "reference": reference,
            "ussd": ussd,
            "mobile_money": mobile_money,
            "device_id": device_id,
            "metadata": metadata,
        }
        return await self.post_request("/charge", data=data)

    async def submit_pin(self, pin: int, reference: str) -> dict:
        """Submit a PIN for a charge
        :param pin
        :param reference

        :return: The response from the API
        :rtype: dict
        """
        data = {
            "pin": pin,
            "reference": reference,
        }
        return await self.post_request("/charge/submit_pin", data=data)

    async def submit_otp(self, otp: int, reference: str) -> dict:
        """Submit OTP to complete a charge
        :param otp
        :param reference

        :return: The response from the API
        :rtype: dict
        """
        data = {
            "otp": otp,
            "reference": reference,
        }
        return await self.post_request("/charge/submit_otp", data=data)

    async def submit_phone(self, phone: str, reference: str) -> dict:
        """Submit a phone number to complete a charge
        :param phone
        :param reference

        :return: The response from the API
        :rtype: dict
        """
        data = {
            "phone": phone,
            "reference": reference,
        }
        return await self.post_request("/charge/submit_phone", data=data)

    async def submit_birthday(self, birthday: str, reference: str) -> dict:
        """submit birthday when required
        :param birthday:  Birthday submitted by user e.g. 2016-09-21
        :param reference

        :return: The response from the API
        :rtype: dict
        """
        data = {
            "birthday": birthday,
            "reference": reference,
        }
        return await self.post_request("/charge/submit_birthday", data=data)

    async def submit_address(
        self, reference: str, address: str, city: str, state: str, zipcode: str
    ) -> dict:
        """Submit address to continue a charge
        :param reference
        :param address
        :param city
        :param state
        :param zipcode

        :return: The response from the API
        :rtype: dict
        """
        data = {
            "reference": reference,
            "address": address,
            "city": city,
            "state": state,
            "zipcode": zipcode,
        }
        return await self.post_request("/charge/submit_address", data=data)

    async def check_pending_charge(self, reference: str) -> dict:
        """Check pending charge
        :param reference

        :return: The response from the API
        :rtype: dict
        """
        return await self.get_request(f"/charge/{reference}")
