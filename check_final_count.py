import csv

# Check all counts
with open('public/ListMJ_hostplants_master.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    total_rows = 0
    has_wamei = 0
    has_zokumei = 0
    has_both = 0
    has_neither = 0
    examples_neither = []
    
    for i, row in enumerate(reader, 2):
        total_rows += 1
        wamei = row.get('和名', '').strip()
        zokumei = row.get('属名', '').strip()
        
        if wamei and zokumei:
            has_both += 1
        elif wamei:
            has_wamei += 1
        elif zokumei:
            has_zokumei += 1
        else:
            has_neither += 1
            if len(examples_neither) < 10:
                examples_neither.append({
                    'row': i,
                    'data': {k: v for k, v in row.items() if v}
                })

print(f"Total rows: {total_rows}")
print(f"Has only 和名: {has_wamei}")
print(f"Has only 属名: {has_zokumei}")
print(f"Has both 和名 and 属名: {has_both}")
print(f"Has neither: {has_neither}")

if examples_neither:
    print(f"\nExamples of rows with neither 和名 nor 属名:")
    for ex in examples_neither:
        print(f"  Row {ex['row']}: {ex['data']}")

# Calculate expected
butterflies = 270
beetles = 167
leafbeetles = 668

print(f"\n=== Calculations ===")
print(f"Moths that should be loaded: {has_wamei + has_zokumei + has_both}")
print(f"Other insects: {butterflies} + {beetles} + {leafbeetles} = {butterflies + beetles + leafbeetles}")
print(f"Expected total: {has_wamei + has_zokumei + has_both + butterflies + beetles + leafbeetles}")
print(f"Currently displayed: 7335")
print(f"Missing: {has_wamei + has_zokumei + has_both + butterflies + beetles + leafbeetles - 7335}")