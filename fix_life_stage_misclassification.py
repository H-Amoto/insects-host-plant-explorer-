#!/usr/bin/env python3
import csv
import re
import os

def fix_life_stage_misclassification():
    """ライフステージ情報の誤分類を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== ライフステージ情報の誤分類修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    fixed_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            life_stage = row['life_stage']
            notes = row['notes']
            original_name = plant_name
            
            # パターン1: 「幼虫は植物名」→ 食草名「植物名」、ライフステージ「幼虫」
            match = re.match(r'^幼虫は(.+)$', plant_name)
            if match:
                actual_plant_name = match.group(1).strip()
                row['plant_name'] = actual_plant_name
                row['life_stage'] = '幼虫'
                fix_count += 1
                print(f"修正 (幼虫は): 行{row_num} {original_name} → 食草:{actual_plant_name}, ステージ:幼虫")
            
            # パターン2: 「成虫は植物名」→ 食草名「植物名」、ライフステージ「成虫」
            elif re.match(r'^成虫は(.+)$', plant_name):
                match = re.match(r'^成虫は(.+)$', plant_name)
                actual_plant_name = match.group(1).strip()
                row['plant_name'] = actual_plant_name
                row['life_stage'] = '成虫'
                fix_count += 1
                print(f"修正 (成虫は): 行{row_num} {original_name} → 食草:{actual_plant_name}, ステージ:成虫")
            
            # パターン3: 「蛹は植物名」→ 食草名「植物名」、ライフステージ「蛹」
            elif re.match(r'^蛹は(.+)$', plant_name):
                match = re.match(r'^蛹は(.+)$', plant_name)
                actual_plant_name = match.group(1).strip()
                row['plant_name'] = actual_plant_name
                row['life_stage'] = '蛹'
                fix_count += 1
                print(f"修正 (蛹は): 行{row_num} {original_name} → 食草:{actual_plant_name}, ステージ:蛹")
            
            # パターン4: 「若齢幼虫は植物名」→ 食草名「植物名」、ライフステージ「若齢幼虫」
            elif re.match(r'^若齢幼虫は(.+)$', plant_name):
                match = re.match(r'^若齢幼虫は(.+)$', plant_name)
                actual_plant_name = match.group(1).strip()
                row['plant_name'] = actual_plant_name
                row['life_stage'] = '若齢幼虫'
                fix_count += 1
                print(f"修正 (若齢幼虫は): 行{row_num} {original_name} → 食草:{actual_plant_name}, ステージ:若齢幼虫")
            
            # パターン5: 長い説明文で始まるもの → 備考に移動、適切な食草名を抽出
            elif len(plant_name) > 50 and ('。' in plant_name or '、' in plant_name):
                # 説明文から食草名を抽出する場合
                if '栽培の害虫' in plant_name and '幼虫は' in plant_name:
                    # 「シイタケ栽培の害虫。幼虫は梢木と子実体を食する」パターン
                    match = re.search(r'([^。、]+)栽培の害虫', plant_name)
                    if match:
                        actual_plant_name = match.group(1).strip()
                        row['plant_name'] = actual_plant_name
                        row['notes'] = f"{notes} {plant_name}".strip()
                        fix_count += 1
                        print(f"修正 (栽培害虫): 行{row_num} {original_name[:30]}... → 食草:{actual_plant_name}")
                
                elif 'のついている' in plant_name:
                    # 「ツリガネタケのついているブナ」パターン
                    match = re.search(r'([^の]+)のついている([^。、]+)', plant_name)
                    if match:
                        fungus_name = match.group(1).strip()
                        tree_name = match.group(2).strip()
                        # この場合は真菌が主な食物
                        row['plant_name'] = fungus_name
                        row['notes'] = f"{notes} {tree_name}に生息".strip()
                        fix_count += 1
                        print(f"修正 (ついている): 行{row_num} {original_name[:30]}... → 食草:{fungus_name}")
                
                elif '発見されていない' in plant_name:
                    # 「幼虫は発見されていないが」パターン
                    row['plant_name'] = '不明'
                    row['notes'] = f"{notes} {plant_name}".strip()
                    fix_count += 1
                    print(f"修正 (発見されていない): 行{row_num} → 食草:不明")
                
                elif 'やがて' in plant_name and '落下' in plant_name:
                    # 「幼虫はやがて雄花とともに地面へ落下し」パターン
                    row['plant_name'] = '雄花'
                    row['notes'] = f"{notes} {plant_name}".strip()
                    fix_count += 1
                    print(f"修正 (落下): 行{row_num} → 食草:雄花")
                
                elif '飼育によって確かめられている' in plant_name:
                    # 「幼虫は飼育によって確かめられているという。」パターン
                    row['plant_name'] = '不明'
                    row['notes'] = f"{notes} {plant_name}".strip()
                    fix_count += 1
                    print(f"修正 (飼育確認): 行{row_num} → 食草:不明")
            
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
                if (plant_name.startswith('幼虫は') or 
                    plant_name.startswith('成虫は') or 
                    len(plant_name) > 30 and '。' in plant_name):
                    remaining_issues.append(plant_name)
        
        if remaining_issues:
            print(f"要確認エントリ ({len(remaining_issues)}件):")
            for issue in remaining_issues[:10]:  # 最大10件表示
                print(f"  {issue}")
            if len(remaining_issues) > 10:
                print(f"  ... (他{len(remaining_issues)-10}件)")
        else:
            print("✅ ライフステージパターンの問題は全て修正されました")
    
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_life_stage_misclassification()