import json
import boto3
from datetime import datetime
from _decimal import Decimal


def format_region_file(_id, floor_num, url):
    with open(url, 'r') as json_file:
        data = json.load(json_file, parse_float=Decimal)
        curr = datetime.now()
        region = {}
        # for matrix in data.get("affine_matrices", data.get("F2C_affine_matrices"), data.get("model", [])).values():
        #     landmarks["floor_num"] = landmark["id"][0]
        #     if "landmarks" not in landmarks:
        #         landmarks["landmarks"] = {}
        region["type"] = "mobile_region"
        region["building_id"] = _id
        region["floor_num"] = floor_num
        region["created_time"] = data.get("created_time", data.get("createdAt", None))
        region["region_id"] = data.get("region_id")
        region["current_model"] = data.get("current_model", (region["region_id"] + "_" +
                                                             curr.strftime("%d%m%Y-%H%M%S")))
        region["id"] = _id + floor_num + region["region_id"]
        region["boundary_points"] = data.get("boundary_points")
        region["created_time"] = data.get("created_time", data.get("createdAt", None))
        return region


def upload_region_to_dynamodb(data, table_name):
    table = boto3.resource('dynamodb').Table(table_name)
    table.put_item(Item={
        "id": data["id"],
        "type": data["type"],
        "floor_num": data["floor_num"],
        "region_id": data["region_id"],
        "current_model": data["current_model"],
        "models": {}
    })


