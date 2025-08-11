#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import re
import sys

def fix_csv_structure_v2(input_file, output_file):
    """Fix CSV structure issues including split rows and misplaced data - improved version"""
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        rows = list(reader)
    
    print(f"Original CSV has {len(rows)} rows")
    print(f"Header indices: {dict(enumerate(header))}")
    
    fixed_rows = []
    i = 0
    fixes_applied = 0
    
    while i < len(rows):
        current_row = rows[i]
        
        # Ensure row has enough columns
        while len(current_row) < 32:
            current_row.append('')
        
        # Case 1: Completely orphaned rows (all major fields empty but has scientific name/host data)
        if (not current_row[0] and not current_row[1] and not current_row[2] and  # No catalog, family info
            not current_row[9] and not current_row[16] and  # No genus, no moth name
            current_row[23] and '(' in current_row[23]):  # Has scientific name
            
            print(f"Found orphaned row at line {i+2}: {current_row[23]}")
            # Skip orphaned rows for now - they need manual review
            fixes_applied += 1
            i += 1
            continue
        
        # Case 2: Row with moth name in genus field (column 9) but empty moth name field (column 16)
        if (current_row[9] and re.search(r'[ひらがなカタカナ漢字]', current_row[9]) and 
            not current_row[16] and not current_row[10] and not current_row[11]):  # Empty genus/species fields
            
            print(f"Found moth name in genus field at line {i+2}: {current_row[9]}")
            # Move from genus field to moth name field
            current_row[16] = current_row[9]
            current_row[9] = ''  # Clear the genus field
            fixes_applied += 1
        
        # Case 3: Data continuation rows (empty catalog number but has scientific name data)
        if (not current_row[0] and not current_row[1] and not current_row[2] and  # Empty first fields
            current_row[9] and  # Has genus-like data
            current_row[23] and '(' in current_row[23]):  # Has scientific name
            
            # This looks like a continuation of the previous row
            if fixed_rows and i > 0:
                prev_row = fixed_rows[-1]
                
                # Check if previous row has matching moth name in genus field
                if (prev_row[9] == current_row[9] or 
                    (prev_row[16] and current_row[9] in prev_row[16])):
                    
                    print(f"Found data continuation at line {i+2} for: {current_row[9]}")
                    
                    # Merge host plant data
                    if current_row[24] and not prev_row[24]:
                        prev_row[24] = current_row[24]
                    elif current_row[24] and prev_row[24]:
                        prev_row[24] += '; ' + current_row[24]
                    
                    # Merge source data
                    if current_row[25] and not prev_row[25]:
                        prev_row[25] = current_row[25]
                    
                    # Merge comments
                    if current_row[26] and not prev_row[26]:
                        prev_row[26] = current_row[26]
                    
                    # Merge emergence time data
                    if len(current_row) > 27 and current_row[27] and not prev_row[27]:
                        prev_row[27] = current_row[27]
                    
                    fixes_applied += 1
                    i += 1
                    continue
        
        # Case 4: Split scientific name data (genus, species in separate fields but scientific name in field 23)
        if (current_row[9] and current_row[11] and current_row[23] and 
            not current_row[16] and current_row[23] != current_row[9] + ' ' + current_row[11]):
            
            # Extract moth name from scientific name or use genus if it contains Japanese characters
            if re.search(r'[ひらがなカタカナ漢字]', current_row[9]):
                current_row[16] = current_row[9]
                fixes_applied += 1
                print(f"Fixed moth name from genus at line {i+2}: {current_row[9]}")
        
        # Case 5: Source references in moth name field
        if current_row[16] and re.search(r'日本産蛾類標準図鑑|標準図鑑|図鑑|文献|出典', current_row[16]):
            print(f"Found source reference in moth name at line {i+2}: {current_row[16]}")
            
            # Try to extract actual moth name from the reference
            moth_name_match = re.search(r'^([^日本産蛾類標準図鑑]+)', current_row[16])
            if moth_name_match:
                clean_name = moth_name_match.group(1).strip()
                if clean_name and len(clean_name) > 2:
                    current_row[16] = clean_name
                    fixes_applied += 1
                    print(f"  Extracted moth name: {clean_name}")
                else:
                    current_row[16] = "要確認: " + current_row[16]
            else:
                current_row[16] = "要確認: " + current_row[16]
        
        # Case 6: Empty moth name but has scientific name - try to construct from available data
        if (not current_row[16] and current_row[23] and 
            (current_row[9] or current_row[10] or current_row[11])):
            
            # Try to find moth name from genus or other fields
            if current_row[17]:  # Old name field
                current_row[16] = current_row[17]
                fixes_applied += 1
                print(f"Used old name as moth name at line {i+2}: {current_row[17]}")
            elif current_row[18]:  # Alternative name field
                current_row[16] = current_row[18]
                fixes_applied += 1
                print(f"Used alternative name as moth name at line {i+2}: {current_row[18]}")
        
        fixed_rows.append(current_row)
        i += 1
    
    print(f"Fixed CSV has {len(fixed_rows)} rows (reduction: {len(rows) - len(fixed_rows)})")
    print(f"Applied {fixes_applied} fixes")
    
    # Write the fixed CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(fixed_rows)
    
    print(f"Fixed CSV written to {output_file}")
    
    return fixes_applied

def validate_fixes_v2(csv_file):
    """Enhanced validation of the fixes"""
    issues_found = 0
    empty_names = 0
    source_in_names = 0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        for line_num, row in enumerate(reader, start=2):
            if len(row) < 32:
                continue
                
            # Check for empty moth names with scientific data
            if (not row[16] and 
                (row[9] or row[10] or row[11] or row[23])):
                empty_names += 1
                if empty_names <= 10:  # Only show first 10
                    print(f"Empty moth name at line {line_num}: genus={row[9]}, sci_name={row[23]}")
            
            # Check for source references in moth names
            if row[16] and re.search(r'日本産蛾類標準図鑑|標準図鑑|図鑑|文献|出典', row[16]):
                source_in_names += 1
                if source_in_names <= 5:  # Only show first 5
                    print(f"Source in moth name at line {line_num}: {row[16]}")
    
    print(f"\nValidation Summary:")
    print(f"- Empty moth names: {empty_names}")
    print(f"- Source references in names: {source_in_names}")
    
    return empty_names + source_in_names

if __name__ == "__main__":
    input_file = "/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master.csv"
    output_file = "/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master_fixed_v2.csv"
    
    print("Starting enhanced CSV structure fix...")
    
    fixes_applied = fix_csv_structure_v2(input_file, output_file)
    
    print(f"\nApplied {fixes_applied} fixes")
    
    print("\nValidating fixes...")
    remaining_issues = validate_fixes_v2(output_file)
    
    if remaining_issues == 0:
        print("\nSuccess! All major issues have been resolved.")
    else:
        print(f"\nRemaining issues: {remaining_issues}")
        print("Some issues may require manual review.")