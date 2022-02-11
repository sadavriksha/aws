import json
import boto3
import hmac
import uuid
import hashlib
import base64
import os

CLIENT_ID="2q2ultg0lo9qq23setf4357ue8"
COGNITO_POOL_ID ="us-east-1_So6AN1vYF"

def sign_me_in(client, username):
    
    try:
      resp = client.initiate_auth(
                 ClientId=CLIENT_ID,
                 AuthFlow='CUSTOM_AUTH',
                 AuthParameters={
                     'USERNAME': username,
                     'PASSWORD':"123456"
                  },
                 ClientMetadata={
                  'username': username,
              }
            )

    except client.exceptions.NotAuthorizedException:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotConfirmedException:
        return None, "User is not confirmed"
    except Exception as e:
        return None, e.__str__()
        
    return resp,None  

def lambda_handler(event, context):
    for field in ["email"]:
       if event.get(field) is None:
            return  {"error": True, 
                "success": False, 
                "message": f"{field} is required", 
                "data": None}
                
    email =event['email']
    client = boto3.client('cognito-idp')

    response, error = sign_me_in(client,email)
    
    if error:
        if 'UserNotFoundException' in error : 
            return {'statusCode': 403, 'detail': 'Email does not exist.Please try with valid email'}
        return {'statusCode': 403, 'detail': error}
        
       
    return {'statusCode': 200, 'detail': response}