import requests


# assetChartData query resolver
def resolve_assetChartData(obj, info, id, vs_currency, days, interval):

    payload = []

    with requests.get(
            f"https://api.coingecko.com/api/v3/coins/{id}/market_chart",
            params={
                "vs_currency": vs_currency,
                "days": days,
                "interval": interval
            },
            headers={"accept": "application/json"}) as response:

        response_json = response.json()

        for element in response_json["prices"]:
            asset_chart_data_chunk = {}
            asset_chart_data_chunk["time_stamp"] = element[0]
            asset_chart_data_chunk["price"] = element[1]
            payload.append(asset_chart_data_chunk)

    return payload


# topAssets query resolver
def resolve_topAssets(obj, info, vs_currency, category=None):

    # Payload
    assets = []

    # Request's arguments
    headers = {"accept": "application/json"}
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h",
    }

    if category != None:
        params["category"] = category

    try:
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets",
            params=params,
            headers=headers,
            timeout=(3, 5))
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        return {
            'success': False,
            'errors': "An Http Error occurred:" + repr(errh),
            'assets': None
        }
    except requests.exceptions.ConnectionError as errc:
        return {
            'success': False,
            'errors': "An Error Connecting to the API occurred:" + repr(errc),
            'assets': None
        }
    except requests.exceptions.Timeout as errt:
        return {
            'success': False,
            'errors': "A Timeout Error occurred:" + repr(errt),
            'assets': None
        }
    except requests.exceptions.RequestException as err:
        return {
            'success': False,
            'errors': "An Unknown Error occurred" + repr(err),
            'assets': None
        }
    else:
        response_json = response.json()

        for element in response_json:
            asset = {}
            asset['id'] = element['id']
            asset['symbol'] = element['symbol']
            asset['name'] = element['name']
            asset['current_price'] = element['current_price']
            asset['market_cap'] = element['market_cap']
            asset['market_cap_rank'] = element['market_cap_rank']
            asset['price_change_percentage_24h'] = element[
                'price_change_percentage_24h']
            asset['total_volume'] = element['total_volume']
            asset['circulating_supply'] = element['circulating_supply']
            asset['total_supply'] = element['total_supply']

            assets.append(asset)

        return {'success': True, 'errors': None, 'assets': assets}
