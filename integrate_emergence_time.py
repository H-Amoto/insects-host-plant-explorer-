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
                }\n    \n    print(f\"統合前hamushi成虫出現時期データ: {len(hamushi_emergence)}種\")\n    \n    # ListMJファイルを処理\n    print(\"\\nListMJファイルを処理中...\")\n    listmj_data = []\n    listmj_columns = []\n    matched_count = 0\n    \n    with open(listmj_path, 'r', encoding='utf-8') as f:\n        reader = csv.DictReader(f)\n        listmj_columns = reader.fieldnames\n        \n        for row in reader:\n            wamei = row.get('和名', '').strip()\n            \n            # 成虫出現時期関連の列を追加\n            row['成虫出現時期'] = ''\n            row['成虫出現時期出典'] = ''\n            row['成虫出現時期備考'] = ''\n            \n            # データがあればマッチング\n            if wamei in emergence_data:\n                row.update(emergence_data[wamei])\n                matched_count += 1\n            elif wamei in hamushi_emergence:\n                row.update(hamushi_emergence[wamei])\n                matched_count += 1\n            \n            listmj_data.append(row)\n    \n    # 新しい列構造を定義\n    new_listmj_columns = listmj_columns + ['成虫出現時期', '成虫出現時期出典', '成虫出現時期備考']\n    \n    # ListMJファイル出力\n    with open(output_listmj, 'w', encoding='utf-8', newline='') as f:\n        writer = csv.DictWriter(f, fieldnames=new_listmj_columns)\n        writer.writeheader()\n        writer.writerows(listmj_data)\n    \n    print(f\"ListMJ処理完了:\")\n    print(f\"- 総種数: {len(listmj_data)}種\")\n    print(f\"- 成虫出現時期マッチ: {matched_count}種\")\n    print(f\"- 出力: {output_listmj}\")\n    \n    # ハムシファイルを処理\n    print(\"\\nハムシファイルを処理中...\")\n    hamushi_data = []\n    hamushi_columns = []\n    hamushi_matched = 0\n    \n    with open(hamushi_path, 'r', encoding='utf-8') as f:\n        reader = csv.DictReader(f)\n        hamushi_columns = reader.fieldnames\n        \n        for row in reader:\n            wamei = row.get('和名', '').strip()\n            \n            # 成虫出現時期関連の列を追加\n            row['成虫出現時期'] = ''\n            row['成虫出現時期出典'] = ''\n            row['成虫出現時期備考'] = ''\n            \n            # データがあればマッチング（優先順位: emergence_data > hamushi_emergence）\n            if wamei in emergence_data:\n                row.update(emergence_data[wamei])\n                hamushi_matched += 1\n            elif wamei in hamushi_emergence:\n                row.update(hamushi_emergence[wamei])\n                hamushi_matched += 1\n            \n            hamushi_data.append(row)\n    \n    # 新しい列構造を定義\n    new_hamushi_columns = hamushi_columns + ['成虫出現時期', '成虫出現時期出典', '成虫出現時期備考']\n    \n    # ハムシファイル出力\n    with open(output_hamushi, 'w', encoding='utf-8', newline='') as f:\n        writer = csv.DictWriter(f, fieldnames=new_hamushi_columns)\n        writer.writeheader()\n        writer.writerows(hamushi_data)\n    \n    print(f\"ハムシ処理完了:\")\n    print(f\"- 総種数: {len(hamushi_data)}種\")\n    print(f\"- 成虫出現時期マッチ: {hamushi_matched}種\")\n    print(f\"- 出力: {output_hamushi}\")\n    \n    # サンプルデータを表示\n    print(f\"\\n=== 成虫出現時期統合サンプル ===\")\n    for i, row in enumerate(listmj_data[:3]):\n        if row.get('成虫出現時期'):\n            print(f\"ListMJ {i+1}. {row.get('和名', 'N/A')} - {row.get('成虫出現時期', 'N/A')} ({row.get('成虫出現時期出典', 'N/A')})\")\n    \n    for i, row in enumerate(hamushi_data[:3]):\n        if row.get('成虫出現時期'):\n            print(f\"ハムシ {i+1}. {row.get('和名', 'N/A')} - {row.get('成虫出現時期', 'N/A')} ({row.get('成虫出現時期出典', 'N/A')})\")\n    \n    print(f\"\\n統合完了: ListMJ {len(new_listmj_columns)}列, ハムシ {len(new_hamushi_columns)}列\")\n    \n    return output_listmj, output_hamushi\n\nif __name__ == \"__main__\":\n    integrate_emergence_time()