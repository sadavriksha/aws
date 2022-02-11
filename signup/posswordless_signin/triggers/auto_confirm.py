import json
import boto3

def lambda_handler(event, context):
    event['response']['autoConfirmUser']=True
   # event['response']['autoVerifyEmail']=True
    
    return event