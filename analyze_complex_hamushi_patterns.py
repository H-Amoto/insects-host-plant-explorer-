#!/usr/bin/env python3
import csv
import re
import os

def analyze_complex_hamushi_patterns():
    """ハムシ.csvの複雑なパターンを詳細分析してhostplants.csvとの不一致を検出"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== ハムシの複雑パターン詳細分析 ===")
    
    # ファイル
    hamushi_file = os.path.join(base_dir, 'public', 'ハムシ.csv')
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    insects_file = os.path.join(base_dir, 'public', 'insects.csv')
    
    # 1. ハムシ.csvから複雑パターンを抽出
    print("\n=== 複雑パターン抽出 ===")
    
    complex_cases = []
    
    with open(hamushi_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダーをスキップ
        
        for row_num, row in enumerate(reader, 2):
            if len(row) >= 3:
                japanese_name = row[0].split('、')[0].strip()
                scientific_name = row[1].split('、')[0].strip() if len(row) > 1 else ""
                food_plants = row[2].strip().strip('""')
                
                # 複雑なパターンを検出
                has_multiple_parts = False
                parts_found = []
                
                if 'の実' in food_plants:
                    parts_found.append('実')
                if 'の花' in food_plants:
                    parts_found.append('花')
                if 'の根' in food_plants:
                    parts_found.append('根')
                if 'の種子' in food_plants:
                    parts_found.append('種子')
                if 'の葉' in food_plants:
                    parts_found.append('葉')
                if 'の新芽' in food_plants:
                    parts_found.append('新芽')
                if 'の果実' in food_plants:
                    parts_found.append('果実')
                
                # 複数の部位が混在するか、「など」を含む複雑なケース
                if len(parts_found) > 1 or ('など' in food_plants and len(parts_found) >= 1):
                    complex_cases.append({
                        'row': row_num,
                        'japanese_name': japanese_name,
                        'scientific_name': scientific_name,
                        'food_plants': food_plants,
                        'parts_found': parts_found
                    })
    
    print(f"複雑パターン数: {len(complex_cases)}件")
    
    # 2. insects.csvから和名→insect_idマッピング
    name_to_id = {}
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['family'] == 'Chrysomelidae':  # ハムシ科のみ
                name_to_id[row['japanese_name'].strip()] = row['insect_id']
    
    # 3. hostplants.csvの現在の状況
    hostplants_data = {}
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            insect_id = row['insect_id']
            if insect_id not in hostplants_data:
                hostplants_data[insect_id] = []
            hostplants_data[insect_id].append({
                'plant_name': row['plant_name'],
                'plant_part': row['plant_part']
            })
    
    # 4. 詳細分析
    print("\n=== 詳細分析結果 ===")
    
    needs_review = []
    
    for case in complex_cases[:10]:  # 最初の10件を詳細分析
        name = case['japanese_name']
        food_plants = case['food_plants']
        
        if name in name_to_id:
            insect_id = name_to_id[name]
            
            print(f"\n{case['row']}行目: {name}")
            print(f"  元データ: {food_plants}")
            print(f"  検出部位: {case['parts_found']}")
            print(f"  ID: {insect_id}")
            
            if insect_id in hostplants_data:
                print("  現在のhostplants.csv:")
                for entry in hostplants_data[insect_id]:
                    print(f"    {entry['plant_name']}: {entry['plant_part']}")
                
                # パターン解析
                if 'の実' in food_plants and 'の花' in food_plants:
                    print("  → 実と花が混在するパターン")
                elif 'など' in food_plants and len(case['parts_found']) == 1:
                    print(f"  → 「など」を含む{case['parts_found'][0]}食性パターン")
                elif len(case['parts_found']) > 1:
                    print(f"  → 複数部位パターン: {', '.join(case['parts_found'])}")
                
                needs_review.append(case)
            else:
                print("  ⚠️ hostplants.csvにデータなし")
    
    # 5. 修正が必要そうなケースの特定
    print(f"\n=== 修正候補の特定 ===")
    
    potential_fixes = []
    
    for case in complex_cases:
        name = case['japanese_name']
        food_plants = case['food_plants']
        
        # 特定のパターンを解析
        if 'の実' in food_plants and ('、' in food_plants or 'など' in food_plants):
            # 「Xの実、Y、Z」パターン
            if '、' in food_plants:
                parts = food_plants.split('、')
                fruit_part = [p for p in parts if 'の実' in p]
                other_parts = [p for p in parts if 'の実' not in p and p.strip()]
                
                if fruit_part and other_parts:
                    potential_fixes.append({
                        'name': name,
                        'pattern': 'fruit_and_others',
                        'fruit_plants': fruit_part,
                        'other_plants': other_parts,
                        'original': food_plants
                    })
        
        elif 'の花' in food_plants and ('、' in food_plants or 'など' in food_plants):
            # 「X、Y、Zなどの花」パターン  
            if food_plants.endswith('などの花') or food_plants.endswith('の花'):
                potential_fixes.append({
                    'name': name,
                    'pattern': 'multiple_flowers',
                    'original': food_plants
                })
    
    print(f"修正候補: {len(potential_fixes)}件")
    
    for fix in potential_fixes[:5]:
        print(f"\n候補: {fix['name']}")
        print(f"  パターン: {fix['pattern']}")
        print(f"  元データ: {fix['original']}")
    
    # 6. 優先修正リスト
    print(f"\n=== 優先修正リスト ===")
    
    priority_fixes = [
        "ナガハムシ",  # ハシドイ、オオカメノキの花など
        "サムライマメゾウムシ",  # ヤマハギの実、ニセアカシアなどの花
        "エンジュマメゾウムシ",  # エンジュ、マユミなどの花
        "イクビマメゾウムシ",  # コクララの実、フジマメ、ヒルガオ、カエデ、ウツギ、ミズキなどの花
        "イネネクイハムシ",  # ジュンサイ、コウホネ、ヒルムシロ、ヒツジグサ、ヒシ、イネの根
        "スゲハムシ",  # スゲ類、ハリイ類、各種の花
        "キンイロネクイハムシ"  # ミクリ類、スゲ類の花
    ]
    
    print("優先的に確認・修正すべき種:")
    for name in priority_fixes:
        if name in name_to_id:
            insect_id = name_to_id[name]
            found_case = next((c for c in complex_cases if c['japanese_name'] == name), None)
            if found_case:
                print(f"\n{name} ({insect_id}):")
                print(f"  元データ: {found_case['food_plants']}")
                if insect_id in hostplants_data:
                    print("  現在の状況:")
                    for entry in hostplants_data[insect_id]:
                        print(f"    {entry['plant_name']}: {entry['plant_part']}")
    
    print(f"\n📋 複雑パターン分析が完了しました！")

if __name__ == "__main__":
    analyze_complex_hamushi_patterns()