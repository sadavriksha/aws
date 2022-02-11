import json
import boto3
CLIENT_ID = "client_id"

def lambda_handler(event, context):
    email = event['email']
    password = event['password']
    phone_number=event['phone_number']
    client = boto3.client('cognito-idp')
    resp = client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password, 
            UserAttributes=[

            {
                'Name': "email",
                'Value': email
            },
            
            {
                'Name': "phone_number",
                'Value': phone_number
            },
            
            ],
            ValidationData=[
                {
                'Name': "email",
                'Value': email
            },
            {
                'Name': "username",
                'Value': email
            }

        ])
    
    return {
        'statusCode': 200,
        'body': json.dumps(resp)
    }