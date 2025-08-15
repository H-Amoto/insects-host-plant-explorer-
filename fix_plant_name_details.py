#!/usr/bin/env python3
import csv
import re
import os

def fix_plant_name_details():
    """食草名の詳細情報を適切な列に分離"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 食草名詳細情報の分離開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    fixed_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            plant_family = row['plant_family']
            plant_part = row['plant_part']
            notes = row['notes']
            original_name = plant_name
            
            # パターン1: 「植物名（可能性が高い）」→ 食草名「植物名」、備考「可能性が高い」
            match = re.match(r'^([^（(]+)（([^）)]*可能性[^）)]*)）$', plant_name)
            if match:
                new_plant_name = match.group(1).strip()
                possibility_note = match.group(2).strip()
                row['plant_name'] = new_plant_name
                row['notes'] = f"{notes} {possibility_note}".strip()
                fix_count += 1
                print(f"修正 (可能性): 行{row_num} {original_name} → 食草:{new_plant_name}, 備考:{possibility_note}")
            
            # パターン2: 「植物名（別名）の部位（科名）」→ 食草名「植物名」、科名「科名」、部位「部位」
            elif re.search(r'の(枝|葉|茎|花|実|根|樹皮|果実)', plant_name) and '（' in plant_name:
                # 「セイヨウミザクラ（桜桃）の枝（バラ科）」パターン
                match = re.match(r'^([^（(]+)（[^）)]*）の(枝|葉|茎|花|実|根|樹皮|果実)（([^）)]*科)）$', plant_name)
                if match:
                    new_plant_name = match.group(1).strip()
                    new_plant_part = match.group(2).strip()
                    new_plant_family = match.group(3).strip()
                    
                    row['plant_name'] = new_plant_name
                    row['plant_part'] = new_plant_part
                    if not plant_family:  # 既存の科名がない場合のみ設定
                        row['plant_family'] = new_plant_family
                    
                    fix_count += 1
                    print(f"修正 (部位・科名): 行{row_num} {original_name} → 食草:{new_plant_name}, 部位:{new_plant_part}, 科名:{new_plant_family}")
                
                # 「植物名の部位」パターン（科名なし）
                else:
                    match = re.match(r'^([^の]+)の(枝|葉|茎|花|実|根|樹皮|果実)$', plant_name)
                    if match:
                        new_plant_name = match.group(1).strip()
                        new_plant_part = match.group(2).strip()
                        
                        # 括弧内の情報を除去
                        new_plant_name = re.sub(r'（[^）]*）', '', new_plant_name).strip()
                        
                        row['plant_name'] = new_plant_name
                        row['plant_part'] = new_plant_part
                        
                        fix_count += 1
                        print(f"修正 (部位): 行{row_num} {original_name} → 食草:{new_plant_name}, 部位:{new_plant_part}")
            
            # パターン3: 「植物名（別名）（科名）」→ 食草名「植物名」、科名「科名」
            elif re.match(r'^[^（(]+（[^）)]*）（[^）)]*科）$', plant_name):
                match = re.match(r'^([^（(]+)（[^）)]*）（([^）)]*科)）$', plant_name)
                if match:
                    new_plant_name = match.group(1).strip()
                    new_plant_family = match.group(2).strip()
                    
                    row['plant_name'] = new_plant_name
                    if not plant_family:  # 既存の科名がない場合のみ設定
                        row['plant_family'] = new_plant_family
                    
                    fix_count += 1
                    print(f"修正 (別名・科名): 行{row_num} {original_name} → 食草:{new_plant_name}, 科名:{new_plant_family}")
            
            # パターン4: 「不明 (日本では)」→ 「不明」、備考「日本では」
            elif plant_name == '不明 (日本では)':
                row['plant_name'] = '不明'
                row['notes'] = f"{notes} 日本では".strip()
                fix_count += 1
                print(f"修正 (日本では): 行{row_num} {original_name} → 食草:不明, 備考:日本では")
            
            fixed_data.append(row)
    
    print(f"\n修正結果:")
    print(f"  修正件数: {fix_count}件")
    print(f"  総エントリ: {len(fixed_data)}件")
    
    # 修正されたデータを保存
    if fix_count > 0:
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
        
        # 検証 - 残存する問題のあるパターンをチェック
        print(f"\n=== 検証 ===")
        remaining_issues = []
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_name = row['plant_name']
                
                # まだ問題がありそうなパターンをチェック
                if '（' in plant_name and ('可能性' in plant_name or 'の枝' in plant_name or 'の葉' in plant_name):
                    remaining_issues.append(plant_name)
        
        if remaining_issues:
            print(f"要確認エントリ ({len(remaining_issues)}件):")
            for issue in remaining_issues[:10]:  # 最大10件表示
                print(f"  {issue}")
            if len(remaining_issues) > 10:
                print(f"  ... (他{len(remaining_issues)-10}件)")
        else:
            print("✅ 類似パターンの問題は全て修正されました")
    
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_plant_name_details()