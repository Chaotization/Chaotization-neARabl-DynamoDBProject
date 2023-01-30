import boto3
import json
from graph.__init__ import Graph


def write_To_DB(url, tableName):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)
    with open(url, 'r') as json_file:
        graph_infor = json.load(json_file)
        if 'floor_num' in graph_infor:
            floor_num = graph_infor['floor_num']
        else:
            floor_num = graph_infor[2][0]

        list = [['createdAt', 'created_time'], ['transformed_floorplan_location', 'transform_world_location'],
                ['landmarks', 'landmark_*']]
        for elem in list[0]:
            if elem in graph_infor:
                created_time = graph_infor[elem]
            else:
                created_time = None
        for elem in list[1]:
            if elem in graph_infor:
                transform_world_location = graph_infor[elem]
            else:
                transform_world_location = []
        for elem in list[2]:
            if elem in graph_infor:
                landmarks = graph_infor[elem]
            else:
                landmarks = []
        graph = Graph(created_time, floor_num, transform_world_location, landmarks)

    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                'id': graph.id,
                'type': graph.type,
                'created_time': graph.created_time,
                'landmark_floor' + graph.floor_num: {
                    graph.landmark_id: {
                        'transform_world_location': graph.transform_world_location,
                        'id': graph.landmark_id,
                        'regions': [graph.regions],
                        'access_level': graph.access_level,
                        'destination_type': graph.destination_type,
                        'connection': graph.connection
                    }
                }
            }
        )
