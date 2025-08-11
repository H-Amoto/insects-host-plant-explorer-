#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import re

def analyze_csv_issues(csv_file):
    """Analyze CSV structure issues"""
    issues = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        expected_fields = len(header)
        
        print(f"Expected fields: {expected_fields}")
        print(f"Header: {header}")
        print("\n" + "="*80 + "\n")
        
        for line_num, row in enumerate(reader, start=2):
            # Check field count
            if len(row) != expected_fields:
                issues.append({
                    'type': 'field_count',
                    'line': line_num,
                    'expected': expected_fields,
                    'actual': len(row),
                    'data': row
                })
                print(f"Line {line_num}: {len(row)} fields (expected {expected_fields})")
                print(f"Data: {row}")
                print("-" * 40)
            
            # Check for source names in moth name field (column 16, 0-indexed)
            if len(row) > 16 and row[16]:
                moth_name = row[16]
                if re.search(r'日本産蛾類標準図鑑', moth_name):
                    issues.append({
                        'type': 'source_in_name',
                        'line': line_num,
                        'moth_name': moth_name,
                        'data': row
                    })
                    print(f"Line {line_num}: Source in moth name field: {moth_name}")
                    print(f"Full row: {row}")
                    print("-" * 40)
                
                # Look for other reference patterns in name field
                if re.search(r'(標準図鑑|図鑑|文献|出典)', moth_name):
                    issues.append({
                        'type': 'reference_in_name',
                        'line': line_num,
                        'moth_name': moth_name,
                        'data': row
                    })
                    print(f"Line {line_num}: Reference in moth name field: {moth_name}")
                    print(f"Full row: {row}")
                    print("-" * 40)
            
            # Check for empty required fields that might indicate split rows
            if len(row) >= 16:
                # If moth name is empty but there's scientific name data
                if not row[16] and any(row[i] for i in [9, 10, 11, 12, 13, 14, 15]):  # genus to year
                    issues.append({
                        'type': 'missing_moth_name',
                        'line': line_num,
                        'data': row
                    })
                    print(f"Line {line_num}: Missing moth name but has scientific data")
                    print(f"Data: {row}")
                    print("-" * 40)
            
            # Stop after checking first 100 issues to avoid overwhelming output
            if len(issues) > 100:
                break
    
    print(f"\n\nSummary: Found {len(issues)} issues")
    issue_types = {}
    for issue in issues:
        issue_type = issue['type']
        issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
    
    for issue_type, count in issue_types.items():
        print(f"- {issue_type}: {count}")
    
    return issues

if __name__ == "__main__":
    csv_file = "/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master.csv"
    issues = analyze_csv_issues(csv_file)