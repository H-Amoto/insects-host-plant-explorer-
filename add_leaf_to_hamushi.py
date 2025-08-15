#!/usr/bin/env python3
import csv
import re
import os

def add_leaf_to_hamushi():
    """ハムシの植物部位が空欄のエントリに「葉」を加筆"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== ハムシの植物部位に「葉」を加筆開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    new_data = []
    add_count = 0
    hamushi_total = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            insect_id = row['insect_id']
            plant_part = row['plant_part']
            
            # ハムシ（H系とCR系）のエントリを特定
            if insect_id.startswith('species-H') or insect_id.startswith('species-CR'):
                hamushi_total += 1
                
                # 植物部位が空欄の場合に「葉」を追加
                if not plant_part or plant_part.strip() == '':
                    print(f"\\n加筆: 行{row_num} (ID: {insect_id})")
                    print(f"  植物名: '{row['plant_name']}'")
                    print(f"  部位: '' → '葉'")
                    
                    row['plant_part'] = '葉'
                    add_count += 1
                
                # 進捗表示（100件ごと）
                if hamushi_total % 100 == 0:
                    print(f"処理中... {hamushi_total}件目")
            
            new_data.append(row)
    
    print(f"\\n処理結果:")
    print(f"  ハムシ総エントリ数: {hamushi_total}件")
    print(f"  「葉」を加筆したエントリ: {add_count}件")
    print(f"  元のエントリ数: {row_num-1}件")
    print(f"  修正後のエントリ数: {len(new_data)}件")
    
    # 修正されたデータを保存
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if new_data:
            writer = csv.DictWriter(file, fieldnames=new_data[0].keys())
            writer.writeheader()
            writer.writerows(new_data)
    
    # normalized_dataフォルダにもコピー
    import shutil
    src = hostplants_file
    dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    print("hostplants.csvを更新しました")
    
    # 最終検証
    print(f"\\n=== 最終検証 ===")
    
    # ハムシエントリの植物部位統計
    hamushi_part_counts = {}
    empty_parts = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            insect_id = row['insect_id']
            plant_part = row['plant_part']
            
            if insect_id.startswith('species-H') or insect_id.startswith('species-CR'):
                if plant_part and plant_part.strip():
                    part = plant_part.strip()
                    hamushi_part_counts[part] = hamushi_part_counts.get(part, 0) + 1
                else:
                    empty_parts += 1
    
    print(f"ハムシの植物部位統計:")
    for part, count in sorted(hamushi_part_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {part}: {count}件")
    
    if empty_parts > 0:
        print(f"  空欄: {empty_parts}件")
    else:
        print("✅ ハムシエントリに空欄の植物部位はありません")
    
    # サンプル確認
    print(f"\\n修正されたエントリの例:")
    sample_count = 0
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if ((row['insect_id'].startswith('species-H') or row['insect_id'].startswith('species-CR')) 
                and row['plant_part'] == '葉' and sample_count < 5):
                print(f"  {row['insect_id']}: {row['plant_name']} → {row['plant_part']}")
                sample_count += 1
    
    print(f"\\n🍃 ハムシの植物部位に「葉」の加筆が完了しました！")

if __name__ == "__main__":
    add_leaf_to_hamushi()