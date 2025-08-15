#!/usr/bin/env python3
import csv
import re
import os

def fix_family_plant_patterns():
    """「科名の植物名」パターンを植物名と科名に分離"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 「科名の植物名」パターン分離開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            original_name = plant_name
            
            # パターン1: 「科名の植物名」の基本形
            pattern1 = re.search(r'^([^の科]+科)の([^（，、]+)', plant_name)
            if pattern1:
                family_name = pattern1.group(1)
                species_name = pattern1.group(2)
                
                # 既存の科名と比較
                current_family = row['plant_family']
                
                print(f"修正: 行{row_num}")
                print(f"  元: plant_name='{original_name}', plant_family='{current_family}'")
                print(f"  新: plant_name='{species_name}', plant_family='{family_name}'")
                
                row['plant_name'] = species_name
                row['plant_family'] = family_name
                fix_count += 1
            
            # パターン2: 特別なケース - 「特に科名の植物名を利用するという」
            elif re.search(r'特に([^の]+科)の([^を]+)を利用するという', plant_name):
                pattern2 = re.search(r'特に([^の]+科)の([^を]+)を利用するという', plant_name)
                if pattern2:
                    family_name = pattern2.group(1)
                    species_name = pattern2.group(2)
                    
                    print(f"修正: 行{row_num}")
                    print(f"  元: '{original_name}'")
                    print(f"  新: plant_name='{species_name}', plant_family='{family_name}', notes='特に利用するという'")
                    
                    row['plant_name'] = species_name
                    row['plant_family'] = family_name
                    row['notes'] = '特に利用するという'
                    fix_count += 1
            
            # パターン3: 「科名の各種植物名」
            elif re.search(r'^([^の]+科)の各種([^（]+)', plant_name):
                pattern3 = re.search(r'^([^の]+科)の各種([^（]+)', plant_name)
                if pattern3:
                    family_name = pattern3.group(1)
                    species_name = pattern3.group(2)
                    
                    print(f"修正: 行{row_num}")
                    print(f"  元: '{original_name}'")
                    print(f"  新: plant_name='{species_name}', plant_family='{family_name}', notes='各種'")
                    
                    row['plant_name'] = species_name
                    row['plant_family'] = family_name
                    row['notes'] = '各種'
                    fix_count += 1
            
            # パターン4: 「科名の属名属」
            elif re.search(r'^([^の]+科)の ([A-Za-z]+) 属', plant_name):
                pattern4 = re.search(r'^([^の]+科)の ([A-Za-z]+) 属', plant_name)
                if pattern4:
                    family_name = pattern4.group(1)
                    genus_name = pattern4.group(2) + '属'
                    
                    print(f"修正: 行{row_num}")
                    print(f"  元: '{original_name}'")
                    print(f"  新: plant_name='{genus_name}', plant_family='{family_name}'")
                    
                    row['plant_name'] = genus_name
                    row['plant_family'] = family_name
                    fix_count += 1
            
            new_data.append(row)
    
    print(f"\\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  総エントリ数: {len(new_data)}件")
    
    # 修正されたデータを保存
    if fix_count > 0:
        with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
            if new_data:
                writer = csv.DictWriter(file, fieldnames=new_data[0].keys())
                writer.writeheader()
                writer.writerows(new_data)
        
        # normalized_dataフォルダにもコピー
        import shutil
        src = hostplants_file
        dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
        if os.path.exists(os.path.dirname(dst)):
            shutil.copy2(src, dst)
        
        print("hostplants.csvを更新しました")
        
        # 検証
        print(f"\\n=== 検証 ===")
        
        # 残存する「科の」パターンをチェック
        remaining_issues = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_name = row['plant_name']
                if re.search(r'科の[^，、]+', plant_name):
                    remaining_issues.append(plant_name[:50])
        
        if remaining_issues:
            print(f"残存する「科の」パターン ({len(remaining_issues)}件):")
            for issue in remaining_issues[:5]:
                print(f"  '{issue}...'")
        else:
            print("✅ 「科の」パターンが全て修正されました")
        
        # 修正された例の確認
        fixed_examples = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_family'] and '科' in row['plant_family']:
                    if row['plant_name'] not in ['不明', '']:
                        fixed_examples.append(f"{row['plant_name']} ({row['plant_family']})")
        
        print(f"\\n修正された例:")
        for example in fixed_examples[:5]:
            print(f"  {example}")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_family_plant_patterns()