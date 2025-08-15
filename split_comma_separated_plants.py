#!/usr/bin/env python3
import csv
import re
import os

def split_comma_separated_plants():
    """カンマ区切りの食草名を個別エントリに分割"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== カンマ区切り食草名の分割開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    split_count = 0
    total_new_entries = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # クォートで囲まれ、内部にカンマがある場合
            if plant_name.startswith('"') and plant_name.endswith('"') and ', ' in plant_name:
                # クォートを除去
                clean_name = plant_name.strip('"')
                
                # カンマで分割
                individual_plants = [name.strip() for name in clean_name.split(',')]
                
                print(f"分割: 行{row_num} {row['insect_id']} → {len(individual_plants)}個の食草")
                print(f"  元: {plant_name}")
                print(f"  分割後: {individual_plants}")
                
                # 各植物名に対して個別エントリを作成
                for i, individual_plant in enumerate(individual_plants):
                    if individual_plant:  # 空でない場合のみ
                        new_row = row.copy()
                        new_row['plant_name'] = individual_plant
                        
                        # record_idを更新（最初の植物は元のID、その他は新しいID）
                        if i == 0:
                            new_row['record_id'] = row['record_id']
                        else:
                            new_row['record_id'] = str(len(new_data) + 1000000)  # 大きな番号で重複回避
                        
                        new_data.append(new_row)
                        total_new_entries += 1
                
                split_count += 1
                
            else:
                # 通常のエントリはそのまま追加
                new_data.append(row)
    
    print(f"\n分割結果:")
    print(f"  分割したエントリ: {split_count}件")
    print(f"  新しい総エントリ数: {len(new_data)}件")
    print(f"  増加したエントリ数: {len(new_data) - (4468 - split_count)}件")
    
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
        
        # 検証 - 残存するカンマ区切りエントリをチェック
        print(f"\n=== 検証 ===")
        remaining_comma_entries = 0
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_name = row['plant_name']
                if plant_name.startswith('"') and ', ' in plant_name:
                    remaining_comma_entries += 1
                    if remaining_comma_entries <= 5:
                        print(f"残存: {plant_name}")
        
        if remaining_comma_entries == 0:
            print("✅ カンマ区切りエントリは全て分割されました")
        else:
            print(f"⚠️  {remaining_comma_entries}件のカンマ区切りエントリが残っています")
        
        # 分割例の確認
        print(f"\n=== 分割例の確認 ===")
        examples = {}
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                insect_id = row['insect_id']
                if insect_id == 'species-2112':  # クロウメモドキの例
                    if insect_id not in examples:
                        examples[insect_id] = []
                    examples[insect_id].append(row['plant_name'])
        
        for insect_id, plants in examples.items():
            print(f"{insect_id}: {plants}")
    
    else:
        print("分割対象が見つかりませんでした")

if __name__ == "__main__":
    split_comma_separated_plants()