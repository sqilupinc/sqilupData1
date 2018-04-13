import boto3 
import time
import calendar

client = boto3.client('cloudformation')
snsHandler =boto3.client('sns')
s3Handler =boto3.client('s3')

month_number = format(list(calendar.month_abbr).index(time.strftime('%b',time.gmtime())),"02d")
add_time = time.strftime('%Y'+month_number+'%d-%H%M',time.gmtime())
stackname = 'SUDB1-CFT-stack-'+add_time

def lambda_handler(event, context):
    dict_evnt = event['Records']
    bucketname = dict_evnt[0]['s3']['bucket']['name']
    cft_filename = dict_evnt[0]['s3']['object']['key']
    s3_region_name = dict_evnt[0]['awsRegion']
    tempurl = 'https://s3.'+s3_region_name+'.amazonaws.com/'+bucketname+'/'+cft_filename
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
    sns_notification(event, context)

def sns_notification(event, context):
    Desc_stack = client.describe_stacks(StackName=stackname)
    getstack = Desc_stack['Stacks']
    status = getstack[0]['StackStatus']
    stackid = getstack[0]['StackId']
    subject = 'SUDB1 - Cloudformation Stack Creation Notifciation - ' + stackname
    if status == 'CREATE_COMPLETE':
        outMsg = 'Hello Sqilup Team, \n \n Cloud Formation Stack has been created successfully \n\n\n ' + '\t Stack id : ' + stackid + '\n\t Stack Name:' + stackname + '\n\t Stack Status:' + status
    elif status == 'CREATE_IN_PROGRESS':
        outMsg = 'Hello Sqilup Team, \n \n Cloud Formation Stack creation is in progress \n\n\n' + '\t Stack id : ' + stackid + '\n\t Stack Name:' + stackname + '\n\t Stack Status:' + status
    elif status == 'CREATE_FAILED':
        outMsg = 'Hello Sqilup Team, \n \n Cloud Formation Stack creation has been Failed \n\n\n'  + '\t Stack id : ' + stackid + '\n\t Stack Name:' + stackname + '\n\t Stack Status:' + status
    else:
        outMsg = 'Hello Sqilup Team, \n \n Cloud Formation Stack is in other status than expected \n\n\n'  + '\t Stack id : ' + stackid + '\n\t Stack Name:' + stackname + '\n\t Stack Status:' + status
    FinalMsg = outMsg + '\n\n\nThanks,\nSqilup Data Batch 1 - Trans team'
    arn = 'arn:aws:sns:us-east-2:015885713785:SUDB1_SEND_NTFN'
    sns_response = snsHandler.publish(TopicArn=arn,Message=FinalMsg,Subject=subject)
    print (sns_response)
    