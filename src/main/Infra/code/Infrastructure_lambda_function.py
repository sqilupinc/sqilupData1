import boto3 
import time
import calendar
import json

client = boto3.client('cloudformation')
snsHandler =boto3.client('sns')
s3Handler =boto3.client('s3')

month_number = format(list(calendar.month_abbr).index(time.strftime('%b',time.gmtime())),"02d")
add_time = time.strftime('%Y'+month_number+'%d-%H%M',time.gmtime())
stackname = 'Sqilup-Stack-'+add_time

def lambda_handler(event, context):
    print (event)
    dict_evnt = event['Records']
    sns_msg_evnt = dict_evnt[0]['Sns']['Message']['Header']['Event']
    sns_msg_status = dict_evnt[0]['Sns']['Message']['Header']['Status']
    sns_msg_time =dict_evnt[0]['Sns']['Message']['Header']['Timestamp']
    bucketname = dict_evnt[0]['Sns']['Message']['Body']['S3']['Bucket_name']
    cft_filename = dict_evnt[0]['Sns']['Message']['Body']['S3']['Filename']
    s3_region_name = dict_evnt[0]['Sns']['Message']['Body']['S3']['Region']
    #print (sns_msg_evnt)
    #print (sns_msg_status)
    #print (sns_msg_time)
    #print (s3_bucketname)
    #print (s3_filename)
    #print (s3_region_name)
    tempurl = 'https://s3.'+s3_region_name+'.amazonaws.com/'+bucketname+'/'+cft_filename
    s3_dict ={
                'bucketname' : bucketname,
                'filename' : cft_filename,
                'region' : s3_region_name,
                'FileURL' : tempurl
             }
    print (bucketname)
    print (cft_filename)
    print (s3_region_name)
    print (tempurl)
    response = client.create_stack(
    StackName=stackname,
    TemplateURL=tempurl,
    Parameters=[
        {
            'ParameterKey': 'InstanceType',
            'ParameterValue': 't2.micro',
            'UsePreviousValue': False
        },
        {
            'ParameterKey': 'KeyName',
            'ParameterValue': 'FromImage_1',
            'UsePreviousValue': False
        }
    ])
    print (response)
    print (event)
    sns_notification(event, context,s3_dict)

def sns_notification(event, context,s3_dict):
    get_s3_dict = s3_dict
    s3_bucketname = get_s3_dict['bucketname']
    s3_filename = get_s3_dict['filename']
    s3_region = get_s3_dict['region']
    s3_url = get_s3_dict['FileURL']
    Desc_stack = client.describe_stacks(StackName=stackname)
    getstack = Desc_stack['Stacks']
    getmd = Desc_stack['ResponseMetadata']
    evnt_name = getstack[0]['Description']
    stackstatus = getstack[0]['StackStatus']
    stackid = getstack[0]['StackId']
    time_of_evnt = getmd['HTTPHeaders']['date']
    print (time_of_evnt)
    if stackstatus == 'CREATE_IN_PROGRESS':
        time.sleep(60)
        sns_notification(event, context,s3_dict)
    if stackstatus == 'CREATE_COMPLETE':
        status = 'Success'
        dict_data = {
            'Header':
                {
                    'Event' : 'Cluster Creation',
                    'Status' : status,
                    'Timestamp' : time_of_evnt,
                },
            'Body':
                {
                    'S3':
                        {
                         'Bucket_name' : s3_bucketname,
                         'Filename' : s3_filename,
                         'Region' : s3_region
                        },
                    'Stack':
                        {
                        'StackId' : stackid, 
                        'StackName' : stackname, 
                        'Stackstatus':stackstatus
                        }
                }
                }
        json_data = json.dumps(dict_data,indent = 4)
        subject = 'Sqilup - Cluster Creation Notifciation'
        if stackstatus == 'CREATE_COMPLETE':
            outMsg = 'Hello Sqilup Team, \n \n Cluster Creation is Success \n \n ' 
        elif stackstatus == 'CREATE_FAILED':
            outMsg = 'Hello Sqilup Team, \n \n Cluster Creation is Failed \n \n'  
        else:
            outMsg = 'Hello Sqilup Team, \n \n Cluster Creation is in other status than expected \n \n'  
        
        print (json_data) 
    
        FinalMsg = outMsg  + '\n\n' + json_data + '\n\n\nThanks,\nSqilup Data Batch 1 - Trans team'
        arn = 'arn:aws:sns:us-east-2:015885713785:SNS_Sqilup_Cluster_Creation'
        sns_response = snsHandler.publish(TopicArn=arn,Message=FinalMsg,Subject=subject)
        print (sns_response)
    