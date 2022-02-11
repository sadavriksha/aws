import json
import boto3
region = "us-east-1:"
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
   print(uuid)
   s3 = boto3.resource('s3')
   my_bucket = s3.Bucket('xivtech-s3-invoiceprocess-development')
   files = []
   for object_summary in my_bucket.objects.filter(Prefix=f"private/{region+uuid}/"):
        source = object_summary.key
        list1 = source.split('/')
        files.append(list1[2])
   print(files)
    
   return {
        'statusCode': 200,
        'body':str(files)
    }
