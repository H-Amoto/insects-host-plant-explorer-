#!/usr/bin/env python3
import csv
import os
import shutil

def fix_engyu_mamezoumushi():
    """エンジュマメゾウムシの植物部位を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== エンジュマメゾウムシの植物部位修正 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    hostplants_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            insect_id = row['insect_id']
            plant_name = row['plant_name']
            current_part = row['plant_part']
            
            # エンジュマメゾウムシ (species-H373) の修正
            if insect_id == 'species-H373' and plant_name == 'エンジュ' and current_part == '葉':
                print(f"修正: エンジュマメゾウムシ ({insect_id})")
                print(f"  植物: {plant_name}")
                print(f"  部位: '葉' → '花'")
                print(f"  理由: 元データ「エンジュ、マユミなどの花」に基づく")
                
                row['plant_part'] = '花'
                fix_count += 1
            
            hostplants_data.append(row)
    
    print(f"\\n修正結果: {fix_count}件")
    
    # ファイルを保存
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if hostplants_data:
            writer = csv.DictWriter(file, fieldnames=hostplants_data[0].keys())
            writer.writeheader()
            writer.writerows(hostplants_data)
    
    # normalized_dataフォルダにもコピー
    src = hostplants_file
    dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    print("hostplants.csvを更新しました")
    
    # 検証
    print(f"\\n=== 修正結果検証 ===")
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['insect_id'] == 'species-H373':
                print(f"  {row['plant_name']}: {row['plant_part']}")
    
    print(f"\\n✅ エンジュマメゾウムシの修正が完了しました！")

if __name__ == "__main__":
    fix_engyu_mamezoumushi()