class SearXNGApi:
    searxng_url: str
    websession: aiohttp.ClientSession

    def __init__(self, url : str, ws: aiohttp.ClientSession):
        self.searxng_url = url
        self.websession = ws

    async def async_validate(self) -> None:
        async with self.websession.get(self.searxng_url) as response:
            await validate_response(response)

    async def search(self, query: str) -> dict:
        params = {"q": query, "format": "json"}
        async with self.websession.get(self.searxng_url+"/search", params=params) as response:
            if not response.status == 200:
                raise Exception

            data = await response.json()
            
            answers = data.get("answers", [])
            if answers:
                return {
                    "content": str(answers[0]),
                    "source": "SearXNG",
                }

            # Check infoboxes
            infoboxes = data.get("infoboxes", [])
            if infoboxes:
                ib = infoboxes[0]
                return {
                    "content": ib.get("content", ""),
                    "source": ib.get("engine", "Unknown"),
                }

            # Check search results
            results = data.get("results", [])
            if results:
                result = results[0]
                return {
                    "content": result.get("content", ""),
                    "source": result.get("url", "Unknown"),
                }

            return {"content": "No answers found.", "source": "None"}

async def validate_response(response):
    if response.status != 200:
        raise Exception
    data = await response.text()
    if "SearXNG" not in data:
        raise Exception
    return True
