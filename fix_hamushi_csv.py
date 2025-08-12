#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys

# Set maximum field size limit
csv.field_size_limit(sys.maxsize)

input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/hamushi_integrated_master.csv'

# Read all rows
rows = []
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows.append(header)
    
    for row_num, row in enumerate(reader, start=2):
        # Ensure all rows have exactly 33 columns
        while len(row) < 33:
            row.append('')
        if len(row) > 33:
            # For rows 625-628, concatenate extra columns into the last valid column
            if row_num in [625, 627, 628]:
                # Concatenate extra columns into notes/remarks field
                extra_data = ' '.join(row[33:])
                if row[32]:  # If last column has data
                    row[32] = row[32] + ' ' + extra_data
                else:
                    row[32] = extra_data
            row = row[:33]
        rows.append(row)

# Write cleaned CSV
with open(input_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Fixed hamushi CSV with {len(rows)} rows")