#!/usr/bin/env python3
import csv
import re
import os

def fix_cultivated_plants():
    """「栽培○○」パターンを食草名と備考に分離"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 栽培植物名の分離修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            notes = row.get('notes', '')
            
            # 「栽培○○」パターンをチェック
            cultivated_match = re.match(r'^栽培(.+)$', plant_name)
            
            if cultivated_match:
                base_plant_name = cultivated_match.group(1)
                
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: 食草名='{plant_name}', 備考='{notes}'")
                
                # 既存の備考がある場合は追加、ない場合は新規作成
                if notes and notes.strip():
                    new_notes = f"栽培。{notes}"
                else:
                    new_notes = "栽培"
                
                print(f"  新: 食草名='{base_plant_name}', 備考='{new_notes}'")
                
                row['plant_name'] = base_plant_name
                row['notes'] = new_notes
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
        budou_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == 'ブドウ' and '栽培' in row.get('notes', ''):
                    budou_entries.append(f"{row['insect_id']}: {row['plant_name']} - 備考: {row['notes']}")
        
        if budou_entries:
            print("ブドウの栽培記録修正例:")
            for entry in budou_entries:
                print(f"  {entry}")
        
        # 修正された他の栽培植物の例
        other_cultivated = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if '栽培' in row.get('notes', '') and row['plant_name'] in ['バラ', 'キク']:
                    other_cultivated.append(f"{row['plant_name']} - 備考: {row['notes']}")
        
        if other_cultivated:
            print("\nその他の栽培植物修正例:")
            for entry in list(set(other_cultivated))[:5]:
                print(f"  {entry}")
        
        # 残存する「栽培」を含む植物名をチェック
        remaining_cultivated = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if '栽培' in row['plant_name']:
                    remaining_cultivated.append(row['plant_name'])
        
        if remaining_cultivated:
            print(f"\n残存する「栽培」を含む植物名 ({len(remaining_cultivated)}件):")
            for entry in list(set(remaining_cultivated)):
                print(f"  '{entry}'")
        else:
            print("\n✅ 栽培植物名の分離が完了しました")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_cultivated_plants()