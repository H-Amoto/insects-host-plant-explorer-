#!/usr/bin/env python3
import csv
import re
import os

def fix_plant_parts_descriptions():
    """植物名から部位と修飾語を適切に分離"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 植物部位と修飾語の分離修正開始 ===")
    
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
        original_plant_name = plant_name
        
        # パターン1: 「アキニレの花と若い果実」
        if plant_name == 'アキニレの花と若い果実':
            print(f"修正: 行{i+2} {row['insect_id']}")
            print(f"  元: '{plant_name}'")
            print(f"  新: 'アキニレ' の '花' と '果実'（若い果実）に分割")
            
            # 1つ目のエントリ: 花
            new_row1 = row.copy()
            new_row1['plant_name'] = 'アキニレ'
            new_row1['plant_part'] = '花'
            new_row1['notes'] = ''
            new_data.append(new_row1)
            
            # 2つ目のエントリ: 果実
            new_row2 = row.copy()
            new_row2['plant_name'] = 'アキニレ'
            new_row2['plant_part'] = '果実'
            new_row2['record_id'] = f"{row['record_id']}-2"
            new_row2['notes'] = '若い果実'
            new_data.append(new_row2)
            
            fix_count += 1
        
        # パターン2: 「クリの葉および雄花」
        elif plant_name == 'クリの葉および雄花':
            print(f"修正: 行{i+2} {row['insect_id']}")
            print(f"  元: '{plant_name}'")
            print(f"  新: 'クリ' の '葉' と '花'に分割")
            
            # 1つ目のエントリ: 葉
            new_row1 = row.copy()
            new_row1['plant_name'] = 'クリ'
            new_row1['plant_part'] = '葉'
            new_row1['notes'] = ''
            new_data.append(new_row1)
            
            # 2つ目のエントリ: 雄花
            new_row2 = row.copy()
            new_row2['plant_name'] = 'クリ'
            new_row2['plant_part'] = '花'
            new_row2['record_id'] = f"{row['record_id']}-2"
            new_row2['notes'] = '雄花'
            new_data.append(new_row2)
            
            fix_count += 1
        
        # パターン3: 「コーラの原料となるヒメコラノキの果実」
        elif plant_name == 'コーラの原料となるヒメコラノキの果実':
            print(f"修正: 行{i+2} {row['insect_id']}")
            print(f"  元: '{plant_name}'")
            print(f"  新: 'ヒメコラノキ' の '果実'、備考: 'コーラの原料となる'")
            
            new_row = row.copy()
            new_row['plant_name'] = 'ヒメコラノキ'
            new_row['plant_part'] = '果実'
            new_row['notes'] = 'コーラの原料となる'
            new_data.append(new_row)
            
            fix_count += 1
        
        # パターン4: 「ツツジ科植物の花につく」
        elif plant_name == 'ツツジ科植物の花につく':
            print(f"修正: 行{i+2} {row['insect_id']}")
            print(f"  元: '{plant_name}'")
            print(f"  新: 'ツツジ科植物' の '花'")
            
            new_row = row.copy()
            new_row['plant_name'] = 'ツツジ科植物'
            new_row['plant_part'] = '花'
            new_row['notes'] = ''
            new_data.append(new_row)
            
            fix_count += 1
        
        # パターン5: 「しばしば若い樹皮をかじる」
        elif plant_name == 'しばしば若い樹皮をかじる':
            print(f"修正: 行{i+2} {row['insect_id']}")
            print(f"  元: '{plant_name}' を前の行の備考に移動")
            
            # 前の行を探して備考を追加
            for j in range(len(new_data)-1, -1, -1):
                if new_data[j]['insect_id'] == row['insect_id']:
                    if new_data[j]['notes']:
                        new_data[j]['notes'] += '; しばしば若い樹皮をかじる'
                    else:
                        new_data[j]['notes'] = 'しばしば若い樹皮をかじる'
                    print(f"  前の行の備考を更新")
                    break
            
            # この行は削除（追加しない）
            rows_to_skip.add(i)
            fix_count += 1
        
        # パターン6: 一般的な「植物名の部位」パターン
        elif re.match(r'^(.+)の(花|葉|果実|実|枝|幹|根|皮|樹皮|茎)$', plant_name):
            match = re.match(r'^(.+)の(花|葉|果実|実|枝|幹|根|皮|樹皮|茎)$', plant_name)
            if match:
                plant_base = match.group(1)
                part = match.group(2)
                
                # 複雑すぎるものはスキップ
                if len(plant_base) <= 20 and '、' not in plant_base and 'など' not in plant_base:
                    print(f"修正: 行{i+2} {row['insect_id']}")
                    print(f"  元: '{plant_name}'")
                    print(f"  新: '{plant_base}' の '{part}'")
                    
                    new_row = row.copy()
                    new_row['plant_name'] = plant_base
                    new_row['plant_part'] = part
                    new_data.append(new_row)
                    
                    fix_count += 1
                else:
                    new_data.append(row)
            else:
                new_data.append(row)
        
        # その他の修飾語つき部位パターン
        elif re.match(r'^(.+)の(若い|古い|新しい|枯れた|乾燥した)(.+)$', plant_name):
            match = re.match(r'^(.+)の(若い|古い|新しい|枯れた|乾燥した)(.+)$', plant_name)
            if match:
                plant_base = match.group(1)
                modifier = match.group(2)
                part = match.group(3)
                
                # 部位として認識できるもののみ
                if part in ['花', '葉', '果実', '実', '枝', '幹', '根', '皮', '樹皮', '茎']:
                    print(f"修正: 行{i+2} {row['insect_id']}")
                    print(f"  元: '{plant_name}'")
                    print(f"  新: '{plant_base}' の '{part}'、備考: '{modifier}{part}'")
                    
                    new_row = row.copy()
                    new_row['plant_name'] = plant_base
                    new_row['plant_part'] = part
                    new_row['notes'] = f'{modifier}{part}'
                    new_data.append(new_row)
                    
                    fix_count += 1
                else:
                    new_data.append(row)
            else:
                new_data.append(row)
        
        else:
            new_data.append(row)
        
        i += 1
    
    print(f"\\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  削除したエントリ: {len(rows_to_skip)}件")
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
        
        # アキニレの修正確認
        akinire_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == 'アキニレ' and row['insect_id'] == 'species-3965':
                    akinire_entries.append(f"{row['plant_part']} - 備考: {row['notes']}")
        
        if akinire_entries:
            print("アキニレの修正例:")
            for entry in akinire_entries:
                print(f"  {entry}")
        
        # クリの修正確認
        kuri_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == 'クリ' and row['insect_id'] == 'species-3965':
                    kuri_entries.append(f"{row['plant_part']} - 備考: {row['notes']}")
        
        if kuri_entries:
            print("\\nクリの修正例:")
            for entry in kuri_entries:
                print(f"  {entry}")
        
        print("\\n✅ 植物部位と修飾語の分離修正が完了しました")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_plant_parts_descriptions()