import boto3
import json
from decimal import Decimal
from graph.__init__ import Graph


def write_To_DB(url, tableName):
    table = boto3.resource('dynamodb').Table(tableName)
    with open(url, 'r') as json_file:
        graph_infor = json.load(json_file, parse_float=Decimal)
        lists = [['created_time', 'createdAt'], ['landmarks', 'landmark_floor001', 'landmark_floor002']]
        for elem in lists[0]:
            if elem in graph_infor:
                print(elem)
                created_time = graph_infor[elem]
            else:
                created_time = None
        for elem in lists[1]:
            print(elem)
            if elem in graph_infor:
                landmark = graph_infor[elem]
        graph = Graph(graph_infor['_id'], created_time, landmark)

    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                'id': graph.id,
                'type': graph.type,
                'created_time': graph.created_time,
                'landmark_floor00' + graph.floor_num: {
                    graph.landmark_id: {
                        'transform_world_location': graph.infor.reverse().pop(),
                        'id': graph.infor.reverse().pop(),
                        'regions': graph.infor.reverse().pop(),
                        'access_level': graph.infor.reverse().pop(),
                        'destination_type': graph.infor.reverse().pop(),
                        'connection': graph.infor.reverse().pop(),
                    }

                }
            }
        )
