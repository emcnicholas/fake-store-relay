import json

from scratch.func import get_products, get_categories, get_products_per_category, tile_def, get_time_utc_now, \
    get_time_period, fakestore_horizontal_bar_data, horizontal_bar_data

if __name__ == '__main__':
    # categories = get_categories()
    # for category in categories:
    #     products = get_products_per_category(category)
    #     print(category, len(products))
    fakestore = tile_def(
        "Product Categories",
        "Number of products per category",
        ["last_hour"],
        "last_hour",
        "horizontal_bar_chart",
        "Number of products per category",
        "fakestore_categories",
        ["categories"]
    )
    print(json.dumps(fakestore, indent=4))

    keys, data = fakestore_horizontal_bar_data()
    print(json.dumps(keys, indent=4))
    print(json.dumps(data, indent=4))

    bar = horizontal_bar_data(
        "last_hour",
        "fakestore_categories",
        keys,
        "last_hour",
        data
    )
    print(json.dumps(bar, indent=4))

