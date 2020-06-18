from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

import boto3, os

ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
SECRET_KEY = os.getenv("AWS_SECRET_KEY")

client = boto3.client(
    'ec2',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY, region_name='ap-south-1'
)

response = client.describe_instances()

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        print(instance)
        print(instance["InstanceId"])