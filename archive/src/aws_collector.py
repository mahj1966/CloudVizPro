# aws_collector.py

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from database_utils import save_resource  # Utility function to save resources to the database

# Initialize logging for better debugging and error tracking
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper function to handle pagination
def paginate(client, operation_name, **kwargs):
    """
    Handles pagination for AWS API calls.
    :param client: Boto3 client object.
    :param operation_name: Name of the operation to paginate.
    :param kwargs: Additional arguments for the operation.
    :return: Generator yielding paginated results.
    """
    paginator = client.get_paginator(operation_name)
    for page in paginator.paginate(**kwargs):
        yield page


# Function to collect EC2 instances
def collect_ec2_instances():
    """
    Collects EC2 instance data from AWS.
    """
    try:
        ec2_client = boto3.client('ec2')
        instances = []

        # Paginate through EC2 instances
        for response in paginate(ec2_client, 'describe_instances'):
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instances.append({
                        'id': instance.get('InstanceId'),
                        'type': 'EC2',
                        'data': instance
                    })
                    save_resource(
                        resource_id=instance.get('InstanceId'),
                        service_name="EC2",
                        resource_type="Instance",
                        resource_data=instance
                    )

        logger.info(f"Collected {len(instances)} EC2 instances.")
        return instances

    except (ClientError, NoCredentialsError) as e:
        logger.error(f"Error collecting EC2 instances: {e}")
        return []


# Function to collect S3 buckets
def collect_s3_buckets():
    """
    Collects S3 bucket data from AWS.
    """
    try:
        s3_client = boto3.client('s3')
        buckets = []

        # List all S3 buckets
        response = s3_client.list_buckets()
        for bucket in response['Buckets']:
            buckets.append({
                'id': bucket.get('Name'),
                'type': 'S3',
                'data': bucket
            })
            save_resource(
                resource_id=bucket.get('Name'),
                service_name="S3",
                resource_type="Bucket",
                resource_data=bucket
            )

        logger.info(f"Collected {len(buckets)} S3 buckets.")
        return buckets

    except (ClientError, NoCredentialsError) as e:
        logger.error(f"Error collecting S3 buckets: {e}")
        return []


# Function to collect RDS instances
def collect_rds_instances():
    """
    Collects RDS instance data from AWS.
    """
    try:
        rds_client = boto3.client('rds')
        instances = []

        # Paginate through RDS instances
        for response in paginate(rds_client, 'describe_db_instances'):
            for db_instance in response['DBInstances']:
                instances.append({
                    'id': db_instance.get('DBInstanceIdentifier'),
                    'type': 'RDS',
                    'data': db_instance
                })
                save_resource(
                    resource_id=db_instance.get('DBInstanceIdentifier'),
                    service_name="RDS",
                    resource_type="Instance",
                    resource_data=db_instance
                )

        logger.info(f"Collected {len(instances)} RDS instances.")
        return instances

    except (ClientError, NoCredentialsError) as e:
        logger.error(f"Error collecting RDS instances: {e}")
        return []


# Function to collect Lambda functions
def collect_lambda_functions():
    """
    Collects Lambda function data from AWS.
    """
    try:
        lambda_client = boto3.client('lambda')
        functions = []

        # Paginate through Lambda functions
        for response in paginate(lambda_client, 'list_functions'):
            for func in response['Functions']:
                functions.append({
                    'id': func.get('FunctionName'),
                    'type': 'Lambda',
                    'data': func
                })
                save_resource(
                    resource_id=func.get('FunctionName'),
                    service_name="Lambda",
                    resource_type="Function",
                    resource_data=func
                )

        logger.info(f"Collected {len(functions)} Lambda functions.")
        return functions

    except (ClientError, NoCredentialsError) as e:
        logger.error(f"Error collecting Lambda functions: {e}")
        return []


# Main execution block
if __name__ == "__main__":
    logger.info("Starting AWS resource collection...")
    
    # Collect data for each service
    collect_ec2_instances()
    collect_s3_buckets()
    collect_rds_instances()
    collect_lambda_functions()

    logger.info("AWS resource collection completed.")