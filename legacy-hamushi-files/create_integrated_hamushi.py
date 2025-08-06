#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys
from collections import defaultdict

def create_integrated_hamushi_csv():
    """
    leafbeetle_hostplants.csvとhamushi_species_integrated.csvを統合
    優先順位: ハムシハンドブック > 目録データベース
    """
    
    # 統合データ格納用
    integrated_data = {}
    
    # Phase 1: leafbeetle_hostplants.csv（ハムシハンドブック、高品質）を読み込み
    print("Phase 1: leafbeetle_hostplants.csvを読み込み中...")
    with open('/Users/akimotohiroki/insects-host-plant-explorer/leafbeetle_fixed.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            species_name = row['和名'].strip()
            if species_name:
                # 食草情報のクリーンアップ（余分な"を削除）
                host_plants = row['食草'].strip().replace('""', '"').strip('"')
                
                integrated_data[species_name] = {
                    'japanese_name': species_name,
                    'scientific_name': row['学名'].strip(),
                    'family': 'ハムシ科',  # すべてハムシ科
                    'subfamily': '',  # leafbeetleには亜科情報なし
                    'host_plants': host_plants,
                    'emergence_time': '',  # leafbeetleには発生時期なし
                    'remarks': '',
                    'source': 'ハムシハンドブック',
                    'quality': 'A',  # 高品質
                    'origin': 'leafbeetle'
                }
    
    print(f"leafbeetle由来: {len(integrated_data)}種")
    
    # Phase 2: hamushi_species_integrated.csvを読み込み、重複しない種のみ追加
    print("Phase 2: hamushi_species_integrated.csvを読み込み中...")
    added_from_hamushi = 0
    skipped_duplicates = 0
    
    with open('/Users/akimotohiroki/insects-host-plant-explorer/public/hamushi_species_integrated.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            species_name = row['和名'].strip()
            if species_name and species_name not in integrated_data:
                # 重複しない種のみ追加
                source = row.get('出典', '').strip()
                quality = 'A' if 'ハムシハンドブック' in source else 'B'
                
                integrated_data[species_name] = {
                    'japanese_name': species_name,
                    'scientific_name': row['学名'].strip(),
                    'family': row.get('科和名', '').strip(),
                    'subfamily': row.get('亜科和名', '').strip(),
                    'host_plants': row.get('食草', '').strip(),
                    'emergence_time': row.get('成虫出現時期', '').strip(),
                    'remarks': row.get('備考', '').strip(),
                    'source': source if source else 'ハムシ目録データベース',
                    'quality': quality,
                    'origin': 'hamushi'
                }
                added_from_hamushi += 1
            elif species_name:
                skipped_duplicates += 1
    
    print(f"hamushi由来追加: {added_from_hamushi}種")
    print(f"重複によりスキップ: {skipped_duplicates}種")
    print(f"統合後総種数: {len(integrated_data)}種")
    
    # Phase 3: 統合CSVファイル出力
    print("Phase 3: 統合CSVファイルを出力中...")
    output_path = '/Users/akimotohiroki/insects-host-plant-explorer/public/hamushi_integrated_master.csv'
    
    # 品質順、種名順でソート
    sorted_species = sorted(integrated_data.items(), key=lambda x: (x[1]['quality'], x[0]))
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = [
            '和名', '学名', '科名', '亜科名', '食草', '成虫出現時期', 
            '備考', '出典', '品質レベル', '由来ファイル'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for species_name, data in sorted_species:
            writer.writerow({
                '和名': data['japanese_name'],
                '学名': data['scientific_name'],
                '科名': data['family'],
                '亜科名': data['subfamily'],
                '食草': data['host_plants'],
                '成虫出現時期': data['emergence_time'],
                '備考': data['remarks'],
                '出典': data['source'],
                '品質レベル': data['quality'],
                '由来ファイル': data['origin']
            })
    
    print(f"統合ファイル作成完了: {output_path}")
    
    # 統計情報出力
    quality_a_count = sum(1 for d in integrated_data.values() if d['quality'] == 'A')
    quality_b_count = sum(1 for d in integrated_data.values() if d['quality'] == 'B')
    leafbeetle_count = sum(1 for d in integrated_data.values() if d['origin'] == 'leafbeetle')
    hamushi_count = sum(1 for d in integrated_data.values() if d['origin'] == 'hamushi')
    
    print(f"\n=== 統合結果 ===")
    print(f"総種数: {len(integrated_data)}種")
    print(f"品質A（ハムシハンドブック由来）: {quality_a_count}種")
    print(f"品質B（目録データベース由来）: {quality_b_count}種")
    print(f"leafbeetle由来: {leafbeetle_count}種")
    print(f"hamushi由来: {hamushi_count}種")
    
    return output_path

if __name__ == "__main__":
    create_integrated_hamushi_csv()