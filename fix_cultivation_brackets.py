#!/usr/bin/env python3
import csv
import os
import shutil
import re

def fix_cultivation_brackets():
    """植物名の「○○(飼育)」を「○○」に修正し、observation_typeを「飼育記録」に設定"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 飼育括弧修正処理 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # データを読み込み・修正
    print("\n=== データ修正 ===")
    
    all_records = []
    fixed_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            original_plant_name = row['plant_name']
            
            # 「○○(飼育)」パターンをチェック
            if '(飼育)' in original_plant_name:
                # 植物名から「(飼育)」を除去
                clean_plant_name = original_plant_name.replace('(飼育)', '').strip()
                row['plant_name'] = clean_plant_name
                
                # observation_typeを飼育記録に設定（既に設定されていない場合）
                if not row['observation_type'] or row['observation_type'] == '':
                    row['observation_type'] = '飼育記録'
                
                print(f"修正: {row['record_id']} - '{original_plant_name}' → '{clean_plant_name}' (observation: {row['observation_type']})")
                fixed_count += 1
            
            all_records.append(row)
    
    print(f"\n修正したレコード数: {fixed_count}件")
    
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
    
    remaining_brackets = 0
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if '(飼育)' in row['plant_name']:
                remaining_brackets += 1
                if remaining_brackets <= 5:  # 最初の5件のみ表示
                    print(f"  残存: {row['record_id']} - {row['plant_name']}")
    
    print(f"残存する括弧付き植物名: {remaining_brackets}件")
    
    # 修正結果のサンプル表示
    print(f"\n修正済みサンプル:")
    sample_count = 0
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['observation_type'] == '飼育記録' and row['reference'] == '日本の冬夜蛾':
                print(f"  {row['record_id']}: {row['plant_name']} - {row['observation_type']}")
                sample_count += 1
                if sample_count >= 5:
                    break
    
    print(f"\n✅ 飼育括弧修正処理が完了しました！")

if __name__ == "__main__":
    fix_cultivation_brackets()