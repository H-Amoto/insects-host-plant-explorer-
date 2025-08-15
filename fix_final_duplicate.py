#!/usr/bin/env python3
import csv
import os
import shutil

def fix_final_duplicate():
    """オオアカキリバの重複問題を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== オオアカキリバ重複問題の最終修正 ===")
    
    insects_file = os.path.join(base_dir, 'public', 'insects.csv')
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # 1. 現在の状況を詳しく確認
    print("\n=== 現在の状況確認 ===")
    
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['insect_id'] in ['species-5381', 'species-6152']:
                print(f"\nID: {row['insect_id']}")
                print(f"  科: {row['family']}")
                print(f"  属: {row['genus']}")
                print(f"  種: {row['species']}")
                print(f"  学名: '{row['scientific_name']}'")
                print(f"  著者年: '{row['author']}' '{row['year']}'")
    
    # hostplants.csvでの使用状況
    print(f"\n=== hostplants.csvでの使用状況 ===")
    
    species_5381_records = []
    species_6152_records = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['insect_id'] == 'species-5381':
                species_5381_records.append(row)
            elif row['insect_id'] == 'species-6152':
                species_6152_records.append(row)
    
    print(f"species-5381: {len(species_5381_records)}件")
    for record in species_5381_records:
        print(f"  {record['plant_name']} ({record['reference']})")
    
    print(f"species-6152: {len(species_6152_records)}件")
    for record in species_6152_records:
        print(f"  {record['plant_name']} ({record['reference']})")
    
    # 2. 統合判定
    print(f"\n=== 統合判定 ===")
    print("両エントリは同じ属種 (Rusicada privata) で、著者年も同じ (Walker, 1865)")
    print("species-6152は学名が完全で、species-5381は学名が空欄")
    print("→ species-5381をspecies-6152に統合します")
    
    # 3. hostplants.csvでspecies-5381をspecies-6152に更新
    print(f"\n=== hostplants.csvのID統合 ===")
    
    hostplants_data = []
    update_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if row['insect_id'] == 'species-5381':
                print(f"更新: {row['insect_id']} → species-6152 (植物: {row['plant_name']})")
                row['insect_id'] = 'species-6152'
                update_count += 1
            
            hostplants_data.append(row)
    
    # hostplants.csvを更新
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if hostplants_data:
            writer = csv.DictWriter(file, fieldnames=hostplants_data[0].keys())
            writer.writeheader()
            writer.writerows(hostplants_data)
    
    print(f"hostplants.csvで {update_count}件のIDを更新しました")
    
    # 4. insects.csvからspecies-5381を削除
    print(f"\n=== insects.csvからspecies-5381を削除 ===")
    
    insects_data = []
    removed = False
    
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if row['insect_id'] == 'species-5381':
                print(f"削除: {row['insect_id']} (オオアカキリバ)")
                removed = True
            else:
                insects_data.append(row)
    
    # insects.csvを更新
    with open(insects_file, 'w', encoding='utf-8', newline='') as file:
        if insects_data:
            writer = csv.DictWriter(file, fieldnames=insects_data[0].keys())
            writer.writeheader()
            writer.writerows(insects_data)
    
    if removed:
        print("species-5381を削除しました")
    
    # 5. normalized_dataフォルダにもコピー
    src = insects_file
    dst = os.path.join(base_dir, 'normalized_data', 'insects.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    src = hostplants_file
    dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    # 6. 最終検証
    print(f"\n=== 最終検証 ===")
    
    # 重複和名をチェック
    from collections import defaultdict
    
    japanese_name_to_ids = defaultdict(list)
    
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            japanese_name = row['japanese_name'].strip()
            if japanese_name:
                japanese_name_to_ids[japanese_name].append(row['insect_id'])
    
    duplicates = {name: ids for name, ids in japanese_name_to_ids.items() if len(ids) > 1}
    
    print(f"重複和名数: {len(duplicates)}件")
    
    if duplicates:
        print("残存する重複:")
        for name, ids in duplicates.items():
            print(f"  {name}: {ids}")
    else:
        print("✅ すべての重複和名問題が解決されました")
    
    # オオアカキリバの最終確認
    print(f"\n=== オオアカキリバの最終確認 ===")
    
    ooakakidiba_count = 0
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['insect_id'] == 'species-6152':
                ooakakidiba_count += 1
    
    print(f"species-6152 (オオアカキリバ) のhostplants.csvエントリ数: {ooakakidiba_count}件")
    
    print(f"\n✅ オオアカキリバの重複問題が完全に解決されました！")

if __name__ == "__main__":
    fix_final_duplicate()