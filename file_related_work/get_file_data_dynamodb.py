import json
import boto3

region='us-east-1:'
dynamobdTableName = 'xivtech-dynamodb-invoiceprocess-development'
dynamobd = boto3.resource('dynamodb')
table = dynamobd.Table(dynamobdTableName)

def lambda_handler(event, context):
   client = boto3.client('cognito-idp')
   for field in ["access_token"]:
      if event['headers'][field] is None:
            return  {"error": True, 
                "success": False, 
                "message": f"{field} is required", 
                "data": None}
                
   access_token = event['headers']['access_token']
   try:
        response = client.get_user(
              AccessToken=access_token)
              
   except Exception as e:
        error=e.__str__()
        if 'Access Token has expired' in error:
              return {
                  'statusCode': 403,
                  'body':'Your login session get expired.Please login again'
                }
        return {
          'statusCode': 200,
          'body':error
          }
       
   uuid=response['Username']
   
   file_name = event['headers']['file_name']
   print(uuid,file_name)
   try:
        response= table.get_item(
            Key = {
                'uuid':region+uuid,
                "file_name":file_name
            }
        )
        if 'Item' in response:

            return{
                'statusCode': 200,
                'body':f"{response['Item']}"                                
            }
            
        else:
            return {
                'statusCode': 200,
                'body':f"File data for {file_name} file not found!!"
            }
            
   except Exception as e:
            error = e.__str__() 
            return {
                'statusCode': 401,
                'body':str(error)
            }
   

