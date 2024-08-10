import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')

ORDER_TABLE = os.environ['ORDER_TABLE']
INVENTORY_TABLE = os.environ['INVENTORY_TABLE']

def lambda_handler(event, context):
    for record in event['Records']:
        sns_message = json.loads(record['body'])  # Load the SQS body
        order = json.loads(sns_message['Message'])  # Load the actual order from the SNS message
        
        # Now order should contain the order_id and other information
        if 'order_id' not in order:
            print(f"Error: 'order_id' not found in the order: {order}")
            continue  # Skip this record

        order_id = order['order_id']
        
        # Process order: store in DynamoDB
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
        Source='no-reply@yourdomain.com',  # Replace with a verified SES email
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

