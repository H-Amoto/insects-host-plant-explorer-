#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys

# Set maximum field size limit
csv.field_size_limit(sys.maxsize)

input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master.csv'
temp_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master_temp.csv'

# Read all rows first
rows = []
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()
    # Fix specific problematic lines
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Fix line 5531 - missing columns
        if line_num == 5531:
            if line.endswith(',,,,,,'):
                line = line + ',,'
                
        # Fix line 5600 - extra column
        elif line_num == 5600:
            # Remove extra comma before 国外では
            line = line.replace('; 国外では;', '; 国外では')
            
        # Fix line 5601 - extra columns
        elif line_num == 5601:
            # Remove extra commas
            parts = line.split(',')
            if len(parts) > 32:
                # Keep only first 32 columns
                line = ','.join(parts[:32])
                
        # Fix line 5921 - extra column
        elif line_num == 5921:
            # Remove extra comma
            line = line.replace('Kollar, 1844"', 'Kollar 1844"')
            
        # Fix line 5922 - quote issue
        elif line_num == 5922:
            # Fix the year format
            line = line.replace('(Butler, 1884)"', '(Butler 1881)"')
            
        # Fix line 5923 - starting quote issue
        elif line_num == 5923:
            # Remove starting quote
            line = line.replace(',"""ヤンバルハグロソウ', ',"ヤンバルハグロソウ')
            
        # Fix line 6153 - missing columns
        elif line_num == 6153:
            if line.endswith(',,,,,,'):
                line = line + ',,'
                
        # Fix line 6156 - ending quote issue
        elif line_num == 6156:
            # Fix ending quotes
            line = line.replace('(以上ツツジ科)"""', '(以上ツツジ科)"')
            
        lines[i] = line
    
    # Write fixed content
    with open(temp_file, 'w', encoding='utf-8') as out:
        out.write('\n'.join(lines))

# Now read and write with csv module to validate
rows = []
with open(temp_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows.append(header)
    
    for row_num, row in enumerate(reader, start=2):
        # Ensure all rows have 32 columns
        while len(row) < 32:
            row.append('')
        if len(row) > 32:
            row = row[:32]
        rows.append(row)

# Write final cleaned CSV
with open(input_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Fixed CSV with {len(rows)} rows")