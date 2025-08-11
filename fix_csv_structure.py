#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import re
import sys

def fix_csv_structure(input_file, output_file):
    """Fix CSV structure issues including split rows and misplaced data"""
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        rows = list(reader)
    
    print(f"Original CSV has {len(rows)} rows")
    
    fixed_rows = []
    i = 0
    
    while i < len(rows):
        current_row = rows[i]
        
        # Check if this is a split row case (missing moth name but has scientific name data)
        if (len(current_row) >= 24 and 
            not current_row[16] and  # Empty moth name (column 16)
            current_row[9]):  # Has genus name (column 9)
            
            # Look for the continuation row
            if i + 1 < len(rows):
                next_row = rows[i + 1]
                
                # Check if next row looks like a continuation (starts with empty fields but has scientific name)
                if (len(next_row) >= 24 and
                    not next_row[0] and not next_row[1] and not next_row[2] and  # Empty first few fields
                    len(next_row[7]) > 0 and '(' in next_row[7]):  # Has scientific name in column 7
                    
                    print(f"Found split row at lines {i+2}-{i+3}")
                    print(f"  Row 1: {current_row[9:16]}")  # genus to year
                    print(f"  Row 2: {next_row[7:11]}")     # scientific name and host
                    
                    # Merge the rows
                    merged_row = current_row.copy()
                    
                    # Extract moth name from genus name if available
                    if current_row[9] and not merged_row[16]:
                        merged_row[16] = current_row[9]  # Use genus as moth name temporarily
                    
                    # Move scientific name from next_row[7] to merged_row[23]
                    if next_row[7]:
                        merged_row[23] = next_row[7]
                    
                    # Move host plant data from next_row[8] to merged_row[24]  
                    if len(next_row) > 8 and next_row[8]:
                        merged_row[24] = next_row[8]
                    
                    # Move source from next_row[9] to merged_row[25]
                    if len(next_row) > 9 and next_row[9]:
                        merged_row[25] = next_row[9]
                    
                    # Move comments from next_row[10] to merged_row[26]
                    if len(next_row) > 10 and next_row[10]:
                        merged_row[26] = next_row[10]
                    
                    fixed_rows.append(merged_row)
                    i += 2  # Skip both rows
                    continue
        
        # Check for rows where moth name contains source/reference information
        if len(current_row) > 16 and current_row[16]:
            moth_name = current_row[16]
            
            # Check if moth name contains source references
            if re.search(r'日本産蛾類標準図鑑|標準図鑑|図鑑|文献|出典', moth_name):
                print(f"Found reference in moth name at line {i+2}: {moth_name}")
                
                # Try to extract actual moth name and move reference to appropriate field
                # This is a complex case that might need manual review
                current_row[16] = "要確認: " + moth_name  # Mark for manual review
        
        # Handle rows with missing moth names but present genus names
        if (len(current_row) > 16 and not current_row[16] and 
            current_row[9] and current_row[9] not in ['', '要確認']):
            
            # Try to construct moth name from genus if it looks like a Japanese name
            genus = current_row[9]
            if re.search(r'[ひらがなカタカナ漢字]', genus):
                print(f"Using genus as moth name at line {i+2}: {genus}")
                current_row[16] = genus
        
        fixed_rows.append(current_row)
        i += 1
    
    print(f"Fixed CSV has {len(fixed_rows)} rows (reduction: {len(rows) - len(fixed_rows)})")
    
    # Write the fixed CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(fixed_rows)
    
    print(f"Fixed CSV written to {output_file}")
    
    return len(rows) - len(fixed_rows)  # Return number of rows merged

def validate_fixes(csv_file):
    """Validate the fixes by checking for common issues"""
    issues_found = 0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        for line_num, row in enumerate(reader, start=2):
            # Check for empty moth names with scientific data
            if (len(row) > 16 and not row[16] and 
                any(row[i] for i in [9, 10, 11, 12, 13, 14, 15])):
                print(f"Still has empty moth name at line {line_num}")
                issues_found += 1
            
            # Check for source references in moth names
            if len(row) > 16 and row[16]:
                if re.search(r'日本産蛾類標準図鑑|標準図鑑|図鑑|文献|出典', row[16]):
                    print(f"Still has reference in moth name at line {line_num}: {row[16]}")
                    issues_found += 1
    
    print(f"Validation found {issues_found} remaining issues")
    return issues_found

if __name__ == "__main__":
    input_file = "/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master.csv"
    output_file = "/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master_fixed.csv"
    
    print("Starting CSV structure fix...")
    
    rows_merged = fix_csv_structure(input_file, output_file)
    
    print(f"\nFixed {rows_merged} split rows")
    
    print("\nValidating fixes...")
    remaining_issues = validate_fixes(output_file)
    
    if remaining_issues == 0:
        print("\nSuccess! All major issues have been resolved.")
    else:
        print(f"\nWarning: {remaining_issues} issues still remain and may need manual review.")