import boto3, json, os
from botocore.vendored import requests
#from netaddr import *

ec2     			= boto3.client('ec2')
port				= 443
proto				= 'tcp'

def main(sgname, sgjson):
	c       	= int(0)
	sg_list 	= []
	json_list	= []
	sg_id		= ''

	try:
		sg  	= ec2.describe_security_groups(Filters=[{'Name': 'tag:dnsservice', 'Values': [sgname]}])['SecurityGroups']

	except:
		sg		= []

	for z in sg:
		sg_id	= z['GroupId']
		for a in z['IpPermissions']:
			for b in a['IpRanges']:
				sg_list.append(b['CidrIp'])
				
	for y in json.loads(sgjson.text)['prefixes']:
		if y['service'] == sgname:
			json_list.append(y['ip_prefix'])
			c   += int(1)

	if sg_id != '':
		for sg in sg_list:
			if sg not in json_list:
				ec2.revoke_security_group_ingress(GroupId = sg_id, IpProtocol = proto, CidrIp = sg, FromPort = int(port), ToPort = int(port))
				print(sg_id+' removing '+sg)
		
		for y in json_list:		
			if y not in sg_list:
				ec2.authorize_security_group_ingress(GroupId = sg_id, IpProtocol = proto, CidrIp = y, FromPort = int(port), ToPort = int(port))
				print(sg_id+' adding '+y)
	
		print(str(c), 'items in ', str(sgname), str(sg_id))

def lambda_handler(event, context):
	serv	= []
	sgjson	= requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json')
	for y in json.loads(sgjson.text)['prefixes']:
		if y['service'] not in serv:
			serv.append(y['service'])

	for s in serv:
		main(s, sgjson)