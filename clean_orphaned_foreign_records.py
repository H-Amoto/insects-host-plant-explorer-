#!/usr/bin/env python3
import csv
import re
import os

def clean_orphaned_foreign_records():
    """孤立した「国外では」エントリを削除"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 孤立した国外記録エントリの削除開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # 孤立した「国外では」エントリを削除
            if plant_name == "国外では":
                print(f"削除: 行{row_num} {row['insect_id']} - 孤立した「国外では」エントリ")
                fix_count += 1
                continue
            
            new_data.append(row)
    
    print(f"\n削除結果:")
    print(f"  削除したエントリ: {fix_count}件")
    print(f"  新しい総エントリ数: {len(new_data)}件")
    
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
        
        # 検証 - 残存する「国外では」エントリをチェック
        print(f"\n=== 検証 ===")
        remaining_foreign = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if '国外では' in row['plant_name']:
                    remaining_foreign.append(row['plant_name'])
        
        if remaining_foreign:
            print(f"残存する国外記録エントリ ({len(remaining_foreign)}件):")
            for entry in remaining_foreign:
                print(f"  {entry}")
        else:
            print("✅ 国外記録エントリの整理が完了しました")
    else:
        print("削除対象が見つかりませんでした")

if __name__ == "__main__":
    clean_orphaned_foreign_records()