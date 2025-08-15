#!/usr/bin/env python3
import csv
import re
import os

def fix_family_only_entries():
    """科名のみのエントリを修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 科名のみエントリの修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    fixed_data = []
    removed_count = 0
    updated_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            plant_family = row['plant_family']
            insect_id = row['insect_id']
            
            # 科名のみのケース
            if plant_name.endswith('科') and len(plant_name) <= 10 and not plant_family:
                # plant_familyが空の場合、この科名を移動
                print(f"修正: 行{row_num} {insect_id} → '{plant_name}' を科名に移動")
                
                # 同じ昆虫の前のエントリがあれば、そこのplant_familyを更新
                if fixed_data and fixed_data[-1]['insect_id'] == insect_id:
                    fixed_data[-1]['plant_family'] = plant_name
                    updated_count += 1
                    print(f"  → 前エントリ ({fixed_data[-1]['plant_name']}) の科名を '{plant_name}' に更新")
                
                removed_count += 1
                continue  # このエントリは削除
            
            # 科名のみで、既にplant_familyがある場合
            elif plant_name.endswith('科') and len(plant_name) <= 10 and plant_family:
                print(f"削除: 行{row_num} {insect_id} → '{plant_name}' (既に科名'{plant_family}'あり)")
                removed_count += 1
                continue  # このエントリは削除
            
            # 正常なエントリは保持
            fixed_data.append(row)
    
    print(f"\n修正結果:")
    print(f"  削除したエントリ: {removed_count}件")
    print(f"  科名を更新したエントリ: {updated_count}件")
    print(f"  残存エントリ: {len(fixed_data)}件")
    
    # 修正されたデータを保存
    if removed_count > 0 or updated_count > 0:
        with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
            if fixed_data:
                writer = csv.DictWriter(file, fieldnames=fixed_data[0].keys())
                writer.writeheader()
                writer.writerows(fixed_data)
        
        # normalized_dataフォルダにもコピー
        import shutil
        src = hostplants_file
        dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
        shutil.copy2(src, dst)
        
        print("hostplants.csvを更新しました")
        
        # 検証
        print(f"\n=== 検証 ===")
        remaining_family_only = 0
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'].endswith('科') and len(row['plant_name']) <= 10:
                    remaining_family_only += 1
                    if remaining_family_only <= 5:
                        print(f"残存科名エントリ: {row['insect_id']} → '{row['plant_name']}'")
        
        if remaining_family_only == 0:
            print("✅ 科名のみエントリは全て修正されました")
        else:
            print(f"⚠️  {remaining_family_only}件の科名エントリが残っています")
    
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_family_only_entries()