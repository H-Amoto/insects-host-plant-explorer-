#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import re

def final_cleanup(input_file, output_file):
    """Final cleanup to merge remaining split rows"""
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        rows = list(reader)
    
    print(f"Final cleanup on {len(rows)} rows")
    
    cleaned_rows = []
    i = 0
    merges = 0
    
    while i < len(rows):
        current_row = rows[i]
        
        # Ensure row has enough columns
        while len(current_row) < 32:
            current_row.append('')
        
        # Look for specific split row pattern: 
        # Current row has scientific name structure but empty moth name
        # Next row starts empty but has scientific name in field 7
        if (i + 1 < len(rows) and
            current_row[9] and current_row[11] and not current_row[16] and  # Has genus/species but no moth name
            not rows[i+1][0] and not rows[i+1][1] and  # Next row starts empty
            len(rows[i+1]) > 7 and rows[i+1][7] and '(' in rows[i+1][7]):  # Next row has scientific name
            
            next_row = rows[i+1]
            
            print(f"Merging split rows at lines {i+2}-{i+3}")
            print(f"  Current: genus={current_row[9]}, species={current_row[11]}")
            print(f"  Next: sci_name={next_row[7]}")
            
            # Extract moth name from the scientific name in next row
            sci_name = next_row[7]
            # Try to find Japanese name or construct one
            if current_row[9]:
                # Use genus if it contains Japanese characters
                if re.search(r'[ひらがなカタカナ漢字]', current_row[9]):
                    current_row[16] = current_row[9]
                # Otherwise, try to extract from scientific name
                elif sci_name:
                    # Extract genus from scientific name for cases like "Thinopteryx delectans"
                    genus_match = re.match(r'^([A-Z][a-z]+)', sci_name)
                    if genus_match and genus_match.group(1) == current_row[9]:
                        # This confirms it's the same species, need to find Japanese name elsewhere
                        current_row[16] = f"{current_row[9]} sp."  # Temporary placeholder
            
            # Move data from next row to current row
            current_row[23] = next_row[7]  # Scientific name
            if len(next_row) > 8 and next_row[8]:
                current_row[24] = next_row[8]  # Host plants
            if len(next_row) > 9 and next_row[9]:
                current_row[25] = next_row[9]  # Source
            if len(next_row) > 10 and next_row[10]:
                current_row[26] = next_row[10]  # Comments
            
            cleaned_rows.append(current_row)
            merges += 1
            i += 2  # Skip both rows
            continue
        
        # Handle remaining rows with moth names in wrong places
        if (not current_row[16] and current_row[9] and 
            re.search(r'[ひらがなカタカナ漢字]', current_row[9])):
            current_row[16] = current_row[9]
            print(f"Moving Japanese name from genus to moth name: {current_row[9]}")
        
        cleaned_rows.append(current_row)
        i += 1
    
    print(f"Merged {merges} split row pairs")
    print(f"Cleaned CSV has {len(cleaned_rows)} rows (reduction: {len(rows) - len(cleaned_rows)})")
    
    # Write the cleaned CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(cleaned_rows)
    
    print(f"Cleaned CSV written to {output_file}")
    return merges

def final_validation(csv_file):
    """Final validation of the cleaned CSV"""
    
    empty_names = 0
    total_rows = 0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        for line_num, row in enumerate(reader, start=2):
            total_rows += 1
            if len(row) > 16:
                # Count empty moth names where there should be one
                if (not row[16] and 
                    (row[23] or (row[9] and row[11]))):  # Has scientific name data
                    empty_names += 1
                    if empty_names <= 5:  # Show first 5
                        print(f"Still empty moth name at line {line_num}: sci_name={row[23]}, genus={row[9]}")
    
    print(f"\nFinal validation:")
    print(f"Total rows: {total_rows}")
    print(f"Empty moth names: {empty_names}")
    print(f"Completion rate: {((total_rows - empty_names) / total_rows * 100):.1f}%")
    
    return empty_names

if __name__ == "__main__":
    input_file = "/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master_final_fixed.csv"
    output_file = "/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master_cleaned.csv"
    
    print("Starting final cleanup...")
    
    merges = final_cleanup(input_file, output_file)
    
    print(f"\nPerformed {merges} final merges")
    
    remaining = final_validation(output_file)
    
    print(f"\nFINAL RESULT:")
    print(f"Successfully cleaned CSV with {remaining} remaining issues")
    print(f"Final file: {output_file}")