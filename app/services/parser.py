import aiohttp
from ..core.settings import get_settings

settings = get_settings()

headers_wb = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.3',
    'accept-language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'se-ch-ua': 'Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105',
    'cache-control': 'max-age=0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

wb_url = settings.parse_url

async def parser(search_phrase: str) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.get(wb_url.format(search_phrase)) as response:
            response_json = await response.json(content_type='text/plain')
            return int(response_json['data']['total'])