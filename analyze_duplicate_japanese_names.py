#!/usr/bin/env python3
import csv
import os
from collections import defaultdict

def analyze_duplicate_japanese_names():
    """和名が同じなのに異なるinsect_idが割り当てられている昆虫を分析"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 和名重複分析開始 ===")
    
    insects_file = os.path.join(base_dir, 'public', 'insects.csv')
    
    # 和名とinsect_idの関係を収集
    japanese_name_to_ids = defaultdict(list)
    id_to_data = {}
    
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            insect_id = row['insect_id']
            japanese_name = row['japanese_name'].strip()
            scientific_name = row['scientific_name']
            
            # 空の和名や「sp.」などの不完全な名前を除外
            if japanese_name and japanese_name != '' and 'sp.' not in japanese_name:
                japanese_name_to_ids[japanese_name].append(insect_id)
                id_to_data[insect_id] = {
                    'japanese_name': japanese_name,
                    'scientific_name': scientific_name,
                    'family': row['family'],
                    'genus': row['genus'],
                    'species': row['species'],
                    'author': row['author'],
                    'year': row['year']
                }
    
    print(f"分析対象: {len(id_to_data)}種")
    
    # 重複する和名を特定
    duplicates = {}
    for japanese_name, ids in japanese_name_to_ids.items():
        if len(ids) > 1:
            duplicates[japanese_name] = ids
    
    print(f"\n重複する和名の数: {len(duplicates)}件")
    
    if duplicates:
        print("\n=== 重複詳細 ===")
        
        # 真の重複（同種に複数ID）vs 異種同名（別種に同じ和名）を分析
        true_duplicates = []  # 同種に複数ID
        homonym_cases = []    # 別種に同じ和名
        
        for japanese_name, ids in duplicates.items():
            print(f"\n和名: {japanese_name}")
            print(f"  割り当てられたID数: {len(ids)}個")
            
            # 各IDの詳細を表示
            scientific_names = set()
            for i, insect_id in enumerate(ids, 1):
                data = id_to_data[insect_id]
                scientific_name = data['scientific_name']
                scientific_names.add(scientific_name.strip())
                
                print(f"  {i}. ID: {insect_id}")
                print(f"     学名: {scientific_name}")
                print(f"     科: {data['family']}")
                print(f"     著者・年: {data['author']} {data['year']}")
            
            # 学名が同じなら真の重複、違うなら異種同名
            if len(scientific_names) == 1:
                true_duplicates.append((japanese_name, ids))
                print(f"  → 真の重複（同種に複数ID）")
            else:
                homonym_cases.append((japanese_name, ids))
                print(f"  → 異種同名（別種に同じ和名）")
        
        # サマリー
        print(f"\n=== サマリー ===")
        print(f"真の重複（同種に複数ID）: {len(true_duplicates)}件")
        if true_duplicates:
            print("  これらは統合が必要:")
            for japanese_name, ids in true_duplicates:
                print(f"    {japanese_name}: {', '.join(ids)}")
        
        print(f"\n異種同名（別種に同じ和名）: {len(homonym_cases)}件")
        if homonym_cases:
            print("  これらは適切な命名規則の検討が必要:")
            for japanese_name, ids in homonym_cases[:5]:  # 最初の5件のみ表示
                print(f"    {japanese_name}: {len(ids)}種")
        
        # 元のファイルとの照合推奨
        print(f"\n=== 推奨アクション ===")
        
        if true_duplicates:
            print("1. 真の重複について:")
            print("   - 元のソースファイル（buprestidae_host.csv, butterfly_host.csv, hamushi_integrated_master.csv）を確認")
            print("   - 統合時のIDマッピングルールを見直し")
            print("   - hostplants.csvで使用されているIDを確認し、統一")
        
        if homonym_cases:
            print("2. 異種同名について:")
            print("   - 和名の命名規則を見直し（亜種名、地域名等の追加）")
            print("   - 分類学的な確認が必要")
        
        # hostplants.csvでの使用状況をチェック
        print(f"\n=== hostplants.csvでの使用状況確認 ===")
        hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
        
        used_duplicate_ids = set()
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                insect_id = row['insect_id']
                for japanese_name, ids in duplicates.items():
                    if insect_id in ids:
                        used_duplicate_ids.add(insect_id)
        
        print(f"hostplants.csvで使用されている重複ID: {len(used_duplicate_ids)}個")
        
        if used_duplicate_ids:
            print("使用されている重複IDの詳細:")
            for insect_id in sorted(used_duplicate_ids):
                data = id_to_data[insect_id]
                print(f"  {insect_id}: {data['japanese_name']} ({data['scientific_name']})")
    
    else:
        print("✅ 重複する和名は見つかりませんでした")
    
    print(f"\n🔍 和名重複分析が完了しました！")

if __name__ == "__main__":
    analyze_duplicate_japanese_names()