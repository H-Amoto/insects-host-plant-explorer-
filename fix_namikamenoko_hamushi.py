#!/usr/bin/env python3
"""
ナミカメノコハムシの修正と669行目（LB109）の削除スクリプト
"""

import csv

def fix_namikamenoko_hamushi():
    print("ナミカメノコハムシの修正と669行目削除を開始します...")
    
    input_file = "public/hamushi_integrated_master.csv"
    output_file = "hamushi_integrated_master_namikamenoko_fixed.csv"
    
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
    removed_count = 0
    filtered_data = []
    
    for i, row in enumerate(data):
        # LB109（カメノコハムシ）の重複エントリを削除
        if row.get('大図鑑カタログNo') == 'LB109':
            print(f"削除対象: 行{i+2} - {row.get('和名')} ({row.get('学名')})")
            removed_count += 1
            continue  # この行をスキップ
        
        # ナミカメノコハムシ（H453）を修正
        elif row.get('和名') == 'ナミカメノコハムシ':
            print(f"\\n修正対象: 行{i+2} - {row.get('和名')}")
            
            # 別名にカメノコハムシを追加
            row['別名'] = 'カメノコハムシ'
            print(f"  別名追加: カメノコハムシ")
            
            # 食草を修正
            row['食草'] = 'アカザ、シロザ'
            print(f"  食草修正: アカザ、シロザ")
            
            # 出典をハムシハンドブックに修正
            row['出典'] = 'ハムシハンドブック, 著者: 尾園暁, 出版社: 文一総合出版, 発行年: 2014'
            print(f"  出典修正: ハムシハンドブック")
            
            # 品質をAに変更
            row['備考'] = '[品質A(ハンドブック)]'
            print(f"  品質変更: A(ハンドブック)")
            
            updated_count += 1
            filtered_data.append(row)
        
        else:
            filtered_data.append(row)
    
    # ファイル出力
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(filtered_data)
    
    print(f"\\n処理完了:")
    print(f"- 修正したナミカメノコハムシ: {updated_count}件")
    print(f"- 削除した重複エントリ: {removed_count}件")
    print(f"- 処理前: {len(data)}行")
    print(f"- 処理後: {len(filtered_data)}行")
    print(f"- 出力ファイル: {output_file}")
    
    return output_file

if __name__ == "__main__":
    fix_namikamenoko_hamushi()