#!/usr/bin/env python3
import csv
import os
import shutil
import re
from collections import defaultdict

def extract_notes_hostplants():
    """備考欄から食草情報を抽出して食草レコードとして分離"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 備考欄食草情報抽出処理 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # 1. 現在のデータを読み込み
    print("\n=== 備考欄食草情報の分析 ===")
    
    all_records = []
    notes_with_plants = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            all_records.append(row)
            
            # 冬尺蛾データで備考に「飼育下では」があるレコードを特定
            if (row['reference'] == '日本の冬尺蛾' and 
                row['notes'] and 
                '飼育下では' in row['notes'] and 
                '食べる' in row['notes']):
                notes_with_plants.append(row)
    
    print(f"備考に食草情報があるレコード数: {len(notes_with_plants)}件")
    
    # 2. 備考から食草名を抽出
    print("\n=== 食草名抽出 ===")
    
    plant_extraction_patterns = [
        # パターン1: 「飼育下ではシダレヤナギ、コナラ、クヌギ、ノイバラも食べる」
        r'飼育下では([^。]+?)も食べる',
        # パターン2: 「飼育下では○○をよく食べる」
        r'飼育下では([^。]+?)をよく食べる',
    ]
    
    extractions = []
    
    for record in notes_with_plants:
        notes = record['notes']
        insect_id = record['insect_id']
        
        for pattern in plant_extraction_patterns:
            matches = re.findall(pattern, notes)
            for match in matches:
                # 植物名をカンマで分割
                plant_names = [name.strip() for name in re.split('[、,]', match)]
                
                for plant_name in plant_names:
                    # 不要な文字を除去
                    plant_name = re.sub(r'^(特に|主に)', '', plant_name).strip()
                    
                    if plant_name and len(plant_name) > 1 and plant_name != 'マメ科':  # 科名は除外
                        extractions.append({
                            'insect_id': insect_id,
                            'plant_name': plant_name,
                            'observation_type': '飼育',
                            'source_record': record['record_id'],
                            'original_notes': notes
                        })
                        print(f"抽出: {insect_id} - {plant_name} (飼育)")
    
    print(f"抽出された食草: {len(extractions)}種類")
    
    # 3. 既存レコードとの重複チェック
    print("\n=== 重複チェック ===")
    
    existing_combinations = set()
    for record in all_records:
        if record['reference'] == '日本の冬尺蛾':
            key = f"{record['insect_id']}_{record['plant_name']}"
            existing_combinations.add(key)
    
    new_hostplants = []
    duplicates = []
    
    for extraction in extractions:
        key = f"{extraction['insect_id']}_{extraction['plant_name']}"
        if key not in existing_combinations:
            new_hostplants.append(extraction)
            existing_combinations.add(key)  # 重複防止
        else:
            duplicates.append(extraction)
    
    print(f"新規食草レコード: {len(new_hostplants)}件")
    print(f"重複（既存）: {len(duplicates)}件")
    
    # 4. 新規食草レコードを作成
    print("\n=== 新規食草レコード作成 ===")
    
    # 最大record_idを取得（record-形式とhostplant-形式の両方に対応）
    max_record_id = 0
    for record in all_records:
        record_id = record['record_id']
        if record_id.startswith('record-'):
            record_id_num = int(record_id.replace('record-', ''))
        elif record_id.startswith('hostplant-'):
            # hostplant-形式は除外（元のシステムのIDのため）
            continue
        else:
            continue
        max_record_id = max(max_record_id, record_id_num)
    
    next_record_id = max_record_id + 1
    
    new_records = []
    for hostplant in new_hostplants:
        new_record = {
            'record_id': f'record-{next_record_id:06d}',
            'insect_id': hostplant['insect_id'],
            'plant_name': hostplant['plant_name'],
            'plant_family': '',
            'observation_type': hostplant['observation_type'],
            'plant_part': '',
            'life_stage': '幼虫',
            'reference': '日本の冬尺蛾',
            'notes': f"備考から抽出（元レコード: {hostplant['source_record']}）"
        }
        new_records.append(new_record)
        next_record_id += 1
        print(f"新規: {new_record['record_id']} - {hostplant['insect_id']} - {hostplant['plant_name']}")
    
    # 5. 元の備考を清理
    print("\n=== 備考清理 ===")
    
    cleaned_count = 0
    for record in all_records:
        if (record['reference'] == '日本の冬尺蛾' and 
            record['notes'] and 
            ('飼育下では' in record['notes'] and '食べる' in record['notes'])):
            
            original_notes = record['notes']
            cleaned_notes = original_notes
            
            # 飼育情報を削除
            for pattern in plant_extraction_patterns:
                cleaned_notes = re.sub(pattern, '', cleaned_notes)
            
            # 清理
            cleaned_notes = re.sub(r'飼育下では[^。]*食べる[。]*\s*', '', cleaned_notes)
            cleaned_notes = re.sub(r'[。]{2,}', '。', cleaned_notes)
            cleaned_notes = re.sub(r'^[。、\s]+|[。、\s]+$', '', cleaned_notes)
            cleaned_notes = cleaned_notes.strip()
            
            if original_notes != cleaned_notes:
                print(f"備考清理: {record['record_id']}")
                print(f"  元: {original_notes}")
                print(f"  後: {cleaned_notes if cleaned_notes else '(空)'}")
                record['notes'] = cleaned_notes
                cleaned_count += 1
    
    print(f"備考を清理したレコード: {cleaned_count}件")
    
    # 6. ファイルを更新
    print("\n=== ファイル更新 ===")
    
    final_records = all_records + new_records
    
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if final_records:
            writer = csv.DictWriter(file, fieldnames=final_records[0].keys())
            writer.writeheader()
            writer.writerows(final_records)
    
    # normalized_dataフォルダにもコピー
    src = hostplants_file
    dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    print("hostplants.csvを更新しました")
    
    # 7. 結果サマリー
    print(f"\n=== 処理結果サマリー ===")
    print(f"総レコード数: {len(final_records):,}件")
    print(f"新規食草レコード追加: {len(new_records)}件")
    print(f"備考清理: {cleaned_count}件")
    print(f"重複回避: {len(duplicates)}件")
    
    if new_records:
        print(f"\n新規追加された食草:")
        for record in new_records:
            print(f"  {record['insect_id']} - {record['plant_name']}")
    
    print(f"\n✅ 備考欄食草情報の抽出処理が完了しました！")

if __name__ == "__main__":
    extract_notes_hostplants()