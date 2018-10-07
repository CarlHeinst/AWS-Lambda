import boto3
# Enter the region your instances are in. Include only the region without specifying Availability Zone; e.g., 'us-east-1'
region = 'eu-west-2'
# Enter your instances here: ex. ['X-XXXXXXXX', 'X-XXXXXXXX']

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    reservations = ec2.describe_instances()['Reservations']
    instances = []
    for reservation in reservations:
         for instance in reservation['Instances']:
             instances.append(instance['InstanceId'])
    print (instances)
    ec2.stop_instances(InstanceIds=instances)
    
    ## The above code will locate all ec2 instances in your given region and then cause them to stop.
    
    RDS = boto3.client('rds',region_name=region)
    rds_reservations = RDS.describe_db_instances()['DBInstances']
    rds_instances = []
    for rds_reservation in rds_reservations:
        rds_instances.append(rds_reservation['DBInstanceIdentifier'])
    print ("Halting instances: {0}".format(str(rds_instances)))
    
    for rds_instance in rds_instances:
        try:
            responseOne = RDS.stop_db_instance(DBInstanceIdentifier=rds_instance)
        except:
            print ("Database Offline, continuing.")
            
    ## The above code will locate all RDS instances in your given region and then cause them to stop.
    
    print ("By Your Command - Halting Legion instances: \n{0}".format(str(instances)))
