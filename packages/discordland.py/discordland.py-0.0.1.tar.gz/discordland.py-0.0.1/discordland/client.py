"""
MIT License

Copyright (c) 2021 Hype3808

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import requests
import aiohttp
from .results import BotInfo
from discordland import results
from .errors import APIError

BASE_URL = "https://discordland.gg"

class Client():
    """
    Synchronous client
    """
    def __init__(self, dland_token: str):
        """
        dland_token = Your Bot's Discord Land Token (NOT DISCORD BOT TOKEN!)
        dland_token can be find in https://discordland.gg/bot/:botid/stats
        """
        self.dland_token = dland_token

    def get_bot_info(self):
        """
        Get the bot's info
        """
        session = requests.Session()
        response = session.get(BASE_URL + f"/api/v1/bots/{self.dland_token}")
        json = response.json()
        if response.status_code != 200:
            raise APIError(f"{response.status_code}: The API is having problem. Join discord.gg/dland for more info")
        if json['code'] != 200:
            raise APIError(f"{json['code']}: {json['message']}")
        return BotInfo(json)

    def get_user_voted(self, user_id: int) -> bool:
        """Check if the user voted for your bot."""
        session = requests.Session()
        response = session.get(BASE_URL + f"/api/v1/bots/{self.dland_token}/{user_id}/has-voted")
        json = response.json()
        if response.status_code != 200:
            raise APIError(f"{response.status_code}: The API is having problem. Join discord.gg/dland for more info")
        status = bool(json['status'])
        return status

class AsyncClient():
    """Asynchronous client"""
    def __init__(self, dland_token: str):
        """
        dland_token = Your Bot's Discord Land Token (NOT DISCORD BOT TOKEN!)
        dland_token can be find in https://discordland.gg/bot/:botid/stats
        """
        self.dland_token = dland_token

    async def get_bot_info(self):
        """
        Get the bot's info
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL + f"/api/v1/bots/{self.dland_token}") as response:
                json = await response.json()
                if response.status != 200:
                    raise APIError(f"{response.status}: The API is having problem. Join discord.gg/dland for more info")
                if json['code'] != 200:
                    raise APIError(f"{json['code']}: {json['message']}")
                await session.close()
                return BotInfo(json)

    async def get_user_voted(self, user_id: int) -> bool:
        """Check if the user voted for your bot."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url=BASE_URL + f"/api/v1/bots/{self.dland_token}/{user_id}/has-voted") as response:
                json = await response.json()
                if response.status != 200:
                    raise APIError(f"{response.status}: The API is having problem. Join discord.gg/dland for more info")
                status = bool(json['status'])
                await session.close()
                return status
