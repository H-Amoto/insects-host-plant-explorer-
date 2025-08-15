#!/usr/bin/env python3
import csv

# Debug the ヨモギネムシガ merge issue
input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master.csv'

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    rows = list(reader)

# Check rows 2253 and 2254 (1-based) = indexes 2252 and 2253 (0-based)
row1 = rows[2252]  # Row 2253: has Japanese name, no food plant
row2 = rows[2253]  # Row 2254: has food plant, no Japanese name in basic info

print("Row 2253 (index 2252):")
print(f"  Japanese name (col 19): '{row1[18] if len(row1) > 18 else ''}'")
print(f"  Scientific name (col 26): '{row1[25] if len(row1) > 25 else ''}'")
print(f"  Food plant 1 (col 27): '{row1[26] if len(row1) > 26 else ''}'")
print()

print("Row 2254 (index 2253):")
print(f"  Japanese name (col 19): '{row2[18] if len(row2) > 18 else ''}'")
print(f"  Scientific name (col 26): '{row2[25] if len(row2) > 25 else ''}'")
print(f"  Food plant 1 (col 27): '{row2[26] if len(row2) > 26 else ''}'")
print()

# Test the matching logic from the script
japanese_name1 = row1[18].strip() if len(row1) > 18 else ""
scientific_name1 = row1[25].strip() if len(row1) > 25 else ""
japanese_name2 = row2[18].strip() if len(row2) > 18 else ""
scientific_name2 = row2[25].strip() if len(row2) > 25 else ""

print("Matching logic test:")
print(f"Row 2253 has Japanese: {bool(japanese_name1)}")
print(f"Row 2254 has Japanese: {bool(japanese_name2)}")
print(f"Row 2253 has Scientific: {bool(scientific_name1)}")
print(f"Row 2254 has Scientific: {bool(scientific_name2)}")
print()

# Check if they would match by the script's logic
match = False
if japanese_name1 and japanese_name2 and japanese_name1 == japanese_name2:
    print("Match by Japanese names: YES")
    match = True
elif scientific_name1 and scientific_name2 and scientific_name1 == scientific_name2:
    print("Match by Scientific names: YES")
    match = True
elif japanese_name1 and scientific_name2 and not japanese_name2:
    if abs(2252 - 2253) <= 5:
        print("Match by Japanese->Scientific proximity: YES")
        match = True
elif scientific_name1 and japanese_name2 and not japanese_name1:
    if abs(2252 - 2253) <= 5:
        print("Match by Scientific->Japanese proximity: YES")
        match = True

if not match:
    print("NO MATCH DETECTED - This is the problem!")