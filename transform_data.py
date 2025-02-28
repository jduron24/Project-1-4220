import json

def transform_item(item):
    """Convert DynamoDB JSON format to MongoDB-compatible JSON."""
    
    # Rename `id` to `_id` (MongoDB requires `_id`)
    if 'id' in item:
        item['_id'] = str(item.pop('id'))  # Ensure it's a string

    # Convert number strings to actual numbers
    for key, value in item.items():
        if isinstance(value, str) and value.isdigit():
            item[key] = int(value)  # Convert to integer
        elif isinstance(value, dict) and 'N' in value:
            item[key] = int(value['N'])  # DynamoDB Number
        elif isinstance(value, dict) and 'SS' in value:
            item[key] = value['SS']  # Convert DynamoDB StringSet to list

    return item

def transform_file(input_file, output_file):
    """Load JSON, transform it, and save to a new file."""
    with open(input_file, 'r') as f:
        data = json.load(f)

    transformed_data = [transform_item(item) for item in data]

    with open(output_file, 'w') as f:
        json.dump(transformed_data, f, indent=4)

    print(f"✅ Transformed {len(transformed_data)} items from {input_file} to {output_file}")

# Process both files
transform_file("data1.json", "transformed_data1.json")
transform_file("data2.json", "transformed_data2.json")
