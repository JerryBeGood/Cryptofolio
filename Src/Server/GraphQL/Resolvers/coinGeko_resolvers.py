import requests
import json


# coinChartData query resolver
def resolve_coinChartData(obj, info, id, vs_currency, days, interval):

    payload = []

    with requests.get(
            f"https://api.coingecko.com/api/v3/coins/{id}/market_chart?vs_currency={vs_currency}&days={days}&interval={interval}"
    ) as response:

        response_json = json.loads(response.text)

        for element in response_json["prices"]:
            coin_chart_data_chunk = {}
            coin_chart_data_chunk["time_stamp"] = element[0]
            coin_chart_data_chunk["price"] = element[1]
            payload.append(coin_chart_data_chunk)

    return payload


# topCoins query resolver
def resolve_topCoins(obj,
                     info,
                     vs_currency,
                     id=None,
                     symbol=None,
                     name=None,
                     current_price=None,
                     market_cap=None,
                     market_cap_rank=None,
                     price_change_percentage_24h=None,
                     circulating_supply=None,
                     total_supply=None):

    payload = []

    with requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={vs_currency}&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=24h"
    ) as response:
        response_json = json.loads(response.text)

        for asset in response_json:
            coin = {}
            coin['id'] = asset['id']
            coin['symbol'] = asset['symbol']
            coin['name'] = asset['name']
            coin['current_price'] = asset['current_price']
            coin['market_cap'] = asset['market_cap']
            coin['market_cap_rank'] = asset['market_cap_rank']
            coin['price_change_percentage_24h'] = asset[
                'price_change_percentage_24h']
            coin['total_volume'] = asset['total_volume']
            coin['circulating_supply'] = asset['circulating_supply']
            coin['total_supply'] = asset['total_supply']
            payload.append(coin)

    return payload