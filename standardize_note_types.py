#!/usr/bin/env python3
import csv
import os
import shutil

def standardize_note_types():
    """general_notes.csvのnote_typeを日本語で統一"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== note_type統一処理 ===")
    
    general_notes_file = os.path.join(base_dir, 'public', 'general_notes.csv')
    
    # note_typeマッピング（英語→日本語）
    note_type_mapping = {
        'emergence_time': '出現時期',
        'hostplants_general': '生態情報',
        '備考': '生態情報'  # 備考も生態情報に統一
    }
    
    print(f"\n=== 変換マッピング ===")
    for en, jp in note_type_mapping.items():
        print(f"  {en} → {jp}")
    
    # データを読み込み・修正
    print(f"\n=== データ修正 ===")
    
    all_records = []
    conversion_counts = {}
    
    with open(general_notes_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            original_note_type = row['note_type']
            
            # note_typeを変換
            if original_note_type in note_type_mapping:
                new_note_type = note_type_mapping[original_note_type]
                row['note_type'] = new_note_type
                
                # カウント
                if original_note_type not in conversion_counts:
                    conversion_counts[original_note_type] = 0
                conversion_counts[original_note_type] += 1
                
                # 最初の数件の変換例を表示
                if conversion_counts[original_note_type] <= 3:
                    print(f"変換: {row['record_id']} - '{original_note_type}' → '{new_note_type}'")
            
            all_records.append(row)
    
    print(f"\n=== 変換結果 ===")
    for original, count in conversion_counts.items():
        new_type = note_type_mapping[original]
        print(f"{original} → {new_type}: {count}件")
    
    # ファイルを更新
    print(f"\n=== ファイル更新 ===")
    
    with open(general_notes_file, 'w', encoding='utf-8', newline='') as file:
        if all_records:
            writer = csv.DictWriter(file, fieldnames=all_records[0].keys())
            writer.writeheader()
            writer.writerows(all_records)
    
    # normalized_dataフォルダにもコピー
    src = general_notes_file
    dst = os.path.join(base_dir, 'normalized_data', 'general_notes.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    print("general_notes.csvを更新しました")
    
    # 検証
    print(f"\n=== 検証 ===")
    
    note_type_stats = {}
    with open(general_notes_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            note_type = row['note_type']
            if note_type:
                note_type_stats[note_type] = note_type_stats.get(note_type, 0) + 1
    
    print(f"統一後のnote_type統計:")
    for note_type, count in sorted(note_type_stats.items()):
        print(f"  {note_type}: {count}件")
    
    # 英語のnote_typeが残っていないかチェック
    english_types = ['emergence_time', 'hostplants_general']
    remaining_english = 0
    for note_type in note_type_stats:
        if note_type in english_types:
            remaining_english += note_type_stats[note_type]
    
    if remaining_english == 0:
        print(f"\n✅ 全ての英語note_typeが日本語に統一されました！")
    else:
        print(f"\n⚠️  残存する英語note_type: {remaining_english}件")
    
    # サンプル表示
    print(f"\n統一後サンプル:")
    sample_count = 0
    with open(general_notes_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['note_type'] in ['出現時期', '生態情報']:
                print(f"  {row['record_id']}: {row['note_type']} - {row['content'][:50]}...")
                sample_count += 1
                if sample_count >= 3:
                    break

if __name__ == "__main__":
    standardize_note_types()