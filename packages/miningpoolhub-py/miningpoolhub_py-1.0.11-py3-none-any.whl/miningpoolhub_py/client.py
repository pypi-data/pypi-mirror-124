from yarl import URL
from aiohttp import ClientSession, ClientResponse


class MiningPoolHubClient:
    def __init__(self, session: ClientSession, api_key: str):
        self.__session = session
        self.__api_key = {"api_key": api_key}

    async def request(self, method: str, path: URL) -> ClientResponse:
        return await self.__session.request(method, path % self.__api_key)

    async def get_request(self, path: URL) -> ClientResponse:
        return await self.request("get", path)
