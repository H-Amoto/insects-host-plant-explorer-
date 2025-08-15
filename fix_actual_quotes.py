#!/usr/bin/env python3
import csv
import os

def fix_actual_quotes():
    """実際の引用符パターンを修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 実際の引用符パターン修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            reference = row.get('reference', '')
            
            # パターン1: "で始まる植物名（前後の引用符を除去）
            if plant_name.startswith('"'):
                new_name = plant_name[1:]  # 最初の"を除去
                
                # 特別処理が必要なケース
                if new_name == '日本では':
                    print(f"削除: 行{row_num} {row['insect_id']}")
                    print(f"  地理的記述 '{plant_name}' を削除")
                    fix_count += 1
                    continue  # この行は追加しない
                elif new_name == '野外ではオオバヤナギ':
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: '{plant_name}'")
                    print(f"  新: 'オオバヤナギ', 備考: '野外'")
                    
                    row['plant_name'] = 'オオバヤナギ'
                    row['notes'] = '野外'
                    fix_count += 1
                else:
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: '{plant_name}'")
                    print(f"  新: '{new_name}'")
                    
                    row['plant_name'] = new_name
                    fix_count += 1
            
            # パターン2: referenceフィールドに不正な引用符（"1954""など）
            elif reference.endswith('""'):
                new_reference = reference.rstrip('"')  # 末尾の"を全て除去
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
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == 'スゲ属の一種':
                    print(f"✅ スゲ属の修正確認: {row['insect_id']}: '{row['plant_name']}'")
                    break
        
        # 修正された他の植物名の例
        fixed_examples = ['ニンジン', 'ハマオモト', 'エゾギク', 'ヨシ', 'カヤツリグサ属']
        found_fixes = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] in fixed_examples:
                    found_fixes.append(row['plant_name'])
        
        if found_fixes:
            print(f"\\n修正された植物名の例:")
            for entry in list(set(found_fixes))[:5]:
                print(f"  '{entry}'")
        
        # 残存する引用符をチェック
        remaining_quotes = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'].startswith('"'):
                    remaining_quotes.append(row['plant_name'])
        
        if remaining_quotes:
            print(f"\\n残存する引用符で始まる植物名:")
            for entry in remaining_quotes:
                print(f"  '{entry}'")
        else:
            print("\\n✅ 不要な引用符の除去が完了しました")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_actual_quotes()