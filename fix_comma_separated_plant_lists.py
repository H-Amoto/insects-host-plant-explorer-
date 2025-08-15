#!/usr/bin/env python3
import csv
import re
import os

def fix_comma_separated_plant_lists():
    """カンマ区切りの植物名リストを個別エントリに分割"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== カンマ区切り植物名リストの分割修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # 特定のパターンを個別に処理
            if plant_name == "ハナウド、ニンジンなど":
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: {plant_name}")
                
                plants = ["ハナウド", "ニンジン"]
                print(f"  新: {len(plants)}個のエントリに分割: {plants}")
                
                for i, individual_plant in enumerate(plants):
                    new_row = row.copy()
                    new_row['plant_name'] = individual_plant
                    
                    # record_idを更新
                    if i == 0:
                        new_row['record_id'] = row['record_id']
                    else:
                        new_row['record_id'] = f"{row['record_id']}-{i+1}"
                    
                    new_data.append(new_row)
                
                fix_count += 1
                
            elif plant_name == "ヤマザクラなどサクラ属、ナナカマド、アズキナシ、ズミ":
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: {plant_name}")
                
                # 複雑なパターンを解析
                plants = ["サクラ属", "ナナカマド", "アズキナシ", "ズミ"]
                print(f"  新: {len(plants)}個のエントリに分割: {plants}")
                print(f"    注: 'ヤマザクラなどサクラ属'は'サクラ属'として統合")
                
                for i, individual_plant in enumerate(plants):
                    new_row = row.copy()
                    new_row['plant_name'] = individual_plant
                    
                    # record_idを更新
                    if i == 0:
                        new_row['record_id'] = row['record_id']
                    else:
                        new_row['record_id'] = f"{row['record_id']}-{i+1}"
                    
                    new_data.append(new_row)
                
                fix_count += 1
                
            else:
                # 一般的なカンマ区切りパターンをチェック
                if '、' in plant_name and not any(skip_word in plant_name for skip_word in [
                    '科', '類', '属各種', '以上', '野外', '飼育', '栽培', 'など多くの', 'と各種'
                ]):
                    # 単純なカンマ区切りの場合
                    parts = [p.strip() for p in plant_name.split('、')]
                    if len(parts) >= 2 and all(len(p) > 0 and len(p) <= 20 for p in parts):
                        # 日本語植物名のパターンをチェック
                        if all(re.match(r'^[ァ-ヶ一-龯ａ-ｚＡ-Ｚ0-9]+$', part) for part in parts):
                            print(f"修正: 行{row_num} {row['insect_id']}")
                            print(f"  元: {plant_name}")
                            print(f"  新: {len(parts)}個のエントリに分割: {parts}")
                            
                            for i, individual_plant in enumerate(parts):
                                new_row = row.copy()
                                new_row['plant_name'] = individual_plant
                                
                                # record_idを更新
                                if i == 0:
                                    new_row['record_id'] = row['record_id']
                                else:
                                    new_row['record_id'] = f"{row['record_id']}-{i+1}"
                                
                                new_data.append(new_row)
                            
                            fix_count += 1
                        else:
                            new_data.append(row)
                    else:
                        new_data.append(row)
                else:
                    new_data.append(row)
    
    print(f"\n修正結果:")
    print(f"  分割したエントリ: {fix_count}件")
    print(f"  新しい総エントリ数: {len(new_data)}件")
    print(f"  増加したエントリ数: {len(new_data) - 4474}件")
    
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
        
        # ハナウドとニンジンの分割確認
        target_plants = ['ハナウド', 'ニンジン']
        for plant in target_plants:
            entries = []
            with open(hostplants_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['plant_name'] == plant and row['insect_id'] == 'species-2152':
                        entries.append(f"{row['insect_id']}: {row['plant_name']} ({row['plant_family']})")
            
            if entries:
                print(f"{plant}の分割確認:")
                for entry in entries:
                    print(f"  {entry}")
        
        # サクラ属等の分割確認
        sakura_plants = ['サクラ属', 'ナナカマド', 'アズキナシ', 'ズミ']
        sakura_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] in sakura_plants and row['insect_id'] == 'species-2168':
                    sakura_entries.append(f"{row['plant_name']}")
        
        if sakura_entries:
            print(f"\nspecies-2168の分割確認: {', '.join(sakura_entries)}")
        
        # 残存するカンマ区切りエントリをチェック
        remaining_comma = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if '、' in row['plant_name'] and not any(skip in row['plant_name'] for skip in ['科', '以上', '野外']):
                    remaining_comma.append(row['plant_name'])
        
        if remaining_comma:
            print(f"\n残存するカンマ区切りエントリ ({len(remaining_comma)}件):")
            for entry in list(set(remaining_comma))[:5]:
                print(f"  '{entry}'")
        else:
            print("\n✅ カンマ区切り植物名リストの分割が完了しました")
    else:
        print("分割対象が見つかりませんでした")

if __name__ == "__main__":
    fix_comma_separated_plant_lists()