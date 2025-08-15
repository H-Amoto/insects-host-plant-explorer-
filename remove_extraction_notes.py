#!/usr/bin/env python3
import csv
import os
import shutil

def remove_extraction_notes():
    """「備考から抽出（元レコード: ○○）」というnotesを削除"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 抽出メモ削除処理 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # データを読み込み・修正
    print("\n=== データ修正 ===")
    
    all_records = []
    cleaned_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # 「備考から抽出」で始まるnotesを空にする
            if row['notes'] and row['notes'].startswith('備考から抽出（元レコード:'):
                print(f"削除: {row['record_id']} - {row['notes']}")
                row['notes'] = ''
                cleaned_count += 1
            
            all_records.append(row)
    
    print(f"削除したnotesの数: {cleaned_count}件")
    
    # ファイルを更新
    print("\n=== ファイル更新 ===")
    
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if all_records:
            writer = csv.DictWriter(file, fieldnames=all_records[0].keys())
            writer.writeheader()
            writer.writerows(all_records)
    
    # normalized_dataフォルダにもコピー
    src = hostplants_file
    dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    print("hostplants.csvを更新しました")
    
    # 検証
    print(f"\n=== 検証 ===")
    
    remaining_extraction_notes = 0
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['notes'] and '備考から抽出' in row['notes']:
                remaining_extraction_notes += 1
    
    print(f"残存する抽出メモ: {remaining_extraction_notes}件")
    
    print(f"\n✅ 抽出メモの削除処理が完了しました！")

if __name__ == "__main__":
    remove_extraction_notes()