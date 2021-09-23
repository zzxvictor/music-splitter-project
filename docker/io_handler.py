# import boto3
import sys
import boto3
from botocore.exceptions import ClientError
import logging
import os
import glob


class Notifier:
    def __init__(self, region='us-east-1'):
        # self.client = boto3.client('ses', region_name=region)
        self.client = boto3.client('sns', region_name=region)

    def send_notification(self, recipient, tracks):
        message = 'Hello! Your request to split music files have been processed.' \
                  ' Please use the following keywords to download them from our website!\n'
        for type_name, s3_key in tracks.items():
            message += '{} track: {}\n'.format(type_name, s3_key)

        self.client.publish(PhoneNumber='+1' + recipient, Message=message)
        # response = self.client.send_email(
        #     Destination={
        #         'ToAddresses': [
        #             recipient,
        #         ],
        #     },
        #     Message={
        #         'Body': {
        #             'Html': {
        #                 'Charset': self.charset,
        #                 'Data': ', '.join(track_lists),
        #             },
        #             'Text': {
        #                 'Charset': self.charset,
        #                 'Data': ', '.join(track_lists),
        #             },
        #         },
        #         'Subject': {
        #             'Charset': self.charset,
        #             'Data': 'your music tracks are ready',
        #         },
        #     },
        #     Source=self.sender
        # )


class IoHandler:
    def __init__(self, bucket_name, retry=3):
        self.bucket = bucket_name
        self.s3_client = boto3.client('s3')
        self.RETRY = retry

    def upload_file(self, file_path, s3_key):
        for i in range(self.RETRY):
            try:
                self.s3_client.upload_file(file_path, self.bucket, s3_key)
                return True
            except ClientError as e:
                logging.error('upload failed, retry # {}/{}'.format(i + 1, self.RETRY))
        return False

    def download_file(self, file_path, s3_key):
        for i in range(self.RETRY):
            try:
                self.s3_client.download_file(self.bucket, s3_key, file_path)
                return True
            except ClientError as e:
                logging.error('download failed, retry # {}/{}'.format(i + 1, self.RETRY))
        return False


if __name__ == '__main__':
    args = sys.argv[1:]
    assert len(args) == 3, 'input not understood. expected 2 args, {} received'.format(len(args))
    bucket_name, s3_key, phone = args
    default_file_name = 'original_music'
    output_default_dir = 'output/' + default_file_name
    handler = IoHandler(bucket_name)
    handler.download_file(default_file_name, s3_key=s3_key)

    os.system('spleeter separate {} -p spleeter:5stems -o output '.format(default_file_name))
    files = glob.glob(output_default_dir + '/*.wav')
    track_lists = {}
    for file in files:
        track_type = file.split('/')[-1][:-4] # /path/track_type.wav
        s3_key = '{}_{}'.format(s3_key, track_type)
        handler.upload_file(file, s3_key)
        track_lists[track_type] = s3_key

    Notifier().send_notification(phone, track_lists)
