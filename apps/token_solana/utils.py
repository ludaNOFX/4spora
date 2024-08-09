from typing import Dict, Union
import requests


def get_token_price(symbol: str) -> Union[float, None]:
    url: str = f'https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd'
    response: requests.Response = requests.get(url)
    data: Dict[str, Union[Dict[str, Union[str, float]], None]] = response.json()
    price_info: Union[Dict[str, Union[str, float]], None] = data.get(symbol)

    if price_info:
        return price_info.get('usd')

    return None