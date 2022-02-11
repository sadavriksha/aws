import json
import boto3
import hmac
import uuid
import hashlib
import base64
import os

CLIENT_ID="2q2ultg0lo9qq23setf4357ue8"
COGNITO_POOL_ID = "us-east-1_evlvsdzZd"
CLIENT_SECRET="103296590jsanujg02bm8hku3dbeq4a19qiju1m2mds3geml255o"

def get_secret_hash(username):
  msg = username + CLIENT_ID 
  dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
  msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
  d2 = base64.b64encode(dig).decode()
  return d2

def lambda_handler(event, context):
    for field in ["answer"]:
          if event['answer'] is None:
            return  {"error": True, 
                "success": False, 
                "message": f"OTP is required", 
                "data": None}
                
    email = event['email']
    session = event['session']
    answer = event['answer']
    SECRET_HASH =  get_secret_hash(email)
    client = boto3.client('cognito-idp')
    try: 
      response =client.respond_to_auth_challenge(                                                                            
                            ClientId=CLIENT_ID,                                                                                                 
                            ChallengeName='CUSTOM_CHALLENGE',                                                                                   
                            Session=session,                                                                                                    
                            ChallengeResponses={                                                                                                
                                  'USERNAME': email, 
                                  'ANSWER': answer
                                }                                                                                                            
                        ) 
    except Exception as e:
        error = e.__str__() 
        if 'UserNotFoundException' in error : 
            return {'statusCode': 403, 'detail': 'Email does not exist.Please try with valid email'}
        if 'Invalid session' in error : 
            return {'statusCode': 403, 'detail': 'Please retry because your session get expire'}
        
        return e.__str__()
    print(response)
    error = str(response)
    if 'AuthenticationResult' not in error:
      return {'statusCode': 403, 'detail': 'First OTP is wrong.Please provide correct new OTP','response':response}
      
    return response