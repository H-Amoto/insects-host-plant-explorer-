#!/usr/bin/env python3
import csv
import re
import os

def fix_scientific_name_as_plant():
    """学名が食草名になっているケースを修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 学名が食草名になっているケースの修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    rows_to_skip = set()
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    
    i = 0
    while i < len(rows):
        row = rows[i]
        
        if i in rows_to_skip:
            i += 1
            continue
        
        plant_name = row['plant_name']
        notes = row.get('notes', '')
        
        # パターン1: Opogona thiadelpha Meyrick
        if plant_name == "Opogona thiadelpha Meyrick":
            print(f"修正: 行{i+2} {row['insect_id']}")
            print(f"  元: 食草名='{plant_name}', 備考='{notes}'")
            
            # 備考欄の植物リストを分割
            plants = [p.strip() for p in notes.split(';')]
            print(f"  新: {len(plants)}個のエントリに分割: {plants}")
            
            for j, individual_plant in enumerate(plants):
                if individual_plant:  # 空でない場合のみ
                    new_row = row.copy()
                    new_row['plant_name'] = individual_plant
                    new_row['notes'] = ''  # 備考をクリア
                    
                    # record_idを更新
                    if j == 0:
                        new_row['record_id'] = row['record_id']
                    else:
                        new_row['record_id'] = f"{row['record_id']}-{j+1}"
                    
                    new_data.append(new_row)
            
            # 次の「不明」行もスキップ
            if i + 1 < len(rows) and rows[i + 1]['insect_id'] == row['insect_id'] and rows[i + 1]['plant_name'] == '不明':
                rows_to_skip.add(i + 1)
            
            fix_count += 1
        
        # パターン2: Callopistria japonibia Inoue & Sugi
        elif plant_name == "Callopistria japonibia Inoue & Sugi":
            print(f"修正: 行{i+2} {row['insect_id']}")
            print(f"  元: 食草名='{plant_name}', 備考='{notes}'")
            
            # 複雑な植物リストを解析
            # "フモトシダ; イワヒメワラビ(以上コバノイシカグマ科); イノデ; リョウメンシダ (以上オシダ科); タチシノブ; イノモトソウ(以上イノモトソウ科); イシカグマ(コバノイシカグマ科)"
            plants_info = [
                ('フモトシダ', 'コバノイシカグマ科'),
                ('イワヒメワラビ', 'コバノイシカグマ科'),
                ('イノデ', 'オシダ科'),
                ('リョウメンシダ', 'オシダ科'),
                ('タチシノブ', 'イノモトソウ科'),
                ('イノモトソウ', 'イノモトソウ科'),
                ('イシカグマ', 'コバノイシカグマ科')
            ]
            
            print(f"  新: {len(plants_info)}個のエントリに分割")
            
            for j, (plant, family) in enumerate(plants_info):
                new_row = row.copy()
                new_row['plant_name'] = plant
                new_row['plant_family'] = family
                new_row['notes'] = ''
                
                # record_idを更新
                if j == 0:
                    new_row['record_id'] = row['record_id']
                else:
                    new_row['record_id'] = f"{row['record_id']}-{j+1}"
                
                new_data.append(new_row)
            
            # 次の「不明」行もスキップ
            if i + 1 < len(rows) and rows[i + 1]['insect_id'] == row['insect_id'] and rows[i + 1]['plant_name'] == '不明':
                rows_to_skip.add(i + 1)
            
            fix_count += 1
        
        # パターン3: Callopistria rivularis Walker
        elif plant_name == "Callopistria rivularis Walker":
            print(f"修正: 行{i+2} {row['insect_id']}")
            print(f"  元: 食草名='{plant_name}', 備考='{notes}'")
            print(f"  新: 食草名='イシカグマ', 科名='コバノイシカグマ科'")
            
            new_row = row.copy()
            new_row['plant_name'] = 'イシカグマ'
            new_row['plant_family'] = 'コバノイシカグマ科'
            new_row['notes'] = ''
            new_data.append(new_row)
            
            # 次の「不明」行もスキップ
            if i + 1 < len(rows) and rows[i + 1]['insect_id'] == row['insect_id'] and rows[i + 1]['plant_name'] == '不明':
                rows_to_skip.add(i + 1)
            
            fix_count += 1
        
        else:
            new_data.append(row)
        
        i += 1
    
    print(f"\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  スキップしたエントリ: {len(rows_to_skip)}件")
    print(f"  新しい総エントリ数: {len(new_data)}件")
    print(f"  増加したエントリ数: {len(new_data) - len(rows)}件")
    
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
        
        # species-0299の修正確認
        species_0299_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['insect_id'] == 'species-0299':
                    species_0299_entries.append(row['plant_name'])
        
        if species_0299_entries:
            print("species-0299の修正例:")
            for entry in species_0299_entries:
                print(f"  {entry}")
        
        # species-5840の修正確認
        species_5840_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['insect_id'] == 'species-5840':
                    species_5840_entries.append(f"{row['plant_name']} ({row['plant_family']})")
        
        if species_5840_entries:
            print(f"\nspecies-5840の修正例:")
            for entry in species_5840_entries[:5]:
                print(f"  {entry}")
        
        print("\n✅ 学名が食草名になっているケースの修正が完了しました")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_scientific_name_as_plant()