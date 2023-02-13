import json
import boto3
from _decimal import Decimal


def format_building_file(url):
    with open(url, 'r') as json_file:
        data = json.load(json_file, parse_float=Decimal)
        result = {"id": data["_id"], "type": "mobile_building", "client_id": "9537cf58-08ee-435e-946f-200ae0bcb08e",
                  "building_name": data["building_name"], "num_floor": data["num_floor"], "address": data["address"],
                  "floors": {}, "s3_location": "floorplan.png", "building_id": data.get("building_id", None)}
        if result["building_id"] is None:
            result["building_id"] = "623a3401d1ed84fa819e6131"
        result["city"] = data.get("city")
        result["state"] = data.get("state", None)
        result["country"] = data.get("country", None)
        result["zip"] = data.get("zip", None)
        result["created_time"] = data.get("created_time", data.get("createdAt", None))
        result["updated_time"] = data.get("updated_time", None)
        for floor in data["floors"]:
            if "floorplan_scale" in floor:
                result["floors"][str(floor["floor_num"])] = {"floorplan_scale": floor["floorplan_scale"],
                                                             "s3_location": "floorplan.png"}
            else:
                result["floors"][str(floor["floor_num"])] = {"floorplan_scale": floor["scale"],
                                                             "s3_location": "floorplan.png"}
        return result


def upload_building_to_dynamodb(convert_data, table_name):
    table = boto3.resource('dynamodb').Table(table_name)
    table.put_item(Item=convert_data)
