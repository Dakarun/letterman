import boto3


def get_ec2_client():
    session = boto3.session.Session()
    return session.client('ec2')
