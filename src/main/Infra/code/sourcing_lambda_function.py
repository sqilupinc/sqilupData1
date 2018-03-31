import boto3 
import time
import calendar
import json

client = boto3.client('cloudformation')
snsHandler =boto3.client('sns')
s3Handler =boto3.client('s3')

def lambda_handler(event, context):
    
    s3Event = event['Records']
    bucketName = s3Event[0]['s3']['bucket']['name']
    cftfileName = s3Event[0]['s3']['object']['key']
    s3Region = s3Event[0]['awsRegion']
    tempUrl = 'https://s3.'+s3Region+'.amazonaws.com/'+bucketName+'/'+cftfileName
    s3Dict={
        'bucketname' : bucketName,
        'filename' : cftfileName,
        'region' : s3Region,
        'FileURL' : tempUrl
    }
    print(s3Dict['bucketname'])
    print(tempUrl)
    
    response=print(event)
    snsNotification(event, context, s3Dict)
    #return response
    
def snsNotification(event, context, s3Dict):
    s3Bucketname = s3Dict['bucketname']
    s3Filename = s3Dict['filename']
    s3Region = s3Dict['region']
    s3Url = s3Dict['FileURL']
    evnt_name = 'Sourcing'
    if s3Bucketname != None: 
        status ='Success'
    elif s3Bucketname == None:
        status ='Success'
    dict_data = {
        'Header':
            {
                'Event' : evnt_name,
                'Status' : status,
                #'Timestamp' : time_of_evnt,
            },
        'Body':
            {
                'S3':
                    {
                        'Bucket_name' : s3Bucketname,
                        'Filename' : s3Filename,
                        'Region' : s3Region,
                        'URL' : s3Url
                    }
            }
            }
               
    json_data = json.dumps(dict_data,indent = 4)
    print (json_data)
    outMsg = (json_data)
    arn = 'arn:aws:sns:us-east-1:420345549088:SUDB1_SNS_NFN_TPC'
    sns_response=snsHandler.publish(TopicArn=arn,Message=outMsg,Subject='Sourcing')
    print (sns_response)
