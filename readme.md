aws-ip-ranges
=============

A  Lambda function to automatically create security groups for the address ranges of CloudFront, Route 53 Healthchecks and other AWS services. This can be helpful in case you want to grant access to your EC2 instances from only one of these services and want to have direct control over which security groups are updated. 

Since the IP address ranges change on regular basis and I'm leveraging several of these services, I found this the simplest way to manage security groups. By default it runs once per hour by default and can whitelist IP ranges for any of the following AWS services (as of December 2018);

- AMAZON
- AMAZON_CONNECT
- CLOUD9
- CLOUDFRONT
- CODEBUILD
- EC2
- GLOBALACCELERATOR
- ROUTE53
- ROUTE53_HEALTHCHECKS
- S3

The function retrieves the AWS IP ranges from the official JSON document containing updates; https://ip-ranges.amazonaws.com/ip-ranges.json .

The function can be considered an alternative to the SNS based function available on the CloudFront GitHub; https://github.com/aws-samples/aws-cloudfront-samples/tree/master/update_security_groups_lambda 

Installation
------------

Use the attached CloudFormation template to deploy the function to Lambda. Next, you should tag all the security groups which should be automatically refreshed with one of the service names mentioned in the AWS JSON file;  


![alt tag](https://raw.githubusercontent.com/marekq/aws-ip-ranges/master/docs/1.png)


When you now invoke the Lambda function, the logs should display the address ranges that are added or removed from the security groups;


![alt tag](https://raw.githubusercontent.com/marekq/aws-ip-ranges/master/docs/2.png)


To-do list
---------

- Add IPv6 support for security groups, currently only IPv4 ranges will be updated. 
- Integrate SNS as a trigger for the Lambda so that changes in IP ranges can be detected faster. 
- Add a simpler way to change the security group port and add UDP support.
- Add support for whitelisting PrivateLink connections available to in the VPC. 
- Add support for whitelisting custom ranges other than from AWS (i.e. a companies private/public IP ranges).

Contact
-------

In case of questions or bugs, please raise an issue or reach out to @marekq!