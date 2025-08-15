#!/usr/bin/env python3
import csv
import re
import os

def fix_foreign_records():
    """国外記録の分割されたエントリを統合修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 国外記録の分割エントリ統合修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    skip_next = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    
    i = 0
    while i < len(rows):
        row = rows[i]
        plant_name = row['plant_name']
        
        if i in skip_next:
            i += 1
            continue
        
        # パターン1: 「国外では」+ 次の行が「○○科の記録がある」
        if plant_name == "国外では" and i + 1 < len(rows):
            next_row = rows[i + 1]
            next_plant_name = next_row['plant_name']
            
            # 「○○科の記録がある」パターンをチェック
            family_match = re.match(r'(.+科)の記録がある。?$', next_plant_name)
            
            if family_match and row['insect_id'] == next_row['insect_id']:
                family_name = family_match.group(1)
                
                print(f"統合: 行{i+2}-{i+3} {row['insect_id']}")
                print(f"  元: 「{plant_name}」+「{next_plant_name}」")
                print(f"  新: 食草名='{family_name}', 観察タイプ='国外'")
                
                # 統合されたエントリを作成
                new_row = row.copy()
                new_row['plant_name'] = family_name
                new_row['plant_family'] = family_name
                new_row['observation_type'] = '国外'
                new_data.append(new_row)
                
                skip_next.append(i + 1)
                fix_count += 1
            else:
                new_data.append(row)
        
        # パターン2: 単独の「国外では」エントリ
        elif plant_name == "国外では":
            print(f"削除: 行{i+2} {row['insect_id']} - 単独の「国外では」エントリ")
            # 削除（新しいデータに追加しない）
            fix_count += 1
        
        # パターン3: 「国外では ○○」の形式
        elif plant_name.startswith("国外では "):
            foreign_plant = plant_name.replace("国外では ", "").strip()
            
            print(f"修正: 行{i+2} {row['insect_id']}")
            print(f"  元: {plant_name}")
            print(f"  新: 食草名='{foreign_plant}', 観察タイプ='国外'")
            
            new_row = row.copy()
            new_row['plant_name'] = foreign_plant
            new_row['observation_type'] = '国外'
            new_data.append(new_row)
            fix_count += 1
        
        else:
            new_data.append(row)
        
        i += 1
    
    print(f"\n修正結果:")
    print(f"  統合・修正したエントリ: {fix_count}件")
    print(f"  新しい総エントリ数: {len(new_data)}件")
    print(f"  削減されたエントリ数: {len(rows) - len(new_data)}件")
    
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
        tuyukusa_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == 'ツユクサ科' and row['observation_type'] == '国外':
                    tuyukusa_entries.append(f"{row['insect_id']}: {row['plant_name']} ({row['observation_type']})")
        
        if tuyukusa_entries:
            print("ツユクサ科の国外記録修正例:")
            for entry in tuyukusa_entries:
                print(f"  {entry}")
        
        # 残存する「国外では」エントリをチェック
        remaining_foreign = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if '国外では' in row['plant_name']:
                    remaining_foreign.append(row['plant_name'])
        
        if remaining_foreign:
            print(f"\n残存する国外記録エントリ ({len(remaining_foreign)}件):")
            for entry in remaining_foreign[:5]:
                print(f"  {entry}")
        else:
            print("\n✅ 国外記録エントリの統合が完了しました")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_foreign_records()