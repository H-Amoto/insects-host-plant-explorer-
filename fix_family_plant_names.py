#!/usr/bin/env python3
import csv
import re
import os

def fix_family_plant_names():
    """科植物、属植物などの植物名を適切に修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 科植物・属植物名の修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            original_plant_name = plant_name
            
            # パターン1: 「ツツジ科植物」→「ツツジ科」
            if plant_name == 'ツツジ科植物':
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: 'ツツジ科'")
                
                row['plant_name'] = 'ツツジ科'
                fix_count += 1
            
            # パターン2: 「他のマツ科植物」→「マツ科」、備考「他の」
            elif plant_name == '他のマツ科植物':
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: 'マツ科'、備考: '他の'")
                
                row['plant_name'] = 'マツ科'
                row['notes'] = '他の'
                fix_count += 1
            
            # パターン3: 「中国ではムクロジ科植物が知られている」→備考に移動
            elif plant_name == '中国ではムクロジ科植物が知られている':
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}' を前の行の備考に移動")
                
                # 前の行を探して備考を追加
                if new_data:
                    last_entry = new_data[-1]
                    if last_entry['insect_id'] == row['insect_id']:
                        if last_entry['notes']:
                            last_entry['notes'] += '; 中国ではムクロジ科植物が知られている'
                        else:
                            last_entry['notes'] = '中国ではムクロジ科植物が知られている'
                        print(f"  前の行の備考を更新")
                        fix_count += 1
                        continue  # この行は追加しない
                
                # 前の行が見つからない場合はそのまま
                new_data.append(row)
                continue
            
            # パターン4: 「ヤナギ科の植物」→「ヤナギ科」
            elif plant_name == 'ヤナギ科の植物':
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: 'ヤナギ科'")
                
                row['plant_name'] = 'ヤナギ科'
                fix_count += 1
            
            # パターン5: 「マメ科など多くの科の植物が記録されている。」→備考に移動
            elif plant_name == 'マメ科など多くの科の植物が記録されている。':
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}' を前の行の備考に移動")
                
                # 前の行を探して備考を追加
                if new_data:
                    last_entry = new_data[-1]
                    if last_entry['insect_id'] == row['insect_id']:
                        if last_entry['notes']:
                            last_entry['notes'] += '; マメ科など多くの科の植物が記録されている'
                        else:
                            last_entry['notes'] = 'マメ科など多くの科の植物が記録されている'
                        print(f"  前の行の備考を更新")
                        fix_count += 1
                        continue  # この行は追加しない
                
                # 前の行が見つからない場合はそのまま
                new_data.append(row)
                continue
            
            # パターン6: 「ときには針葉樹」→「針葉樹」
            elif plant_name == 'ときには針葉樹':
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: '針葉樹'、備考: 'ときには'")
                
                row['plant_name'] = '針葉樹'
                existing_notes = row.get('notes', '')
                if existing_notes:
                    row['notes'] = f"ときには; {existing_notes}"
                else:
                    row['notes'] = 'ときには'
                fix_count += 1
            
            # 一般的なパターン: 「○○科植物」→「○○科」
            elif re.match(r'^(.+科)植物$', plant_name):
                match = re.match(r'^(.+科)植物$', plant_name)
                family_name = match.group(1)
                
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: '{family_name}'")
                
                row['plant_name'] = family_name
                fix_count += 1
            
            # 一般的なパターン: 「○○属植物」→「○○属」
            elif re.match(r'^(.+属)植物$', plant_name):
                match = re.match(r'^(.+属)植物$', plant_name)
                genus_name = match.group(1)
                
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: '{genus_name}'")
                
                row['plant_name'] = genus_name
                fix_count += 1
            
            new_data.append(row)
    
    print(f"\\n修正結果:")
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
        print(f"\\n=== 検証 ===")
        
        # ツツジ科の修正確認
        tsutsuji_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == 'ツツジ科' and row['insect_id'] == 'species-4412':
                    tsutsuji_entries.append(f"部位: {row['plant_part']}")
        
        if tsutsuji_entries:
            print("ツツジ科の修正例:")
            for entry in tsutsuji_entries:
                print(f"  {entry}")
        
        # マツ科の修正確認
        matsu_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == 'マツ科' and row['notes'] == '他の':
                    matsu_entries.append(f"備考: {row['notes']}")
        
        if matsu_entries:
            print("\\nマツ科の修正例:")
            for entry in matsu_entries:
                print(f"  {entry}")
        
        # 修正後の科植物パターンが残っているかチェック
        remaining_patterns = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if '科植物' in row['plant_name'] or '属植物' in row['plant_name']:
                    remaining_patterns.append(row['plant_name'])
        
        if remaining_patterns:
            print(f"\\n残存する「植物」パターン:")
            for pattern in list(set(remaining_patterns))[:3]:
                print(f"  '{pattern}'")
        else:
            print("\\n✅ 「科植物」「属植物」パターンの修正が完了しました")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_family_plant_names()