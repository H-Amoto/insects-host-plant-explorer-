#!/usr/bin/env python3
import csv
import os
import re

def fix_above_family_names():
    """「以上◯◯科」を「◯◯科」に修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 「以上」付き科名修正処理 ===")
    
    # 両方のファイルを修正
    files_to_fix = [
        os.path.join(base_dir, 'public', 'hostplants.csv'),
        os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    ]
    
    for hostplants_file in files_to_fix:
        if not os.path.exists(hostplants_file):
            print(f"ファイルが見つかりません: {hostplants_file}")
            continue
            
        print(f"\n=== {hostplants_file} の修正 ===")
        
        all_records = []
        fixed_count = 0
        fixes_by_family = {}
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_family = row['plant_family']
                
                # 「以上◯◯科」のパターンを検出
                match = re.match(r'以上(.+科)', plant_family)
                if match:
                    new_family_name = match.group(1)
                    print(f"修正: {row['record_id']} - '{plant_family}' → '{new_family_name}'")
                    row['plant_family'] = new_family_name
                    fixed_count += 1
                    
                    if plant_family not in fixes_by_family:
                        fixes_by_family[plant_family] = 0
                    fixes_by_family[plant_family] += 1
                
                all_records.append(row)
        
        print(f"修正したレコード数: {fixed_count}件")
        if fixes_by_family:
            print("科別修正数:")
            for old_family, count in sorted(fixes_by_family.items(), key=lambda x: x[1], reverse=True):
                new_family = re.match(r'以上(.+)', old_family).group(1)
                print(f"  {old_family} → {new_family}: {count}件")
        
        # ファイルを更新
        print(f"\n=== ファイル更新 ===")
        
        with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
            if all_records:
                writer = csv.DictWriter(file, fieldnames=all_records[0].keys())
                writer.writeheader()
                writer.writerows(all_records)
        
        print(f"{hostplants_file} を更新しました")
    
    # 検証
    print(f"\n=== 検証 ===")
    
    for hostplants_file in files_to_fix:
        if not os.path.exists(hostplants_file):
            continue
            
        print(f"\n{hostplants_file}:")
        remaining_above_families = {}
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_family = row['plant_family']
                
                # 残存する「以上」付きの科名をチェック
                if plant_family.startswith('以上'):
                    if plant_family not in remaining_above_families:
                        remaining_above_families[plant_family] = 0
                    remaining_above_families[plant_family] += 1
        
        if remaining_above_families:
            print(f"  残存「以上」付き科名:")
            for family, count in remaining_above_families.items():
                print(f"    {family}: {count}件")
        else:
            print(f"  残存「以上」付き科名: なし")
    
    # 修正例の表示
    print(f"\n=== 修正後のサンプル ===")
    
    with open(files_to_fix[0], 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        sample_records = []
        
        for row in reader:
            plant_family = row['plant_family']
            # よく使われる科の修正例を表示
            if plant_family in ['ブナ科', 'バラ科', 'キク科', 'カバノキ科', 'マツ科']:
                sample_records.append({
                    'insect_id': row['insect_id'],
                    'plant_name': row['plant_name'],
                    'plant_family': plant_family,
                    'record_id': row['record_id']
                })
            
            if len(sample_records) >= 15:  # 最初の15件
                break
        
        for record in sample_records:
            print(f"  {record['insect_id']} - {record['plant_name']} ({record['plant_family']})")
    
    print(f"\n✅ 「以上」付き科名修正処理が完了しました！")

if __name__ == "__main__":
    fix_above_family_names()