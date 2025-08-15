#!/usr/bin/env python3
import csv
import os
import shutil
import re

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

def integrate_winter_moths():
    """日本の冬尺蛾.csvの食草情報をhostplants.csvに正規化して追加"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 冬尺蛾食草データの正規化統合 ===")
    
    # ファイル
    winter_moths_file = os.path.join(base_dir, 'public', '日本の冬尺蛾.csv')
    insects_file = os.path.join(base_dir, 'public', 'insects.csv')
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
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
    
    # 2. 現在のhostplants.csvの最大record_idを取得
    print("\n=== 現在のhostplants.csv分析 ===")
    
    max_record_id = 0
    existing_records = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_records.append(row)
            record_id = row['record_id']
            
            # record-形式とhostplant-形式の両方に対応
            if record_id.startswith('record-'):
                record_id_num = int(record_id.replace('record-', ''))
            elif record_id.startswith('hostplant-'):
                record_id_num = int(record_id.replace('hostplant-', ''))
            else:
                # その他の形式は0として扱う
                record_id_num = 0
            
            max_record_id = max(max_record_id, record_id_num)
    
    print(f"既存レコード数: {len(existing_records)}件")
    print(f"最大record_id: record-{max_record_id}")
    
    # 3. 冬尺蛾データを正規化
    print("\n=== 冬尺蛾データ正規化 ===")
    
    new_records = []
    next_record_id = max_record_id + 1
    
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
                    # 学名を結合
                    scientific_name = f"{parts[1].strip()}, {parts[2].strip()}"
                    food_plants = parts[3].strip().strip('"')
                    food_notes = parts[4].strip().strip('"')
                    emergence_time = parts[5].strip().strip('"')
                else:  # len(parts) == 5
                    scientific_name = parts[1].strip()
                    food_plants = parts[2].strip().strip('"')
                    food_notes = parts[3].strip().strip('"')
                    emergence_time = parts[4].strip().strip('"')
            else:
                continue
            
            # insect_idを取得
            if japanese_name not in name_to_id:
                print(f"⚠️ {japanese_name}: insects.csvに見つからない")
                continue
            
            insect_id = name_to_id[japanese_name]
            
            print(f"\n処理中: {japanese_name} ({insect_id})")
            print(f"  食草: {food_plants}")
            
            # 食草を分析・分割
            if food_plants == '不明':
                # 食草不明の場合
                new_record = {
                    'record_id': f'record-{next_record_id}',
                    'insect_id': insect_id,
                    'plant_name': '不明',
                    'plant_family': '',
                    'observation_type': '',
                    'plant_part': '',
                    'life_stage': '成虫',
                    'reference': '日本の冬尺蛾',
                    'notes': food_notes if food_notes else ''
                }
                new_records.append(new_record)
                next_record_id += 1
                print(f"    → {new_record['plant_name']}")
            
            else:
                # 食草リストを解析
                plants = parse_plant_list(food_plants)
                
                for plant_info in plants:
                    plant_name = plant_info['name']
                    plant_part = plant_info['part']
                    plant_family = plant_info['family']
                    
                    # 飼育記録かどうかの判定
                    observation_type = ''
                    if '飼育' in food_notes or '飼育記録' in food_notes:
                        if plant_name in food_notes:
                            observation_type = '飼育記録'
                    
                    # 備考欄の作成
                    notes_parts = []
                    if food_notes:
                        notes_parts.append(food_notes)
                    if emergence_time:
                        notes_parts.append(f"成虫発生時期: {emergence_time}")
                    
                    new_record = {
                        'record_id': f'record-{next_record_id}',
                        'insect_id': insect_id,
                        'plant_name': plant_name,
                        'plant_family': plant_family,
                        'observation_type': observation_type,
                        'plant_part': plant_part,
                        'life_stage': '成虫',
                        'reference': '日本の冬尺蛾',
                        'notes': '; '.join(notes_parts)
                    }
                    new_records.append(new_record)
                    next_record_id += 1
                    
                    print(f"    → {plant_name} ({plant_part}) {plant_family}")
    
    print(f"\n新規レコード作成: {len(new_records)}件")
    
    # 4. hostplants.csvに追加
    print("\n=== hostplants.csv更新 ===")
    
    all_records = existing_records + new_records
    
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if all_records:
            fieldnames = all_records[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_records)
    
    # normalized_dataフォルダにもコピー
    src = hostplants_file
    dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    print(f"hostplants.csvを更新しました")
    print(f"総レコード数: {len(all_records)}件")
    
    # 5. 統合結果の検証
    print(f"\n=== 統合結果検証 ===")
    
    winter_moth_sources = 0
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['reference'] == '日本の冬尺蛾':
                winter_moth_sources += 1
    
    print(f"日本の冬尺蛾出典のエントリ: {winter_moth_sources}件")
    print(f"✅ 冬尺蛾食草データの統合が完了しました！")

def parse_plant_list(food_plants_text):
    """食草リストを解析して個別の植物情報に分割"""
    plants = []
    
    # カンマまたは中点で分割
    plant_items = re.split(r'[、,]', food_plants_text)
    
    for item in plant_items:
        item = item.strip()
        if not item:
            continue
        
        plant_name = item
        plant_part = ''
        plant_family = ''
        
        # 部位の抽出（括弧内）
        part_match = re.search(r'\(([^)]+)\)', item)
        if part_match:
            plant_part = part_match.group(1)
            plant_name = re.sub(r'\([^)]+\)', '', item).strip()
        
        # 「〜の花」「〜の葉」パターン
        part_patterns = {
            r'の花': '花',
            r'の葉': '葉', 
            r'の実': '実',
            r'の花蕾': '花蕾',
            r'の新芽': '新芽'
        }
        
        for pattern, part in part_patterns.items():
            if pattern in item:
                plant_part = part
                plant_name = re.sub(pattern, '', item).strip()
                break
        
        # 科名の処理（今回は空のまま）
        plant_family = ''
        
        # クリーニング
        plant_name = re.sub(r'[\(\)]', '', plant_name).strip()
        
        if plant_name:
            plants.append({
                'name': plant_name,
                'part': plant_part,
                'family': plant_family
            })
    
    return plants

if __name__ == "__main__":
    integrate_winter_moths()