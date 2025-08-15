#!/usr/bin/env python3
import csv
import os
import shutil

def parse_csv_line_manual(line):
    """学名にカンマが含まれるCSVを手動で解析"""
    parts = []
    current_part = ""
    in_quotes = False
    
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            parts.append(current_part.strip())
            current_part = ""
        else:
            current_part += char
    
    parts.append(current_part.strip())
    return parts

def fix_emergence_time_notes():
    """間違った発生時期情報を削除して正しい情報を追加"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 発生時期情報修正処理 ===")
    
    # ファイル
    winter_moths_file = os.path.join(base_dir, 'public', '日本の冬尺蛾.csv')
    insects_file = os.path.join(base_dir, 'public', 'insects.csv')
    general_notes_file = os.path.join(base_dir, 'public', 'general_notes.csv')
    
    # 1. insects.csvから和名→insect_idマッピングを作成
    print("\n=== 昆虫ID対応表作成 ===")
    
    name_to_id = {}
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            japanese_name = row['japanese_name'].strip()
            insect_id = row['insect_id']
            name_to_id[japanese_name] = insect_id
    
    # 2. 元データから正しい発生時期情報を抽出
    print("\n=== 正しい発生時期情報抽出 ===")
    
    correct_emergence_data = {}
    
    with open(winter_moths_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            
            parts = parse_csv_line_manual(line)
            
            if len(parts) >= 5:
                japanese_name = parts[0].strip()
                
                # 学名が分割されている場合（年号が別カラムになっている）
                if len(parts) == 6:
                    emergence_time = parts[5].strip().strip('"')
                else:  # len(parts) == 5
                    emergence_time = parts[4].strip().strip('"')
                
                if japanese_name in name_to_id and emergence_time:
                    insect_id = name_to_id[japanese_name]
                    correct_emergence_data[insect_id] = emergence_time
                    print(f"正しい発生時期: {japanese_name} → {emergence_time}")
    
    # 3. general_notes.csvから冬尺蛾関連エントリを削除
    print(f"\n=== general_notes.csv冬尺蛾エントリ削除 ===")
    
    filtered_notes = []
    deleted_count = 0
    
    with open(general_notes_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['reference'] == '日本の冬尺蛾':
                print(f"削除: {row['record_id']} - {row['content'][:50]}...")
                deleted_count += 1
            else:
                filtered_notes.append(row)
    
    print(f"削除されたエントリ: {deleted_count}件")
    
    # 4. 正しい発生時期情報を追加
    print(f"\n=== 正しい発生時期情報追加 ===")
    
    # 最大note_idを取得
    max_note_id = 0
    for note in filtered_notes:
        note_id_num = int(note['record_id'].replace('note-', ''))
        max_note_id = max(max_note_id, note_id_num)
    
    # 新しい発生時期ノートを追加
    next_note_id = max_note_id + 1
    
    for insect_id, emergence_time in correct_emergence_data.items():
        new_note = {
            'record_id': f'note-{next_note_id:06d}',
            'insect_id': insect_id,
            'note_type': 'emergence_time',
            'content': emergence_time,
            'reference': '日本の冬尺蛾',
            'page': '',
            'year': ''
        }
        filtered_notes.append(new_note)
        next_note_id += 1
        print(f"追加: {insect_id} → {emergence_time}")
    
    # 5. general_notes.csvを更新
    print(f"\n=== general_notes.csv更新 ===")
    
    with open(general_notes_file, 'w', encoding='utf-8', newline='') as file:
        if filtered_notes:
            writer = csv.DictWriter(file, fieldnames=filtered_notes[0].keys())
            writer.writeheader()
            writer.writerows(filtered_notes)
    
    # normalized_dataフォルダにもコピー
    dst = os.path.join(base_dir, 'normalized_data', 'general_notes.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(general_notes_file, dst)
    
    print(f"general_notes.csvを更新しました")
    print(f"総レコード数: {len(filtered_notes)}件")
    print(f"冬尺蛾発生時期情報: {len(correct_emergence_data)}件")
    
    print(f"\n✅ 発生時期情報の修正が完了しました！")

if __name__ == "__main__":
    fix_emergence_time_notes()