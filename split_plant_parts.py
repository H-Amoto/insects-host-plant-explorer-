#!/usr/bin/env python3
import csv
import re
import os

def split_plant_parts():
    """「植物名の部位・部位・部位」パターンを個別のレコードに分割"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 植物名の複数部位分割開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # パターン: 「植物名の部位・部位・部位」
            match = re.match(r'^([^の]+)の(.+)$', plant_name)
            if match and '・' in match.group(2):
                species_name = match.group(1)
                parts_text = match.group(2)
                
                # 「・」で部位を分割
                parts = [part.strip() for part in parts_text.split('・') if part.strip()]
                
                if len(parts) > 1:
                    print(f"\n修正対象: 行{row_num}")
                    print(f"  元: '{plant_name}'")
                    print(f"  植物名: '{species_name}'")
                    print(f"  部位: {parts}")
                    
                    # 各部位に対して個別のレコードを作成
                    for i, part in enumerate(parts):
                        new_row = row.copy()
                        new_row['plant_name'] = species_name
                        new_row['plant_part'] = part
                        
                        # record_idを調整（最初のエントリは元のIDを保持、以降は新規生成）
                        if i > 0:
                            new_row['record_id'] = f"temp-{row_num}-{i+1}"
                        
                        new_data.append(new_row)
                        print(f"    分割{i+1}: '{species_name}' の{part}")
                    
                    print(f"  分割結果: {len(parts)}個のレコードに分割")
                else:
                    # 部位が1つしかない場合は通常の処理
                    new_data.append(row)
            else:
                # パターンにマッチしない場合は元のレコードを保持
                new_data.append(row)
    
    print(f"\n分割結果:")
    print(f"  元のエントリ数: {row_num-1}件")
    print(f"  分割後のエントリ数: {len(new_data)}件")
    print(f"  増加したエントリ数: {len(new_data) - (row_num-1)}件")
    
    # record_idを正規化
    print("\nrecord_idを正規化中...")
    for i, row in enumerate(new_data):
        row['record_id'] = f"hostplant-{i+1:06d}"
    
    # 修正されたデータを保存
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_data)
    
    # normalized_dataフォルダにもコピー
    import shutil
    src = hostplants_file
    dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    print("hostplants.csvを更新しました")
    
    # 検証
    print(f"\n=== 検証 ===")
    
    # 残存する複数部位パターンをチェック
    remaining_multi_parts = []
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            plant_name = row['plant_name']
            match = re.match(r'^([^の]+)の(.+)$', plant_name)
            if match and '・' in match.group(2):
                remaining_multi_parts.append(plant_name[:50])
    
    if remaining_multi_parts:
        print(f"残存する複数部位パターン ({len(remaining_multi_parts)}件):")
        for pattern in remaining_multi_parts[:3]:
            print(f"  '{pattern}...'")
    else:
        print("✅ 複数部位パターンが全て分割されました")
    
    # 分割された例の確認
    split_examples = []
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['plant_name'] == 'タカナタマメ' and row['plant_part']:
                split_examples.append(f"{row['plant_name']} の{row['plant_part']}")
    
    print(f"\nタカナタマメの分割例:")
    for example in split_examples:
        print(f"  {example}")
    
    print(f"\n🌱 植物名の複数部位分割が完了しました！")

if __name__ == "__main__":
    split_plant_parts()