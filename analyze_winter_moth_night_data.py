#!/usr/bin/env python3
import csv
import os

def analyze_winter_moth_night_data():
    """冬夜蛾データと既存データの重複チェック"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 冬夜蛾データ分析 ===")
    
    winter_night_moths_file = os.path.join(base_dir, 'public', '日本の冬夜蛾.csv')
    insects_file = os.path.join(base_dir, 'public', 'insects.csv')
    
    # 1. 冬夜蛾データを読み込み
    print("\n=== 冬夜蛾データ読み込み ===")
    
    winter_night_moths = []
    with open(winter_night_moths_file, 'r', encoding='utf-8-sig') as file:  # BOM対応
        reader = csv.DictReader(file)
        for row in reader:
            winter_night_moths.append({
                'japanese_name': row['和名'].strip(),
                'scientific_name': row['学名'].strip(),
                'food_plants': row['食草'].strip(),
                'food_notes': row['食草に関する備考'].strip(),
                'emergence_time': row['成虫の発生時期'].strip()
            })
    
    print(f"冬夜蛾種数: {len(winter_night_moths)}種")
    
    # 2. 既存insects.csvを読み込み
    print("\n=== 既存昆虫データ読み込み ===")
    
    existing_insects = {}
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            japanese_name = row['japanese_name'].strip()
            existing_insects[japanese_name] = {
                'insect_id': row['insect_id'],
                'scientific_name': row['scientific_name']
            }
    
    print(f"既存昆虫種数: {len(existing_insects)}種")
    
    # 3. 重複チェック
    print("\n=== 重複チェック ===")
    
    duplicates = []
    new_species = []
    
    for moth in winter_night_moths:
        japanese_name = moth['japanese_name']
        if japanese_name in existing_insects:
            duplicates.append({
                'japanese_name': japanese_name,
                'existing_id': existing_insects[japanese_name]['insect_id'],
                'existing_scientific': existing_insects[japanese_name]['scientific_name'],
                'new_scientific': moth['scientific_name']
            })
        else:
            new_species.append(moth)
    
    print(f"重複種数: {len(duplicates)}種")
    print(f"新規種数: {len(new_species)}種")
    
    # 4. 重複種の詳細確認
    if duplicates:
        print(f"\n=== 重複種詳細（最初の10種） ===")
        for i, dup in enumerate(duplicates[:10]):
            print(f"{i+1}. {dup['japanese_name']}")
            print(f"   既存: {dup['existing_scientific']} (ID: {dup['existing_id']})")
            print(f"   新規: {dup['new_scientific']}")
            
            # 学名が異なる場合は指摘
            if dup['existing_scientific'] != dup['new_scientific']:
                print(f"   ⚠️  学名相違！")
            print()
    
    # 5. 新規種の詳細確認
    if new_species:
        print(f"\n=== 新規種詳細（最初の10種） ===")
        for i, moth in enumerate(new_species[:10]):
            print(f"{i+1}. {moth['japanese_name']} - {moth['scientific_name']}")
            print(f"   食草: {moth['food_plants']}")
            if moth['food_notes']:
                print(f"   備考: {moth['food_notes']}")
            print()
    
    # 6. 食草データサンプル確認
    print(f"\n=== 食草データサンプル ===")
    for i, moth in enumerate(winter_night_moths[:5]):
        print(f"{i+1}. {moth['japanese_name']}")
        print(f"   食草: {moth['food_plants']}")
        if moth['food_notes']:
            print(f"   備考: {moth['food_notes']}")
        print()
    
    return {
        'total_species': len(winter_night_moths),
        'duplicates': len(duplicates),
        'new_species': len(new_species),
        'duplicate_list': duplicates,
        'new_species_list': new_species
    }

if __name__ == "__main__":
    analyze_winter_moth_night_data()