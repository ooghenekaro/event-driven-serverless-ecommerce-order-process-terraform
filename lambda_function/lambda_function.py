import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')

ORDER_TABLE = os.environ['ORDER_TABLE']
INVENTORY_TABLE = os.environ['INVENTORY_TABLE']

def lambda_handler(event, context):
    for record in event['Records']:
        order = json.loads(record['body'])

        # Process order: store in DynamoDB
        order_id = order['order_id']
        store_order_in_db(order)
        
        # Send confirmation email
        send_confirmation_email(order['customer_email'], order_id)
        
        # Update inventory
        update_inventory(order['items'])
        
    return {
        'statusCode': 200,
        'body': json.dumps('Order processed successfully!')
    }

def store_order_in_db(order):
    table = dynamodb.Table(ORDER_TABLE)
    table.put_item(Item=order)

def send_confirmation_email(customer_email, order_id):
    response = ses.send_email(
        Source='no-reply@yourdomain.com',  # We need to Replace with a verified SES email
        Destination={
            'ToAddresses': [customer_email]
        },
        Message={
            'Subject': {
                'Data': 'Order Confirmation'
            },
            'Body': {
                'Text': {
                    'Data': f'Thank you for your order. Your order ID is {order_id}.'
                }
            }
        }
    )

def update_inventory(items):
    table = dynamodb.Table(INVENTORY_TABLE)
    for item in items:
        response = table.update_item(
            Key={'item_id': item['item_id']},
            UpdateExpression="SET quantity = quantity - :val",
            ExpressionAttributeValues={':val': item['quantity']}
        )
