#!/usr/bin/env python3
import csv
import os

def normalize_record_ids():
    """record_idを統一的な命名規則に正規化"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== record_id正規化開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    notes_file = os.path.join(base_dir, 'public', 'general_notes.csv')
    
    # hostplants.csvの処理
    print("\\nhostplants.csvの処理...")
    new_hostplants_data = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        record_counter = 1
        for row in reader:
            old_record_id = row['record_id']
            new_record_id = f"hostplant-{record_counter:06d}"
            
            row['record_id'] = new_record_id
            new_hostplants_data.append(row)
            
            if record_counter <= 5 or record_counter % 1000 == 0:
                print(f"  {old_record_id} -> {new_record_id}")
            
            record_counter += 1
    
    print(f"  ...（中略）...")
    print(f"  総record_id更新数: {len(new_hostplants_data)}件")
    
    # hostplants.csvを保存
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if new_hostplants_data:
            writer = csv.DictWriter(file, fieldnames=new_hostplants_data[0].keys())
            writer.writeheader()
            writer.writerows(new_hostplants_data)
    
    print("hostplants.csvを更新しました")
    
    # general_notes.csvの処理
    print("\\ngeneral_notes.csvの処理...")
    new_notes_data = []
    
    with open(notes_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        note_counter = 1
        for row in reader:
            old_record_id = row['record_id']
            new_record_id = f"note-{note_counter:06d}"
            
            row['record_id'] = new_record_id
            new_notes_data.append(row)
            
            if note_counter <= 5 or note_counter % 100 == 0:
                print(f"  {old_record_id} -> {new_record_id}")
            
            note_counter += 1
    
    print(f"  総note record_id更新数: {len(new_notes_data)}件")
    
    # general_notes.csvを保存
    with open(notes_file, 'w', encoding='utf-8', newline='') as file:
        if new_notes_data:
            writer = csv.DictWriter(file, fieldnames=new_notes_data[0].keys())
            writer.writeheader()
            writer.writerows(new_notes_data)
    
    print("general_notes.csvを更新しました")
    
    # 正規化後の検証
    print(f"\\n=== 検証 ===")
    
    # record_idの形式確認
    hostplant_sample_ids = []
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i < 5:
                hostplant_sample_ids.append(row['record_id'])
    
    note_sample_ids = []
    with open(notes_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i < 5:
                note_sample_ids.append(row['record_id'])
    
    print(f"hostplantsのrecord_idサンプル:")
    for rid in hostplant_sample_ids:
        print(f"  {rid}")
    
    print(f"\\nnotesのrecord_idサンプル:")
    for rid in note_sample_ids:
        print(f"  {rid}")
    
    # 重複チェック
    all_hostplant_ids = set()
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            record_id = row['record_id']
            if record_id in all_hostplant_ids:
                print(f"⚠️  重複するrecord_id: {record_id}")
            all_hostplant_ids.add(record_id)
    
    all_note_ids = set()
    with open(notes_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            record_id = row['record_id']
            if record_id in all_note_ids:
                print(f"⚠️  重複するnote record_id: {record_id}")
            all_note_ids.add(record_id)
    
    if len(all_hostplant_ids) == len(new_hostplants_data):
        print("✅ 全てのhostplant record_idが一意です")
    else:
        print(f"⚠️  hostplant record_id重複があります")
    
    if len(all_note_ids) == len(new_notes_data):
        print("✅ 全てのnote record_idが一意です")
    else:
        print(f"⚠️  note record_id重複があります")
    
    # normalized_dataフォルダにもコピー
    import shutil
    normalized_dir = os.path.join(base_dir, 'normalized_data')
    if os.path.exists(normalized_dir):
        shutil.copy2(hostplants_file, os.path.join(normalized_dir, 'hostplants.csv'))
        shutil.copy2(notes_file, os.path.join(normalized_dir, 'general_notes.csv'))
        print("\\nnormalized_dataフォルダにもコピーしました")
    
    print(f"\\n🔢 record_id正規化が完了しました！")
    print(f"  hostplant records: hostplant-000001 ～ hostplant-{len(new_hostplants_data):06d}")
    print(f"  note records: note-000001 ～ note-{len(new_notes_data):06d}")

if __name__ == "__main__":
    normalize_record_ids()