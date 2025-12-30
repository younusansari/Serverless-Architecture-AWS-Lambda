import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    buckets = s3.list_buckets().get('Buckets', [])
    non_kms_buckets = []

    for bucket in buckets:
        bucket_name = bucket['Name']
        try:
            enc = s3.get_bucket_encryption(Bucket=bucket_name)
            rules = enc['ServerSideEncryptionConfiguration']['Rules']
            sse_algo = rules[0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']

            if sse_algo != 'aws:kms':
                non_kms_buckets.append(bucket_name)
                print(f"❌ Non-KMS bucket: {bucket_name} (Using {sse_algo})")
            else:
                print(f"✅ SSE-KMS enabled: {bucket_name}")

        except ClientError as e:
            # Only log unexpected errors (permission, throttling, etc.)
            print(f"⚠️ Unable to evaluate bucket {bucket_name}: {e}")

    if non_kms_buckets:
        print(f"\nTotal buckets NOT using SSE-KMS: {len(non_kms_buckets)}")
    else:
        print("🎉 All buckets are compliant with SSE-KMS")

    return {
        "non_kms_buckets": non_kms_buckets
    }
