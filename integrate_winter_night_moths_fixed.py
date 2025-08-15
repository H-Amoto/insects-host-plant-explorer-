#!/usr/bin/env python3
import csv
import os
import shutil
import re
from collections import defaultdict

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

def integrate_winter_night_moths():
    """冬夜蛾データをinsects.csvとhostplants.csvに統合"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 冬夜蛾データ統合処理 ===")
    
    # ファイルパス
    winter_night_moths_file = os.path.join(base_dir, 'public', '日本の冬夜蛾.csv')
    insects_file = os.path.join(base_dir, 'public', 'insects.csv')
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    general_notes_file = os.path.join(base_dir, 'public', 'general_notes.csv')
    
    # 1. 既存データを読み込み
    print("\n=== 既存データ読み込み ===")
    
    # insects.csv
    insects_data = []
    existing_insects = {}
    max_insect_id = 0
    
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            insects_data.append(row)
            japanese_name = row['japanese_name'].strip()
            existing_insects[japanese_name] = row['insect_id']
            
            # 最大insect_idを取得（species-形式のみ）
            if row['insect_id'].startswith('species-'):
                insect_id_num = int(row['insect_id'].replace('species-', ''))
                max_insect_id = max(max_insect_id, insect_id_num)
    
    # hostplants.csv
    hostplants_data = []
    max_hostplant_id = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            hostplants_data.append(row)
            
            # 最大record_idを取得
            if row['record_id'].startswith('record-'):
                record_id_num = int(row['record_id'].replace('record-', ''))
                max_hostplant_id = max(max_hostplant_id, record_id_num)
    
    # general_notes.csv
    general_notes_data = []
    max_note_id = 0
    
    with open(general_notes_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            general_notes_data.append(row)
            
            # 最大note_idを取得
            note_id_num = int(row['record_id'].replace('note-', ''))
            max_note_id = max(max_note_id, note_id_num)
    
    print(f"既存昆虫: {len(insects_data)}種")
    print(f"既存食草記録: {len(hostplants_data)}件")
    print(f"既存一般記録: {len(general_notes_data)}件")
    print(f"最大insect_id: species-{max_insect_id}")
    
    # 2. 冬夜蛾データを読み込み
    print("\n=== 冬夜蛾データ読み込み ===")
    
    winter_night_moths = []
    with open(winter_night_moths_file, 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()
        for line in lines[1:]:  # ヘッダーを除外
            line = line.strip()
            if not line:
                continue
            
            parts = parse_csv_line_manual(line)
            if len(parts) >= 5:
                winter_night_moths.append({
                    'japanese_name': parts[0].strip().strip('"'),
                    'scientific_name': parts[1].strip().strip('"'),
                    'food_plants': parts[2].strip().strip('"'),
                    'food_notes': parts[3].strip().strip('"'),
                    'emergence_time': parts[4].strip().strip('"')
                })
    
    print(f"冬夜蛾: {len(winter_night_moths)}種")
    
    # 3. 新規昆虫を特定
    print("\n=== 新規昆虫特定 ===")
    
    new_insects = []
    existing_moths = []
    next_insect_id = max_insect_id + 1
    
    for moth in winter_night_moths:
        japanese_name = moth['japanese_name']
        if japanese_name in existing_insects:
            moth['insect_id'] = existing_insects[japanese_name]
            existing_moths.append(moth)
        else:
            moth['insect_id'] = f'species-{next_insect_id:04d}'
            new_insect = {
                'insect_id': moth['insect_id'],
                'japanese_name': japanese_name,
                'scientific_name': moth['scientific_name'],
                'order': 'チョウ目',
                'family': 'ヤガ科',
                'subfamily': '',
                'tribe': '',
                'genus': moth['scientific_name'].split(' ')[0] if ' ' in moth['scientific_name'] else '',
                'species': moth['scientific_name'].split(' ')[1] if ' ' in moth['scientific_name'] else '',
                'subspecies': '',
                'author': '',
                'year': '',
                'reference': '日本の冬夜蛾',
                'page': '',
                'notes': ''
            }
            new_insects.append(new_insect)
            existing_moths.append(moth)
            next_insect_id += 1
    
    print(f"新規昆虫: {len(new_insects)}種")
    print(f"既存昆虫: {len(existing_moths) - len(new_insects)}種")
    
    # 4. 食草レコードを作成
    print("\n=== 食草レコード作成 ===")
    
    new_hostplants = []
    new_general_notes = []
    next_hostplant_id = max_hostplant_id + 1
    next_note_id = max_note_id + 1
    
    for moth in existing_moths:
        insect_id = moth['insect_id']
        food_plants_text = moth['food_plants']
        food_notes = moth['food_notes']
        emergence_time = moth['emergence_time']
        
        # 食草を解析
        if food_plants_text and food_plants_text != '不明':
            # 食草名を分離（カンマ、日本語読点、「など」で区切り）
            plant_names = re.split('[、,]|など', food_plants_text)
            
            for plant_name in plant_names:
                plant_name = plant_name.strip()
                # 括弧内の情報を除去して植物名を抽出
                plant_name_clean = re.sub(r'\\([^)]*\\)', '', plant_name)
                plant_name_clean = re.sub(r'（[^）]*）', '', plant_name_clean).strip()
                
                # 観察種別を判定
                observation_type = ''
                if '飼育' in plant_name or '飼育' in food_notes:
                    observation_type = '飼育記録'
                elif '野外' in food_notes:
                    observation_type = '野外記録'
                else:
                    observation_type = ''  # 空欄
                
                if plant_name_clean and len(plant_name_clean) > 1:
                    hostplant_record = {
                        'record_id': f'record-{next_hostplant_id:06d}',
                        'insect_id': insect_id,
                        'plant_name': plant_name_clean,
                        'plant_family': '',
                        'observation_type': observation_type,
                        'plant_part': '',
                        'life_stage': '幼虫',  # 夜蛾も食草は幼虫記録
                        'reference': '日本の冬夜蛾',
                        'notes': food_notes if food_notes else ''
                    }
                    new_hostplants.append(hostplant_record)
                    next_hostplant_id += 1
                    
                    print(f"食草追加: {insect_id} - {plant_name_clean} ({observation_type})")
        
        # 成虫発生時期を general_notes に追加
        if emergence_time:
            emergence_note = {
                'record_id': f'note-{next_note_id:06d}',
                'insect_id': insect_id,
                'note_type': 'emergence_time',
                'content': emergence_time,
                'reference': '日本の冬夜蛾',
                'page': '',
                'year': ''
            }
            new_general_notes.append(emergence_note)
            next_note_id += 1
    
    print(f"\n新規食草レコード: {len(new_hostplants)}件")
    print(f"新規発生時期レコード: {len(new_general_notes)}件")
    
    # 5. ファイルを更新
    print("\n=== ファイル更新 ===")
    
    # insects.csv更新
    if new_insects:
        final_insects = insects_data + new_insects
        with open(insects_file, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=final_insects[0].keys())
            writer.writeheader()
            writer.writerows(final_insects)
        print(f"insects.csv更新: +{len(new_insects)}種")
    
    # hostplants.csv更新
    if new_hostplants:
        final_hostplants = hostplants_data + new_hostplants
        with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=final_hostplants[0].keys())
            writer.writeheader()
            writer.writerows(final_hostplants)
        print(f"hostplants.csv更新: +{len(new_hostplants)}件")
    
    # general_notes.csv更新
    if new_general_notes:
        final_notes = general_notes_data + new_general_notes
        with open(general_notes_file, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=final_notes[0].keys())
            writer.writeheader()
            writer.writerows(final_notes)
        print(f"general_notes.csv更新: +{len(new_general_notes)}件")
    
    # normalized_dataフォルダにコピー
    for src, filename in [(insects_file, 'insects.csv'), (hostplants_file, 'hostplants.csv'), (general_notes_file, 'general_notes.csv')]:
        dst = os.path.join(base_dir, 'normalized_data', filename)
        if os.path.exists(os.path.dirname(dst)):
            shutil.copy2(src, dst)
    
    print("normalized_dataフォルダを更新しました")
    
    # 6. 結果サマリー
    print(f"\n=== 統合結果サマリー ===")
    print(f"処理した冬夜蛾: {len(winter_night_moths)}種")
    print(f"新規追加昆虫: {len(new_insects)}種")
    print(f"新規食草レコード: {len(new_hostplants)}件")
    print(f"新規発生時期レコード: {len(new_general_notes)}件")
    
    if new_insects:
        print(f"\n新規追加された昆虫:")
        for insect in new_insects:
            print(f"  {insect['insect_id']}: {insect['japanese_name']} - {insect['scientific_name']}")
    
    print(f"\n✅ 冬夜蛾データの統合処理が完了しました！")

if __name__ == "__main__":
    integrate_winter_night_moths()