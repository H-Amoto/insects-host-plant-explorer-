#!/usr/bin/env python3
import csv
import os
import shutil
import re

def fix_winter_moth_year_plant_names():
    """冬尺蛾データの年号が食草名になっているレコードを削除"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 冬尺蛾データ年号食草名修正 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # 年号パターンを定義
    year_patterns = [
        r'^\d{4}\)$',  # 年号+括弧閉じ (例: 1929))
        r'^\d{4}$',    # 年号のみ (例: 1935)
        r'^\(\w+,?\s*\d{4}\)$',  # 括弧内著者+年号 (例: (Prout, 1929))
        r'^\w+,?\s*\d{4}$'  # 著者+年号 (例: Wehrli, 1935)
    ]
    
    hostplants_data = []
    deleted_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            should_delete = False
            
            # 冬尺蛾データかつ植物名が年号パターンにマッチする場合
            if row['reference'] == '日本の冬尺蛾':
                plant_name = row['plant_name'].strip()
                
                # 年号パターンをチェック
                for pattern in year_patterns:
                    if re.match(pattern, plant_name):
                        print(f"削除: {row['record_id']} - 植物名: '{plant_name}' (昆虫ID: {row['insect_id']})")
                        should_delete = True
                        deleted_count += 1
                        break
                
                # 特定の問題のある年号も直接チェック
                problematic_years = ['1911', '1929', '1935', '1927', '1878', '1861', '1872', '1896', 
                                   '1894', '1989', '1995', '1944', '1881', '1954', '1987', '1992', 
                                   '1974', '1879', '1891', '1955', '1908', '1982', '1897', '1933',
                                   '1911)', '1929)', '1927)', '1878)', '1861)', '1872)', '1896)',
                                   '1894)', '1989)', '1995)', '1944)', '1881)', '1954)', '1987)',
                                   '1992)', '1974)', '1879)', '1891)', '1955)', '1908)', '1982)',
                                   '1897)', '1933)']
                
                if plant_name in problematic_years:
                    print(f"削除: {row['record_id']} - 問題のある年号: '{plant_name}' (昆虫ID: {row['insect_id']})")
                    should_delete = True
                    deleted_count += 1
            
            if not should_delete:
                hostplants_data.append(row)
    
    print(f"\n削除結果: {deleted_count}件")
    
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
    
    # 修正結果の検証
    print(f"\n=== 修正結果検証 ===")
    
    winter_moth_entries = []
    remaining_problematic = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['reference'] == '日本の冬尺蛾':
                winter_moth_entries.append(row)
                
                plant_name = row['plant_name']
                # 年号パターンが残っているかチェック
                if (plant_name.isdigit() or 
                    re.match(r'^\d{4}\)?$', plant_name) or
                    any(year in plant_name for year in problematic_years)):
                    remaining_problematic.append(plant_name)
    
    print(f"修正後の冬尺蛾レコード数: {len(winter_moth_entries)}件")
    print(f"残存する問題のある食草名: {len(remaining_problematic)}件")
    
    if remaining_problematic:
        print("残存問題:")
        for name in remaining_problematic[:5]:
            print(f"  {name}")
    
    # 総レコード数の確認
    total_records = len(hostplants_data)
    print(f"\nhostplants.csv総レコード数: {total_records:,}件")
    
    print(f"\n✅ 冬尺蛾データの年号食草名修正が完了しました！")

if __name__ == "__main__":
    fix_winter_moth_year_plant_names()