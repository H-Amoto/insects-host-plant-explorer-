#!/usr/bin/env python3
import csv
import os
import shutil

def fix_missing_plant_names():
    """植物名が「不明」で科名が特定されているレコードを修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 不明植物名修正処理 ===")
    
    # 修正マッピング: family -> plant_name
    family_to_plant = {
        'ゴマ科': 'ゴマ',
        'アケビ科': 'アケビ', 
        'アサ科': 'アサ',
        'アマ科': 'アマ',
        'イグサ科': 'イグサ',
        'ガマ科': 'ガマ',
        'アオイ科': 'アオイ',
        'アブラナ科': 'アブラナ',
        'ウコギ科': 'ウコギ',
        'セリ科': 'セリ',
        'タデ科': 'タデ',
        'ネギ科': 'ネギ',
        'メギ科': 'メギ',
        '以上ゴマ科': 'クコ',  # 元データで「クコ (以上ゴマ科)」の記録あり
        '以上アケビ科': 'アケビ',
        '以上アサ科': 'アサ',
        '以上アマ科': 'アマ'
    }
    
    print("修正マッピング:")
    for family, plant in family_to_plant.items():
        print(f"  {family} → {plant}")
    
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
                plant_name = row['plant_name']
                plant_family = row['plant_family']
                
                # 植物名が「不明」でplant_familyが修正対象の場合
                if plant_name == '不明' and plant_family in family_to_plant:
                    new_plant_name = family_to_plant[plant_family]
                    print(f"修正: {row['record_id']} ({row['insect_id']}) - '不明' → '{new_plant_name}' ({plant_family})")
                    row['plant_name'] = new_plant_name
                    fixed_count += 1
                    
                    if plant_family not in fixes_by_family:
                        fixes_by_family[plant_family] = 0
                    fixes_by_family[plant_family] += 1
                
                all_records.append(row)
        
        print(f"修正したレコード数: {fixed_count}件")
        if fixes_by_family:
            print("科別修正数:")
            for family, count in fixes_by_family.items():
                print(f"  {family}: {count}件")
        
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
        plant_counts = {}
        remaining_unknown = {}
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_name = row['plant_name']
                plant_family = row['plant_family']
                
                # 修正された植物をカウント
                if plant_family in family_to_plant:
                    expected_plant = family_to_plant[plant_family]
                    if plant_name == expected_plant:
                        if expected_plant not in plant_counts:
                            plant_counts[expected_plant] = 0
                        plant_counts[expected_plant] += 1
                    elif plant_name == '不明':
                        if plant_family not in remaining_unknown:
                            remaining_unknown[plant_family] = 0
                        remaining_unknown[plant_family] += 1
        
        print(f"  修正済み植物:")
        for plant, count in sorted(plant_counts.items()):
            print(f"    {plant}: {count}件")
        
        if remaining_unknown:
            print(f"  残存「不明」:")
            for family, count in remaining_unknown.items():
                print(f"    {family}: {count}件")
        else:
            print(f"  残存「不明」: なし")
    
    # 修正済み昆虫の詳細表示
    print(f"\n=== 修正済み昆虫サンプル ===")
    
    with open(files_to_fix[0], 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fixed_insects = {}
        
        for row in reader:
            plant_name = row['plant_name']
            plant_family = row['plant_family']
            if plant_family in family_to_plant and plant_name == family_to_plant[plant_family]:
                insect_id = row['insect_id']
                if insect_id not in fixed_insects:
                    fixed_insects[insect_id] = []
                fixed_insects[insect_id].append(f"{plant_name} ({plant_family})")
        
        sample_count = 0
        for insect_id, plants in fixed_insects.items():
            print(f"  {insect_id}: {', '.join(plants)}")
            sample_count += 1
            if sample_count >= 10:  # Show first 10
                break
        
        if len(fixed_insects) > 10:
            print(f"  ... and {len(fixed_insects) - 10} more insects")
    
    print(f"\n✅ 不明植物名修正処理が完了しました！")

if __name__ == "__main__":
    fix_missing_plant_names()