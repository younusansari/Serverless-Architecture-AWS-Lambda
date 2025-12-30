import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = "yunus-s3-bucket"
DAYS_OLD = 5

def lambda_handler(event, context):
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS_OLD)
    deleted = False

    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' not in response:
        print("No objects found in the bucket.")
        return

    for obj in response['Contents']:
        if obj['LastModified'] < cutoff_date:
            s3.delete_object(Bucket=BUCKET_NAME, Key=obj['Key'])
            print(f"Deleted: {obj['Key']}")
            deleted = True

    if not deleted:
        print("No files older than 5 days found. Nothing to delete.")
