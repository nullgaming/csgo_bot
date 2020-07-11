from pathlib import Path
from dotenv import load_dotenv
import boto3, os
import json

load_dotenv()

class CSGO_EC2:
	def __init__(self):
		ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
		SECRET_KEY = os.getenv("AWS_SECRET_KEY")

		self.client = boto3.client(
			'ec2',
			aws_access_key_id=ACCESS_KEY,
			aws_secret_access_key=SECRET_KEY, region_name='ap-south-1'
		)

		self.instance_description = self.client.describe_instances()

	
	def get_instance_IP(self):
		try:
			instance_ip = self.instance_description['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicIp']
			return instance_ip
		except KeyError:
			return "Server not started yet"



	def get_instance_id(self):
		try:
			instance_id = self.instance_description['Reservations'][0]['Instances'][0]['InstanceId']
			return instance_id
		except KeyError as e:
			raise Exception("No Instances found")



	def get_server_status(self):
		# update server status
		self.instance_description = self.client.describe_instances()
		
		# pending runnning shutting-down terminated stopping stoppped
		return self.instance_description['Reservations'][0]['Instances'][0]['State']['Name']



	def start_server(self):
		response = self.client.start_instances(
			InstanceIds = [
				self.get_instance_id()
			],
			AdditionalInfo='string',
			DryRun=False
		)

		return response

	
	def stop_server(self):
		response = self.client.stop_instances(
			InstanceIds = [
				self.get_instance_id()
			],
			Hibernate=False,
			DryRun=False,
			Force=True
		)

		return response
