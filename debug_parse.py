import csv

# Parse CSV with header mapping
with open('public/ListMJ_hostplants_master.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    total_rows = 0
    rows_with_japanese_name = 0
    rows_without_japanese_name = 0
    missing_examples = []
    
    for i, row in enumerate(reader, 2):  # Start from row 2 (after header)
        total_rows += 1
        japanese_name = row.get('和名', '').strip()
        
        if japanese_name:
            rows_with_japanese_name += 1
        else:
            rows_without_japanese_name += 1
            if len(missing_examples) < 10:
                missing_examples.append({
                    'row': i,
                    'all_fields': row
                })

print(f"Total data rows: {total_rows}")
print(f"Rows with Japanese name: {rows_with_japanese_name}")
print(f"Rows without Japanese name: {rows_without_japanese_name}")

if missing_examples:
    print(f"\nFirst row without Japanese name:")
    for key, value in missing_examples[0]['all_fields'].items():
        if value:
            print(f"  {key}: {value}")