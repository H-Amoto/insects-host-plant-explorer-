#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import re

def fix_csv_final(input_file, output_file):
    """Final comprehensive fix for CSV structure issues"""
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        rows = list(reader)
    
    print(f"Starting final fixes on {len(rows)} rows")
    
    fixed_rows = []
    fixes_applied = 0
    
    for i, row in enumerate(rows):
        # Ensure row has enough columns
        while len(row) < 32:
            row.append('')
        
        # Fix remaining cases where moth name is in genus field
        if (row[9] and re.search(r'[ひらがなカタカナ漢字]', row[9]) and 
            not row[16] and  # Empty moth name field
            row[23] and '(' in row[23]):  # Has scientific name
            
            print(f"Final fix: Moving moth name from genus field at line {i+2}: {row[9]}")
            row[16] = row[9]  # Move to moth name field
            fixes_applied += 1
        
        # Handle cases where the genus field contains the Japanese name but moth name is empty
        elif (not row[16] and row[9] and 
              re.search(r'[ひらがなカタカナ漢字]', row[9]) and
              not row[10] and not row[11]):  # No actual genus/species data
            
            print(f"Converting genus to moth name at line {i+2}: {row[9]}")
            row[16] = row[9]
            row[9] = ''  # Clear the genus field since it was actually the moth name
            fixes_applied += 1
        
        # Handle split data where scientific name construction is incorrect
        if (row[9] and row[11] and not row[16] and  # Has genus and species but no moth name
            not re.search(r'[a-zA-Z]', row[9])):  # Genus is not Latin (likely Japanese)
            
            row[16] = row[9]  # Use the Japanese name in genus field as moth name
            fixes_applied += 1
            print(f"Fixed genus->moth name at line {i+2}: {row[9]}")
        
        # Special handling for rows with malformed scientific names in year field
        if (row[14] and not row[14].isdigit() and 
            len(row[14]) > 4 and row[23]):  # Year field has non-year data
            
            # Check if it looks like an author name that should be in column 13
            if not row[13] and ',' not in row[14] and len(row[14]) < 50:
                row[13] = row[14]  # Move to author field
                row[14] = ''       # Clear year field
                fixes_applied += 1
                print(f"Fixed author in year field at line {i+2}: {row[13]}")
        
        fixed_rows.append(row)
    
    print(f"Applied {fixes_applied} final fixes")
    
    # Write the fixed CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(fixed_rows)
    
    print(f"Final fixed CSV written to {output_file}")
    return fixes_applied

def create_summary_report(original_file, fixed_file):
    """Create a summary report of all fixes applied"""
    
    print("\n" + "="*60)
    print("SUMMARY REPORT: CSV Structure Fixes")
    print("="*60)
    
    # Count original issues
    with open(original_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        original_rows = list(reader)
    
    # Count fixed issues
    with open(fixed_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        fixed_rows = list(reader)
    
    original_empty_names = 0
    original_source_in_names = 0
    fixed_empty_names = 0
    fixed_source_in_names = 0
    
    # Count original issues
    for row in original_rows:
        if len(row) > 16:
            if not row[16] and (row[9] or row[23]):
                original_empty_names += 1
            if row[16] and re.search(r'日本産蛾類標準図鑑', row[16]):
                original_source_in_names += 1
    
    # Count remaining issues
    for row in fixed_rows:
        if len(row) > 16:
            if not row[16] and (row[9] or row[23]):
                fixed_empty_names += 1
            if row[16] and re.search(r'日本産蛾類標準図鑑', row[16]):
                fixed_source_in_names += 1
    
    print(f"Original rows: {len(original_rows)}")
    print(f"Fixed rows: {len(fixed_rows)}")
    print(f"Rows merged/removed: {len(original_rows) - len(fixed_rows)}")
    print()
    print("ISSUE FIXES:")
    print(f"Empty moth names: {original_empty_names} → {fixed_empty_names} (fixed: {original_empty_names - fixed_empty_names})")
    print(f"Source in moth names: {original_source_in_names} → {fixed_source_in_names} (fixed: {original_source_in_names - fixed_source_in_names})")
    print()
    print(f"Total improvement: {(original_empty_names + original_source_in_names) - (fixed_empty_names + fixed_source_in_names)} issues resolved")
    
    if fixed_empty_names > 0:
        print(f"\nRemaining {fixed_empty_names} empty moth names may require manual review.")
    
    return (original_empty_names + original_source_in_names) - (fixed_empty_names + fixed_source_in_names)

if __name__ == "__main__":
    input_file = "/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master.csv"
    temp_file = "/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master_fixed_v2.csv"
    final_file = "/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master_final_fixed.csv"
    
    print("Applying final comprehensive fixes...")
    
    # Apply final fixes to the already-improved version
    final_fixes = fix_csv_final(temp_file, final_file)
    
    # Create summary report
    total_improvements = create_summary_report(input_file, final_file)
    
    print(f"\nFINAL RESULT: {total_improvements} total issues resolved!")
    print(f"Fixed CSV saved as: {final_file}")