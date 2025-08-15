#!/usr/bin/env python3
import csv
import os
import shutil

def fix_duplicate_japanese_names():
    """重複する和名の問題を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 重複和名問題の修正開始 ===")
    
    # 修正対象の重複IDペア
    # (削除するID, 統合先ID, 和名, 理由)
    fixes = [
        ("species-1497", "species-1498", "ワタアカミムシガ", "species-1497は未使用"),
        ("species-1815", "species-1816", "カラマツイトヒキハマキ", "species-1815は未使用"),
        ("species-1972", "species-1973", "アカガネヒメハマキ", "両方未使用だがspecies-1973を保持"),
        ("species-2153", "species-2154", "フタシロモンヒメハマキ", "species-2153は未使用"),
        ("species-2155", "species-2156", "オオナガバヒメハマキ", "species-2155は未使用"),
        ("species-2157", "species-2158", "ダケカンバヒメハマキ", "species-2157は未使用"),
        # オオアカキリバは両方使用されているため手動で処理
    ]
    
    insects_file = os.path.join(base_dir, 'public', 'insects.csv')
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # 1. insects.csvから重複エントリを削除
    print("\n=== insects.csvの重複エントリ削除 ===")
    
    insects_data = []
    removed_count = 0
    
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            insect_id = row['insect_id']
            
            # 削除対象のIDをチェック
            should_remove = False
            for remove_id, keep_id, japanese_name, reason in fixes:
                if insect_id == remove_id:
                    print(f"削除: {insect_id} ({japanese_name}) - {reason}")
                    should_remove = True
                    removed_count += 1
                    break
            
            if not should_remove:
                insects_data.append(row)
    
    # insects.csvを更新
    with open(insects_file, 'w', encoding='utf-8', newline='') as file:
        if insects_data:
            writer = csv.DictWriter(file, fieldnames=insects_data[0].keys())
            writer.writeheader()
            writer.writerows(insects_data)
    
    print(f"insects.csvから {removed_count}個の重複エントリを削除しました")
    
    # 2. hostplants.csvのIDを統合先に更新（必要に応じて）
    print("\n=== hostplants.csvのID更新確認 ===")
    
    hostplants_data = []
    update_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            insect_id = row['insect_id']
            
            # ID更新が必要かチェック
            for remove_id, keep_id, japanese_name, reason in fixes:
                if insect_id == remove_id:
                    print(f"更新: {remove_id} → {keep_id} ({japanese_name})")
                    row['insect_id'] = keep_id
                    update_count += 1
                    break
            
            hostplants_data.append(row)
    
    if update_count > 0:
        # hostplants.csvを更新
        with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
            if hostplants_data:
                writer = csv.DictWriter(file, fieldnames=hostplants_data[0].keys())
                writer.writeheader()
                writer.writerows(hostplants_data)
        print(f"hostplants.csvで {update_count}個のIDを更新しました")
    else:
        print("hostplants.csvにID更新は不要でした")
    
    # 3. オオアカキリバの特別処理
    print("\n=== オオアカキリバの特別処理 ===")
    print("species-5381とspecies-6152は両方使用されているため手動確認が必要")
    
    # 各IDの詳細を表示
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['insect_id'] in ['species-5381', 'species-6152']:
                print(f"\nID: {row['insect_id']}")
                print(f"  科: {row['family']}")
                print(f"  属種: {row['genus']} {row['species']}")
                print(f"  学名: {row['scientific_name']}")
                print(f"  著者年: {row['author']} {row['year']}")
    
    # hostplants.csvでの使用例を表示
    print("\nhostplants.csvでの使用例:")
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['insect_id'] in ['species-5381', 'species-6152']:
                print(f"  {row['insect_id']}: {row['plant_name']} ({row['reference']})")
    
    # 4. normalized_dataフォルダにもコピー
    src = insects_file
    dst = os.path.join(base_dir, 'normalized_data', 'insects.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    src = hostplants_file
    dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    # 5. 最終検証
    print("\n=== 最終検証 ===")
    
    # 残存する重複和名をチェック
    from collections import defaultdict
    
    japanese_name_to_ids = defaultdict(list)
    
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            japanese_name = row['japanese_name'].strip()
            if japanese_name:
                japanese_name_to_ids[japanese_name].append(row['insect_id'])
    
    remaining_duplicates = {name: ids for name, ids in japanese_name_to_ids.items() if len(ids) > 1}
    
    print(f"修正後の重複和名数: {len(remaining_duplicates)}件")
    
    if remaining_duplicates:
        print("残存する重複:")
        for name, ids in remaining_duplicates.items():
            print(f"  {name}: {ids}")
    else:
        print("✅ 重複和名問題が解決されました")
    
    print(f"\n🔧 重複和名問題の修正が完了しました！")

if __name__ == "__main__":
    fix_duplicate_japanese_names()