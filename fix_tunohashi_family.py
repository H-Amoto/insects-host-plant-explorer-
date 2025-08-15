#!/usr/bin/env python3
import csv
import re
import os

def fix_tunohashi_family():
    """ツノハシバミの科名修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== ツノハシバミの科名修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # ツノハシバミ(カバノキ科)を修正
            if plant_name == "ツノハシバミ(カバノキ科)":
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: {plant_name}")
                print(f"  新: 食草名='ツノハシバミ', 科名='カバノキ科'")
                
                new_row = row.copy()
                new_row['plant_name'] = 'ツノハシバミ'
                new_row['plant_family'] = 'カバノキ科'
                new_data.append(new_row)
                fix_count += 1
            else:
                new_data.append(row)
    
    print(f"\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    
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
        shutil.copy2(src, dst)
        
        print("hostplants.csvを更新しました")
        
        # 検証
        print(f"\n=== 検証 ===")
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == 'ツノハシバミ' and row['plant_part'] == '皮':
                    print(f"修正確認: {row['insect_id']} - 食草名='{row['plant_name']}', 部位='{row['plant_part']}', 科名='{row['plant_family']}'")
                    break
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_tunohashi_family()