#!/usr/bin/env python3
import csv
import re
import os

def fix_invalid_hostplant_names():
    """不適切な食草名を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 不適切な食草名の修正開始 ===")
    
    # hostplants.csvを読み込み
    hostplants_file = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    fixed_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            plant_name = row['plant_name']
            original_name = plant_name
            
            # パターン1: "1852)不明" -> "不明"に修正
            if re.match(r'^\d{4}\)不明$', plant_name):
                row['plant_name'] = '不明'
                fix_count += 1
                print(f"修正: {original_name} → {row['plant_name']}")
            
            # パターン2: "1852)その他の文字列" -> "その他の文字列"に修正  
            elif re.match(r'^\d{4}\)(.+)$', plant_name):
                match = re.match(r'^\d{4}\)(.+)$', plant_name)
                if match:
                    row['plant_name'] = match.group(1)
                    fix_count += 1
                    print(f"修正: {original_name} → {row['plant_name']}")
            
            # その他の問題のある文字列をチェック
            # パターン3: 学名らしき文字列が含まれている場合
            elif re.search(r'\([A-Z][a-z]+\)', plant_name):
                print(f"要確認: {plant_name} (学名らしき文字列が含まれています)")
            
            # パターン4: 数字で始まる異常な植物名
            elif re.match(r'^\d+', plant_name) and plant_name != '不明':
                print(f"要確認: {plant_name} (数字で始まっています)")
            
            fixed_data.append(row)
    
    # 修正されたデータを保存
    if fix_count > 0:
        with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
            if fixed_data:
                writer = csv.DictWriter(file, fieldnames=fixed_data[0].keys())
                writer.writeheader()
                writer.writerows(fixed_data)
        
        # publicフォルダにもコピー
        import shutil
        src = hostplants_file
        dst = os.path.join(base_dir, 'public', 'hostplants.csv')
        shutil.copy2(src, dst)
        
        print(f"\n=== 修正完了 ===")
        print(f"修正件数: {fix_count}件")
        print("hostplants.csvを更新しました")
    else:
        print("修正対象が見つかりませんでした")
    
    # 修正後の検証
    print("\n=== 修正後の検証 ===")
    problematic_count = 0
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            plant_name = row['plant_name']
            if re.match(r'^\d{4}\)', plant_name):
                problematic_count += 1
                print(f"残存問題: {plant_name}")
    
    if problematic_count == 0:
        print("✅ 年号パターンの問題は全て修正されました")
    else:
        print(f"⚠️  {problematic_count}件の問題が残っています")

if __name__ == "__main__":
    fix_invalid_hostplant_names()