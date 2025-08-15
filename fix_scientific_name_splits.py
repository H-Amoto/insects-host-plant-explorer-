#!/usr/bin/env python3
import csv
import re
import os

def fix_scientific_name_splits():
    """学名の不適切な分割を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 学名の不適切な分割修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    # 修正が必要なパターンを定義
    fix_patterns = {
        'Acronicta strigosa (Denis & Schiffermüller': 'Acronicta strigosa (Denis & Schiffermüller, 1775)',
        'Acronicta jozana (Matsumura': 'Acronicta jozana (Matsumura, 1926)',
        'Acronicta omorii (Matsumura': 'Acronicta omorii (Matsumura, 1926)',
        'Acronicta albistigma (Hampson': 'Acronicta albistigma (Hampson, 1909)',
        'Acronicta subpurpurea (Matsumura': 'Acronicta subpurpurea (Matsumura, 1926)',
        'Acronicta sugii (Kinoshita': 'Acronicta sugii (Kinoshita, 1990)'
    }
    
    # 削除すべき年だけのエントリ
    year_only_entries = ['1775)', '1926)', '1909)', '1990)']
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # 年だけのエントリは削除
            if plant_name in year_only_entries:
                print(f"削除: 行{row_num} - {plant_name}")
                continue
            
            # 不完全な学名を修正
            if plant_name in fix_patterns:
                row['plant_name'] = fix_patterns[plant_name]
                print(f"修正: 行{row_num}")
                print(f"  元: {plant_name}")
                print(f"  新: {fix_patterns[plant_name]}")
                fix_count += 1
            
            new_data.append(row)
    
    print(f"\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  新しい総エントリ数: {len(new_data)}件")
    
    # 修正されたデータを保存
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
    
    # 検証 - 修正後の状態確認
    print(f"\n=== 検証 ===")
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        acronicta_entries = []
        for row in reader:
            if 'Acronicta' in row['plant_name']:
                acronicta_entries.append(row['plant_name'])
        
        if acronicta_entries:
            print("修正後のAcronicta学名:")
            for entry in acronicta_entries:
                print(f"  {entry}")
        
        # モミ属・トウヒ属の確認
        momu_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] in ['モミ属', 'トウヒ属']:
                    momu_entries.append(f"{row['insect_id']}: {row['plant_name']}")
        
        if momu_entries:
            print("\nモミ属・トウヒ属の分割確認:")
            for entry in momu_entries:
                print(f"  {entry}")

if __name__ == "__main__":
    fix_scientific_name_splits()