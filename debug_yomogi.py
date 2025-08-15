#!/usr/bin/env python3
import csv

# ヨモギネムシガの問題をデバッグ
input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master.csv'

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    
    for row_idx, row in enumerate(reader):
        if len(row) > 25:
            japanese_name = row[18].strip() if len(row) > 18 else ""
            scientific_name = row[25].strip() if len(row) > 25 else ""
            
            if 'ヨモギネムシガ' in japanese_name or 'Epiblema foenella' in scientific_name:
                print(f"Row {row_idx + 2}:")
                print(f"  Japanese name (col 19): '{japanese_name}'")
                print(f"  Scientific name (col 26): '{scientific_name}'")
                print(f"  ID: {row[0]}")
                print(f"  Has japanese: {bool(japanese_name and not japanese_name.isdigit() and len(japanese_name) > 1)}")
                print()