import configparser
import logging
import boto3
import requests
from botocore.exceptions import ClientError
from botocore.config import Config

config = configparser.RawConfigParser()
config.read('C://Users//Administrator//Desktop//ml_models//config.properties')
bucket_name = config.get("aws", "S3_BUCKET")
aws_region = config.get("aws", "AWS_REGION")
s3_client = boto3.client('s3', config=Config(region_name=aws_region, s3={'addressing_style': 'path'},
                                             signature_version='s3v4'))


# UPLOAD OBJECTS IN S3 BUCKET
# def upload_screenshots(name,file_path):
#     s3_object = name
#     s3_client.upload_file(
#         file_path,
#         bucket_name,
#         s3_object,
#         ExtraArgs={'ContentType': config.get("content-type", "CONTENT_TYPE")}
#     )
#     response = s3_client.head_object(Bucket=bucket_name, Key=s3_object)
#     # print(response)
#     my_bucket = boto3.resource('s3').Bucket(bucket_name)
#     url = ''
#     for my_bucket_object in my_bucket.objects.all():
#
#         # print(my_bucket_object.key)
#         url = create_presigned_url(bucket_name, my_bucket_object.key)
#         # print(url)
#         if url is not None:
#             response = requests.get(url)
#             # print(response)
#     return url
def upload_screenshots(name, file_path,model_path):
    s3_object = name
    s3_client.upload_file(
        file_path,
        bucket_name,
        s3_object,
        ExtraArgs={'ContentType': config.get("content-type", "CONTENT_TYPE")}
    )
    response = s3_client.head_object(Bucket=bucket_name, Key=s3_object)
    # print(response)

    secure_url = s3_client.generate_presigned_url('get_object',
                                           Params={'Bucket': bucket_name,
                                                   'Key': s3_object},
                                           ExpiresIn=604800, HttpMethod='GET')
    # url = url[0: url.index('?')]

    url=config.get('aws','cloudfront')+config.get('aws','BUCKET_FOLDER')+model_path
    #print(url)

    return secure_url


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
        response = response[0: response.index('?')]
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

def create_cf_url(model_path):
    url=config.get('aws','cloudfront')+config.get('aws','BUCKET_FOLDER')+model_path
    #print(url)
    return url
    


# DELETE OBJECTS FROM S3 BUCKET
def delete_object_from_bucket(file_name):
    response = s3_client.delete_object(Bucket=bucket_name, Key=file_name)
    print(response)


if __name__ == '__main__':

    # Getting response from S3 bucket
    response = s3_client.list_objects_v2(
        Bucket=bucket_name
    )

    # print(response)

    # Delete objects from S3 bucket
    for content in response.get('Contents', []):
        print(content)
        delete_object_from_bucket(content['Key'])
