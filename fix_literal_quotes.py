#!/usr/bin/env python3
import csv
import os

def fix_literal_quotes():
    """食草名のリテラル引用符を除去"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 食草名のリテラル引用符除去開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            reference = row.get('reference', '')
            original_plant_name = plant_name
            
            # 具体的な修正対象をリストアップ
            quote_fixes = {
                '""ニンジン"': 'ニンジン',
                '""ハマオモト"': 'ハマオモト', 
                '""エゾギク"': 'エゾギク',
                '""スゲ属の一種"': 'スゲ属の一種',
                '""テンキグサク"': 'テンキグサク',
                '""テンキグサ"': 'テンキグサ',
                '""ヨシ"': 'ヨシ',
                '""カヤツリグサ属"': 'カヤツリグサ属',
                '""日本では"': None,  # 削除
                '""野外ではオオバヤナギ"': 'オオバヤナギ',
                '""シナノキ属"': 'シナノキ属',
                '""ハルニレ"': 'ハルニレ',
                '""クスギ"': 'クスギ',
                '""ズミ"': 'ズミ',
                '""シナノキ"': 'シナノキ',
                '""ドロヤナギ"': 'ドロヤナギ',
                '""シラカシ"': 'シラカシ',
                '""リンゴ"': 'リンゴ',
                '""フルグミ"': 'フルグミ',
                '""タマネギ"': 'タマネギ',
                '""コナラ"': 'コナラ'
            }
            
            # 食草名の修正
            if plant_name in quote_fixes:
                new_name = quote_fixes[plant_name]
                if new_name is None:
                    # 削除対象
                    print(f"削除: 行{row_num} {row['insect_id']}")
                    print(f"  地理的記述 '{plant_name}' を削除")
                    fix_count += 1
                    continue  # この行は追加しない
                elif new_name == 'オオバヤナギ':
                    # 特別処理
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: '{plant_name}'")
                    print(f"  新: '{new_name}', 備考: '野外'")
                    
                    row['plant_name'] = new_name
                    row['notes'] = '野外'
                    fix_count += 1
                else:
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: '{plant_name}'")
                    print(f"  新: '{new_name}'")
                    
                    row['plant_name'] = new_name
                    fix_count += 1
            
            # referenceフィールドの修正（"1954""" のような場合）
            elif reference.endswith('""'):
                new_reference = reference[:-2]  # 末尾の2つの引用符を除去
                print(f"修正: 行{row_num} {row['insect_id']} (reference)")
                print(f"  元: reference='{reference}'")
                print(f"  新: reference='{new_reference}'")
                
                row['reference'] = new_reference
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
                if row['plant_name'] == 'スゲ属の一種':
                    suge_entries.append(f"{row['insect_id']}: {row['plant_name']}")
        
        if suge_entries:
            print("スゲ属の修正確認:")
            for entry in suge_entries:
                print(f"  {entry}")
        
        # 修正された他の植物名
        fixed_plants = ['ニンジン', 'ハマオモト', 'エゾギク', 'ヨシ', 'カヤツリグサ属']
        confirmed_fixes = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] in fixed_plants:
                    confirmed_fixes.append(row['plant_name'])
        
        if confirmed_fixes:
            print(f"\\n修正された植物名の例:")
            for entry in list(set(confirmed_fixes))[:5]:
                print(f"  '{entry}'")
        
        # 残存する引用符をチェック
        remaining_quotes = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if '""' in row['plant_name']:
                    remaining_quotes.append(row['plant_name'])
        
        if remaining_quotes:
            print(f"\\n残存する引用符を含む食草名:")
            for entry in remaining_quotes:
                print(f"  '{entry}'")
        else:
            print("\\n✅ 不要な引用符の除去が完了しました")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_literal_quotes()