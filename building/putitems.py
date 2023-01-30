import boto3
import json
from building.__init__ import Building


def write_To_DB(url, tableName):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)
    with open(url, 'r') as json_file:
        building_infor = json.load(json_file)
        _dict = {'city': None, 'zip': None, 'country': None,
                 'update_time': None, 'created_time': None}
        for key in _dict.keys():
            if key in building_infor:
                _dict.update({key: building_infor[key]})

        building = Building(building_infor['_id'], building_infor['building_name'], building_infor['num_floor'],
                            building_infor['address'], _dict.get('city'), building_infor['state'],
                            _dict.get('country'), _dict.get('zip'), _dict.get('created_time'),
                            _dict.get('update_time'), building_infor['floors'])

    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                'id': building.id,
                'type': building.type,
                'client_id': building.client_id,
                'building_name': building.building_name,
                'building_id': building.building_id,
                'num_floor': building.num_floor,
                'address': building.address,
                'city': building.city,
                'state': building.state,
                'county': building.country,
                'zip': building.zip,
                'created_time': building.create_time,
                'update_time': building.update_time,
                'floor': {'floorplan_scale': building.scale, 's3_location': building.s3_location}
            }
        )
