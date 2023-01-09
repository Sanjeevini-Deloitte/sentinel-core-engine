import configparser
import json
import boto3
from botocore.exceptions import ClientError
import logging
from datetime import datetime
import time
config = configparser.RawConfigParser()
config.read('config.properties')

AWS_REGION = config.get("aws","AWS_REGION")
sqs_client = boto3.client("sqs", region_name=AWS_REGION)
sqs_resource = boto3.resource("sqs", region_name=AWS_REGION)
QUEUE_URL = config.get("aws","QUEUE_URL")
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')



def send_queue_message( msg_body,group):
    """
    Sends a message to the specified queue.
    """
    # print("Entered sqs")
    d_id =time.strftime('%Y%m%d%H%M%S')+str(datetime.now().microsecond)
    try:
        response = sqs_client.send_message(QueueUrl=QUEUE_URL,
                                           MessageBody=msg_body,
                                           MessageDeduplicationId=d_id,
                                           MessageGroupId=group)
        #print("DID -",d_id)
    except ClientError:
        logger.exception(f'Could not send meessage to the - {QUEUE_URL}.')
        raise
    else:
        return response


def receive_message():
    sqs_client = boto3.client("sqs", region_name="us-east-2")
    response = sqs_client.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=2,
    )
    print(f"Number of messages received: {len(response.get('Messages', []))}")

    for message in response.get("Messages", []):
        message_body = message["Body"]
        print(f"Message body: {json.loads(message_body)}")
        # print(f"Receipt Handle: {message['ReceiptHandle']}")
    return response


def delete_message(receipt_handle):
    sqs_client = boto3.client("sqs", region_name="us-east-2")
    response = sqs_client.delete_message(
        QueueUrl=QUEUE_URL,
        ReceiptHandle=receipt_handle,
    )
    print(response)


if __name__ == '__main__':

    mydictionary={"date": "2022-11-13", "violationType": "FIRE",
     "imageLink": "https://i.pinimg.com/736x/9a/2a/98/9a2a988dc97d2833c174d36e3e67bc83.jpg", "intensityLevel": 13,
     "confidenceLevel": 90, "cameraNo": 7, "time": "18:59:22"}
    data=json.dumps(mydictionary)
    send_queue_message(data,"test")


    messages = receive_message()
    print(messages)
    for message in messages.get("Messages", []):
        print(message)
        delete_message(message['ReceiptHandle'])
