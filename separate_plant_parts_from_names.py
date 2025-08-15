#!/usr/bin/env python3
import csv
import os
import shutil
import re

def separate_plant_parts_from_names():
    """植物名に含まれる部位名を分離してplant_partフィールドに移動"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 植物名部位分離処理 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # データを読み込み・修正
    print("\n=== データ修正 ===")
    
    all_records = []
    fixed_count = 0
    
    # 部位名パターンと対応する部位名
    part_patterns = {
        r'^(.+?)の花$': '花',
        r'^(.+?)の葉$': '葉', 
        r'^(.+?)の実$': '実',
        r'^(.+?)の果実$': '果実',
        r'^(.+?)の種子$': '種子',
        r'^(.+?)の根$': '根',
        r'^(.+?)の茎$': '茎',
        r'^(.+?)の枯れ葉$': '枯れ葉',
        r'^(.+?)の新芽$': '新芽',
        r'^(.+?)の若葉$': '若葉'
    }
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            original_plant_name = row['plant_name']
            plant_part_extracted = None
            clean_plant_name = original_plant_name
            
            # 各部位パターンをチェック
            for pattern, part_name in part_patterns.items():
                match = re.match(pattern, original_plant_name.strip())
                if match:
                    clean_plant_name = match.group(1).strip()
                    plant_part_extracted = part_name
                    break
            
            # 部位名が抽出された場合
            if plant_part_extracted:
                row['plant_name'] = clean_plant_name
                
                # plant_partフィールドを更新（既存の値を上書き）
                row['plant_part'] = plant_part_extracted
                
                print(f"修正: {row['record_id']}")
                print(f"  元: '{original_plant_name}'")
                print(f"  植物名: '{clean_plant_name}'")
                print(f"  部位: '{plant_part_extracted}'")
                print()
                fixed_count += 1
            
            all_records.append(row)
    
    print(f"修正したレコード数: {fixed_count}件")
    
    # ファイルを更新
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
    
    # 検証
    print(f"\n=== 検証 ===")
    
    remaining_patterns = 0
    fixed_examples = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            plant_name = row['plant_name']
            
            # まだ部位パターンが残っているかチェック
            if re.search(r'の(花|葉|実|果実|種子|根|茎|枯れ葉|新芽|若葉)$', plant_name):
                remaining_patterns += 1
                if remaining_patterns <= 5:  # 最初の5件のみ表示
                    print(f"  残存: {row['record_id']} - '{plant_name}'")
            
            # 修正済みサンプルを収集
            if (row['plant_part'] in ['花', '実', '果実', '種子', '根', '茎', '枯れ葉', '新芽', '若葉'] and 
                len(fixed_examples) < 5):
                fixed_examples.append({
                    'record_id': row['record_id'],
                    'plant_name': row['plant_name'],
                    'plant_part': row['plant_part']
                })
    
    print(f"残存する部位パターン: {remaining_patterns}件")
    
    if fixed_examples:
        print(f"\n修正済みサンプル:")
        for example in fixed_examples:
            print(f"  {example['record_id']}: {example['plant_name']} (部位: {example['plant_part']})")
    
    # 統計情報
    part_stats = {}
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            part = row['plant_part']
            if part:
                part_stats[part] = part_stats.get(part, 0) + 1
    
    print(f"\n部位統計:")
    for part, count in sorted(part_stats.items()):
        print(f"  {part}: {count}件")
    
    print(f"\n✅ 植物名部位分離処理が完了しました！")

if __name__ == "__main__":
    separate_plant_parts_from_names()