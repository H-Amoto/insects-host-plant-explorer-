#!/usr/bin/env python3
import csv
import os
import shutil
import re

def fix_problematic_plant_names():
    """不適切な植物名を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 不適切植物名修正処理 ===")
    
    # 両方のファイルを修正
    files_to_fix = [
        os.path.join(base_dir, 'public', 'hostplants.csv'),
        os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    ]
    
    for hostplants_file in files_to_fix:
        if not os.path.exists(hostplants_file):
            print(f"ファイルが見つかりません: {hostplants_file}")
            continue
            
        print(f"\n=== {hostplants_file} の修正 ===")
        
        all_records = []
        fixed_count = 0
        deleted_count = 0
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                original_plant_name = row['plant_name']
                
                # 問題のあるパターンをチェック
                should_delete = False
                
                # Pattern 1: 明らかに説明文である
                if ('あるいは1齢がバルーニング後に到着した結果' == original_plant_name or
                    'バルーニング' in original_plant_name or
                    '後に到着' in original_plant_name or
                    'した結果' in original_plant_name):
                    print(f"削除: {row['record_id']} - '{original_plant_name}' (説明文)")
                    should_delete = True
                    deleted_count += 1
                
                # Pattern 2: 年号で始まる（データ破損）
                elif re.match(r'^\d{4}.*', original_plant_name):
                    print(f"削除: {row['record_id']} - '{original_plant_name}' (年号で開始)")
                    should_delete = True
                    deleted_count += 1
                
                # Pattern 3: ピリオドで始まる
                elif original_plant_name.startswith('.'):
                    # ピリオドを除去して修正
                    clean_plant_name = original_plant_name.lstrip('.')
                    if clean_plant_name:
                        print(f"修正: {row['record_id']} - '{original_plant_name}' → '{clean_plant_name}'")
                        row['plant_name'] = clean_plant_name
                        fixed_count += 1
                    else:
                        print(f"削除: {row['record_id']} - '{original_plant_name}' (空の植物名)")
                        should_delete = True
                        deleted_count += 1
                
                # Pattern 4: その他の句読点で始まる
                elif re.match(r'^[。、！？\.,!?].*', original_plant_name):
                    clean_plant_name = re.sub(r'^[。、！？\.,!?]+', '', original_plant_name).strip()
                    if clean_plant_name:
                        print(f"修正: {row['record_id']} - '{original_plant_name}' → '{clean_plant_name}'")
                        row['plant_name'] = clean_plant_name
                        fixed_count += 1
                    else:
                        print(f"削除: {row['record_id']} - '{original_plant_name}' (空の植物名)")
                        should_delete = True
                        deleted_count += 1
                
                if not should_delete:
                    all_records.append(row)
        
        print(f"修正したレコード数: {fixed_count}件")
        print(f"削除したレコード数: {deleted_count}件")
        
        # ファイルを更新
        print(f"\n=== ファイル更新 ===")
        
        with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
            if all_records:
                writer = csv.DictWriter(file, fieldnames=all_records[0].keys())
                writer.writeheader()
                writer.writerows(all_records)
        
        print(f"{hostplants_file} を更新しました")
    
    # 不適切なメタページファイルを削除
    print(f"\n=== 不適切なメタページ削除 ===")
    
    meta_plant_dir = os.path.join(base_dir, 'dist', 'meta', 'plant')
    if os.path.exists(meta_plant_dir):
        problematic_files = []
        
        for filename in os.listdir(meta_plant_dir):
            if (filename.startswith('1990') or 
                filename.startswith('.') or
                'バルーニング' in filename or
                '後に到着' in filename):
                problematic_files.append(filename)
        
        for filename in problematic_files:
            file_path = os.path.join(meta_plant_dir, filename)
            try:
                os.remove(file_path)
                print(f"削除: {filename}")
            except OSError as e:
                print(f"削除失敗: {filename} - {e}")
        
        if not problematic_files:
            print("削除する不適切なメタページはありませんでした")
    
    # 検証
    print(f"\n=== 検証 ===")
    
    for hostplants_file in files_to_fix:
        if not os.path.exists(hostplants_file):
            continue
            
        print(f"\n{hostplants_file}:")
        problematic_remaining = 0
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_name = row['plant_name']
                
                if (plant_name.startswith('.') or 
                    re.match(r'^\d+', plant_name) or
                    'バルーニング' in plant_name):
                    problematic_remaining += 1
                    if problematic_remaining <= 3:
                        print(f"  残存問題: {row['record_id']} - '{plant_name}'")
        
        print(f"  残存問題エントリ: {problematic_remaining}件")
    
    print(f"\n✅ 不適切植物名修正処理が完了しました！")

if __name__ == "__main__":
    fix_problematic_plant_names()