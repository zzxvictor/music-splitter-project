import json
# Boto3 is a library that allows you to interact with AWS services such as S3 and DynamoDB
import boto3
import uuid

BUCKET_NAME = 'YOUR S3 BUCKET NAME HERE'

"""
If your requests aren't going through, check the following:
    1. Is it a CORS error? make sure CORS is enabled in the API gateway console 
    2. Does your lambda has S3 permission? Modify the IAM role assigned to your Lambda 
    3. For debugging, use the CloudWatch logs 
"""

def create_s3_put_url(key, content_type):
    """
    generate a put pre-signed URL for file submission

    :param key: str, randomly generated to avoid file collision
    :param content_type:str, he type of the file
    :return: str, pre-signed url
    """
    url = boto3.client('s3').generate_presigned_url(
        ## TODO
    )

    return url


def lambda_handler(event, context):
    if isinstance(event, str):
        # for testing only, should not be called by API gateway
        metadata = json.loads(event)
    else:
        metadata = json.loads(event['body'])

    # grab the metadata submitted by the user, you might need to change the keywords here
    user_email = metadata['email']
    # get the content type
    content_type = metadata['type']
    # generate a random file name
    key = uuid.uuid4().hex

    response = {'presigned_url': create_s3_put_url(##TODO)}

    #######################################################
    # donn't modify this part, the headers are used for CORS
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(response)
    }
