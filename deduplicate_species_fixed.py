#!/usr/bin/env python3
import csv
import re
from collections import defaultdict

def merge_species_data():
    """同種の重複データを統合する"""
    print("同種の重複データを統合しています...")
    
    input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master.csv'
    output_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master_deduplicated.csv'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    
    # 和名と学名の対応表を作成
    japanese_to_scientific = {}
    scientific_to_japanese = {}
    
    for i, row in enumerate(rows):
        # 和名を複数の列から検索（メインの和名列、または他の列に誤って入っている場合）
        japanese_name = ""
        if len(row) > 18 and row[18].strip():
            japanese_name = row[18].strip()
        elif len(row) > 11 and row[11].strip() and not row[11].strip().isdigit():
            japanese_name = row[11].strip()  # 亜族名_1列もチェック
        
        scientific_name = row[25].strip() if len(row) > 25 else ""
        
        if japanese_name and scientific_name:
            japanese_to_scientific[japanese_name] = scientific_name
            scientific_to_japanese[scientific_name] = japanese_name
    
    # 統合対象を見つけて統合する
    processed_rows = set()  # 処理済み行のインデックス
    merged_rows = []
    duplicates_found = 0
    
    for i, row in enumerate(rows):
        if i in processed_rows:
            continue
            
        # 和名を複数の列から検索
        japanese_name = ""
        if len(row) > 18 and row[18].strip():
            japanese_name = row[18].strip()
        elif len(row) > 11 and row[11].strip() and not row[11].strip().isdigit():
            japanese_name = row[11].strip()
        
        scientific_name = row[25].strip() if len(row) > 25 else ""
        
        # 統合候補を探す
        candidates = [i]  # 自分自身を含む
        
        for j, other_row in enumerate(rows):
            if j == i or j in processed_rows:
                continue
                
            # 和名を複数の列から検索
            other_japanese = ""
            if len(other_row) > 18 and other_row[18].strip():
                other_japanese = other_row[18].strip()
            elif len(other_row) > 11 and other_row[11].strip() and not other_row[11].strip().isdigit():
                other_japanese = other_row[11].strip()
            
            other_scientific = other_row[25].strip() if len(other_row) > 25 else ""
            
            # マッチング条件
            match = False
            
            # 1. 和名が同じ（両方にある場合）
            if japanese_name and other_japanese and japanese_name == other_japanese:
                match = True
            # 2. 学名が同じ（両方にある場合）
            elif scientific_name and other_scientific and scientific_name == other_scientific:
                match = True
            # 3. 和名と学名の対応関係による一致
            elif japanese_name and other_scientific and not other_japanese:
                # 和名から対応する学名をチェック
                if japanese_name in japanese_to_scientific and japanese_to_scientific[japanese_name] == other_scientific:
                    match = True
            elif scientific_name and other_japanese and not japanese_name:
                # 学名から対応する和名をチェック
                if scientific_name in scientific_to_japanese and scientific_to_japanese[scientific_name] == other_japanese:
                    match = True
            # 4. 近接行での補完的なマッチング（より慎重に）
            elif abs(i - j) <= 3:  # 近い行での候補を確認（範囲を狭める）
                if (japanese_name and other_scientific and not other_japanese) or (scientific_name and other_japanese and not japanese_name):
                    match = True
                    
            if match:
                candidates.append(j)
        
        # 複数の候補がある場合は統合
        if len(candidates) > 1:
            print(f"統合対象発見: 行 {[c+2 for c in candidates]} - {japanese_name or scientific_name}")
            duplicates_found += len(candidates) - 1
            
            # ベース行を選択（最も完全な分類情報を持つ行）
            base_idx = None
            best_score = -1
            
            for idx in candidates:
                row_candidate = rows[idx]
                # 分類情報の完全性をスコア化
                score = sum([1 for i in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17] if i < len(row_candidate) and row_candidate[i].strip()])
                if score > best_score:
                    best_score = score
                    base_idx = idx
            
            base_row = rows[base_idx][:]
            
            # 食草データを統合
            food_plants = []
            
            for idx in candidates:
                candidate_row = rows[idx]
                # 食草データを抽出（27列目から7列ずつ、最大10個）
                for plant_idx in range(26, min(len(candidate_row), 96), 7):
                    if plant_idx < len(candidate_row) and candidate_row[plant_idx].strip():
                        plant_name = candidate_row[plant_idx].strip()
                        # 重複チェック
                        if not any(fp['name'] == plant_name for fp in food_plants):
                            food_plants.append({
                                'name': plant_name,
                                'family': candidate_row[plant_idx+1] if plant_idx+1 < len(candidate_row) else '',
                                'observation': candidate_row[plant_idx+2] if plant_idx+2 < len(candidate_row) else '',
                                'part': candidate_row[plant_idx+3] if plant_idx+3 < len(candidate_row) else '',
                                'stage': candidate_row[plant_idx+4] if plant_idx+4 < len(candidate_row) else '',
                                'reference': candidate_row[plant_idx+5] if plant_idx+5 < len(candidate_row) else '',
                                'notes': candidate_row[plant_idx+6] if plant_idx+6 < len(candidate_row) else ''
                            })
            
            # 統合された行を作成
            merged_row = base_row[:26]  # 基本情報部分
            
            # 食草データ部分をクリア
            while len(merged_row) < 96:
                merged_row.append('')
            
            # 統合した食草データを追加（最大10個）
            for i, fp in enumerate(food_plants[:10]):
                base_idx = 26 + i * 7
                if base_idx + 6 < len(merged_row):
                    merged_row[base_idx] = fp['name']
                    merged_row[base_idx + 1] = fp['family']
                    merged_row[base_idx + 2] = fp['observation']
                    merged_row[base_idx + 3] = fp['part']
                    merged_row[base_idx + 4] = fp['stage']
                    merged_row[base_idx + 5] = fp['reference']
                    merged_row[base_idx + 6] = fp['notes']
            
            # 残りの列をベース行からコピー
            if len(base_row) > 96:
                merged_row.extend(base_row[96:])
            
            # ヘッダー数に合わせる
            while len(merged_row) < len(headers):
                merged_row.append('')
            
            merged_rows.append(merged_row)
            
            # 処理済みとしてマーク
            for idx in candidates:
                processed_rows.add(idx)
        else:
            # 統合対象なし
            merged_rows.append(row)
            processed_rows.add(i)
    
    # 結果を書き出し
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(merged_rows)
    
    print(f"統合完了: {duplicates_found}件の重複を解決")
    print(f"統合前: {len(rows)}行")
    print(f"統合後: {len(merged_rows)}行")
    print(f"出力ファイル: {output_file}")

if __name__ == "__main__":
    merge_species_data()