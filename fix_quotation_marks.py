#!/usr/bin/env python3
import csv
import re
import os

def fix_quotation_marks():
    """食草名の不要な引用符を除去"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 食草名の引用符除去開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            reference = row.get('reference', '')
            original_plant_name = plant_name
            
            # パターン1: 三重引用符で囲まれた食草名 (例: """スゲ属の一種")
            if plant_name.startswith('"""') and plant_name.endswith('"'):
                new_name = plant_name[3:-1]  # 最初の3つと最後の1つの引用符を除去
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: '{new_name}'")
                
                row['plant_name'] = new_name
                fix_count += 1
            
            # パターン2: 標準的な引用符で囲まれた食草名 (例: "植物名")
            elif plant_name.startswith('"') and plant_name.endswith('"') and len(plant_name) > 2:
                new_name = plant_name[1:-1]  # 前後の引用符を除去
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: '{new_name}'")
                
                row['plant_name'] = new_name
                fix_count += 1
            
            # パターン3: referenceフィールドに不適切な引用符がある場合
            elif reference.endswith('"""'):
                new_reference = reference[:-3]  # 末尾の三重引用符を除去
                print(f"修正: 行{row_num} {row['insect_id']} (reference)")
                print(f"  元: reference='{reference}'")
                print(f"  新: reference='{new_reference}'")
                
                row['reference'] = new_reference
                fix_count += 1
            
            # パターン4: 不完全な引用符パターン
            elif '"""' in plant_name or '""' in plant_name:
                # 不完全な引用符を除去
                new_name = plant_name.replace('"""', '').replace('""', '')
                if new_name != plant_name:
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: '{plant_name}'")
                    print(f"  新: '{new_name}'")
                    
                    row['plant_name'] = new_name
                    fix_count += 1
            
            # パターン5: 「"日本では"」のような地理的記述
            elif plant_name == '"日本では"':
                print(f"削除: 行{row_num} {row['insect_id']}")
                print(f"  地理的記述 '{plant_name}' を削除")
                fix_count += 1
                continue  # この行は追加しない
            
            # パターン6: 「"野外ではオオバヤナギ"」のような記述から植物名を抽出
            elif plant_name == '"野外ではオオバヤナギ"':
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: 'オオバヤナギ', 備考: '野外'")
                
                row['plant_name'] = 'オオバヤナギ'
                row['notes'] = '野外'
                fix_count += 1
            
            new_data.append(row)
    
    print(f"\\n修正結果:")
    print(f"  修正・削除したエントリ: {fix_count}件")
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
        print(f"\\n=== 検証 ===")
        
        # スゲ属の修正確認
        suge_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'スゲ属' in row['plant_name']:
                    suge_entries.append(row['plant_name'])
        
        if suge_entries:
            print("スゲ属の修正例:")
            for entry in suge_entries:
                print(f"  '{entry}'")
        
        # 残存する引用符をチェック
        remaining_quotes = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if ('"' in row['plant_name'] or 
                    '"""' in row['plant_name'] or
                    row['plant_name'].startswith('"') or 
                    row['plant_name'].endswith('"')):
                    remaining_quotes.append(row['plant_name'])
        
        if remaining_quotes:
            print(f"\\n残存する引用符を含む食草名 ({len(remaining_quotes)}件):")
            for entry in list(set(remaining_quotes))[:5]:
                print(f"  '{entry}'")
        else:
            print("\\n✅ 不要な引用符の除去が完了しました")
        
        # 修正された植物名の例
        fixed_examples = [
            'スゲ属の一種', 'ニンジン', 'ハマオモト', 'エゾギク', 'ヨシ', 
            'カヤツリグサ属', 'シナノキ属', 'ハルニレ', 'ズミ', 'シラカシ'
        ]
        
        valid_examples = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] in fixed_examples:
                    valid_examples.append(row['plant_name'])
        
        if valid_examples:
            print(f"\\n修正された植物名の例:")
            for entry in list(set(valid_examples))[:5]:
                print(f"  '{entry}'")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_quotation_marks()