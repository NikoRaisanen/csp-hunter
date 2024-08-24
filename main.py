import requests
import json
from pprint import pprint
import boto3
from botocore.exceptions import ClientError

ACCESS_KEY = None
SECRET_KEY = None
with open('./secrets.json', 'r') as fp:
    data = json.load(fp)
    ACCESS_KEY = data.get('accessKey', '')
    SECRET_KEY = data.get('secretAccessKey', '')

def check_bucket_exists(bucket_name):
    """Check if an S3 bucket exists."""
    # Initialize an S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name='us-west-2'
    )

    try:
        bucket_region = s3_client.head_bucket(Bucket=bucket_name).get('BucketRegion')

        print(f"Bucket '{bucket_name}' exists in region {bucket_region}.")
        return True
    except ClientError as e:
        # If a client error is thrown w/ status 404 -> bucket does not exist
        print('error: ', e)
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"Bucket '{bucket_name}' does not exist.")
        else:
            print(f"ClientError: {e}")
        return False
    
# NOTE for v2: Check domain availability: https://docs.aws.amazon.com/Route53/latest/APIReference/API_domains_CheckDomainAvailability.html
def call_api(url: str):
    r = requests.get(url)
    print("Status:", r.status_code)

    # Check if the Content-Security-Policy header exists
    csp_header = r.headers.get("Content-Security-Policy")
    return csp_header


def parse_csp(csp: str):
    directives = csp.split(";")
    csp_dict = {}

    for directive in directives:
        if directive.strip():
            parts = directive.strip().split(" ")
            directive_name = parts[0]
            sources = parts[1:] if len(parts) > 1 else []
            csp_dict[directive_name] = sources

    return csp_dict


if __name__ == "__main__":
    check_bucket_exists('nikoraisanen.com')
    domain = input()
    csp = call_api(domain)
    if not csp:
        raise ValueError('No CSP to evaluate')
    parsed_csp = parse_csp(csp)
    print("Parsed Content-Security-Policy:")
    pprint(parsed_csp)
