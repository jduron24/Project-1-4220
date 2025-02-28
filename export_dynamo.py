import boto3
import json
import os

# Load AWS Credentials from environment variables
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
REGION = os.environ.get('AWS_DEFAULT_REGION')

# Initialize DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION
)

# Define tables to export
tables = {
    "Users": "data1.json",
    "PhotoGallery": "data2.json"
}

def export_table(table_name, output_file):
    """Scans a DynamoDB table and exports it to a JSON file."""
    table = dynamodb.Table(table_name)
    
    try:
        response = table.scan()
        items = response['Items']
        
        with open(output_file, 'w') as f:
            json.dump(items, f, indent=4)
        
        print(f"✅ Successfully exported {len(items)} items from {table_name} to {output_file}")
    
    except Exception as e:
        print(f"❌ Error exporting {table_name}: {e}")

# Run the export for each table
for table, file in tables.items():
    export_table(table, file)
