import json
import boto3

def lambda_handler(event, context):
    
    response = event.get('response')
    request = event.get('request')
    session = request.get('session')

    
    if request.get('userNotFound') is True:
        response.update({
            'issueTokens': False,
            'failAuthentication': True,+
            'msg': "User does not exist"
        })
    elif len(session) >=3 and session[2].get('challengeResult') is False:
        response.update({
            'issueTokens': False,
            'failAuthentication': True
        })
    elif len(session) > 0 and session[-1].get('challengeResult') is True:
        response.update({
            'issueTokens': True,
            'failAuthentication': False,
        })
    else:
        response.update({
            'issueTokens': False,
            'failAuthentication': False,
            'challengeName': 'CUSTOM_CHALLENGE'
        })
        
    print(event)
    print(session)
    return  event