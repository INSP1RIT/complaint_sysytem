import json

from fastapi import HTTPException

import requests
import aiohttp
from decouple import config
import asyncio


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

    # def _get_profile_id(self):
    #     url = "https://api.sandbox.transferwise.tech/v2/profiles"
    #     response = requests.get(url, headers=self.headers)
    #
    #     a = 5

    async def _get_profile_id(self):
        url = f"{self.main_url}/v2/profiles"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    res = await response.json()
                    return [el['id'] for el in res if el["type"] == "PERSONAL"][0]
                raise HTTPException(
                    status_code=500,
                    detail="Payment provider is not available at the moment",
                )

    async def create_quote(self, amount):
        url = f"{self.main_url}/v3/quotes/"

        data = {
            "sourceCurrency": "EUR",
            "targetCurrency": "EUR",
            "sourceAmount": amount,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=json.dumps(data)) as response:
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
            "profile": str(self.profile_id),
            "ownedByCustomer": "false",
            "accountHolderName": full_name,
            "details": {
                "legalType": "PRIVATE",
                "iban": iban
            }
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


if __name__ == "__main__":
    import asyncio

    wise = WiseService()
    res = asyncio.run(
        wise.create_recipient_account(
            "Alex Abisher", "AL35202111090000000001234567"
        )
    )
    print(res)

    # d = asyncio.run(wise._get_profile_id())
