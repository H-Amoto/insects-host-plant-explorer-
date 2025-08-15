#!/usr/bin/env python3
import csv
import re
import os

def fix_geographic_location_patterns():
    """地理的記述パターンを適切に修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 地理的記述パターンの修正開始 ===")
    
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
        insect_id = row['insect_id']
        
        # パターン1: species-4828の「ヨーロッパでは」+ ヤナギラン + タンポポ
        if plant_name == 'ヨーロッパでは' and insect_id == 'species-4828':
            print(f"修正: 行{i+2} species-4828")
            print(f"  元: ヨーロッパでは + ヤナギラン + タンポポ")
            print(f"  新: ヤナギラン、タンポポ (国外、ヨーロッパ)")
            
            # 次の2行をチェック
            if (i + 1 < len(rows) and rows[i + 1]['insect_id'] == insect_id and
                i + 2 < len(rows) and rows[i + 2]['insect_id'] == insect_id):
                
                # ヤナギランのエントリを作成
                yanagiran_row = rows[i + 1].copy()
                yanagiran_row['observation_type'] = '国外'
                yanagiran_row['notes'] = 'ヨーロッパ'
                new_data.append(yanagiran_row)
                
                # タンポポのエントリを作成
                tanpopo_row = rows[i + 2].copy()
                tanpopo_row['observation_type'] = '国外'
                tanpopo_row['notes'] = 'ヨーロッパ'
                new_data.append(tanpopo_row)
                
                # 次の2行をスキップ
                rows_to_skip.add(i + 1)
                rows_to_skip.add(i + 2)
                
                fix_count += 1
                
            i += 1
            continue
        
        # パターン2: species-4565の「台湾では」+ ウラジロエノキ
        elif plant_name == '台湾では' and insect_id == 'species-4565':
            print(f"修正: 行{i+2} species-4565")
            print(f"  元: 台湾では + ウラジロエノキ")
            print(f"  新: ウラジロエノキ (国外、台湾)")
            
            # 次の行をチェック
            if i + 1 < len(rows) and rows[i + 1]['insect_id'] == insect_id:
                # ウラジロエノキのエントリを作成
                urajiro_row = rows[i + 1].copy()
                urajiro_row['observation_type'] = '国外'
                urajiro_row['notes'] = '台湾'
                new_data.append(urajiro_row)
                
                # 次の行をスキップ
                rows_to_skip.add(i + 1)
                
                fix_count += 1
                
            i += 1
            continue
        
        # パターン3: 「ヨーロッパでは[植物名]」形式
        elif re.match(r'^ヨーロッパでは(.+)$', plant_name):
            match = re.match(r'^ヨーロッパでは(.+)$', plant_name)
            plant_base = match.group(1)
            
            print(f"修正: 行{i+2} {insect_id}")
            print(f"  元: '{plant_name}'")
            print(f"  新: '{plant_base}' (国外、ヨーロッパ)")
            
            row['plant_name'] = plant_base
            row['observation_type'] = '国外'
            row['notes'] = 'ヨーロッパ'
            new_data.append(row)
            
            fix_count += 1
            i += 1
            continue
        
        # パターン4: 「台湾では[植物名]」形式
        elif re.match(r'^台湾では(.+)$', plant_name):
            match = re.match(r'^台湾では(.+)$', plant_name)
            plant_base = match.group(1)
            
            print(f"修正: 行{i+2} {insect_id}")
            print(f"  元: '{plant_name}'")
            print(f"  新: '{plant_base}' (国外、台湾)")
            
            row['plant_name'] = plant_base
            row['observation_type'] = '国外'
            row['notes'] = '台湾'
            new_data.append(row)
            
            fix_count += 1
            i += 1
            continue
        
        # パターン5: 「北アメリカでは[植物名]」形式
        elif re.match(r'^北アメリカでは(.+)$', plant_name):
            match = re.match(r'^北アメリカでは(.+)$', plant_name)
            plant_base = match.group(1)
            
            print(f"修正: 行{i+2} {insect_id}")
            print(f"  元: '{plant_name}'")
            print(f"  新: '{plant_base}' (国外、北アメリカ)")
            
            row['plant_name'] = plant_base
            row['observation_type'] = '国外'
            row['notes'] = '北アメリカ'
            new_data.append(row)
            
            fix_count += 1
            i += 1
            continue
        
        # パターン6: 地理的記述が空の場合（連続パターンの残り）
        elif (plant_name in ['ヨーロッパでは', '台湾では', '中国では', '北アメリカでは'] and
              not row['plant_family'] and not row['reference']):
            
            print(f"削除: 行{i+2} {insect_id}")
            print(f"  地理的記述のみの行 '{plant_name}' を削除")
            
            # この行は削除（追加しない）
            fix_count += 1
            i += 1
            continue
        
        # その他の地理的記述パターン
        elif any(geo in plant_name for geo in ['ヨーロッパでは', '中国では', 'インドでは', '台湾では']):
            # 既に備考に移動済みの可能性が高いのでそのまま
            new_data.append(row)
        
        else:
            new_data.append(row)
        
        i += 1
    
    print(f"\\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  スキップしたエントリ: {len(rows_to_skip)}件")
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
        
        # species-4828の修正確認
        species_4828_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['insect_id'] == 'species-4828' and row['observation_type'] == '国外':
                    species_4828_entries.append(f"{row['plant_name']} ({row['plant_family']}) - {row['notes']}")
        
        if species_4828_entries:
            print("species-4828の修正例:")
            for entry in species_4828_entries:
                print(f"  {entry}")
        
        # 国外記録の確認
        foreign_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['observation_type'] == '国外' and row['notes'] in ['ヨーロッパ', '台湾', '北アメリカ']:
                    foreign_entries.append(f"{row['plant_name']} - {row['notes']}")
        
        if foreign_entries:
            print(f"\\n国外記録の例 ({len(foreign_entries)}件):")
            for entry in list(set(foreign_entries))[:5]:
                print(f"  {entry}")
        
        # 残存する地理的記述パターンをチェック
        remaining_geo = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if any(geo in row['plant_name'] for geo in ['ヨーロッパでは', '台湾では', '中国では', '北アメリカでは']):
                    remaining_geo.append(row['plant_name'])
        
        if remaining_geo:
            print(f"\\n残存する地理的記述パターン:")
            for pattern in list(set(remaining_geo))[:3]:
                print(f"  '{pattern}'")
        else:
            print("\\n✅ 地理的記述パターンの修正が完了しました")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_geographic_location_patterns()