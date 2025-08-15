#!/usr/bin/env python3
import csv
import os
import shutil

def fix_tsuge_plant_names():
    """植物名が「不明」でplant_familyが「ツゲ科」のレコードを「ツゲ」に修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== ツゲ植物名修正処理 ===")
    
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
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_name = row['plant_name']
                plant_family = row['plant_family']
                
                # 植物名が「不明」でplant_familyが「ツゲ科」の場合
                if plant_name == '不明' and plant_family == 'ツゲ科':
                    print(f"修正: {row['record_id']} ({row['insect_id']}) - '不明' → 'ツゲ' (ツゲ科)")
                    row['plant_name'] = 'ツゲ'
                    fixed_count += 1
                
                all_records.append(row)
        
        print(f"修正したレコード数: {fixed_count}件")
        
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
        tsuge_count = 0
        remaining_unknown_tsuge = 0
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_name = row['plant_name']
                plant_family = row['plant_family']
                
                # ツゲ科の植物をカウント
                if plant_family == 'ツゲ科':
                    if plant_name == 'ツゲ':
                        tsuge_count += 1
                    elif plant_name == '不明':
                        remaining_unknown_tsuge += 1
                        print(f"  未修正: {row['record_id']} - '{plant_name}' (ツゲ科)")
        
        print(f"  ツゲ科植物:")
        print(f"    ツゲ: {tsuge_count}件")
        print(f"    残存「不明」: {remaining_unknown_tsuge}件")
    
    # 修正済み昆虫の詳細表示
    print(f"\n=== 修正済み昆虫詳細 ===")
    
    with open(files_to_fix[0], 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fixed_insects = {}
        
        for row in reader:
            if row['plant_name'] == 'ツゲ' and row['plant_family'] == 'ツゲ科':
                insect_id = row['insect_id']
                if insect_id not in fixed_insects:
                    fixed_insects[insect_id] = []
                fixed_insects[insect_id].append(row['record_id'])
        
        for insect_id, record_ids in fixed_insects.items():
            print(f"  {insect_id}: {len(record_ids)}件のツゲ記録")
    
    print(f"\n✅ ツゲ植物名修正処理が完了しました！")

if __name__ == "__main__":
    fix_tsuge_plant_names()