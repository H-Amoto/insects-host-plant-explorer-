#!/usr/bin/env python3
import csv
import os
from collections import defaultdict

def fix_duplicate_hostplants():
    """同じ昆虫種の同じ植物名の重複レコードを出典統合で修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 重複食草レコード修正処理 ===")
    
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
        
        # 重複を検出
        duplicates = defaultdict(lambda: defaultdict(list))
        all_records = []
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                insect_id = row['insect_id']
                plant_name = row['plant_name']
                duplicates[insect_id][plant_name].append(row)
                all_records.append(row)
        
        # 重複の統合処理
        records_to_keep = []
        merged_count = 0
        deleted_count = 0
        
        processed_combinations = set()
        
        for record in all_records:
            insect_id = record['insect_id']
            plant_name = record['plant_name']
            combination_key = f"{insect_id}_{plant_name}"
            
            # すでに処理済みの組み合わせはスキップ
            if combination_key in processed_combinations:
                continue
                
            duplicate_records = duplicates[insect_id][plant_name]
            
            if len(duplicate_records) > 1:
                # 重複がある場合、統合処理
                print(f"\n重複統合: {insect_id} - {plant_name} ({len(duplicate_records)}件)")
                
                # 最も完全な情報を持つレコードをベースにする
                base_record = None
                references = []
                
                for dup_record in duplicate_records:
                    print(f"  {dup_record['record_id']}: {dup_record['reference']} ({dup_record['plant_family']})")
                    
                    # 植物科名がある、または他の情報が豊富なレコードを優先
                    if (base_record is None or 
                        (dup_record['plant_family'] and not base_record['plant_family']) or
                        (dup_record['observation_type'] and not base_record['observation_type'])):
                        base_record = dup_record.copy()
                    
                    # 出典を収集
                    if dup_record['reference']:
                        references.append(dup_record['reference'])
                
                # 出典を統合（セミコロンで区切り）
                if references:
                    unique_references = []
                    for ref in references:
                        if ref not in unique_references:
                            unique_references.append(ref)
                    base_record['reference'] = '; '.join(unique_references)
                
                # 備考欄に統合情報を追加
                if len(duplicate_records) > 1:
                    original_notes = base_record['notes'] if base_record['notes'] else ''
                    merge_note = f"複数出典統合({len(duplicate_records)}件)"
                    if original_notes:
                        base_record['notes'] = f"{original_notes}; {merge_note}"
                    else:
                        base_record['notes'] = merge_note
                
                print(f"  → 統合後: {base_record['reference']}")
                records_to_keep.append(base_record)
                merged_count += 1
                deleted_count += len(duplicate_records) - 1
                
            else:
                # 重複がない場合はそのまま保持
                records_to_keep.append(record)
            
            processed_combinations.add(combination_key)
        
        print(f"\n統合したレコード数: {merged_count}件")
        print(f"削除したレコード数: {deleted_count}件")
        print(f"最終レコード数: {len(records_to_keep)}件 (元: {len(all_records)}件)")
        
        # ファイルを更新
        print(f"\n=== ファイル更新 ===")
        
        with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
            if records_to_keep:
                writer = csv.DictWriter(file, fieldnames=records_to_keep[0].keys())
                writer.writeheader()
                writer.writerows(records_to_keep)
        
        print(f"{hostplants_file} を更新しました")
    
    # 検証
    print(f"\n=== 検証 ===")
    
    for hostplants_file in files_to_fix:
        if not os.path.exists(hostplants_file):
            continue
            
        print(f"\n{hostplants_file}:")
        duplicates_remaining = defaultdict(lambda: defaultdict(int))
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                insect_id = row['insect_id']
                plant_name = row['plant_name']
                duplicates_remaining[insect_id][plant_name] += 1
        
        remaining_duplicates = 0
        for insect_id, plants in duplicates_remaining.items():
            for plant_name, count in plants.items():
                if count > 1:
                    remaining_duplicates += 1
                    if remaining_duplicates <= 5:  # 最初の5件表示
                        print(f"  残存重複: {insect_id} - {plant_name}: {count}件")
        
        print(f"  残存重複総数: {remaining_duplicates}件")
    
    # 統合された例を表示
    print(f"\n=== 統合例 ===")
    
    with open(files_to_fix[0], 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        merged_examples = []
        
        for row in reader:
            if '複数出典統合' in row['notes']:
                merged_examples.append({
                    'insect_id': row['insect_id'],
                    'plant_name': row['plant_name'],
                    'reference': row['reference'],
                    'notes': row['notes']
                })
            
            if len(merged_examples) >= 10:  # 最初の10件
                break
        
        for example in merged_examples:
            print(f"  {example['insect_id']} - {example['plant_name']}")
            print(f"    出典: {example['reference']}")
            print(f"    備考: {example['notes']}")
            print()
    
    print(f"\n✅ 重複食草レコード修正処理が完了しました！")

if __name__ == "__main__":
    fix_duplicate_hostplants()