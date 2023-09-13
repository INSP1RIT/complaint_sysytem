import uuid

import aiohttp
from decouple import config
from fastapi import HTTPException


class WiseService:
    def __init__(self):
        self.main_url = config("WISE_URL")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {config("WISE_TOKEN")}',
        }
        self.key = config("WISE_TOKEN")
        self.secret_key = config("SECRET_KEY")
        self.profile_id = asyncio.run(self._get_profile_id())

    async def _get_profile_id(self):
        url = f"{self.main_url}/v2/profiles"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    res = await response.json()
                    return [el["id"] for el in res if el["type"] == "PERSONAL"][0]
                raise HTTPException(
                    status_code=500,
                    detail="Payment provider is not available at the moment",
                )

    async def create_quote(self, amount):
        url = f"{self.main_url}/v2/quotes/"

        data = {
            "sourceCurrency": "EUR",
            "targetCurrency": "EUR",
            "sourceAmount": amount,
            "profile": self.profile_id,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=data) as response:
                if response.status == 200:
                    res = await response.json()
                    return res["id"]
                raise HTTPException(
                    status_code=500,
                    detail="Payment provider is not available at the moment",
                )

    async def create_recipient_account(self, full_name, iban):
        url = f"{self.main_url}/v1/accounts"
        data = {
            "currency": "EUR",
            "type": "iban",
            "profile": self.profile_id,
            "accountHolderName": full_name,
            "details": {"legalType": "PRIVATE", "iban": iban},
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=data) as response:
                try:
                    if response.status == 200:
                        res = await response.json()
                        return res["id"]
                    raise HTTPException(
                        status_code=500,
                        detail="Payment provider is not available at the moment",
                    )
                except Exception as ex:
                    print(await response.text())

    async def create_transfer(self, target_account_id, quote_id):
        url = f"{self.main_url}/v1/transfers"
        customer_transaction_id = str(uuid.uuid4())

        data = {
            "targetAccount": target_account_id,
            "quoteUuid": quote_id,
            "customerTransactionId": customer_transaction_id,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=data) as response:
                try:
                    if response.status == 200:
                        res = await response.json()
                        return res["id"]
                    raise HTTPException(
                        status_code=500,
                        detail="Payment provider is not available at the moment",
                    )
                except Exception as ex:
                    print(await response.text())

    async def fund_transfer(self, transfer_id):
        url = f"{self.main_url}/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments"
        data = {"type": "BALANCE"}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=data) as response:
                try:
                    if response.status == 201:
                        res = await response.json()
                        return res
                    raise HTTPException(
                        status_code=500,
                        detail="Payment provider is not available at the moment",
                    )
                except Exception as ex:
                    print("SUKA")
                    print(await response.text())


if __name__ == "__main__":
    import asyncio

    wise = WiseService()

    quote_id = asyncio.run(wise.create_quote(10000))
    recipient_id = asyncio.run(
        wise.create_recipient_account("Alex Abisher", "AL35202111090000000001234567")
    )
    transfer_id = asyncio.run(wise.create_transfer(recipient_id, quote_id))

    fund_id = asyncio.run(wise.fund_transfer(transfer_id))

    print(quote_id)
    print(recipient_id)
    print(transfer_id)
    print(fund_id)

    # d = asyncio.run(wise._get_profile_id())
