#!/usr/bin/env python3
import csv
import re
import os

def split_comma_separated_plants_v2():
    """カンマ区切りの食草名を個別エントリに分割（修正版）"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== カンマ区切り食草名の分割開始（修正版） ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    split_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # デバッグ: 最初の数行を確認
            if row_num <= 500 and ', ' in plant_name:
                print(f"Debug 行{row_num}: '{plant_name}'")
            
            # 様々なカンマ区切りパターンをチェック
            should_split = False
            
            # パターン1: "植物1, 植物2" (クォート付き)
            if plant_name.startswith('"') and plant_name.endswith('"') and ', ' in plant_name:
                should_split = True
                clean_name = plant_name.strip('"')
            
            # パターン2: 植物1, 植物2 (クォートなし、複数の日本語植物名)
            elif ', ' in plant_name and not any(word in plant_name for word in ['科', '属', '類', '以上', '栽培', '野外']):
                # 日本語植物名のパターンをチェック
                parts = plant_name.split(', ')
                if all(re.match(r'^[ァ-ヶ一-龯]+$', part.strip()) for part in parts if part.strip()):
                    should_split = True
                    clean_name = plant_name
            
            if should_split:
                # カンマで分割
                individual_plants = [name.strip().strip('"') for name in clean_name.split(',')]
                
                print(f"分割: 行{row_num} {row['insect_id']} → {len(individual_plants)}個の食草")
                print(f"  元: {plant_name}")
                print(f"  分割後: {individual_plants}")
                
                # 各植物名に対して個別エントリを作成
                for i, individual_plant in enumerate(individual_plants):
                    if individual_plant:  # 空でない場合のみ
                        new_row = row.copy()
                        new_row['plant_name'] = individual_plant
                        
                        # record_idを更新
                        if i == 0:
                            new_row['record_id'] = row['record_id']
                        else:
                            new_row['record_id'] = f"{row['record_id']}-{i+1}"
                        
                        new_data.append(new_row)
                
                split_count += 1
            else:
                # 通常のエントリはそのまま追加
                new_data.append(row)
    
    print(f"\n分割結果:")
    print(f"  分割したエントリ: {split_count}件")
    print(f"  元のエントリ数: 4468件")
    print(f"  新しい総エントリ数: {len(new_data)}件")
    print(f"  増加したエントリ数: {len(new_data) - 4468}件")
    
    # 修正されたデータを保存
    if split_count > 0:
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
        
        # 検証例
        print(f"\n=== 分割例の確認 ===")
        species_2112_plants = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['insect_id'] == 'species-2112':
                    species_2112_plants.append(row['plant_name'])
        
        print(f"species-2112の食草: {species_2112_plants}")
    
    else:
        print("分割対象が見つかりませんでした")

if __name__ == "__main__":
    split_comma_separated_plants_v2()