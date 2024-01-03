# Functions to interact with Fake Store API

from datetime import datetime, timedelta
import requests

########################
# Get formatted UTC Time
########################


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

#######################################################################################################################
# Tile definition will create the tile type to use in the dashboard.
# title             - Type "string". The title that will appear at the top of the tile.
# desc              - Type "string". Description of the tile that will appear in the tile.
# periods           - Type [list] of "strings". Can be last_hour, last_24_hours, last_7_days, last_30_days. ex ["last_hour", "last_24_hours"]
# default_period    - Type "string". The default period set for the tile.
# short_description - Type "string". A short description of the tile.
# tile_id           - Type "string". ID is used to refer the tile data to the tile type.
# tags              - Type [list] of "strings". Use tags to identify the tile.
#######################################################################################################################


def tile_def(title, desc, periods, default_period, tile_type, short_desc, tile_id, tags):
    data = {
        "title": title,
        "description": desc,
        "periods": periods,
        "default_period": default_period,
        "type": tile_type,
        "short_description": short_desc,
        "id": tile_id,
        "tags": tags
    }
    return data


#
# This function is used to populate data into a horizontal bar graph in dashboard.
# tile_id  - Type "string". ID is used to refer the tile data to the tile type.
# keys     - Type [list] of key value pairs to identify the bars in the graph. For example, electronics, jewelery, etc...
# period   - Type "string. The le

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


def donut_graph_data(time_period, tile_id, label_headers, labels, period, data):
    start_time, end_time = get_time_period(time_period)
    data = {
            "valid_time": {
                "start_time": start_time,
                "end_time": end_time
            },
            "tile_id": tile_id,
            "label_headers": label_headers,
            "labels": labels,
            "cache_scope": "org",
            "period": period,
            "observed_time": {
                "start_time": start_time,
                "end_time": end_time
            },
            "data": data
        }
    return data


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


def get_product_info():
    product_list = []
    products = get_products()
    for product in products:
        product_list.append(
            {
                "title": product["title"],
                "price": product["price"],
                "category": product["category"],
                "rating": product["rating"]["rate"],
                "count": product["rating"]["count"]
            }
        )
    return product_list


def get_category_rating_amount(products):
    ratings_amount = []
    zero = [product for product in products if product["rating"]["rate"] < 1]
    ratings_amount.append(len(zero))
    one = [product for product in products if 1 <= product["rating"]["rate"] < 2]
    ratings_amount.append(len(one))
    two = [product for product in products if 2 <= product["rating"]["rate"] < 3]
    ratings_amount.append(len(two))
    three = [product for product in products if 3 <= product["rating"]["rate"] < 4]
    ratings_amount.append(len(three))
    four = [product for product in products if 4 <= product["rating"]["rate"] < 5]
    ratings_amount.append(len(four))
    five = [product for product in products if product["rating"]["rate"] >= 5]
    ratings_amount.append(len(five))

    return ratings_amount


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


def get_fakestore_donut_graph_data():
    categories = get_categories()
    category_amount = []
    category_rating_amount = []
    label_headers = ["Category", "Rating"]
    ratings = ["0", "1", "2", "3", "4", "5"]
    labels = [categories, ratings]
    data = []
    for category in categories:
        category_products = get_products_per_category(category)
        category_amount.append(len(category_products))
        category_ratings = get_category_rating_amount(category_products)
        category_rating_amount.append(category_ratings)
        segment = []
        for key, rating in enumerate(category_ratings):
            segment.append(
                {
                    "key": key,
                    "value": rating
                }
            )

        data.append(
            {
                "key": categories.index(category),
                "value": len(category_products),
                "link_uri": f"https://fakestoreapi.com/products/category/{category}",
                "tooltip": f"Fake Store Category {category}",
                "segments": segment
            }
        )

    return label_headers, labels, data

