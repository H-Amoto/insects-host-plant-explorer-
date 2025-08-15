#!/usr/bin/env python3
import csv
from collections import defaultdict, Counter

def analyze_data_quality():
    """データ品質の詳細分析"""
    file_path = '/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master_backup_combined.csv'
    
    # 分析用のカウンター
    catalog_nos = []
    scientific_names = []
    japanese_names = []
    hostplant_patterns = []
    general_notes = []
    
    print("=== データ品質分析開始 ===")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(reader, 2):
                catalog_no = row.get('大図鑑カタログNo', '').strip()
                scientific_name = row.get('学名', '').strip() 
                japanese_name = row.get('和名', '').strip()
                hostplant = row.get('食草', '').strip()
                notes = row.get('備考', '').strip()
                
                # データ収集
                catalog_nos.append(catalog_no)
                scientific_names.append(scientific_name)
                japanese_names.append(japanese_name)
                hostplant_patterns.append(hostplant)
                
                # 総合備考の候補を探す
                if notes and notes not in ['日本産蛾類標準図鑑2', '日本産蛾類標準図鑑3', '日本のハマキガ1']:
                    if len(notes) > 30:  # 長い備考は総合備考の可能性
                        general_notes.append((japanese_name, notes))
        
        # 統計出力
        print(f"\n=== 基本統計 ===")
        print(f"総レコード数: {len(catalog_nos)}")
        print(f"カタログNo空白: {catalog_nos.count('')}")
        print(f"学名空白: {scientific_names.count('')}")
        print(f"和名空白: {japanese_names.count('')}")
        
        # 重複分析
        print(f"\n=== 重複分析 ===")
        scientific_counter = Counter([name for name in scientific_names if name])
        japanese_counter = Counter([name for name in japanese_names if name])
        
        print(f"学名重複件数: {sum(1 for count in scientific_counter.values() if count > 1)}")
        print(f"和名重複件数: {sum(1 for count in japanese_counter.values() if count > 1)}")
        
        print(f"\n=== 学名重複例（上位5件）===")
        for name, count in scientific_counter.most_common(10):
            if count > 1:
                print(f"{name}: {count}件")
        
        print(f"\n=== 和名重複例（上位5件）===")
        for name, count in japanese_counter.most_common(10):
            if count > 1:
                print(f"{name}: {count}件")
        
        # 食草パターン分析
        print(f"\n=== 食草パターン分析 ===")
        unknown_count = sum(1 for hp in hostplant_patterns if hp in ['不明', ''])
        single_count = sum(1 for hp in hostplant_patterns if hp not in ['不明', ''] and ';' not in hp)
        multiple_count = sum(1 for hp in hostplant_patterns if ';' in hp)
        
        print(f"食草不明・空白: {unknown_count}")
        print(f"食草単一: {single_count}")  
        print(f"食草複数: {multiple_count}")
        
        # 複数食草の例
        print(f"\n=== 複数食草の例（上位5件）===")
        multiple_hostplants = [(hp, hp.count(';')+1) for hp in hostplant_patterns if ';' in hp]
        multiple_hostplants.sort(key=lambda x: x[1], reverse=True)
        
        for hp, count in multiple_hostplants[:5]:
            print(f"{count}種の食草: {hp[:100]}...")
        
        # 総合備考の候補
        print(f"\n=== 総合備考候補（上位5件）===")
        for japanese_name, note in general_notes[:5]:
            print(f"{japanese_name}: {note[:100]}...")
            
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    analyze_data_quality()