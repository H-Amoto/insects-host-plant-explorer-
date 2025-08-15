#!/usr/bin/env python3
import csv
import os
import shutil
import re

def move_emergence_time_to_general_notes():
    """冬尺蛾データの成虫発生時期情報をhostplants.csvからgeneral_notes.csvに移動"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 成虫発生時期情報移動処理 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    general_notes_file = os.path.join(base_dir, 'public', 'general_notes.csv')
    
    # 1. 既存のgeneral_notes.csvを読み込み
    print("\n=== 既存general_notes.csv分析 ===")
    
    existing_notes = []
    max_note_id = 0
    
    with open(general_notes_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_notes.append(row)
            note_id_num = int(row['record_id'].replace('note-', ''))
            max_note_id = max(max_note_id, note_id_num)
    
    print(f"既存general_notesレコード数: {len(existing_notes)}件")
    print(f"最大note_id: note-{max_note_id:06d}")
    
    # 2. 冬尺蛾データの発生時期情報を抽出・移動
    print("\n=== hostplants.csvの成虫発生時期情報処理 ===")
    
    updated_hostplant_records = []
    emergence_notes = {}  # insect_id -> emergence_time_info
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if row['reference'] == '日本の冬尺蛾':
                notes = row['notes']
                
                # 成虫発生時期情報を抽出
                emergence_match = re.search(r'成虫発生時期:\s*([^;]+)', notes)
                if emergence_match:
                    emergence_time = emergence_match.group(1).strip()
                    insect_id = row['insect_id']
                    
                    # 発生時期情報を記録
                    if insect_id not in emergence_notes:
                        emergence_notes[insect_id] = emergence_time
                    
                    # hostplants.csvのnotesから発生時期情報を除去
                    cleaned_notes = re.sub(r'成虫発生時期:\s*[^;]+;?\s*', '', notes)
                    cleaned_notes = re.sub(r'^;\s*|;\s*$', '', cleaned_notes)  # 先頭・末尾のセミコロンを除去
                    cleaned_notes = cleaned_notes.strip()
                    
                    row['notes'] = cleaned_notes
            
            updated_hostplant_records.append(row)
    
    print(f"発生時期情報を持つ昆虫: {len(emergence_notes)}種")
    
    # 3. general_notes.csvに発生時期情報を追加
    print("\n=== general_notes.csvに発生時期情報追加 ===")
    
    new_notes = []
    next_note_id = max_note_id + 1
    
    for insect_id, emergence_time in emergence_notes.items():
        new_note = {
            'record_id': f'note-{next_note_id:06d}',
            'insect_id': insect_id,
            'note_type': 'emergence_time',
            'content': emergence_time,
            'reference': '日本の冬尺蛾',
            'page': '',
            'year': ''
        }
        new_notes.append(new_note)
        next_note_id += 1
        
        print(f"追加: {insect_id} → {emergence_time[:50]}...")
    
    print(f"\n新規general_notesレコード: {len(new_notes)}件")
    
    # 4. ファイルを更新
    print("\n=== ファイル更新 ===")
    
    # hostplants.csvを更新
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if updated_hostplant_records:
            writer = csv.DictWriter(file, fieldnames=updated_hostplant_records[0].keys())
            writer.writeheader()
            writer.writerows(updated_hostplant_records)
    
    # general_notes.csvを更新
    all_notes = existing_notes + new_notes
    with open(general_notes_file, 'w', encoding='utf-8', newline='') as file:
        if all_notes:
            writer = csv.DictWriter(file, fieldnames=all_notes[0].keys())
            writer.writeheader()
            writer.writerows(all_notes)
    
    # normalized_dataフォルダにもコピー
    for src_file, filename in [(hostplants_file, 'hostplants.csv'), (general_notes_file, 'general_notes.csv')]:
        dst = os.path.join(base_dir, 'normalized_data', filename)
        if os.path.exists(os.path.dirname(dst)):
            shutil.copy2(src_file, dst)
    
    print("hostplants.csvとgeneral_notes.csvを更新しました")
    
    # 5. 移動結果の検証
    print(f"\n=== 移動結果検証 ===")
    
    # hostplants.csvでの発生時期情報の残存確認
    remaining_emergence_info = 0
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['reference'] == '日本の冬尺蛾' and '成虫発生時期' in row['notes']:
                remaining_emergence_info += 1
    
    # general_notes.csvでの発生時期情報確認
    emergence_notes_count = 0
    with open(general_notes_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['note_type'] == 'emergence_time' and row['reference'] == '日本の冬尺蛾':
                emergence_notes_count += 1
    
    print(f"hostplants.csvに残存する発生時期情報: {remaining_emergence_info}件")
    print(f"general_notes.csvの発生時期情報: {emergence_notes_count}件")
    print(f"general_notes.csv総レコード数: {len(existing_notes) + len(new_notes)}件")
    
    print(f"\n✅ 成虫発生時期情報の移動が完了しました！")

if __name__ == "__main__":
    move_emergence_time_to_general_notes()