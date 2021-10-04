import json
import boto3


def record_handler(record):
    details = record['dynamodb']['NewImage']
    # TODO
    # get file id and user email from record
    parameters = ['music-files-bucket', file_id, user_email]
    submit_ecs_job(parameters)


def submit_ecs_job(parameters):
    ecs_client = boto3.client('ecs')
    response = ecs_client.run_task(cluster='default',
                                   count=1,
                                   launchType='FARGATE',
                                   taskDefinition=#TODO the task name you created on AWS,
                                   networkConfiguration={
                                       'awsvpcConfiguration': {
                                           'subnets': [
                                               # the VPC subnet you wish to you (stick to the default one)
                                           ],
                                           'assignPublicIp': 'ENABLED'
                                       }

                                   },
                                   overrides={
                                       'containerOverrides': [{
                                           'name': # name of the container ,
                                           'command': parameters
                                       }]
                                   }

                                   )


def lambda_handler(event, context):
    for record in event['Records']:
        record_handler(record)


