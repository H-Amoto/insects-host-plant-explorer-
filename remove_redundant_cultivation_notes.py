#!/usr/bin/env python3
import csv
import os
import shutil
import re

def remove_redundant_cultivation_notes():
    """既存食草レコードで反映済みの「○○は飼育記録」備考を削除"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 重複飼育記録備考削除処理 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # 1. データを読み込み、昆虫別の食草記録を収集
    print("\n=== データ分析 ===")
    
    all_records = []
    insect_cultivation_plants = {}  # insect_id -> set of plant names with cultivation records
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            all_records.append(row)
            
            if row['reference'] == '日本の冬尺蛾':
                insect_id = row['insect_id']
                plant_name = row['plant_name']
                observation_type = row['observation_type']
                
                # 飼育記録として登録されている植物を記録
                if observation_type == '飼育記録':
                    if insect_id not in insect_cultivation_plants:
                        insect_cultivation_plants[insect_id] = set()
                    insect_cultivation_plants[insect_id].add(plant_name)
    
    print(f"総レコード数: {len(all_records):,}件")
    print(f"飼育記録がある昆虫数: {len(insect_cultivation_plants)}種")
    
    # 2. 重複備考を特定・削除
    print("\n=== 重複備考削除 ===")
    
    cleaned_count = 0
    
    for record in all_records:
        if (record['reference'] == '日本の冬尺蛾' and 
            record['notes'] and 
            'は飼育記録' in record['notes']):
            
            insect_id = record['insect_id']
            original_notes = record['notes']
            cleaned_notes = original_notes
            removed_plants = []
            
            # この昆虫で飼育記録がある植物を取得
            if insect_id in insect_cultivation_plants:
                cultivation_plants = insect_cultivation_plants[insect_id]
                
                # 各飼育植物について備考から重複情報を削除
                for plant in cultivation_plants:
                    # パターン1: 「植物名は飼育記録。」
                    pattern1 = f'{plant}は飼育記録[。；;]*\\s*'
                    if re.search(pattern1, cleaned_notes):
                        cleaned_notes = re.sub(pattern1, '', cleaned_notes)
                        removed_plants.append(plant)
                        continue
                    
                    # パターン2: 文中の「、植物名は飼育記録」
                    pattern2 = f'[。、；;]\\s*{plant}は飼育記録[。；;]*\\s*'
                    if re.search(pattern2, cleaned_notes):
                        cleaned_notes = re.sub(pattern2, '。', cleaned_notes)
                        removed_plants.append(plant)
                        continue
            
            # テキストの後処理
            cleaned_notes = re.sub(r'[。]{2,}', '。', cleaned_notes)  # 重複句点を統合
            cleaned_notes = re.sub(r'^[。；;、\s]+', '', cleaned_notes)  # 先頭の句読点を除去
            cleaned_notes = re.sub(r'[。；;、\s]+$', '', cleaned_notes)  # 末尾の句読点を除去
            cleaned_notes = cleaned_notes.strip()
            
            # 適切に句点で終わるよう調整
            if cleaned_notes and not cleaned_notes.endswith(('。', '；', ';')):
                cleaned_notes += '。'
            
            if original_notes != cleaned_notes:
                print(f"修正: {record['record_id']} ({insect_id})")
                print(f"  元: {original_notes}")
                print(f"  後: {cleaned_notes if cleaned_notes else '(空)'}")
                if removed_plants:
                    print(f"  削除: {', '.join(removed_plants)}の飼育記録情報")
                print()
                
                record['notes'] = cleaned_notes
                cleaned_count += 1
    
    print(f"修正したレコード数: {cleaned_count}件")
    
    # 3. ファイルを更新
    print("\n=== ファイル更新 ===")
    
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if all_records:
            writer = csv.DictWriter(file, fieldnames=all_records[0].keys())
            writer.writeheader()
            writer.writerows(all_records)
    
    # normalized_dataフォルダにもコピー
    src = hostplants_file
    dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    print("hostplants.csvを更新しました")
    
    # 4. 検証
    print(f"\n=== 検証 ===")
    
    remaining_redundant = 0
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (row['reference'] == '日本の冬尺蛾' and 
                row['notes'] and 
                'は飼育記録' in row['notes']):
                
                insect_id = row['insect_id']
                notes = row['notes']
                
                # まだ重複があるかチェック
                if insect_id in insect_cultivation_plants:
                    cultivation_plants = insect_cultivation_plants[insect_id]
                    for plant in cultivation_plants:
                        if f'{plant}は飼育記録' in notes:
                            remaining_redundant += 1
                            if remaining_redundant <= 3:  # 最初の3件のみ表示
                                print(f"  残存重複: {row['record_id']} - {plant}は飼育記録")
                            break
    
    print(f"残存重複: {remaining_redundant}件")
    
    print(f"\n✅ 重複飼育記録備考の削除処理が完了しました！")

if __name__ == "__main__":
    remove_redundant_cultivation_notes()