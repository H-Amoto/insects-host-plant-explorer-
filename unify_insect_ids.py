#!/usr/bin/env python3
import csv
import os

def unify_insect_ids():
    """insect_idを連番に統一し、関連テーブルも更新"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    # IDマッピング辞書
    old_to_new_id = {}
    
    print("=== insect_id統一処理開始 ===")
    
    # 1. insects.csvを読み込み、新しいIDでマッピング作成
    insects_file = os.path.join(base_dir, 'normalized_data', 'insects.csv')
    insects_data = []
    
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader, 1):
            old_id = row['insect_id']
            new_id = f"species-{i:04d}"
            old_to_new_id[old_id] = new_id
            
            # 新しいIDで更新
            row['insect_id'] = new_id
            insects_data.append(row)
    
    print(f"昆虫データ: {len(insects_data)}件のIDを更新")
    
    # 2. insects.csvを新しいIDで保存
    with open(insects_file, 'w', encoding='utf-8', newline='') as file:
        if insects_data:
            writer = csv.DictWriter(file, fieldnames=insects_data[0].keys())
            writer.writeheader()
            writer.writerows(insects_data)
    
    # 3. hostplants.csvのinsect_idを更新
    hostplants_file = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    hostplants_data = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            old_id = row['insect_id']
            if old_id in old_to_new_id:
                row['insect_id'] = old_to_new_id[old_id]
                hostplants_data.append(row)
            else:
                print(f"警告: hostplantsに未知のinsect_id: {old_id}")
    
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if hostplants_data:
            writer = csv.DictWriter(file, fieldnames=hostplants_data[0].keys())
            writer.writeheader()
            writer.writerows(hostplants_data)
    
    print(f"食草データ: {len(hostplants_data)}件のIDを更新")
    
    # 4. general_notes.csvのinsect_idを更新
    notes_file = os.path.join(base_dir, 'normalized_data', 'general_notes.csv')
    notes_data = []
    
    with open(notes_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            old_id = row['insect_id']
            if old_id in old_to_new_id:
                row['insect_id'] = old_to_new_id[old_id]
                notes_data.append(row)
            else:
                print(f"警告: general_notesに未知のinsect_id: {old_id}")
    
    with open(notes_file, 'w', encoding='utf-8', newline='') as file:
        if notes_data:
            writer = csv.DictWriter(file, fieldnames=notes_data[0].keys())
            writer.writeheader()
            writer.writerows(notes_data)
    
    print(f"総合備考データ: {len(notes_data)}件のIDを更新")
    
    # 5. publicフォルダにもコピー
    import shutil
    for filename in ['insects.csv', 'hostplants.csv', 'general_notes.csv']:
        src = os.path.join(base_dir, 'normalized_data', filename)
        dst = os.path.join(base_dir, 'public', filename)
        shutil.copy2(src, dst)
        print(f"{filename} をpublicフォルダに更新")
    
    print("\n=== ID統一完了 ===")
    print(f"総変更件数: {len(old_to_new_id)}件")
    print("新ID形式: species-0001 ～ species-6155")
    
    # サンプル表示
    print("\n変更例:")
    sample_items = list(old_to_new_id.items())[:5]
    for old_id, new_id in sample_items:
        print(f"  {old_id} → {new_id}")

if __name__ == "__main__":
    unify_insect_ids()