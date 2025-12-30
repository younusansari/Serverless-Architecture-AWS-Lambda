import boto3

ec2 = boto3.client('ec2')

def get_instances(action, state):
    resp = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': [action]},
            {'Name': 'instance-state-name', 'Values': [state]}
        ]
    )
    return [i['InstanceId']
            for r in resp['Reservations']
            for i in r['Instances']]


# Fetch instances
to_stop = get_instances('Auto-Stop', 'running')
to_start = get_instances('Auto-Start', 'stopped')


# Stop / Start instances
if to_stop:
    ec2.stop_instances(InstanceIds=to_stop)
    print("Stopped:", to_stop)

if to_start:
    ec2.start_instances(InstanceIds=to_start)
    print("Started:", to_start)

if not to_stop and not to_start:
    print("No instances affected.")
