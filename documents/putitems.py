import boto3
import json
from documents.__init__ import Client


def write_To_DB(url, tableName):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)
    with open(url, 'r') as json_file:
        client_infor = json.load(json_file)
        _dict = {'_city': None, '_zip': None, '_country': None,
                 '_update_time': None, 'created_time': None}
        for key in _dict.keys():
            if not key in client_infor:
                _dict.update({key: ''})
            else:
                _dict.update({key: client_infor[key]})

        client = Client(client_infor['_id'], client_infor['building_name'], client_infor['num_floor'],
                        client_infor['address'], _dict.get('_city'), client_infor['state'],
                        _dict.get('_country'), _dict.get('_zip'), _dict.get('_created_time'),
                        _dict.get('_update_time'), client_infor['floors'])
    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                'id': client.id,
                'type': client.type,
                'client_id': client.client_id,
                'building_name': client.building_name,
                'building_id': client.building_id,
                'num_floor': client.num_floor,
                'address': client.address,
                'city': client.city,
                'state': client.state,
                'county': client.country,
                'zip': client.zip,
                'created_time': client.create_time,
                'update_time': client.update_time,
                'floor': {'floorplan_scale': client.scale, 's3_location': client.s3_location}
            }
        )
