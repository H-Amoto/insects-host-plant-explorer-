#!/usr/bin/env python3
import csv
import os
import shutil
import re

def remove_redundant_cultivation_notes():
    """observation_typeが飼育記録の場合、備考から重複する飼育情報を削除"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 飼育記録重複備考削除処理 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # データを読み込み・修正
    print("\n=== データ修正 ===")
    
    all_records = []
    fixed_count = 0
    
    # 削除対象のパターン
    redundant_patterns = [
        r'飼育下での記録[。；;]*\s*',
        r'飼育記録[。；;]*\s*',
        r'飼育での記録[。；;]*\s*',
        r'飼育による記録[。；;]*\s*',
        r'飼育によって確認[。；;]*\s*',
        r'飼育により確認[。；;]*\s*',
        r'は飼育下での記録[。；;]*\s*',
        r'は飼育記録[。；;]*\s*',
        r'[、,]飼育下での記録[。；;]*\s*',
        r'[。]飼育下での記録[。；;]*\s*',
    ]
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            observation_type = row['observation_type']
            original_notes = row['notes']
            
            # observation_typeが「飼育記録」の場合のみ処理
            if observation_type == '飼育記録' and original_notes:
                cleaned_notes = original_notes
                removed_patterns = []
                
                # 各重複パターンを削除
                for pattern in redundant_patterns:
                    if re.search(pattern, cleaned_notes):
                        before_clean = cleaned_notes
                        cleaned_notes = re.sub(pattern, '', cleaned_notes)
                        if before_clean != cleaned_notes:
                            removed_patterns.append(pattern.replace(r'[。；;]*\s*', '').replace(r'[、,]', '').replace(r'[。]', ''))
                
                # テキストの後処理
                cleaned_notes = re.sub(r'[。]{2,}', '。', cleaned_notes)  # 重複句点を統合
                cleaned_notes = re.sub(r'^[。；;、,\s]+', '', cleaned_notes)  # 先頭の句読点を除去
                cleaned_notes = re.sub(r'[。；;、,\s]+$', '', cleaned_notes)  # 末尾の句読点を除去
                cleaned_notes = re.sub(r'\s+', ' ', cleaned_notes)  # 重複スペースを統合
                cleaned_notes = cleaned_notes.strip()
                
                # 適切に句点で終わるよう調整（内容がある場合のみ）
                if cleaned_notes and not cleaned_notes.endswith(('。', '；', ';')):
                    cleaned_notes += '。'
                
                if original_notes != cleaned_notes:
                    print(f"修正: {row['record_id']} ({row['insect_id']})")
                    print(f"  元: {original_notes}")
                    print(f"  後: {cleaned_notes if cleaned_notes else '(空)'}")
                    if removed_patterns:
                        print(f"  削除: {', '.join(set(removed_patterns))}")
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
    
    remaining_redundant = 0
    cultivation_records = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['observation_type'] == '飼育記録':
                cultivation_records += 1
                
                # まだ重複情報が残っているかチェック
                if row['notes'] and ('飼育下での記録' in row['notes'] or '飼育記録' in row['notes']):
                    remaining_redundant += 1
                    if remaining_redundant <= 5:  # 最初の5件のみ表示
                        print(f"  残存重複: {row['record_id']} - {row['notes']}")
    
    print(f"飼育記録レコード総数: {cultivation_records}件")
    print(f"残存重複: {remaining_redundant}件")
    
    # 修正済みサンプル表示
    print(f"\n修正済みサンプル:")
    sample_count = 0
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (row['observation_type'] == '飼育記録' and 
                row['reference'] in ['日本の冬夜蛾', '日本の冬尺蛾'] and
                row['notes']):
                print(f"  {row['record_id']}: {row['notes'][:80]}...")
                sample_count += 1
                if sample_count >= 3:
                    break
    
    print(f"\n✅ 飼育記録重複備考削除処理が完了しました！")

if __name__ == "__main__":
    remove_redundant_cultivation_notes()