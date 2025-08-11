#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import re

def fix_remaining_empty_names(input_file, output_file):
    """Fix the remaining empty moth name cases"""
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        rows = list(reader)
    
    print(f"Fixing remaining empty names in {len(rows)} rows")
    
    fixes = 0
    
    for i, row in enumerate(rows):
        # Ensure row has enough columns
        while len(row) < 32:
            row.append('')
        
        # Fix cases where moth name is empty but genus contains Japanese text
        if (not row[16] and row[9] and 
            re.search(r'[ひらがなカタカナ漢字]', row[9]) and
            (row[23] or row[11])):  # Has scientific name or species data
            
            print(f"Fixing line {i+2}: Moving '{row[9]}' from genus to moth name")
            row[16] = row[9]  # Move Japanese name to moth name field
            # Don't clear genus field in case it's needed for scientific name construction
            fixes += 1
    
    print(f"Applied {fixes} fixes")
    
    # Write the fixed CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(rows)
    
    print(f"Final CSV written to {output_file}")
    return fixes

def create_final_summary(original_file, final_file):
    """Create final summary of all improvements"""
    
    # Count issues in original file
    original_empty = 0
    original_source_refs = 0
    
    with open(original_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if len(row) > 16:
                if not row[16] and (row[9] or (len(row) > 23 and row[23])):
                    original_empty += 1
                if row[16] and re.search(r'日本産蛾類標準図鑑', row[16]):
                    original_source_refs += 1
    
    # Count remaining issues in final file
    final_empty = 0
    final_source_refs = 0
    total_rows = 0
    
    with open(final_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            total_rows += 1
            if len(row) > 16:
                if not row[16] and (row[9] or (len(row) > 23 and row[23])):
                    final_empty += 1
                if row[16] and re.search(r'日本産蛾類標準図鑑', row[16]):
                    final_source_refs += 1
    
    print("\n" + "="*70)
    print("COMPREHENSIVE SUMMARY: CSV Structure Fixes")
    print("="*70)
    print(f"Original issues found:")
    print(f"  • Empty moth names: {original_empty}")
    print(f"  • Source references in names: {original_source_refs}")
    print(f"  • Total issues: {original_empty + original_source_refs}")
    print()
    print(f"After all fixes:")
    print(f"  • Empty moth names: {final_empty}")
    print(f"  • Source references in names: {final_source_refs}")  
    print(f"  • Total remaining: {final_empty + final_source_refs}")
    print()
    print(f"IMPROVEMENTS:")
    print(f"  • Fixed empty names: {original_empty - final_empty}")
    print(f"  • Fixed source refs: {original_source_refs - final_source_refs}")
    print(f"  • Total fixed: {(original_empty + original_source_refs) - (final_empty + final_source_refs)}")
    print()
    print(f"SUCCESS RATE: {((original_empty + original_source_refs) - (final_empty + final_source_refs)) / (original_empty + original_source_refs) * 100:.1f}%")
    print(f"DATA QUALITY: {(total_rows - final_empty) / total_rows * 100:.1f}% complete")
    
    return (original_empty + original_source_refs) - (final_empty + final_source_refs)

if __name__ == "__main__":
    input_file = "/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master_cleaned.csv"
    output_file = "/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master_final.csv"
    original_file = "/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master.csv"
    
    print("Applying final fixes to remaining empty names...")
    
    final_fixes = fix_remaining_empty_names(input_file, output_file)
    
    print(f"\nApplied {final_fixes} final fixes")
    
    # Create comprehensive summary
    total_improvements = create_final_summary(original_file, output_file)
    
    print(f"\nALL DONE! Total improvements: {total_improvements}")
    print(f"Final cleaned CSV: {output_file}")