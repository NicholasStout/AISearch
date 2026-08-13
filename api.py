class SearXNGApi:
    searxng_url: str
    websession: aiohttp.ClientSession

    def __init__(self, url : str, ws: aiohttp.ClientSession):
        self.searxng_url = url
        self.websession = ws

    async def async_validate(self) -> None:
        async with self.websession.get(self.searxng_url) as response:
            if response.status == 200:
                return
            else:
                raise Exception

    async def search(self, query: str) -> dict:
        params = {"q": query, "format": "json"}
        async with self.websession.get(self.searxng_url+"/search", params=params) as response:
            if not response.status == 200:
                raise Exception

            data = await response.json()
            result = data["results"][0]
            return {"content": result["content"], "source": result["parsed_url"][1]}