#!/usr/bin/env python3
import csv
import os
from collections import defaultdict

def find_and_remove_duplicates():
    """重複エントリを検索して削除"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 重複エントリの検索と削除開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # 重複検出のためのキーを作成する関数
    def create_key(row):
        """重複判定のためのキーを生成"""
        return (
            row['insect_id'],
            row['plant_name'],
            row['plant_family'],
            row['observation_type'],
            row['plant_part'],
            row['life_stage'],
            row['reference']
        )
    
    duplicates = defaultdict(list)
    all_rows = []
    
    # 全行を読み込み、重複を検出
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            key = create_key(row)
            duplicates[key].append((row_num, row))
            all_rows.append((row_num, row))
    
    # 重複があるエントリを特定
    duplicate_entries = []
    for key, entries in duplicates.items():
        if len(entries) > 1:
            duplicate_entries.append((key, entries))
    
    print(f"検出された重複グループ: {len(duplicate_entries)}個")
    
    # 重複を表示
    rows_to_remove = set()
    for i, (key, entries) in enumerate(duplicate_entries):
        print(f"\n重複グループ {i+1}:")
        print(f"  昆虫ID: {key[0]}")
        print(f"  食草名: {key[1]}")
        print(f"  科名: {key[2]}")
        
        for j, (row_num, row) in enumerate(entries):
            print(f"    行{row_num}: {row['record_id']} - 備考: '{row.get('notes', '')}'")
            
            # 最初のエントリ以外を削除対象にする
            if j > 0:
                rows_to_remove.add(row_num)
    
    print(f"\n削除対象行数: {len(rows_to_remove)}行")
    
    # 重複を除去した新しいデータを作成
    new_data = []
    removed_count = 0
    
    for row_num, row in all_rows:
        if row_num not in rows_to_remove:
            new_data.append(row)
        else:
            removed_count += 1
    
    print(f"\n削除結果:")
    print(f"  削除したエントリ: {removed_count}件")
    print(f"  元のエントリ数: {len(all_rows)}件")
    print(f"  新しい総エントリ数: {len(new_data)}件")
    
    # 修正されたデータを保存
    if removed_count > 0:
        with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
            if new_data:
                fieldnames = new_data[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(new_data)
        
        # normalized_dataフォルダにもコピー
        import shutil
        src = hostplants_file
        dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
        shutil.copy2(src, dst)
        
        print("hostplants.csvを更新しました")
        
        # 検証 - 特定のケースをチェック
        print(f"\n=== 検証 ===")
        species_0332_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['insect_id'] == 'species-0332' and '針葉樹' in row['plant_name']:
                    species_0332_entries.append(f"食草名: {row['plant_name']}")
        
        if species_0332_entries:
            print("species-0332の針葉樹関連記録:")
            for entry in species_0332_entries:
                print(f"  {entry}")
        
        print(f"\n✅ 重複エントリの除去が完了しました")
    else:
        print("重複エントリが見つかりませんでした")

if __name__ == "__main__":
    find_and_remove_duplicates()