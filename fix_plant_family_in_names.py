#!/usr/bin/env python3
import csv
import os
import shutil
import re

def fix_plant_family_in_names():
    """植物名に含まれる科名を分離してplant_familyフィールドに移動"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 植物名科名分離処理 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # データを読み込み・修正
    print("\n=== データ修正 ===")
    
    all_records = []
    fixed_count = 0
    
    # 科名を抽出するパターン
    family_patterns = [
        # パターン1: 「植物名 (科名)」
        r'^(.+?)\s*\(([^)]*科)\)$',
        # パターン2: 「植物名 (学名)(以上科名)」
        r'^(.+?)\s*\([^)]*\)\s*\(以上([^)]*科)\)$',
        # パターン3: 「植物名(以上科名)」
        r'^(.+?)\s*\(以上([^)]*科)\)$',
    ]
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            original_plant_name = row['plant_name']
            plant_family_extracted = None
            clean_plant_name = original_plant_name
            
            # 各パターンをチェック
            for pattern in family_patterns:
                match = re.match(pattern, original_plant_name.strip())
                if match:
                    if len(match.groups()) == 2:
                        clean_plant_name = match.group(1).strip()
                        plant_family_extracted = match.group(2).strip()
                        break
            
            # 科名が抽出された場合
            if plant_family_extracted:
                row['plant_name'] = clean_plant_name
                
                # plant_familyフィールドが空の場合のみ設定
                if not row['plant_family'] or row['plant_family'].strip() == '':
                    row['plant_family'] = plant_family_extracted
                
                print(f"修正: {row['record_id']}")
                print(f"  元: '{original_plant_name}'")
                print(f"  植物名: '{clean_plant_name}'")
                print(f"  科名: '{plant_family_extracted}'")
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
            
            # まだ科名パターンが残っているかチェック
            if ('科)' in plant_name or '科）' in plant_name) and '(' in plant_name:
                remaining_patterns += 1
                if remaining_patterns <= 5:  # 最初の5件のみ表示
                    print(f"  残存: {row['record_id']} - '{plant_name}'")
            
            # 修正済みサンプルを収集
            if (row['plant_family'] and 
                row['reference'] in ['日本の冬夜蛾', '日本の冬尺蛾'] and 
                len(fixed_examples) < 5):
                fixed_examples.append({
                    'record_id': row['record_id'],
                    'plant_name': row['plant_name'],
                    'plant_family': row['plant_family']
                })
    
    print(f"残存する科名パターン: {remaining_patterns}件")
    
    if fixed_examples:
        print(f"\n修正済みサンプル:")
        for example in fixed_examples:
            print(f"  {example['record_id']}: {example['plant_name']} ({example['plant_family']})")
    
    print(f"\n✅ 植物名科名分離処理が完了しました！")

if __name__ == "__main__":
    fix_plant_family_in_names()