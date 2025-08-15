#!/usr/bin/env python3
import csv
import re
import os

def split_genus_entries_direct():
    """属名のカンマ区切りエントリを直接分割"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 属名カンマ区切りエントリの直接分割開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    split_count = 0
    
    # 分割対象の特定エントリを直接指定
    target_patterns = [
        'モミ属, トウヒ属',
        'ヨーロッパクロマツ, ハイマツ', 
        'ヨモギ, オオヨモギ, ニガヨモギ, 栽培キク'
    ]
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # デバッグ: 特定の行を確認
            if row_num in [544, 579, 593]:
                print(f"Debug 行{row_num}: '{plant_name}' (type: {type(plant_name)})")
            
            # 直接パターンマッチングまたはカンマを含む場合をチェック
            should_split = False
            
            # パターン1: 直接指定されたパターン
            if plant_name in target_patterns:
                should_split = True
                clean_name = plant_name
            
            # パターン2: 属で終わる名前のカンマ区切り
            elif ', ' in plant_name and ('属' in plant_name or plant_name.count(',') >= 1):
                # 複数の植物名らしきパターン
                parts = [p.strip() for p in plant_name.split(',')]
                if len(parts) >= 2 and all(len(p) > 1 for p in parts):
                    # 科名や説明文でないことを確認
                    if not any(word in plant_name for word in ['科', '以上', '栽培の', '野外', '飼育', 'など']):
                        should_split = True
                        clean_name = plant_name
            
            if should_split:
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
        
        # 検証例の確認
        print(f"\n=== 分割例の確認 ===")
        momu_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] in ['モミ属', 'トウヒ属']:
                    momu_entries.append(f"{row['insect_id']}: {row['plant_name']}")
        
        if momu_entries:
            print("モミ属・トウヒ属の分割例:")
            for entry in momu_entries:
                print(f"  {entry}")
        else:
            print("モミ属・トウヒ属が見つかりません")
    
    else:
        print("分割対象が見つかりませんでした")

if __name__ == "__main__":
    split_genus_entries_direct()