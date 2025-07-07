# src/dbt_mapper.py

##############################
# # Example usage
# steps = parse_dbt_schema("data_dictionary/schema.yml")
# for step in steps:
#     print(step)
##############################

import yaml

def parse_dbt_schema(schema_path):
    with open(schema_path, 'r') as f:
        schema = yaml.safe_load(f)

    cleaning_steps = []
    model = schema['models'][0]  # Simple example: first model
    for col in model['columns']:
        col_name = col['name']
        desc = col.get('description', '')
        tests = col.get('tests', [])

        if 'not_null' in tests:
            cleaning_steps.append(f"Drop rows where {col_name} is null")
        if 'YYYY-MM-DD' in desc:
            cleaning_steps.append(f"Convert {col_name} to datetime format YYYY-MM-DD")
        if 'redact' in desc.lower():
            cleaning_steps.append(f"Redact {col_name}")
        if '0-120' in desc:
            cleaning_steps.append(f"Filter {col_name} between 0 and 120")
        if 'Gender' in desc:
            cleaning_steps.append(f"Standardize categories in {col_name} to Male, Female, Other")

    return cleaning_steps
