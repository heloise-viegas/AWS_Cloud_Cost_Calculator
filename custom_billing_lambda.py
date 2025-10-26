import json
import boto3
from datetime import datetime, timedelta
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
#fetch json from cloudwatch billing metrics
 
#connect to aws account
ce=boto3.client('ce')
s3=boto3.client('s3')

BUCKET_NAME = os.environ['BUCKET_NAME']
KEY = os.environ.get('BILLING_KEY', 'billing_report.json')
COMPARISON_KEY = os.environ.get('COMPARISON_KEY', 'comparison_report.json')

def lambda_handler(event, context):

    #fetch last weeks data
    report_old = {}
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=KEY)
        report_old = json.loads(obj['Body'].read())
    except s3.exceptions.NoSuchKey:
        report_old = {}  # first time, no previous data



    # Last 7 days
    end = datetime.utcnow().date()
    start = end - timedelta(days=7)

    resp = ce.get_cost_and_usage(
        TimePeriod={'Start': str(start), 'End': str(end)},
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    logger.info(json.dumps(resp, indent=2, default=str))


    report = {}
    for day in resp['ResultsByTime']:
        for g in day['Groups']:
            service = g['Keys'][0]
            cost = float(g['Metrics']['UnblendedCost']['Amount'])
            report[service] = report.get(service, 0) + cost

    # Add total
    report['Total'] = sum(report.values())



    # Save to S3
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=KEY,
        Body=json.dumps(report, indent=2),
        ContentType='application/json'
    )


# Compare old and new reports
    comparison = {}
    all_services = set(report_old.keys()) | set(report.keys())
    all_services.discard('Total') 

    for service in all_services:
        prev = report_old.get(service, 0)
        curr = report.get(service, 0)
        diff = curr - prev
        percent_change = ((diff / prev) * 100) if prev != 0 else 100
        comparison[service] = {
            "previous": prev,
            "current": curr,
            "diff": diff,
            "percent_change": percent_change
        }

    logger.info("Comparison: %s", json.dumps(comparison, indent=2))

    # Save comparison to S3
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=COMPARISON_KEY,
        Body=json.dumps({"services": comparison}, indent=2),
        ContentType='application/json'
    )


    return {'statusCode': 200, 'body': 'Billing report updated in S3'}
