#!/usr/bin/env python3
import csv
import os
import shutil
import re
from collections import defaultdict

def final_duplicate_cleanup():
    """備考欄から既存食草レコードと重複する植物名言及を削除（最終版）"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 冬尺蛾データ備考欄重複情報削除（最終版） ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # 1. 昆虫別の食草記録を収集
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
    
    # 2. 具体的な問題パターンを特定して削除
    print("\n=== 具体的問題パターン削除 ===")
    
    cleaned_records = []
    clean_count = 0
    
    for row in all_records:
        if row['reference'] == '日本の冬尺蛾' and row['notes']:
            insect_id = row['insect_id']
            original_notes = row['notes']
            cleaned_notes = original_notes
            
            existing_plants = insect_plants[insect_id]
            removed_mentions = []
            
            # 具体的な削除パターン
            for plant in existing_plants:
                if plant in cleaned_notes and plant != row['plant_name']:
                    
                    # パターン1: 「ケヤキは飼育記録」
                    pattern1 = f'{plant}は飼育記録[。；;]*\\s*'
                    if re.search(pattern1, cleaned_notes):
                        cleaned_notes = re.sub(pattern1, '', cleaned_notes)
                        removed_mentions.append(f"{plant}(飼育記録)")
                        continue
                    
                    # パターン2: 列挙の一部「リンゴ、サクラ」
                    # 文末に列挙されている場合
                    pattern2 = f'[、,]\\s*{plant}\\s*$'
                    if re.search(pattern2, cleaned_notes):
                        cleaned_notes = re.sub(pattern2, '', cleaned_notes)
                        removed_mentions.append(f"{plant}(文末列挙)")
                        continue
                        
                    # パターン3: 「○○、○○」の形式
                    pattern3 = f'{plant}[、,]\\s*{plant}\\b'
                    if re.search(pattern3, cleaned_notes):
                        cleaned_notes = re.sub(pattern3, plant, cleaned_notes)
                        removed_mentions.append(f"{plant}(重複)")
                        continue
                    
                    # パターン4: 「○○によく見られる」の前の列挙
                    # 「比較的広食性だが、サクラ類によく見られる。リンゴ、サクラ」
                    pattern4 = f'([^。]*{plant}[^。]*によく見られる[^。]*)[。]*\\s*([^。]*、)*{plant}\\b[^。]*$'
                    if re.search(pattern4, cleaned_notes):
                        # 文末の重複植物名部分を削除
                        pattern4_clean = f'([。])([^。]*、)*{plant}\\b[^。]*$'
                        cleaned_notes = re.sub(pattern4_clean, r'\1', cleaned_notes)
                        removed_mentions.append(f"{plant}(文末重複)")
                        continue
                    
                    # パターン5: 実験結果の重複言及
                    # 「孵化幼虫にクヌギ、ヤマハンノキ、サクラを与えたところ、サクラを多少食べた」
                    pattern5 = f'[、,]\\s*{plant}を多少食べた\\s*$'
                    if re.search(pattern5, cleaned_notes):
                        cleaned_notes = re.sub(pattern5, '', cleaned_notes)
                        removed_mentions.append(f"{plant}(実験結果)")
                        continue
            
            # テキストの後処理
            cleaned_notes = re.sub(r'[。；;]{2,}', '。', cleaned_notes)  # 重複句読点を統合
            cleaned_notes = re.sub(r'^[。；;、,\s]+', '', cleaned_notes)  # 先頭の句読点を除去
            cleaned_notes = re.sub(r'[。；;、,\s]+$', '', cleaned_notes)  # 末尾の句読点を除去
            cleaned_notes = re.sub(r'\s+', ' ', cleaned_notes)  # 重複スペースを統合
            cleaned_notes = cleaned_notes.strip()
            
            # 空白の調整
            cleaned_notes = re.sub(r'([^。])$', r'\1。', cleaned_notes) if cleaned_notes and not cleaned_notes.endswith(('。', '；', ';')) else cleaned_notes
            
            if original_notes != cleaned_notes:
                print(f"修正: {row['record_id']} ({insect_id})")
                print(f"  元: {original_notes}")
                print(f"  後: {cleaned_notes if cleaned_notes else '(空)'}")
                if removed_mentions:
                    print(f"  削除: {', '.join(removed_mentions)}")
                print()
                clean_count += 1
                
                row['notes'] = cleaned_notes
        
        cleaned_records.append(row)
    
    print(f"修正結果: {clean_count}件のレコードの備考を修正")
    
    # 3. ファイルを保存
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
    
    print("\nhostplants.csvを更新しました")
    
    # 4. 最終検証
    print(f"\n=== 最終検証 ===")
    
    remaining_duplicates = 0
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if row['reference'] == '日本の冬尺蛾' and row['notes']:
                insect_id = row['insect_id']
                notes = row['notes']
                
                existing_plants = insect_plants[insect_id]
                duplicate_plants = []
                
                for plant in existing_plants:
                    if plant in notes and plant != row['plant_name']:
                        duplicate_plants.append(plant)
                
                if duplicate_plants:
                    remaining_duplicates += 1
    
    print(f"残存重複: {remaining_duplicates}件")
    print(f"\n✅ 冬尺蛾データの備考欄重複情報削除（最終版）が完了しました！")

if __name__ == "__main__":
    final_duplicate_cleanup()