#!/usr/bin/env python3
import csv
import re
import os

def fix_plant_part_separation():
    """植物名と部位の分離を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 植物名と部位の分離修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    # 修正パターンを定義
    patterns = [
        {
            'original': 'ミヤマキリシマの葉・花',
            'plant_name': 'ミヤマキリシマ',
            'plant_parts': ['葉', '花']
        },
        {
            'original': 'ガガイモの花蕾・葉', 
            'plant_name': 'ガガイモ',
            'plant_parts': ['花蕾', '葉']
        },
        {
            'original': 'ガマズミの花・蕾',
            'plant_name': 'ガマズミ',
            'plant_parts': ['花', '蕾']
        },
        {
            'original': 'ヤマツツジの葉・花',
            'plant_name': 'ヤマツツジ',
            'plant_parts': ['葉', '花']
        },
        {
            'original': 'ブナの葉・種子',
            'plant_name': 'ブナ',
            'plant_parts': ['葉', '種子']
        }
    ]
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # パターンマッチングをチェック
            pattern_found = None
            for pattern in patterns:
                if plant_name == pattern['original']:
                    pattern_found = pattern
                    break
            
            if pattern_found:
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: {plant_name}")
                print(f"  新: {pattern_found['plant_name']} (部位: {', '.join(pattern_found['plant_parts'])})")
                
                # 最初の部位で元のエントリを更新
                first_row = row.copy()
                first_row['plant_name'] = pattern_found['plant_name']
                first_row['plant_part'] = pattern_found['plant_parts'][0]
                new_data.append(first_row)
                
                # 追加の部位で新しいエントリを作成
                for i, part in enumerate(pattern_found['plant_parts'][1:], 1):
                    new_row = row.copy()
                    new_row['plant_name'] = pattern_found['plant_name']
                    new_row['plant_part'] = part
                    new_row['record_id'] = f"{row['record_id']}-part{i+1}"
                    new_data.append(new_row)
                
                fix_count += 1
            else:
                # 通常のエントリはそのまま追加
                new_data.append(row)
    
    print(f"\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  新しい総エントリ数: {len(new_data)}件")
    print(f"  増加したエントリ数: {len(new_data) - 4498}件")
    
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
        miyama_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == 'ミヤマキリシマ':
                    miyama_entries.append(f"部位: {row['plant_part']}")
        
        if miyama_entries:
            print("ミヤマキリシマの修正例:")
            for entry in miyama_entries:
                print(f"  {entry}")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_plant_part_separation()