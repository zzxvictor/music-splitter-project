import json
import boto3

BUCKET_NAME = 'YOUR S3 BUCKET NAME HERE'


"""
If your requests aren't going through, check the following:
    1. Is it a CORS error? make sure CORS is enabled in the API gateway console 
    2. Does your lambda has S3 permission? Modify the IAM role assigned to your Lambda 
    3. For debugging, use the CloudWatch logs 
"""

def create_s3_get_url(file_id):
    """
    generate a pre-signed URL so that the front-end can download the file

    :param file_id: str, the file ID user submitted
    :return: str, a pre-sigined URL
    """
    url = boto3.client('s3').generate_presigned_url(
        ## TODO )

    return url


def lambda_handler(event, context):
    if isinstance(event, str):
        # for testing only, should not be called by API gateway
        metadata = json.loads(event)['pathParameters']
    else:
        metadata = event['pathParameters']
    # grab the file_id from request. You might need to change the key name
    file_id = metadata['fileid']

    response = {'presigned_url': create_s3_get_url(##TODO)}


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
