#!/usr/bin/env python3
"""
ハムシハンドブックの出典表記を統一するスクリプト
"""

import csv

def standardize_handbook_citation():
    print("ハムシハンドブックの出典表記統一を開始します...")
    
    # 標準的な出典表記
    standard_citation = "ハムシハンドブック, 著者: 尾園暁, 出版社: 文一総合出版, 発行年: 2014"
    
    input_file = "public/hamushi_integrated_master.csv"
    output_file = "hamushi_integrated_master_citation_standardized.csv"
    
    data = []
    headers = []
    
    # CSVファイルを読み込み
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            data.append(row)
    
    print(f"読み込み完了: {len(data)}行")
    
    updated_count = 0
    
    # ハムシハンドブック関連の表記パターン
    handbook_patterns = [
        "ハムシハンドブック",
        "ハムシハンドブック, 著者: 尾園暁, 出版社: 文一総合出版, 発行年: 2014"
    ]
    
    for i, row in enumerate(data):
        line_number = i + 2  # CSVの行番号（ヘッダーを除く）
        updated_this_row = False
        
        # 出典フィールドをチェック
        if row.get('出典'):
            current_citation = row.get('出典')
            if any(pattern in current_citation for pattern in handbook_patterns):
                if current_citation != standard_citation:
                    print(f"行{line_number}: 出典統一")
                    print(f"  変更前: {current_citation}")
                    print(f"  変更後: {standard_citation}")
                    row['出典'] = standard_citation
                    updated_this_row = True
        
        # 成虫出現時期出典フィールドもチェック
        if row.get('成虫出現時期出典'):
            current_emergence_citation = row.get('成虫出現時期出典')
            if any(pattern in current_emergence_citation for pattern in handbook_patterns):
                if current_emergence_citation != standard_citation:
                    print(f"行{line_number}: 成虫出現時期出典統一")
                    print(f"  変更前: {current_emergence_citation}")
                    print(f"  変更後: {standard_citation}")
                    row['成虫出現時期出典'] = standard_citation
                    updated_this_row = True
        
        if updated_this_row:
            updated_count += 1
    
    # ファイル出力
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"\\n統一完了:")
    print(f"- 更新した行数: {updated_count}行")
    print(f"- 標準出典: {standard_citation}")
    print(f"- 出力ファイル: {output_file}")
    
    return output_file

if __name__ == "__main__":
    standardize_handbook_citation()