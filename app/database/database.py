from app import logger
from app.helper import helper


def users(client):
    if not helper.is_db_exists(client, 'Users'):
        client.create_table(
            TableName='Users',
            BillingMode='PAY_PER_REQUEST',
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S',
                },
            ],
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH',
                },
            ],
        )
        logger.info('DDB Users table created.')
    else:
        logger.info('DDB Users table already exists.')


def movies(client):
    if not helper.is_db_exists(client, 'Movies'):
        client.create_table(
            TableName='Movies',
            BillingMode='PAY_PER_REQUEST',
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S',
                },
            ],
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH',
                },
            ],
        )
        logger.info('DDB Movies table created.')
    else:
        logger.info('DDB Movies table already exists.')
