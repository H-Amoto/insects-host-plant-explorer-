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

def add_emergence_time_from_source():
    """元の冬尺蛾.csvから成虫発生時期情報を抽出してgeneral_notes.csvに追加"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 元データから成虫発生時期情報抽出・追加 ===")
    
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
    
    print(f"昆虫ID対応表: {len(name_to_id)}件")
    
    # 2. 既存のgeneral_notes.csvを読み込み
    print("\n=== 既存general_notes.csv分析 ===")
    
    existing_notes = []
    max_note_id = 0
    existing_emergence_notes = set()
    
    with open(general_notes_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_notes.append(row)
            note_id_num = int(row['record_id'].replace('note-', ''))
            max_note_id = max(max_note_id, note_id_num)
            
            # 既存の発生時期情報をチェック
            if row['note_type'] == 'emergence_time':
                existing_emergence_notes.add(row['insect_id'])
    
    print(f"既存general_notesレコード数: {len(existing_notes)}件")
    print(f"既存の発生時期情報: {len(existing_emergence_notes)}種")
    
    # 3. 冬尺蛾データから発生時期情報を抽出
    print("\n=== 冬尺蛾データ発生時期情報抽出 ===")
    
    emergence_data = {}
    
    with open(winter_moths_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        # ヘッダー行をスキップ
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            
            # 手動でCSV解析
            parts = parse_csv_line_manual(line)
            
            if len(parts) >= 5:
                japanese_name = parts[0].strip()
                
                # 学名が分割されている場合（年号が別カラムになっている）
                if len(parts) == 6:
                    emergence_time = parts[5].strip().strip('"')
                else:  # len(parts) == 5
                    emergence_time = parts[4].strip().strip('"')
                
                # insect_idを取得
                if japanese_name not in name_to_id:
                    print(f"⚠️ {japanese_name}: insects.csvに見つからない")
                    continue
                
                insect_id = name_to_id[japanese_name]
                
                # 発生時期情報を記録
                if emergence_time and emergence_time != '不明':
                    emergence_data[insect_id] = {
                        'japanese_name': japanese_name,
                        'emergence_time': emergence_time
                    }
                    print(f"抽出: {japanese_name} → {emergence_time[:50]}...")
    
    print(f"\n発生時期情報を持つ昆虫: {len(emergence_data)}種")
    
    # 4. general_notes.csvに発生時期情報を追加
    print("\n=== general_notes.csvに発生時期情報追加 ===")
    
    new_notes = []
    next_note_id = max_note_id + 1
    add_count = 0
    skip_count = 0
    
    for insect_id, data in emergence_data.items():
        # 既存の発生時期情報があるかチェック
        if insect_id in existing_emergence_notes:
            print(f"スキップ: {data['japanese_name']} (既存の発生時期情報あり)")
            skip_count += 1
            continue
        
        new_note = {
            'record_id': f'note-{next_note_id:06d}',
            'insect_id': insect_id,
            'note_type': 'emergence_time',
            'content': data['emergence_time'],
            'reference': '日本の冬尺蛾',
            'page': '',
            'year': ''
        }
        new_notes.append(new_note)
        next_note_id += 1
        add_count += 1
        
        print(f"追加: {data['japanese_name']} → {data['emergence_time'][:50]}...")
    
    print(f"\n新規追加: {add_count}件, スキップ: {skip_count}件")
    
    # 5. general_notes.csvを更新
    if new_notes:
        print("\n=== general_notes.csv更新 ===")
        
        all_notes = existing_notes + new_notes
        with open(general_notes_file, 'w', encoding='utf-8', newline='') as file:
            if all_notes:
                writer = csv.DictWriter(file, fieldnames=all_notes[0].keys())
                writer.writeheader()
                writer.writerows(all_notes)
        
        # normalized_dataフォルダにもコピー
        dst = os.path.join(base_dir, 'normalized_data', 'general_notes.csv')
        if os.path.exists(os.path.dirname(dst)):
            shutil.copy2(general_notes_file, dst)
        
        print("general_notes.csvを更新しました")
        print(f"総レコード数: {len(all_notes)}件")
    else:
        print("追加するレコードがありません")
    
    # 6. 最終検証
    print(f"\n=== 最終検証 ===")
    
    emergence_notes_count = 0
    with open(general_notes_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['note_type'] == 'emergence_time' and row['reference'] == '日本の冬尺蛾':
                emergence_notes_count += 1
    
    print(f"general_notes.csvの冬尺蛾発生時期情報: {emergence_notes_count}件")
    print(f"✅ 成虫発生時期情報の追加が完了しました！")

if __name__ == "__main__":
    add_emergence_time_from_source()