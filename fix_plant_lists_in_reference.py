#!/usr/bin/env python3
import csv
import re
import os

def fix_plant_lists_in_reference():
    """出典欄に植物リストが誤って記載されているケースを修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 出典欄の植物リスト修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    rows_to_modify = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    
    i = 0
    while i < len(rows):
        row = rows[i]
        reference = row.get('reference', '')
        
        # パターン1: species-5840の場合（植物リストが出典欄にある）
        if (row['insect_id'] == 'species-5840' and 
            'フモトシダ; イワヒメワラビ' in reference):
            
            print(f"修正: species-5840の出典欄植物リストを修正")
            print(f"  植物リスト出典: '{reference[:50]}...'")
            print(f"  正しい出典: '日本産蛾類標準図鑑2'")
            
            # すべてのspecies-5840エントリの出典を修正
            j = i
            while j < len(rows) and rows[j]['insect_id'] == 'species-5840':
                rows[j]['reference'] = '日本産蛾類標準図鑑2'
                j += 1
            
            fix_count += 1
            i = j
            continue
        
        # パターン2: species-5844の場合（植物リストが出典欄にあり、食草名が「不明」）
        elif (row['insect_id'] == 'species-5844' and 
              'イシカグマ (コバノイシカグマ科)' in reference):
            
            print(f"修正: species-5844の植物リストを個別エントリに分割")
            print(f"  元: 食草名='不明', 出典='{reference}'")
            
            # 植物リストを解析
            plants_info = [
                ('イシカグマ', 'コバノイシカグマ科'),
                ('ケホシダ', 'ヒメシダ科'),
                ('タマシダ', 'ツルシダ科')
            ]
            
            # 各植物のエントリを作成
            for k, (plant, family) in enumerate(plants_info):
                new_row = row.copy()
                new_row['plant_name'] = plant
                new_row['plant_family'] = family
                new_row['reference'] = '日本産蛾類標準図鑑2'
                
                if k > 0:
                    new_row['record_id'] = f"{row['record_id']}-{k+1}"
                
                new_data.append(new_row)
                print(f"  新エントリ: {plant} ({family})")
            
            fix_count += 1
            i += 1
            continue
        
        new_data.append(row)
        i += 1
    
    print(f"\\n修正結果:")
    print(f"  修正したケース: {fix_count}件")
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
        
        # species-5840の出典確認
        species_5840_refs = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['insect_id'] == 'species-5840':
                    species_5840_refs.append(row['reference'])
        
        if species_5840_refs:
            unique_refs = list(set(species_5840_refs))
            print(f"species-5840の出典確認:")
            for ref in unique_refs:
                print(f"  '{ref}'")
        
        # species-5844の植物確認
        species_5844_plants = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['insect_id'] == 'species-5844':
                    species_5844_plants.append(f"{row['plant_name']} ({row['plant_family']})")
        
        if species_5844_plants:
            print(f"\\nspecies-5844の植物確認:")
            for plant in species_5844_plants:
                print(f"  {plant}")
        
        # 残存する問題パターンをチェック
        remaining_issues = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ref = row.get('reference', '')
                if ('; ' in ref and '科' in ref and 
                    len(ref) > 30 and '日本産蛾類標準図鑑' not in ref):
                    remaining_issues.append(ref[:50])
        
        if remaining_issues:
            print(f"\\n残存する問題パターン:")
            for issue in list(set(remaining_issues))[:3]:
                print(f"  '{issue}...'")
        else:
            print("\\n✅ 出典欄の植物リスト問題の修正が完了しました")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_plant_lists_in_reference()