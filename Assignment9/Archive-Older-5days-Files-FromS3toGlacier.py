import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = 'yunus-s3-bucket'
DAYS_OLD = 5  # Archive files older than 5 days

def lambda_handler(event, context):
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS_OLD)
    archived_files = []

    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' not in response:
        print("Bucket is empty")
        return

    for obj in response['Contents']:
        key = obj['Key']
        last_modified = obj['LastModified']
        storage_class = obj.get('StorageClass', 'STANDARD')

        if last_modified < cutoff_date and storage_class == 'STANDARD':
            s3.copy_object(
                Bucket=BUCKET_NAME,
                CopySource={'Bucket': BUCKET_NAME, 'Key': key},
                Key=key,
                StorageClass='GLACIER',
                MetadataDirective='REPLACE'
            )

            archived_files.append(key)
            print(f"Archived to Glacier: {key}")

    if not archived_files:
        print("No files older than 5 days found")
    else:
        print(f"Total files archived: {len(archived_files)}")
