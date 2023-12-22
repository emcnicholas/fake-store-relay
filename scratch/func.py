import requests
from datetime import datetime, timedelta


def get_time_utc_now():
    # Get current UTC time
    utc_now = datetime.utcnow()

    # Format as a string
    formatted_time = utc_now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    #print(formatted_time)
    return formatted_time


def get_time_period(period):
    utc_now = datetime.utcnow()
    end_time = utc_now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    if period == "last_hour":
        time = utc_now - timedelta(hours=1)
        start_time = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    elif period == "last_24_hours":
        time = utc_now - timedelta(hours=24)
        start_time = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    elif period == "last_7_days":
        time = utc_now - timedelta(days=7)
        start_time = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    elif period == "last_30_days":
        time = utc_now - timedelta(days=30)
        start_time = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    else:
        time = utc_now - timedelta(days=90)
        start_time = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    return start_time, end_time


def get_products():
    url = "https://fakestoreapi.com/products"

    payload = {}
    headers = {}

    response = requests.get(url, headers=headers, data=payload)

    if response.status_code != 200:
        return f'Response code: {response.status_code}'
    else:
        json_response = response.json()
        return json_response


def get_categories():
    url = "https://fakestoreapi.com/products/categories"

    payload = {}
    headers = {}

    response = requests.get(url, headers=headers, data=payload)

    if response.status_code != 200:
        return f'Response code: {response.status_code}'
    else:
        json_response = response.json()
        return json_response


def get_products_per_category(category):
    url = f"https://fakestoreapi.com/products/category/{category}"

    payload = {}
    headers = {}

    response = requests.get(url, headers=headers, data=payload)

    if response.status_code != 200:
        return f'Response code: {response.status_code}'
    else:
        json_response = response.json()
        return json_response


def tile_def(title, desc, periods, default_period, tile_type, short_desc, tile_id, tags):

    data = {
        "title": title,
        "description": desc,
        "periods": periods,  # Must be list
        "default_period": default_period,
        "type": tile_type,
        "short_description": short_desc,
        "id": tile_id,
        "tags": tags
    }

    return data


def horizontal_bar_data(time_period, tile_id, keys, period, data):
    start_time, end_time = get_time_period(time_period)
    data = {
            "valid_time": {
                "start_time": start_time,
                "end_time": end_time
            },
            "tile_id": tile_id,
            "keys": keys,
            "cache_scope": "org",
            "period": period,
            "observed_time": {
                "start_time": start_time,
                "end_time": end_time
            },
            "data": data
        }
    return data


def fakestore_horizontal_bar_data():
    keys = []
    data = []
    categories = get_categories()
    for category in categories:
        keys.append(
            {
                "key": category,
                "label": category
            }
        )
        products = get_products_per_category(category)
        data.append(
            {
                "key": category,
                "label": category,
                "value": len(products),
                "values": [
                    {
                        "key": category,
                        "link": f"https://fakestoreapi.com/products/category/{category}",
                        "value": len(products)
                    }
                ]
            }
        )
    return keys, data

