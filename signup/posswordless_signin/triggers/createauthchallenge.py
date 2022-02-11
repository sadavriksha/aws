import json
import random
import os
import boto3

def send_plain_email(email,OTP):
    ses_client = boto3.client("ses")
    CHARSET = "UTF-8"

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                email,
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": "comformation OTP! : "+OTP,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": OTP,
            },
        },
        Source="sada.vriksha@xivtech.io",
    )
    return "success"

def random_OTP():
       OTP=str(random.randint(100000,999999))
       return OTP
    
    
def lambda_handler(event, context):
    print(event)
    
    response = event.get('response')
    request = event.get('request')

    secretLoginCode =random_OTP()
    
    email = event['request']['userAttributes']['email']
    print(email)
    out = send_plain_email(email,secretLoginCode)


    event['response']['privateChallengeParameters']=dict()
    event['response']['privateChallengeParameters']['answer']=secretLoginCode
    
    return event