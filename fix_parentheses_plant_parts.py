#!/usr/bin/env python3
import csv
import re
import os

def fix_parentheses_plant_parts():
    """括弧内の部位情報を適切に分離"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 括弧内部位情報の分離修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    # 部位に関する語彙を定義
    plant_parts = ['皮', '葉', '花', '蕾', '種子', '実', '根', '茎', '枝', '果実', '花蕾', '若葉', '新芽', '樹皮']
    feeding_conditions = ['飼育', '野外', '栽培']
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # 括弧内が部位情報のパターンをチェック
            match = re.match(r'^([^(]+)\(([^)]+)\)(.*)$', plant_name)
            
            if match:
                base_name = match.group(1).strip()
                parentheses_content = match.group(2).strip()
                suffix = match.group(3).strip()
                
                # 括弧内が部位かどうか判定
                is_plant_part = parentheses_content in plant_parts
                is_feeding_condition = parentheses_content in feeding_conditions
                
                # 特定パターンの処理
                if is_plant_part:
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: {plant_name}")
                    print(f"  新: 食草名='{base_name}', 部位='{parentheses_content}'")
                    
                    new_row = row.copy()
                    new_row['plant_name'] = base_name + suffix
                    new_row['plant_part'] = parentheses_content
                    new_data.append(new_row)
                    fix_count += 1
                
                elif is_feeding_condition:
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: {plant_name}")
                    print(f"  新: 食草名='{base_name}', 観察タイプ='{parentheses_content}'")
                    
                    new_row = row.copy()
                    new_row['plant_name'] = base_name + suffix  
                    new_row['observation_type'] = parentheses_content
                    new_data.append(new_row)
                    fix_count += 1
                
                # 複雑なケースの個別処理
                elif plant_name == "セイヨウハコヤナギ(ポプラ) (ヤナギ科)":
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: {plant_name}")
                    print(f"  新: 食草名='セイヨウハコヤナギ', 科名='ヤナギ科'")
                    
                    new_row = row.copy()
                    new_row['plant_name'] = 'セイヨウハコヤナギ'
                    new_row['plant_family'] = 'ヤナギ科'
                    new_data.append(new_row)
                    fix_count += 1
                
                elif plant_name == "オニグルミ (クルミ)":
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: {plant_name}")
                    print(f"  新: 食草名='オニグルミ'")
                    
                    new_row = row.copy()
                    new_row['plant_name'] = 'オニグルミ'
                    new_data.append(new_row)
                    fix_count += 1
                
                elif plant_name == "ミチヤナギ (ニワヤナギ)":
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: {plant_name}")
                    print(f"  新: 食草名='ミチヤナギ'")
                    
                    new_row = row.copy()
                    new_row['plant_name'] = 'ミチヤナギ'
                    new_data.append(new_row)
                    fix_count += 1
                
                elif plant_name == "イジュ (ヒメツバキ) (ツバキ科)":
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: {plant_name}")
                    print(f"  新: 食草名='イジュ', 科名='ツバキ科'")
                    
                    new_row = row.copy()
                    new_row['plant_name'] = 'イジュ'
                    new_row['plant_family'] = 'ツバキ科'
                    new_data.append(new_row)
                    fix_count += 1
                
                elif plant_name == "ウラシマツツジ(別名クマコケモモ)":
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: {plant_name}")
                    print(f"  新: 食草名='ウラシマツツジ'")
                    
                    new_row = row.copy()
                    new_row['plant_name'] = 'ウラシマツツジ'
                    new_data.append(new_row)
                    fix_count += 1
                
                else:
                    # その他は元のまま
                    new_data.append(row)
            else:
                # 括弧がないエントリは元のまま
                new_data.append(row)
    
    print(f"\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
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
        
        # 検証
        print(f"\n=== 検証 ===")
        tunohashi_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == 'ツノハシバミ':
                    tunohashi_entries.append(f"部位: {row['plant_part']}")
        
        if tunohashi_entries:
            print("ツノハシバミの修正例:")
            for entry in tunohashi_entries:
                print(f"  {entry}")
                
        # 残存する括弧付きエントリの確認
        remaining_parentheses = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if '(' in row['plant_name'] and ')' in row['plant_name']:
                    remaining_parentheses.append(row['plant_name'])
        
        if remaining_parentheses:
            print(f"\n残存する括弧付きエントリ ({len(remaining_parentheses)}件):")
            for entry in remaining_parentheses[:10]:
                print(f"  {entry}")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_parentheses_plant_parts()