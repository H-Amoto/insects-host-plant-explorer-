#!/usr/bin/env python3
import csv
import os

def fix_remaining_parentheses():
    """植物名の不要な括弧を除去"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 植物名の不要な括弧除去開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            original_name = plant_name
            
            # パターン1: 末尾の「）」のみを除去
            if plant_name.endswith('）') and '（' not in plant_name:
                plant_name = plant_name[:-1]  # 末尾の「）」を除去
                print(f"修正: 行{row_num}")
                print(f"  元: '{original_name}'")
                print(f"  新: '{plant_name}'")
                row['plant_name'] = plant_name
                fix_count += 1
            
            # パターン2: 開き括弧がないのに閉じ括弧がある場合
            elif '）' in plant_name and '（' not in plant_name:
                plant_name = plant_name.replace('）', '')
                print(f"修正: 行{row_num}")
                print(f"  元: '{original_name}'")
                print(f"  新: '{plant_name}'")
                row['plant_name'] = plant_name
                fix_count += 1
            
            # パターン3: 「（」で始まって「）」で終わらない場合（開き括弧のみ）
            elif plant_name.startswith('（') and not plant_name.endswith('）'):
                plant_name = plant_name[1:]  # 先頭の「（」を除去
                print(f"修正: 行{row_num}")
                print(f"  元: '{original_name}'")
                print(f"  新: '{plant_name}'")
                row['plant_name'] = plant_name
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
        
        # 残存する括弧問題をチェック
        remaining_issues = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_name = row['plant_name']
                
                # 問題のあるパターンをチェック
                if (plant_name.endswith('）') and '（' not in plant_name) or \
                   (plant_name.startswith('（') and not plant_name.endswith('）')) or \
                   ('）' in plant_name and '（' not in plant_name):
                    remaining_issues.append(plant_name)
        
        if remaining_issues:
            print(f"残存する括弧問題 ({len(remaining_issues)}件):")
            for issue in remaining_issues[:5]:
                print(f"  '{issue}'")
        else:
            print("✅ 植物名の括弧問題が全て修正されました")
        
        # 正常な括弧のペアをチェック
        normal_parentheses = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_name = row['plant_name']
                if '（' in plant_name and '）' in plant_name:
                    normal_parentheses.append(plant_name)
        
        print(f"\\n正常な括弧ペアの例 ({len(normal_parentheses)}件):")
        for example in normal_parentheses[:3]:
            print(f"  '{example}'")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_remaining_parentheses()