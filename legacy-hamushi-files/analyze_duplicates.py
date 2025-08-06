#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys
from collections import defaultdict

def analyze_leafbeetle_files():
    """
    leafbeetle_hostplants.csvとhamushi_species_integrated.csvを分析
    重複種を特定し、統合戦略を策定
    """
    
    # leafbeetle_hostplants.csvを読み込み
    leafbeetle_data = {}
    with open('/Users/akimotohiroki/insects-host-plant-explorer/leafbeetle_fixed.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            species_name = row['和名'].strip()
            if species_name:  # 空でない場合のみ
                leafbeetle_data[species_name] = {
                    'scientific_name': row['学名'].strip(),
                    'host_plants': row['食草'].strip(),
                    'source': 'ハムシハンドブック',
                    'quality': 'A'  # 高品質
                }
    
    # hamushi_species_integrated.csvを読み込み
    hamushi_data = {}
    hamushi_handbook_count = 0
    hamushi_db_count = 0
    
    with open('/Users/akimotohiroki/insects-host-plant-explorer/public/hamushi_species_integrated.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            species_name = row['和名'].strip()
            if species_name:  # 空でない場合のみ
                source = row.get('出典', '').strip()
                if 'ハムシハンドブック' in source:
                    hamushi_handbook_count += 1
                    quality = 'A'
                else:
                    hamushi_db_count += 1
                    quality = 'B'  # 暫定的
                
                hamushi_data[species_name] = {
                    'scientific_name': row['学名'].strip(),
                    'host_plants': row.get('食草', '').strip(),
                    'emergence_time': row.get('成虫出現時期', '').strip(),
                    'remarks': row.get('備考', '').strip(),
                    'source': source,
                    'quality': quality,
                    'family': row.get('科和名', '').strip(),
                    'subfamily': row.get('亜科和名', '').strip()
                }
    
    # 重複分析
    duplicates = []
    leafbeetle_only = []
    hamushi_only = []
    
    for species in leafbeetle_data:
        if species in hamushi_data:
            duplicates.append(species)
        else:
            leafbeetle_only.append(species)
    
    for species in hamushi_data:
        if species not in leafbeetle_data:
            hamushi_only.append(species)
    
    # 結果出力
    print("=== ハムシデータ統合分析結果 ===")
    print(f"leafbeetle_hostplants.csv: {len(leafbeetle_data)}種 (すべてハムシハンドブック由来)")
    print(f"hamushi_species_integrated.csv: {len(hamushi_data)}種")
    print(f"  - ハムシハンドブック由来: {hamushi_handbook_count}種")
    print(f"  - ハムシ目録データベース由来: {hamushi_db_count}種")
    print()
    print(f"重複種: {len(duplicates)}種")
    print(f"leafbeetleのみ: {len(leafbeetle_only)}種")
    print(f"hamushiのみ: {len(hamushi_only)}種")
    print()
    
    # 重複種の詳細分析
    print("=== 重複種の比較 ===")
    for species in duplicates[:5]:  # 最初の5種のみ表示
        print(f"\n【{species}】")
        lb = leafbeetle_data[species]
        hm = hamushi_data[species]
        print(f"leafbeetle: {lb['scientific_name']} | 食草: {lb['host_plants']}")
        print(f"hamushi: {hm['scientific_name']} | 食草: {hm['host_plants']} | 出典: {hm['source']}")
        
        # 食草情報の差異チェック
        if lb['host_plants'] != hm['host_plants']:
            print(f"  → 食草情報に差異あり")
    
    # 統合方針の提案
    print("\n=== 統合方針 ===")
    print("1. 重複種: leafbeetle_hostplants.csv(ハムシハンドブック)を優先")
    print("2. leafbeetleのみ: そのまま採用")
    print("3. hamushiのみ: ハムシハンドブック由来は採用、目録データベース由来は分類情報のみ採用")
    
    # 統合後の予想種数
    hamushi_handbook_only = [s for s in hamushi_only if hamushi_data[s]['quality'] == 'A']
    hamushi_db_only = [s for s in hamushi_only if hamushi_data[s]['quality'] == 'B']
    
    integrated_count = len(leafbeetle_data) + len(hamushi_handbook_only) + len(hamushi_db_only)
    print(f"\n統合後予想種数: {integrated_count}種")
    print(f"  - ハムシハンドブック品質: {len(leafbeetle_data) + len(hamushi_handbook_only)}種")
    print(f"  - 目録データベース品質: {len(hamushi_db_only)}種")
    
    return {
        'leafbeetle_data': leafbeetle_data,
        'hamushi_data': hamushi_data,
        'duplicates': duplicates,
        'leafbeetle_only': leafbeetle_only,
        'hamushi_only': hamushi_only,
        'hamushi_handbook_only': hamushi_handbook_only,
        'hamushi_db_only': hamushi_db_only
    }

if __name__ == "__main__":
    analyze_leafbeetle_files()