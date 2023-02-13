import json
import boto3
from _decimal import Decimal


def format_graph_file(_id, url):
    with open(url, 'r') as json_file:
        data = json.load(json_file, parse_float=Decimal)
        landmarks = {}
        for landmark in data.get("landmark_floor002",
                                 data.get("landmarks", data.get("landmark_floor001", None))).values():
            landmarks["floor_num"] = landmark["id"][0]
            if "landmarks" not in landmarks:
                landmarks["landmarks"] = {}
            landmarks["landmarks"][landmark["id"]] = {
                "transform_world_location": landmark.get("transform_world_location",
                                                         landmark.get("transformed_w_location", [])),
                "camera_location": landmark.get("camera_location", None),
                "id": landmark["id"],
                "regions": landmarks.get("regions",
                                         [(landmark.get("transform_world_location"), landmark.get("camera_location"))]),
                "access_level": landmark.get("access_level", 1),
                "destination_type": landmark.get("destination_type", 2),
                "connection": {
                    "get": landmarks.get("connection", {}).get("to", [])
                }
            }
            landmarks.update(landmarks["landmarks"])

        landmarks["id"] = _id
        landmarks["type"] = "mobile_region"
        landmarks["created_time"] = data.get("created_time", data.get("createdAt", None))
        return landmarks


def upload_graph_to_dynamodb(data, table_name):
    table = boto3.resource('dynamodb').Table(table_name)
    table.put_item(Item={
        "id": data["id"],
        "type": data["type"],
        "created_time": data["created_time"],
        "landmark_floor00" + str(data["floor_num"]): {}
    })
    for landmark_name, landmark_data in data["landmarks"].items():
        table.update_item(
            Key={
                "id": data["id"],
                "type": data["type"],
            },
            UpdateExpression=f"SET landmark_floor00{data['floor_num']}.#l = :l",
            ExpressionAttributeNames={
                "#l": landmark_name
            },
            ExpressionAttributeValues={
                ":l": {
                    "transform_world_location": landmark_data["transform_world_location"],
                    "id": landmark_data["id"],
                    "regions": landmark_data["regions"],
                    "access_level": landmark_data["access_level"],
                    "destination_type": landmark_data["destination_type"],
                    "connection": landmark_data["connection"]
                }
            }
        )
