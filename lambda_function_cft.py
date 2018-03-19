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
    tempurl = 'https://s3.us-east-2.amazonaws.com/cf-templates-1qvjgmx78h22d-us-east-2/ec2_cft.json'
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
    # TODO implement
    print (response)
    print (event)
    #time.sleep(60)
    sns_notification(event, context)
    #s3upload(event, context)

def sns_notification(event, context):
    Desc_stack = client.describe_stacks(StackName=stackname)
    getstack = Desc_stack['Stacks']
    status = getstack[0]['StackStatus']
    stackid = getstack[0]['StackId']
    if status == 'CREATE_COMPLETE':
        msg = 'The Stack ' +  stackname + ' has been created'
        outMsg = 'Cloud Formation Stack has been created successfully \n ' + '\t Stack id : ' + stackid + '\n\t Stack Name:' + stackname + '\n\t Stack Status:' + status
    elif status == 'CREATE_IN_PROGRESS':
        msg = 'The Stack '+  stackname + ' creation is in progress'
        outMsg = 'Cloud Formation Stack creation is in progress \n' + '\t Stack id : ' + stackid + '\n\t Stack Name:' + stackname + '\n\t Stack Status:' + status
    elif status == 'CREATE_FAILED':
        msg = 'The stack ' + stackname + ' creation Failed'
        outMsg = 'Cloud Formation Stack creation has been Failed \n'  + '\t Stack id : ' + stackid + '\n\t Stack Name:' + stackname + '\n\t Stack Status:' + status
    else:
        msg = 'The stack ' + stackname + ' is in other status. please check'
        outMsg = 'Cloud Formation Stack is in other status than expected \n'  + '\t Stack id : ' + stackid + '\n\t Stack Name:' + stackname + '\n\t Stack Status:' + status
    FinalMsg = outMsg + '\n' + msg
    #outMsg = 'Cloud Formation Stack has been created successfully'
    arn = 'arn:aws:sns:us-east-2:015885713785:SUDB1_SEND_NTFN'
    sns_response = snsHandler.publish(TopicArn=arn,Message=FinalMsg,Subject='SUDB1_SEND_NTFN - Create the cloudformation Stack')
    print (sns_response)
    
#def s3upload(event, contex):
 #   evnt = event
  #  dict_evnt = evnt['Records']
   # bucketname = dict_evnt[0]['s3']['bucket']['name']
    #cft_filename = dict_evnt[0]['s3']['Object']['key']
    #response = s3Handler.list_objects(
    #Bucket='cf-templates-1qvjgmx78h22d-us-east-2')
    #print (evnt)
    #print (bucketname)
    #print (cft_filename)
    