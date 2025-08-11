import csv

# Read CSV and analyze missing Japanese names
with open('public/ListMJ_hostplants_master.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    
    total_rows = 0
    rows_with_japanese_name = 0
    rows_without_japanese_name = 0
    missing_examples = []
    
    for i, row in enumerate(reader, 2):  # Start from row 2 (after header)
        if len(row) > 23:
            total_rows += 1
            japanese_name = row[9].strip() if len(row) > 9 else ''
            scientific_name = row[23].strip() if len(row) > 23 else ''
            
            if japanese_name:
                rows_with_japanese_name += 1
            else:
                rows_without_japanese_name += 1
                if len(missing_examples) < 10:
                    missing_examples.append({
                        'row': i,
                        'scientific_name': scientific_name,
                        'host_plants': row[25] if len(row) > 25 else '',
                        'source': row[19] if len(row) > 19 else ''
                    })

print(f"Total data rows: {total_rows}")
print(f"Rows with Japanese name: {rows_with_japanese_name}")
print(f"Rows without Japanese name: {rows_without_japanese_name}")
print(f"\nExamples of rows without Japanese name:")
for example in missing_examples:
    print(f"  Row {example['row']}: {example['scientific_name']} (Source: {example['source']})")
    
# Expected total
butterflies = 270
beetles = 167
leafbeetles = 668
expected_with_all = total_rows + butterflies + beetles + leafbeetles
expected_with_named_only = rows_with_japanese_name + butterflies + beetles + leafbeetles

print(f"\n=== Expected Totals ===")
print(f"If all moths included: {expected_with_all}")
print(f"If only moths with Japanese names: {expected_with_named_only}")
print(f"Currently displayed: 7257")