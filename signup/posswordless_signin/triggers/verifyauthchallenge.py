import json

def lambda_handler(event, context):
    
    try:
       challenge = event['request']['privateChallengeParameters']['answer']
    except : 
         event['response']['answerCorrect']=False
         return event
         

    if (event['request']['challengeAnswer']==challenge):
        event['response']['answerCorrect']=True
        return event

    event['response']['answerCorrect']=False
    return event