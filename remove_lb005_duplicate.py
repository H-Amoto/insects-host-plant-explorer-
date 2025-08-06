#!/usr/bin/env python3
"""
626行目のLB005（ネクイハムシ）重複エントリを削除するスクリプト
"""

import csv

def remove_lb005_duplicate():
    print("626行目のLB005重複エントリ削除を開始します...")
    
    input_file = "public/hamushi_integrated_master.csv"
    output_file = "hamushi_integrated_master_lb005_removed.csv"
    
    data = []
    headers = []
    
    # CSVファイルを読み込み
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            data.append(row)
    
    print(f"読み込み完了: {len(data)}行")
    
    # LB005行を特定して削除
    removed_count = 0
    filtered_data = []
    
    for i, row in enumerate(data):
        if row.get('大図鑑カタログNo') == 'LB005':
            print(f"削除対象発見: 行{i+2} - {row.get('和名')} ({row.get('学名')})")
            removed_count += 1
            continue  # この行をスキップ
        else:
            filtered_data.append(row)
    
    # ファイル出力
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(filtered_data)
    
    print(f"\\n削除完了:")
    print(f"- 削除前: {len(data)}行")
    print(f"- 削除後: {len(filtered_data)}行")
    print(f"- 削除数: {removed_count}行")
    print(f"- 出力ファイル: {output_file}")
    
    return output_file

if __name__ == "__main__":
    remove_lb005_duplicate()