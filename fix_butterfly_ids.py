#!/usr/bin/env python3
import csv
import os
from typing import Dict, Set

def fix_butterfly_ids():
    """蝶のinsect_idをspecies-番号形式に正規化"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 蝶のinsect_id正規化開始 ===")
    
    insects_file = os.path.join(base_dir, 'public', 'insects.csv')
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    notes_file = os.path.join(base_dir, 'public', 'general_notes.csv')
    
    # 既存のspecies-番号を調査して、開始番号を決定
    existing_species_ids: Set[str] = set()
    
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            insect_id = row['insect_id']
            if insect_id.startswith('species-'):
                existing_species_ids.add(insect_id)
    
    print(f"既存のspecies-ID数: {len(existing_species_ids)}")
    
    # 新しいID番号の開始点を見つける
    max_num = 0
    for species_id in existing_species_ids:
        try:
            # species-の後の番号部分を抽出（数値または英数字）
            suffix = species_id[8:]  # "species-"を除去
            if suffix.isdigit():
                max_num = max(max_num, int(suffix))
        except:
            continue
    
    # 蝶用の新しいID開始番号（安全な範囲）
    butterfly_start_id = max_num + 10000
    print(f"蝶の新しいID開始番号: species-{butterfly_start_id}")
    
    # 蝶のinsect_idマッピングを作成
    old_to_new_id_mapping: Dict[str, str] = {}
    new_insects_data = []
    
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        butterfly_counter = butterfly_start_id
        
        for row in reader:
            old_id = row['insect_id']
            
            if old_id.startswith('butterfly-'):
                # 新しいIDを生成
                new_id = f"species-{butterfly_counter}"
                old_to_new_id_mapping[old_id] = new_id
                row['insect_id'] = new_id
                butterfly_counter += 1
                print(f"  {old_id} -> {new_id}")
            
            new_insects_data.append(row)
    
    print(f"\\n蝶のID変換対象: {len(old_to_new_id_mapping)}件")
    
    # insects.csvを更新
    with open(insects_file, 'w', encoding='utf-8', newline='') as file:
        if new_insects_data:
            writer = csv.DictWriter(file, fieldnames=new_insects_data[0].keys())
            writer.writeheader()
            writer.writerows(new_insects_data)
    
    print("insects.csvを更新しました")
    
    # hostplants.csvを更新
    new_hostplants_data = []
    hostplant_updates = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            old_insect_id = row['insect_id']
            if old_insect_id in old_to_new_id_mapping:
                row['insect_id'] = old_to_new_id_mapping[old_insect_id]
                hostplant_updates += 1
            
            new_hostplants_data.append(row)
    
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if new_hostplants_data:
            writer = csv.DictWriter(file, fieldnames=new_hostplants_data[0].keys())
            writer.writeheader()
            writer.writerows(new_hostplants_data)
    
    print(f"hostplants.csvを更新しました ({hostplant_updates}件のinsect_id更新)")
    
    # general_notes.csvを更新
    new_notes_data = []
    notes_updates = 0
    
    with open(notes_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            old_insect_id = row['insect_id']
            if old_insect_id in old_to_new_id_mapping:
                row['insect_id'] = old_to_new_id_mapping[old_insect_id]
                notes_updates += 1
            
            new_notes_data.append(row)
    
    with open(notes_file, 'w', encoding='utf-8', newline='') as file:
        if new_notes_data:
            writer = csv.DictWriter(file, fieldnames=new_notes_data[0].keys())
            writer.writeheader()
            writer.writerows(new_notes_data)
    
    print(f"general_notes.csvを更新しました ({notes_updates}件のinsect_id更新)")
    
    # 検証
    print(f"\\n=== 検証 ===")
    
    # butterflynameの残存チェック
    remaining_butterfly_ids = []
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['insect_id'].startswith('butterfly-'):
                remaining_butterfly_ids.append(row['insect_id'])
    
    if remaining_butterfly_ids:
        print(f"⚠️  残存するbutterfly-ID: {len(remaining_butterfly_ids)}件")
        for rid in remaining_butterfly_ids[:3]:
            print(f"  {rid}")
    else:
        print("✅ 全ての蝶IDが正規化されました")
    
    # 新しいspecies-IDの範囲確認
    new_species_ids = []
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            insect_id = row['insect_id']
            if insect_id.startswith('species-'):
                try:
                    suffix = insect_id[8:]
                    if suffix.isdigit() and int(suffix) >= butterfly_start_id:
                        new_species_ids.append(insect_id)
                except:
                    continue
    
    print(f"\\n新しく割り当てられたspecies-ID:")
    print(f"  範囲: species-{butterfly_start_id} ～ species-{butterfly_start_id + len(old_to_new_id_mapping) - 1}")
    print(f"  件数: {len(new_species_ids)}件")
    
    # hostplants.csvでのID一貫性チェック
    hostplant_insect_ids = set()
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            hostplant_insect_ids.add(row['insect_id'])
    
    insect_ids = set()
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            insect_ids.add(row['insect_id'])
    
    orphaned_hostplants = hostplant_insect_ids - insect_ids
    if orphaned_hostplants:
        print(f"⚠️  対応する昆虫がない食草記録: {len(orphaned_hostplants)}件")
    else:
        print("✅ 全ての食草記録に対応する昆虫が存在します")
    
    print("\\n🦋 蝶のinsect_id正規化が完了しました！")

if __name__ == "__main__":
    fix_butterfly_ids()