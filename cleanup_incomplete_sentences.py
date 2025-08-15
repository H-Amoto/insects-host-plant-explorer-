#!/usr/bin/env python3
import csv
import os
import shutil
import re

def cleanup_incomplete_sentences():
    """不完全な文を修正（「○○は。」等）"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 不完全文修正処理 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # データを読み込み・修正
    print("\n=== データ修正 ===")
    
    all_records = []
    fixed_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            original_notes = row['notes']
            
            if original_notes:
                cleaned_notes = original_notes
                
                # 不完全な文のパターンを修正
                patterns_to_fix = [
                    # パターン1: 「○○は。」→ 削除
                    (r'^[^。]*は[。；;]\s*$', ''),
                    # パターン2: 「○○、○○は。」→ 削除
                    (r'^[^。]*、[^。]*は[。；;]\s*$', ''),
                    # パターン3: 「あり。」のみ → 削除
                    (r'^あり[。；;]\s*$', ''),
                    # パターン4: 「からナツツバキがホストと推測される。」→ 「ナツツバキがホストと推測される。」
                    (r'^から(.+)', r'\1'),
                    # パターン5: 末尾の不要な文字を除去
                    (r'([^。；;])\s*[。；;]+\s*$', r'\1。'),
                ]
                
                for pattern, replacement in patterns_to_fix:
                    new_notes = re.sub(pattern, replacement, cleaned_notes)
                    if new_notes != cleaned_notes:
                        cleaned_notes = new_notes
                        break
                
                # 空白のみの場合は完全に空にする
                cleaned_notes = cleaned_notes.strip()
                
                if original_notes != cleaned_notes:
                    print(f"修正: {row['record_id']}")
                    print(f"  元: '{original_notes}'")
                    print(f"  後: '{cleaned_notes if cleaned_notes else '(空)'}'")
                    print()
                    
                    row['notes'] = cleaned_notes
                    fixed_count += 1
            
            all_records.append(row)
    
    print(f"修正したレコード数: {fixed_count}件")
    
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
    
    incomplete_sentences = 0
    empty_notes = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            notes = row['notes']
            
            if not notes:
                empty_notes += 1
            elif re.match(r'^[^。]*は[。；;]\s*$', notes) or notes == 'あり。':
                incomplete_sentences += 1
                if incomplete_sentences <= 3:  # 最初の3件のみ表示
                    print(f"  残存不完全文: {row['record_id']} - '{notes}'")
    
    print(f"空の備考: {empty_notes}件")
    print(f"残存不完全文: {incomplete_sentences}件")
    
    print(f"\n✅ 不完全文修正処理が完了しました！")

if __name__ == "__main__":
    cleanup_incomplete_sentences()