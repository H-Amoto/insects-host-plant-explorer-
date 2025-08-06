#!/usr/bin/env python3
"""
成虫出現時期データをListMJとハムシファイルの両方に統合するスクリプト
"""

import csv
import os

def integrate_emergence_time():
    print("成虫出現時期統合を開始します...")
    
    # ファイルパス
    emergence_path = "public/emergence_time_integrated.csv"
    listmj_path = "public/ListMJ_hostplants_master.csv"
    hamushi_path = "hamushi_integrated_master.csv"
    legacy_hamushi_path = "legacy-local-hamushi-files/hamushi_species_integrated.csv"
    
    output_listmj = "ListMJ_hostplants_master_with_emergence.csv"
    output_hamushi = "hamushi_integrated_master_with_emergence.csv"
    
    # 成虫出現時期データを読み込み
    emergence_data = {}
    with open(emergence_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            wamei = row.get('和名', '').strip()
            if wamei:
                emergence_data[wamei] = {
                    '成虫出現時期': row.get('成虫出現時期', '').strip(),
                    '成虫出現時期出典': row.get('出典', '').strip(),
                    '成虫出現時期備考': row.get('備考', '').strip()
                }
    
    print(f"成虫出現時期データ: {len(emergence_data)}種")
    
    # 統合前hamushiファイルから成虫出現時期データも取得
    hamushi_emergence = {}
    with open(legacy_hamushi_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            wamei = row.get('和名', '').strip()
            emergence_time = row.get('成虫出現時期', '').strip()
            if wamei and emergence_time:
                hamushi_emergence[wamei] = {
                    '成虫出現時期': emergence_time,
                    '成虫出現時期出典': row.get('出典', '').strip(),
                    '成虫出現時期備考': ''
                }
    
    print(f"統合前hamushi成虫出現時期データ: {len(hamushi_emergence)}種")
    
    # ListMJファイルを処理
    print("\nListMJファイルを処理中...")
    listmj_data = []
    listmj_columns = []
    matched_count = 0
    
    with open(listmj_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        listmj_columns = reader.fieldnames
        
        for row in reader:
            wamei = row.get('和名', '').strip()
            
            # 成虫出現時期関連の列を追加
            row['成虫出現時期'] = ''
            row['成虫出現時期出典'] = ''
            row['成虫出現時期備考'] = ''
            
            # データがあればマッチング
            if wamei in emergence_data:
                row.update(emergence_data[wamei])
                matched_count += 1
            elif wamei in hamushi_emergence:
                row.update(hamushi_emergence[wamei])
                matched_count += 1
            
            listmj_data.append(row)
    
    # 新しい列構造を定義
    new_listmj_columns = listmj_columns + ['成虫出現時期', '成虫出現時期出典', '成虫出現時期備考']
    
    # ListMJファイル出力
    with open(output_listmj, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=new_listmj_columns)
        writer.writeheader()
        writer.writerows(listmj_data)
    
    print(f"ListMJ処理完了:")
    print(f"- 総種数: {len(listmj_data)}種")
    print(f"- 成虫出現時期マッチ: {matched_count}種")
    print(f"- 出力: {output_listmj}")
    
    # ハムシファイルを処理
    print("\nハムシファイルを処理中...")
    hamushi_data = []
    hamushi_columns = []
    hamushi_matched = 0
    
    with open(hamushi_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        hamushi_columns = reader.fieldnames
        
        for row in reader:
            wamei = row.get('和名', '').strip()
            
            # 成虫出現時期関連の列を追加
            row['成虫出現時期'] = ''
            row['成虫出現時期出典'] = ''
            row['成虫出現時期備考'] = ''
            
            # データがあればマッチング（優先順位: emergence_data > hamushi_emergence）
            if wamei in emergence_data:
                row.update(emergence_data[wamei])
                hamushi_matched += 1
            elif wamei in hamushi_emergence:
                row.update(hamushi_emergence[wamei])
                hamushi_matched += 1
            
            hamushi_data.append(row)
    
    # 新しい列構造を定義
    new_hamushi_columns = hamushi_columns + ['成虫出現時期', '成虫出現時期出典', '成虫出現時期備考']
    
    # ハムシファイル出力
    with open(output_hamushi, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=new_hamushi_columns)
        writer.writeheader()
        writer.writerows(hamushi_data)
    
    print(f"ハムシ処理完了:")
    print(f"- 総種数: {len(hamushi_data)}種")
    print(f"- 成虫出現時期マッチ: {hamushi_matched}種")
    print(f"- 出力: {output_hamushi}")
    
    # サンプルデータを表示
    print(f"\n=== 成虫出現時期統合サンプル ===")
    emergence_samples = [row for row in listmj_data if row.get('成虫出現時期')]
    for i, row in enumerate(emergence_samples[:3]):
        print(f"ListMJ {i+1}. {row.get('和名', 'N/A')} - {row.get('成虫出現時期', 'N/A')} ({row.get('成虫出現時期出典', 'N/A')})")
    
    hamushi_emergence_samples = [row for row in hamushi_data if row.get('成虫出現時期')]
    for i, row in enumerate(hamushi_emergence_samples[:3]):
        print(f"ハムシ {i+1}. {row.get('和名', 'N/A')} - {row.get('成虫出現時期', 'N/A')} ({row.get('成虫出現時期出典', 'N/A')})")
    
    print(f"\n統合完了: ListMJ {len(new_listmj_columns)}列, ハムシ {len(new_hamushi_columns)}列")
    
    return output_listmj, output_hamushi

if __name__ == "__main__":
    integrate_emergence_time()