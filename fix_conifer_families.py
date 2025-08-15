#!/usr/bin/env python3
import csv
import os

def fix_conifer_families():
    """針葉樹の科名が空白のものを「マツ科」に修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 針葉樹科名修正処理 ===")
    
    # マツ科に属する植物名のマッピング
    conifer_plants = {
        'シラビソ': 'マツ科',
        'オオシラビソ': 'マツ科', 
        'コメツガ': 'マツ科',
        'トウヒ': 'マツ科',
        'ドイツトウヒ': 'マツ科',
        'ウラジロモミ': 'マツ科',
        'ゴヨウマツ': 'マツ科',
        'トウヒ属': 'マツ科',
        'モミ': 'マツ科',
        'ツガ': 'マツ科',
        'カラマツ': 'マツ科',
        'アカマツ': 'マツ科',
        'クロマツ': 'マツ科',
        'ヒメツガ': 'マツ科',
        'バラモミ': 'マツ科',
        'ヤツガタケトウヒ': 'マツ科',
        'エゾマツ': 'マツ科'
    }
    
    print("修正対象植物:")
    for plant, family in conifer_plants.items():
        print(f"  {plant} → {family}")
    
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
        fixes_by_plant = {}
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_name = row['plant_name']
                plant_family = row['plant_family']
                
                # 対象植物で科名が空白または不正確な場合に修正
                if plant_name in conifer_plants:
                    correct_family = conifer_plants[plant_name]
                    if not plant_family or plant_family != correct_family:
                        print(f"修正: {row['record_id']} - '{plant_name}' の科名 '{plant_family}' → '{correct_family}'")
                        row['plant_family'] = correct_family
                        fixed_count += 1
                        
                        if plant_name not in fixes_by_plant:
                            fixes_by_plant[plant_name] = 0
                        fixes_by_plant[plant_name] += 1
                
                all_records.append(row)
        
        print(f"修正したレコード数: {fixed_count}件")
        if fixes_by_plant:
            print("植物別修正数:")
            for plant, count in fixes_by_plant.items():
                print(f"  {plant}: {count}件")
        
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
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            conifer_family_counts = {}
            
            for row in reader:
                plant_name = row['plant_name']
                plant_family = row['plant_family']
                
                if plant_name in conifer_plants:
                    key = f"{plant_name} ({plant_family})"
                    if key not in conifer_family_counts:
                        conifer_family_counts[key] = 0
                    conifer_family_counts[key] += 1
        
        print(f"  針葉樹の科名状況:")
        for plant_family, count in sorted(conifer_family_counts.items()):
            print(f"    {plant_family}: {count}件")
    
    print(f"\n✅ 針葉樹科名修正処理が完了しました！")

if __name__ == "__main__":
    fix_conifer_families()