#!/usr/bin/env python3
import csv
import re
import os

def split_remaining_quoted_entries():
    """残りのクォート付きカンマ区切りエントリを分割"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 残りのクォート付きカンマ区切りエントリの分割開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    split_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # クォート付きでカンマを含むエントリを探す
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
    print(f"  元のエントリ数: 4493件")
    print(f"  新しい総エントリ数: {len(new_data)}件")
    print(f"  増加したエントリ数: {len(new_data) - 4493}件")
    
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
        
        # 検証 - 残存するクォート付きカンマエントリをチェック
        print(f"\n=== 検証 ===")
        remaining_quoted_entries = 0
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_name = row['plant_name']
                if plant_name.startswith('"') and ', ' in plant_name and plant_name.endswith('"'):
                    remaining_quoted_entries += 1
                    if remaining_quoted_entries <= 5:
                        print(f"残存: {plant_name}")
        
        if remaining_quoted_entries == 0:
            print("✅ クォート付きカンマ区切りエントリは全て分割されました")
        else:
            print(f"⚠️  {remaining_quoted_entries}件のクォート付きカンマエントリが残っています")
        
        # 分割例の確認 - モミ属、トウヒ属
        print(f"\n=== 分割例の確認 ===")
        momu_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] in ['モミ属', 'トウヒ属']:
                    momu_entries.append(f"{row['insect_id']}: {row['plant_name']}")
        
        if momu_entries:
            print("モミ属・トウヒ属の分割例:")
            for entry in momu_entries[:5]:
                print(f"  {entry}")
        
    else:
        print("分割対象が見つかりませんでした")
        
        # 残存するクォート付きエントリの確認
        print(f"\n=== 残存クォート付きエントリの確認 ===")
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            quoted_entries = []
            for row in reader:
                plant_name = row['plant_name']
                if plant_name.startswith('"') and plant_name.endswith('"'):
                    quoted_entries.append(plant_name)
        
        if quoted_entries:
            print(f"残存クォート付きエントリ ({len(quoted_entries)}件):")
            for entry in quoted_entries[:10]:
                print(f"  {entry}")
        else:
            print("クォート付きエントリはありません")

if __name__ == "__main__":
    split_remaining_quoted_entries()