import json
import dateutil.parser

import boto3


def lambda_handler(event, context):
    try:
        db = boto3.client('dynamodb')

        for sqsEvent in event['Records']:
            s3_event = json.loads(sqsEvent['body'])

            for record in s3_event['Records']:
                timestamp = dateutil.parser.parse(record['eventTime'])
                key = record['s3']['object']['key'].rsplit('/', 1)
                type = key[0].split('/', 1)[0]
                path = f"{record['s3']['bucket']['name']}/{key[0]}/"

                db.transact_write_items(
                    TransactItems=[
                        {
                            "Put": {
                                "TableName": "Project-tweet-date",
                                "Item": {
                                    "load_date": {"S": f"{timestamp.date()} {timestamp.hour}"},
                                    "metadata": {"S": type},
                                    "path": {"S": path}
                                }
                            },
                        },
                        {
                            "Put": {
                                "TableName": "Project-tweet-path",
                                "Item": {
                                    "bucket": {"S": path},
                                    "file": {"S": key[1]},
                                }
                            },
                        }
                    ]
                )

        return {
            'statusCode': 200
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 400
        }
