#!/usr/bin/env python3
import csv
from collections import defaultdict

def check_duplicates():
    """統合データの重複をチェック"""
    file_path = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master.csv'
    
    # 学名での重複チェック
    scientific_names = defaultdict(list)
    japanese_names = defaultdict(list)
    insect_ids = defaultdict(list)
    
    print("=== 重複チェック開始 ===")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row_num, row in enumerate(reader, 2):  # 2から開始（ヘッダーは1行目）
            insect_id = row.get('昆虫ID', '').strip()
            scientific_name = row.get('学名', '').strip()
            japanese_name = row.get('和名', '').strip()
            classification = row.get('分類群', '').strip()
            
            if insect_id:
                insect_ids[insect_id].append((row_num, classification, japanese_name, scientific_name))
            
            if scientific_name:
                scientific_names[scientific_name].append((row_num, insect_id, classification, japanese_name))
            
            if japanese_name:
                japanese_names[japanese_name].append((row_num, insect_id, classification, scientific_name))
    
    # 昆虫ID重複チェック
    print(f"\n=== 昆虫ID重複（{len([k for k, v in insect_ids.items() if len(v) > 1])}件） ===")
    for insect_id, entries in insect_ids.items():
        if len(entries) > 1:
            print(f"ID: {insect_id} ({len(entries)}件)")
            for row_num, classification, japanese_name, scientific_name in entries:
                print(f"  行{row_num}: {classification} - {japanese_name} ({scientific_name})")
    
    # 学名重複チェック
    print(f"\n=== 学名重複（{len([k for k, v in scientific_names.items() if len(v) > 1])}件） ===")
    duplicate_count = 0
    for scientific_name, entries in scientific_names.items():
        if len(entries) > 1:
            duplicate_count += 1
            if duplicate_count <= 10:  # 最初の10件のみ表示
                print(f"学名: {scientific_name} ({len(entries)}件)")
                for row_num, insect_id, classification, japanese_name in entries:
                    print(f"  行{row_num}: {insect_id} - {classification} - {japanese_name}")
    
    if duplicate_count > 10:
        print(f"  ... 他{duplicate_count - 10}件の重複学名")
    
    # 和名重複チェック
    print(f"\n=== 和名重複（{len([k for k, v in japanese_names.items() if len(v) > 1])}件） ===")
    duplicate_count = 0
    for japanese_name, entries in japanese_names.items():
        if len(entries) > 1:
            duplicate_count += 1
            if duplicate_count <= 10:  # 最初の10件のみ表示
                print(f"和名: {japanese_name} ({len(entries)}件)")
                for row_num, insect_id, classification, scientific_name in entries:
                    print(f"  行{row_num}: {insect_id} - {classification} - {scientific_name}")
    
    if duplicate_count > 10:
        print(f"  ... 他{duplicate_count - 10}件の重複和名")
    
    # 統計
    total_ids = len(insect_ids)
    duplicate_ids = len([k for k, v in insect_ids.items() if len(v) > 1])
    unique_scientific = len(scientific_names)
    duplicate_scientific = len([k for k, v in scientific_names.items() if len(v) > 1])
    unique_japanese = len(japanese_names)
    duplicate_japanese = len([k for k, v in japanese_names.items() if len(v) > 1])
    
    print(f"\n=== 重複統計 ===")
    print(f"総昆虫ID数: {total_ids}")
    print(f"重複昆虫ID: {duplicate_ids}")
    print(f"ユニーク学名: {unique_scientific}")
    print(f"重複学名: {duplicate_scientific}")
    print(f"ユニーク和名: {unique_japanese}")
    print(f"重複和名: {duplicate_japanese}")

if __name__ == "__main__":
    check_duplicates()