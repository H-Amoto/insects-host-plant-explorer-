#!/usr/bin/env python3
import csv
import re
import os

def fix_final_issues():
    """最終的な残り問題を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 最終問題の修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    fixed_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            notes = row['notes']
            original_name = plant_name
            
            # 個別の問題ケースを修正
            
            # 1. 「ツリガネタケのついているブナ」→ 「ツリガネタケ」
            if plant_name == 'ツリガネタケのついているブナ':
                row['plant_name'] = 'ツリガネタケ'
                row['notes'] = f"{notes} ブナに付着".strip()
                fix_count += 1
                print(f"修正 (ツリガネタケ): 行{row_num} → 食草:ツリガネタケ")
            
            # 2. 「シイタケ栽培の害虫。幼虫は梢木と子実体を食する」→ 「シイタケ」
            elif '栽培の害虫' in plant_name and '幼虫は' in plant_name:
                match = re.match(r'^([^栽]+)栽培の害虫', plant_name)
                if match:
                    actual_plant = match.group(1).strip()
                    row['plant_name'] = actual_plant
                    row['notes'] = f"{notes} {plant_name}".strip()
                    fix_count += 1
                    print(f"修正 (栽培害虫): 行{row_num} → 食草:{actual_plant}")
            
            # 3. その他の長い説明文
            elif len(plant_name) > 50:
                # 動物性食物のケース
                if any(keyword in plant_name for keyword in ['またその加工品', '毛織物', 'ペレット']):
                    if 'またその加工品' in plant_name:
                        row['plant_name'] = '動物性食物'
                    elif '毛織物' in plant_name:
                        row['plant_name'] = '毛織物'
                    elif 'ペレット' in plant_name:
                        row['plant_name'] = 'ペレット'
                    
                    row['notes'] = f"{notes} {original_name}".strip()
                    fix_count += 1
                    print(f"修正 (動物性): 行{row_num} → 食草:{row['plant_name']}")
                
                # 地衣類のケース
                elif '地衣類' in plant_name:
                    row['plant_name'] = '地衣類'
                    row['notes'] = f"{notes} {original_name}".strip()
                    fix_count += 1
                    print(f"修正 (地衣類): 行{row_num} → 食草:地衣類")
                
                # 複合的な食物のケース
                elif '草本類' in plant_name:
                    row['plant_name'] = '草本類'
                    row['notes'] = f"{notes} {original_name}".strip()
                    fix_count += 1
                    print(f"修正 (草本類): 行{row_num} → 食草:草本類")
                
                # その他の長い説明
                elif '。' in plant_name or '、' in plant_name:
                    # 最初の有用な名詞を抽出を試行
                    words = re.findall(r'[ァ-ヴ]+|[ぁ-ん]+|[一-龯]+', plant_name)
                    if words:
                        # 一般的でない長い単語を探す
                        meaningful_word = None
                        for word in words:
                            if len(word) >= 3 and word not in ['ヨーロッパ', 'フクロウ', 'ハト', 'モグラ', 'オオタカ', 'ネズミ']:
                                meaningful_word = word
                                break
                        
                        if meaningful_word:
                            row['plant_name'] = meaningful_word
                            row['notes'] = f"{notes} {original_name}".strip()
                            fix_count += 1
                            print(f"修正 (抽出): 行{row_num} → 食草:{meaningful_word}")
                        else:
                            # 抽出できない場合は「不明」
                            row['plant_name'] = '不明'
                            row['notes'] = f"{notes} {original_name}".strip()
                            fix_count += 1
                            print(f"修正 (不明): 行{row_num} → 食草:不明")
            
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
        
        # 最終確認
        print(f"\n=== 最終確認 ===")
        long_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if len(row['plant_name']) > 30:
                    long_entries.append(row['plant_name'])
        
        if long_entries:
            print(f"残存する長いエントリ ({len(long_entries)}件):")
            for entry in long_entries[:5]:
                print(f"  {entry}")
        else:
            print("✅ 長い説明文は全て修正されました")
    
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_final_issues()