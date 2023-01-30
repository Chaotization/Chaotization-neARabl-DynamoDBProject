import boto3


def CreateTable(tableName):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
        TableName=tableName,
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'},  # Partition key
            {'AttributeName': 'type', 'KeyType': 'RANGE'},  # Sort key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'},
            {'AttributeName': 'type', 'AttributeType': 'S'},
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10}
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=tableName)
