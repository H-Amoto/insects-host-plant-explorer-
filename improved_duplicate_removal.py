#!/usr/bin/env python3
import csv
import os
import shutil
import re
from collections import defaultdict

def remove_duplicate_plant_mentions_improved():
    """備考欄から既存食草レコードと重複する植物名言及を削除（改良版）"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 冬尺蛾データ備考欄重複情報削除（改良版） ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # 1. 昆虫別の食草記録を収集
    print("\n=== 昆虫別食草記録収集 ===")
    
    insect_plants = defaultdict(set)
    all_records = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            all_records.append(row)
            
            if row['reference'] == '日本の冬尺蛾':
                insect_id = row['insect_id']
                plant_name = row['plant_name']
                if plant_name and plant_name != '不明':
                    insect_plants[insect_id].add(plant_name)
    
    print(f"冬尺蛾昆虫数: {len(insect_plants)}種")
    
    # 2. 備考欄から重複植物名を削除（改良版）
    print("\n=== 備考欄重複情報削除（改良版） ===")
    
    cleaned_records = []
    clean_count = 0
    
    for row in all_records:
        if row['reference'] == '日本の冬尺蛾' and row['notes']:
            insect_id = row['insect_id']
            original_notes = row['notes']
            cleaned_notes = original_notes
            
            existing_plants = insect_plants[insect_id]
            removed_mentions = []
            
            # 各植物名について備考から削除（より保守的なパターン）
            for plant in existing_plants:
                if plant in cleaned_notes and plant != row['plant_name']:
                    # より具体的で安全なパターンのみを使用
                    patterns_to_remove = [
                        # 完全な文または句の削除
                        f'{plant}は飼育記録[。；;]*\\s*',
                        f'{plant}は野外記録[。；;]*\\s*',
                        f'{plant}によく見られる[。；;]*\\s*',
                        f'{plant}を最も好む[。；;]*\\s*',
                        f'{plant}を好む[。；;]*\\s*',
                        f'{plant}も食べる[。；;]*\\s*',
                        # リスト形式での削除（より慎重に）
                        f'、{plant}は飼育記録',
                        f'{plant}、.*?は飼育記録',
                    ]
                    
                    for pattern in patterns_to_remove:
                        original_cleaned = cleaned_notes
                        cleaned_notes = re.sub(pattern, '', cleaned_notes, flags=re.DOTALL)
                        if original_cleaned != cleaned_notes:
                            removed_mentions.append(f"{plant}")
                            break  # 一つのパターンがマッチしたら次の植物へ
            
            # テキストの後処理（より慎重に）
            cleaned_notes = re.sub(r'[；;]{2,}', '；', cleaned_notes)  # 重複セミコロンを統合
            cleaned_notes = re.sub(r'^[；;。、\s]+', '', cleaned_notes)  # 先頭の句読点を除去
            cleaned_notes = re.sub(r'[；;。、\s]+$', '', cleaned_notes)  # 末尾の句読点を除去
            cleaned_notes = re.sub(r'\s+', ' ', cleaned_notes)  # 重複スペースを統合
            cleaned_notes = cleaned_notes.strip()
            
            if original_notes != cleaned_notes:
                print(f"修正: {row['record_id']} ({insect_id})")
                print(f"  元: {original_notes}")
                print(f"  後: {cleaned_notes if cleaned_notes else '(空)'}")
                if removed_mentions:
                    print(f"  削除対象: {', '.join(set(removed_mentions))}")
                clean_count += 1
                
                row['notes'] = cleaned_notes
        
        cleaned_records.append(row)
    
    print(f"\n修正結果: {clean_count}件のレコードの備考を修正")
    
    # 3. ファイルを保存
    print("\n=== ファイル更新 ===")
    
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if cleaned_records:
            writer = csv.DictWriter(file, fieldnames=cleaned_records[0].keys())
            writer.writeheader()
            writer.writerows(cleaned_records)
    
    # normalized_dataフォルダにもコピー
    src = hostplants_file
    dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    print("hostplants.csvを更新しました")
    
    # 4. 修正結果の検証
    print(f"\n=== 修正結果検証 ===")
    
    remaining_duplicates = 0
    sample_cleaned = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if row['reference'] == '日本の冬尺蛾' and row['notes']:
                insect_id = row['insect_id']
                notes = row['notes']
                
                # 重複チェック
                existing_plants = insect_plants[insect_id]
                duplicate_plants = []
                
                for plant in existing_plants:
                    if plant in notes and plant != row['plant_name']:
                        duplicate_plants.append(plant)
                
                if duplicate_plants:
                    remaining_duplicates += 1
                    if remaining_duplicates <= 5:  # 最初の5件のみ表示
                        print(f"  残存重複 {remaining_duplicates}: {row['record_id']} - {duplicate_plants}")
                        print(f"    備考: {notes}")
                else:
                    if len(sample_cleaned) < 3:
                        sample_cleaned.append({
                            'record_id': row['record_id'],
                            'notes': notes[:80] + '...' if len(notes) > 80 else notes
                        })
    
    print(f"\n残存重複: {remaining_duplicates}件")
    print(f"修正済みサンプル:")
    for sample in sample_cleaned:
        print(f"  {sample['record_id']}: {sample['notes']}")
    
    print(f"\n✅ 冬尺蛾データの備考欄重複情報削除（改良版）が完了しました！")

if __name__ == "__main__":
    remove_duplicate_plant_mentions_improved()