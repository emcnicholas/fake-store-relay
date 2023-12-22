from flask import Blueprint
from api.utils import jsonify_data, get_jwt, get_json
from api.schemas import DashboardTileSchema, DashboardTileDataSchema

from api.fakestore import tile_def, fakestore_horizontal_bar_data, horizontal_bar_data

dashboard_api = Blueprint("dashboard", __name__)


@dashboard_api.route("/tiles", methods=["POST"])
def tiles():
    #_ = get_jwt()
    return jsonify_data([
        tile_def("Product Categories Horizontal Bar Chart",
                 "Number of products per category",
                 ["last_hour"],
                 "last_hour",
                 "horizontal_bar_chart",
                 "Number of products per category",
                 "fakestore_categories",
                 ["categories"]),
        tile_def("Product Categories Vertical Bar Chart",
                 "Number of products per category",
                 ["last_hour"],
                 "last_hour",
                 "vertical_bar_chart",
                 "Number of products per category",
                 "fakestore_categories_vertical",
                 ["categories"])
    ])


@dashboard_api.route("/tiles/tile", methods=["POST"])
def tile():
    #_ = get_jwt()
    _ = get_json(DashboardTileSchema())
    return jsonify_data({})


@dashboard_api.route("/tiles/tile-data", methods=["POST"])
def tile_data():
    #_ = get_jwt()
    req = get_json(DashboardTileDataSchema())
    period = req["period"]
    if req["tile_id"] == "fakestore_categories":
        keys, data = fakestore_horizontal_bar_data()
        tile_data = horizontal_bar_data(
            period,
            "fakestore_categories",
            keys,
            "last_hour",
            data
        )
        return jsonify_data(tile_data)
    elif req["tile_id"] == "fakestore_categories_vertical":
        keys, data = fakestore_horizontal_bar_data()
        tile_data = horizontal_bar_data(
            period,
            "fakestore_categories_vertical",
            keys,
            "last_hour",
            data
        )
        return jsonify_data(tile_data)

    else:
        return jsonify_data({})
