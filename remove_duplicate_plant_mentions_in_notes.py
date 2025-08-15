#!/usr/bin/env python3
import csv
import os
import shutil
import re
from collections import defaultdict

def remove_duplicate_plant_mentions_in_notes():
    """備考欄から既存食草レコードと重複する植物名言及を削除"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 冬尺蛾データ備考欄重複情報削除 ===")
    
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
    
    # 2. 備考欄から重複植物名を削除
    print("\n=== 備考欄重複情報削除 ===")
    
    cleaned_records = []
    clean_count = 0
    
    for row in all_records:
        if row['reference'] == '日本の冬尺蛾' and row['notes']:
            insect_id = row['insect_id']
            original_notes = row['notes']
            cleaned_notes = original_notes
            
            existing_plants = insect_plants[insect_id]
            removed_mentions = []
            
            # 各植物名について備考から削除
            for plant in existing_plants:
                if plant in cleaned_notes and plant != row['plant_name']:
                    # 植物名を含む文脈的フレーズを削除
                    patterns_to_remove = [
                        f'{plant}は飼育記録[。、；;]*\\s*',
                        f'{plant}は飼育[。、；;]*\\s*',
                        f'{plant}は野外[。、；;]*\\s*',
                        f'{plant}[、,]?\\s*{plant}[、,]?\\s*は飼育記録[。、；;]*\\s*',
                        f'{plant}[、,]?\\s*は飼育記録[。、；;]*\\s*',
                        f'{plant}[、,]?\\s*は野外記録[。、；;]*\\s*',
                        f'特に{plant}[。、；;]*\\s*',
                        f'{plant}によく見られる[。、；;]*\\s*',
                        f'{plant}を最も好[むみ][。、；;]*\\s*',
                        f'{plant}を好[むみ][。、；;]*\\s*',
                        f'{plant}[、,]\\s*{plant}[、,]\\s*は飼育記録[。、；;]*\\s*',
                        f'{plant}[、,]\\s*は食べ[たる][。、；;]*\\s*',
                        f'{plant}[、,]\\s*も食べる[。、；;]*\\s*'
                    ]
                    
                    for pattern in patterns_to_remove:
                        if re.search(pattern, cleaned_notes):
                            cleaned_notes = re.sub(pattern, '', cleaned_notes)
                            removed_mentions.append(f"{plant} ({pattern.split('[')[0]})")
                    
                    # より一般的なパターンも削除
                    # 「植物名、植物名、植物名は飼育記録」のようなパターン
                    plant_list_pattern = f'[^。]*{plant}[^。]*は飼育記録[。；;]*\\s*'
                    if re.search(plant_list_pattern, cleaned_notes):
                        cleaned_notes = re.sub(plant_list_pattern, '', cleaned_notes)
                        removed_mentions.append(f"{plant} (リスト形式)")
            
            # 清理后的备注
            cleaned_notes = re.sub(r'[；;]+', '；', cleaned_notes)  # 重複セミコロンを統合
            cleaned_notes = re.sub(r'^[；;。、\s]+|[；;。、\s]+$', '', cleaned_notes)  # 先頭・末尾の句読点を除去
            cleaned_notes = re.sub(r'\\s+', ' ', cleaned_notes)  # 重複スペースを統合
            cleaned_notes = cleaned_notes.strip()
            
            if original_notes != cleaned_notes:
                print(f"清理: {row['record_id']} ({insect_id})")
                print(f"  元: {original_notes[:80]}...")
                print(f"  后: {cleaned_notes[:80] if cleaned_notes else '(空)'}...")
                if removed_mentions:
                    print(f"  削除: {', '.join(removed_mentions[:3])}...")
                clean_count += 1
                
                row['notes'] = cleaned_notes
        
        cleaned_records.append(row)
    
    print(f"\n清理結果: {clean_count}件のレコードの備考を修正")
    
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
    
    # 4. 清理結果の検証
    print(f"\n=== 清理結果検証 ===")
    
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
                has_duplicate = False
                
                for plant in existing_plants:
                    if plant in notes and plant != row['plant_name']:
                        has_duplicate = True
                        break
                
                if has_duplicate:
                    remaining_duplicates += 1
                else:
                    if len(sample_cleaned) < 5:
                        sample_cleaned.append({
                            'record_id': row['record_id'],
                            'notes': notes[:60] + '...' if len(notes) > 60 else notes
                        })
    
    print(f"残存重複: {remaining_duplicates}件")
    print(f"清理済みサンプル:")
    for sample in sample_cleaned:
        print(f"  {sample['record_id']}: {sample['notes']}")
    
    print(f"\n✅ 冬尺蛾データの備考欄重複情報削除が完了しました！")

if __name__ == "__main__":
    remove_duplicate_plant_mentions_in_notes()