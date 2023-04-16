import requests
import json
import boto3
from botocore.exceptions import ClientError



def insert_data(data, db=None, table='CurrencyRate'):
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    response = table.put_item(Item=data)
    print('@insert_data: response', response)
    return response


def lambda_handler(event, context):
    # TODO implement
    from_currency = 'USD'
    to_currency = 'CNY'
    url = "https://api.fastforex.io/fetch-one?from={}&to={}&api_key={}".format(from_currency, to_currency, api_key)
    url = "https://api.fastforex.io/fetch-multi?from=USD&to=EUR,GBP,CHF,JPY,AUD,CAD,CNY,HKD&api_key={}".format(api_key)
    headers = {"accept": "application/json"}
    response = json.loads(requests.get(url, headers=headers).text)
    print(response)
    # response: {"base":"USD","result":{"CNY":6.87022},"updated":"2023-04-02 23:55:16","ms":4}
    # updated time is in Greenwich Mean Time (GMT)
    response['update_time'] = response['updated']
    response.pop('ms',None)
    response.pop('updated', None)
    for k in response['results']:
        response['results'][k] = str(response['results'][k])

    insert_data(response)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

