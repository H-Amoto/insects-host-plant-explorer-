#!/usr/bin/env python3
import csv
import os
import shutil
import re

def fix_winter_moth_plant_parts():
    """冬尺蛾データの植物部位を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 冬尺蛾データ植物部位修正 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    hostplants_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if row['reference'] == '日本の冬尺蛾':
                plant_name = row['plant_name']
                plant_part = row['plant_part']
                
                # 「植物名(部位)」パターンを修正
                if '(' in plant_name and ')' in plant_name:
                    # 括弧内の部位を抽出
                    match = re.search(r'\(([^)]+)\)', plant_name)
                    if match:
                        extracted_part = match.group(1)
                        
                        # 部位として有効なものかチェック
                        valid_parts = ['花', '葉', '実', '根', '茎', '花蕾', '新芽', '花・葉', '果実']
                        if any(part in extracted_part for part in valid_parts):
                            clean_plant_name = re.sub(r'\([^)]+\)', '', plant_name).strip()
                            
                            print(f"修正: {plant_name} → 植物名: '{clean_plant_name}', 部位: '{extracted_part}'")
                            
                            row['plant_name'] = clean_plant_name
                            row['plant_part'] = extracted_part
                            fix_count += 1
                        else:
                            # 部位以外の情報（飼育、別名など）の場合は植物名のクリーニングのみ
                            if extracted_part in ['飼育', 'ハコヤナギ', 'シロツメクサ', 'ムラサキツメクサ']:
                                clean_plant_name = re.sub(r'\([^)]+\)', '', plant_name).strip()
                                
                                print(f"修正: {plant_name} → 植物名: '{clean_plant_name}' ('{extracted_part}'を除去)")
                                
                                row['plant_name'] = clean_plant_name
                                if extracted_part == '飼育':
                                    row['observation_type'] = '飼育記録'
                                fix_count += 1
                
                # 特別なケース: 「クローバー(シロツメクサ)」のような学名併記
                if '(シロツメクサ)' in plant_name:
                    row['plant_name'] = 'シロツメクサ'
                    print(f"修正: {plant_name} → シロツメクサ")
                    fix_count += 1
                elif '(ムラサキツメクサ)' in plant_name:
                    row['plant_name'] = 'ムラサキツメクサ'
                    print(f"修正: {plant_name} → ムラサキツメクサ")
                    fix_count += 1
                elif '(ハコヤナギ)' in plant_name:
                    row['plant_name'] = 'ヤマナラシ'
                    print(f"修正: {plant_name} → ヤマナラシ")
                    fix_count += 1
            
            hostplants_data.append(row)
    
    print(f"\n修正結果: {fix_count}件")
    
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
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['reference'] == '日本の冬尺蛾':
                winter_moth_entries.append(row)
    
    # 部位情報の分析
    part_counts = {}
    for entry in winter_moth_entries:
        part = entry['plant_part'] or '(なし)'
        part_counts[part] = part_counts.get(part, 0) + 1
    
    print("部位別エントリ数:")
    for part, count in sorted(part_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {part}: {count}件")
    
    print(f"\n✅ 冬尺蛾データの植物部位修正が完了しました！")

if __name__ == "__main__":
    fix_winter_moth_plant_parts()