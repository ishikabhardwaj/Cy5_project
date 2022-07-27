import boto3
import json

# Create IAM client
iam = boto3.client('iam')

user={}
access_key_data={}
access_key={}

# List users with the pagination interface
paginator = iam.get_paginator('list_users')
for response in paginator.paginate():
    print(response)

for i in range(len(response['Users'])):
    user[response['Users'][i]['UserName']]= {'PasswordLastUsed': response['Users'][i]['PasswordLastUsed']}


# List access keys through the pagination interface.
paginator = iam.get_paginator('list_access_keys')
for i in user:
    access_key_data={}
    for access_key_response in paginator.paginate(UserName=i):
        print(access_key_response)


    for j in range(len(access_key_response['AccessKeyMetadata'])):
        access_key={}
        access_key['AccessKeyId']= access_key_response['AccessKeyMetadata'][j]['AccessKeyId']
        access_key['CreateDate']= access_key_response['AccessKeyMetadata'][j]['CreateDate']

        # Get last use of access key
        last_used = iam.get_access_key_last_used(
            AccessKeyId=access_key_response['AccessKeyMetadata'][j]['AccessKeyId']
        )
        access_key['LastUsed']= last_used['AccessKeyLastUsed']

        access_key_data[j]=access_key
        
    user[i]['AccessKeyData']= access_key_data

# Serializing json
user_json = json.dumps(user,  indent=4, default=str)
print(user_json)

 
# Writing to sample.json
with open("userdata.json", "w") as outfile:
    outfile.write(user_json)