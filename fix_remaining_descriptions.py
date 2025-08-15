#!/usr/bin/env python3
import csv
import re
import os

def fix_remaining_descriptions():
    """残りの説明文を適切に処理"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 残りの説明文の修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    fixed_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            notes = row['notes']
            original_name = plant_name
            
            # 長い説明文で特定のパターン
            if len(plant_name) > 30:
                
                # パターン1: 「ツリガネタケのついているブナ」→ 「ツリガネタケ」
                if 'のついている' in plant_name:
                    match = re.match(r'^([^の]+)のついている(.+)$', plant_name)
                    if match:
                        main_plant = match.group(1).strip()
                        host_plant = match.group(2).strip()
                        row['plant_name'] = main_plant
                        row['notes'] = f"{notes} {host_plant}に付着".strip()
                        fix_count += 1
                        print(f"修正 (ついている): 行{row_num} → 食草:{main_plant}")
                
                # パターン2: 「発見されていないが」→ 「不明」
                elif '発見されていない' in plant_name:
                    row['plant_name'] = '不明'
                    row['notes'] = f"{notes} {plant_name}".strip()
                    fix_count += 1
                    print(f"修正 (発見されていない): 行{row_num} → 食草:不明")
                
                # パターン3: 「多くのツツジ科植物の花につく」→ 「ツツジ科植物の花」
                elif '多くの' in plant_name and 'につく' in plant_name:
                    match = re.search(r'多くの([^の]+の[^に]+)につく', plant_name)
                    if match:
                        actual_plant = match.group(1).strip()
                        row['plant_name'] = actual_plant
                        row['notes'] = f"{notes} 多くの種類".strip()
                        fix_count += 1
                        print(f"修正 (多くの): 行{row_num} → 食草:{actual_plant}")
                
                # パターン4: 「やがて雄花とともに地面へ落下し」→ 「雄花」
                elif 'やがて' in plant_name and '落下' in plant_name:
                    row['plant_name'] = '雄花'
                    row['notes'] = f"{notes} {plant_name}".strip()
                    fix_count += 1
                    print(f"修正 (落下): 行{row_num} → 食草:雄花")
                
                # パターン5: 「飼育によって確かめられているという。」→ 「不明」
                elif '飼育によって確かめられている' in plant_name:
                    row['plant_name'] = '不明'
                    row['notes'] = f"{notes} {plant_name}".strip()
                    fix_count += 1
                    print(f"修正 (飼育確認): 行{row_num} → 食草:不明")
                
                # パターン6: 「しばしば若い樹皮をかじる」→ 「樹皮」
                elif 'しばしば' in plant_name and 'かじる' in plant_name:
                    if '樹皮' in plant_name:
                        row['plant_name'] = '樹皮'
                        row['plant_part'] = '樹皮'
                        row['notes'] = f"{notes} {plant_name}".strip()
                        fix_count += 1
                        print(f"修正 (樹皮): 行{row_num} → 食草:樹皮")
                
                # パターン7: 動物性食物の場合
                elif any(keyword in plant_name for keyword in ['毛織物', 'ペレット', '鰹節', '骨', '肉', 'ケラチン', '卵塊']):
                    # 主要な食物を抽出
                    if '毛織物' in plant_name:
                        row['plant_name'] = '毛織物'
                    elif '鰹節' in plant_name:
                        row['plant_name'] = '鰹節'
                    elif 'ペレット' in plant_name:
                        row['plant_name'] = 'ペレット'
                    elif 'ケラチン' in plant_name:
                        row['plant_name'] = 'ケラチン質'
                    elif '卵塊' in plant_name:
                        row['plant_name'] = '卵塊'
                    else:
                        row['plant_name'] = '動物性食物'
                    
                    row['notes'] = f"{notes} {original_name}".strip()
                    fix_count += 1
                    print(f"修正 (動物性): 行{row_num} → 食草:{row['plant_name']}")
                
                # パターン8: 複合的な食物「草本類も食べる」
                elif '草本類' in plant_name and '食べる' in plant_name:
                    row['plant_name'] = '草本類'
                    row['notes'] = f"{notes} {plant_name}".strip()
                    fix_count += 1
                    print(f"修正 (草本類): 行{row_num} → 食草:草本類")
                
                # パターン9: 地衣類について
                elif '地衣類' in plant_name:
                    row['plant_name'] = '地衣類'
                    row['notes'] = f"{notes} {plant_name}".strip()
                    fix_count += 1
                    print(f"修正 (地衣類): 行{row_num} → 食草:地衣類")
            
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
    
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_remaining_descriptions()