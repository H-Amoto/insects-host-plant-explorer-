#!/usr/bin/env python3
import csv
import re
import os

def fix_specific_etc_genus_patterns():
    """「具体名など属名/科名」パターンを適切に分離"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 「具体名など属名/科名」パターンの分離修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            original_plant_name = plant_name
            
            # パターン1: 「具体名など属名」→ 属名 + 備考「具体名など」
            pattern1 = re.match(r'^(.+)など(.+属)$', plant_name)
            if pattern1:
                specific_name = pattern1.group(1)
                genus_name = pattern1.group(2)
                
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: 食草名='{genus_name}', 備考='{specific_name}など'")
                
                row['plant_name'] = genus_name
                row['notes'] = f"{specific_name}など"
                fix_count += 1
            
            # パターン2: 「具体名などの科名」→ 科名 + 備考「具体名など」
            elif re.match(r'^(.+)などの(.+科)$', plant_name):
                pattern2 = re.match(r'^(.+)などの(.+科)$', plant_name)
                specific_name = pattern2.group(1)
                family_name = pattern2.group(2)
                
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: 食草名='{family_name}', 備考='{specific_name}など'")
                
                row['plant_name'] = family_name
                row['notes'] = f"{specific_name}など"
                fix_count += 1
            
            # パターン3: 「具体名など類」→ 類 + 備考「具体名など」
            elif re.match(r'^(.+)などの(.+類)$', plant_name):
                pattern3 = re.match(r'^(.+)などの(.+類)$', plant_name)
                specific_name = pattern3.group(1)
                category_name = pattern3.group(2)
                
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: 食草名='{category_name}', 備考='{specific_name}など'")
                
                row['plant_name'] = category_name
                row['notes'] = f"{specific_name}など"
                fix_count += 1
            
            # パターン4: 「具体名など」（単純形）
            elif re.match(r'^(.+)など$', plant_name) and not any(skip in plant_name for skip in ['多くの', 'その他', '各種']):
                pattern4 = re.match(r'^(.+)など$', plant_name)
                base_name = pattern4.group(1)
                
                # 複雑すぎるものはスキップ
                if len(base_name) <= 20 and '、' not in base_name:
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: '{plant_name}'")
                    print(f"  新: 食草名='{base_name}', 備考='など'")
                    
                    row['plant_name'] = base_name
                    row['notes'] = 'など'
                    fix_count += 1
            
            # 特殊ケース: ハイビスカス (Hibiscus rosa-sinensis など フヨウ属)
            elif 'Hibiscus rosa-sinensis など フヨウ属' in plant_name:
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: 食草名='フヨウ属', 備考='ハイビスカス (Hibiscus rosa-sinensis など)'")
                
                row['plant_name'] = 'フヨウ属'
                row['notes'] = 'ハイビスカス (Hibiscus rosa-sinensis など)'
                fix_count += 1
            
            new_data.append(row)
    
    print(f"\n修正結果:")
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
        shutil.copy2(src, dst)
        
        print("hostplants.csvを更新しました")
        
        # 検証
        print(f"\n=== 検証 ===")
        
        # マツ属の修正確認
        matsu_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == 'マツ属' and 'アカマツ' in row.get('notes', ''):
                    matsu_entries.append(f"{row['insect_id']}: {row['plant_name']} - 備考: {row['notes']}")
        
        if matsu_entries:
            print("マツ属の修正例:")
            for entry in matsu_entries:
                print(f"  {entry}")
        
        # その他の属/科修正例
        other_examples = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if ('属' in row['plant_name'] or '科' in row['plant_name'] or '類' in row['plant_name']) and 'など' in row.get('notes', ''):
                    other_examples.append(f"{row['plant_name']} - 備考: {row['notes']}")
        
        if other_examples:
            print(f"\nその他の修正例:")
            for entry in list(set(other_examples))[:5]:
                print(f"  {entry}")
        
        # 残存する「など」パターンをチェック
        remaining_nado = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'など' in row['plant_name'] and not any(skip in row['plant_name'] for skip in ['多くの', 'その他', '各種']):
                    remaining_nado.append(row['plant_name'])
        
        if remaining_nado:
            print(f"\n残存する「など」パターン ({len(remaining_nado)}件):")
            for entry in list(set(remaining_nado))[:5]:
                print(f"  '{entry}'")
        else:
            print("\n✅ 「具体名など属名/科名」パターンの分離が完了しました")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_specific_etc_genus_patterns()