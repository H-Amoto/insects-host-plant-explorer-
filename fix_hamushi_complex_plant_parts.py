#!/usr/bin/env python3
import csv
import re
import os
import shutil

def fix_hamushi_complex_plant_parts():
    """元のハムシ.csvと比較してhostplants.csvの植物部位を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== ハムシの複雑な植物部位パターン修正開始 ===")
    
    # 元データファイルと現在のファイル
    hamushi_file = os.path.join(base_dir, 'public', 'ハムシ.csv')
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    insects_file = os.path.join(base_dir, 'public', 'insects.csv')
    
    # 1. 元のハムシ.csvから複雑なパターンを抽出
    print("\n=== 元データの複雑パターン分析 ===")
    
    complex_patterns = {}
    
    with open(hamushi_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダーをスキップ
        
        for row in reader:
            if len(row) >= 3:
                japanese_name = row[0].split('、')[0].strip()  # 和名の最初の部分
                scientific_name = row[1].split('、')[0].strip() if len(row) > 1 else ""
                food_plants = row[2].strip().strip('""')
                
                # 複雑なパターンを検出（複数の部位が混在）
                if ('の実' in food_plants and 'の花' in food_plants) or \
                   ('の根' in food_plants and ('、' in food_plants or 'など' in food_plants)) or \
                   ('の花' in food_plants and '、' in food_plants and not food_plants.endswith('の花')):
                    
                    complex_patterns[japanese_name] = {
                        'scientific_name': scientific_name,
                        'food_plants': food_plants
                    }
                    
                    print(f"\n複雑パターン発見: {japanese_name}")
                    print(f"  学名: {scientific_name}")
                    print(f"  食草: {food_plants}")
    
    print(f"\n複雑パターン総数: {len(complex_patterns)}件")
    
    # 2. insects.csvから和名→insect_idのマッピングを作成
    print("\n=== 昆虫IDマッピング作成 ===")
    
    name_to_id = {}
    
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            japanese_name = row['japanese_name'].strip()
            insect_id = row['insect_id']
            
            # ハムシ科で複雑パターンに該当するもの
            if row['family'] == 'Chrysomelidae' and japanese_name in complex_patterns:
                name_to_id[japanese_name] = insect_id
    
    print(f"マッピング作成完了: {len(name_to_id)}件")
    
    # 3. 具体的な修正ルールを定義
    print("\n=== 修正ルール定義 ===")
    
    fix_rules = {
        'イクビマメゾウムシ': {
            'insect_id': 'species-H355',
            'original': 'コクララの実、フジマメ、ヒルガオ、カエデ、ウツギ、ミズキなどの花',
            'corrections': {
                'コクララ': '実',
                'フジマメ': '花',
                'ヒルガオ': '花', 
                'カエデ': '花',
                'ウツギ': '花',
                'ミズキなど': '花'
            }
        },
        'サムライマメゾウムシ': {
            'insect_id': None,  # 後で検索
            'original': 'ヤマハギの実、ニセアカシアなどの花',
            'corrections': {
                'ヤマハギ': '実',
                'ニセアカシアなど': '花'
            }
        },
        'イネネクイハムシ': {
            'insect_id': None,  # 後で検索
            'original': 'ジュンサイ、コウホネ、ヒルムシロ、ヒツジグサ、ヒシ、イネの根',
            'corrections': {
                'ジュンサイ': '葉',  # 一般的に葉を食べる
                'コウホネ': '葉',
                'ヒルムシロ': '葉',
                'ヒツジグサ': '葉',
                'ヒシ': '葉',
                'イネ': '根'
            }
        }
    }
    
    # 不明なinsect_idを検索
    for name, rule in fix_rules.items():
        if rule['insect_id'] is None and name in name_to_id:
            rule['insect_id'] = name_to_id[name]
            print(f"{name} のID: {rule['insect_id']}")
    
    # 4. hostplants.csvを修正
    print("\n=== hostplants.csv修正実行 ===")
    
    hostplants_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            insect_id = row['insect_id']
            plant_name = row['plant_name']
            current_part = row['plant_part']
            
            # 修正ルールをチェック
            for name, rule in fix_rules.items():
                if insect_id == rule['insect_id']:
                    if plant_name in rule['corrections']:
                        correct_part = rule['corrections'][plant_name]
                        if current_part != correct_part:
                            print(f"\\n修正: {name} ({insect_id})")
                            print(f"  植物: {plant_name}")
                            print(f"  部位: '{current_part}' → '{correct_part}'")
                            print(f"  元データ: {rule['original']}")
                            
                            row['plant_part'] = correct_part
                            fix_count += 1
                        break
            
            hostplants_data.append(row)
    
    print(f"\\n修正結果: {fix_count}件")
    
    # 5. ファイルを保存
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if hostplants_data:
            writer = csv.DictWriter(file, fieldnames=hostplants_data[0].keys())
            writer.writeheader()
            writer.writerows(hostplants_data)
    
    # normalized_dataフォルダにもコピー
    src = hostplants_file
    dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    print("hostplants.csvを更新しました")
    
    # 6. 検証
    print(f"\\n=== 修正結果検証 ===")
    
    # 修正された項目を確認
    for name, rule in fix_rules.items():
        if rule['insect_id']:
            print(f"\\n{name} ({rule['insect_id']}):")
            
            with open(hostplants_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['insect_id'] == rule['insect_id']:
                        print(f"  {row['plant_name']}: {row['plant_part']}")
    
    # 7. 他の複雑パターンも分析
    print(f"\\n=== 他の複雑パターン分析 ===")
    
    other_patterns = []
    for name, data in complex_patterns.items():
        if name not in fix_rules:
            other_patterns.append((name, data))
    
    if other_patterns:
        print(f"修正未対応の複雑パターン ({len(other_patterns)}件):")
        for name, data in other_patterns[:5]:  # 最初の5件を表示
            print(f"  {name}: {data['food_plants']}")
        
        if len(other_patterns) > 5:
            print(f"  ... 他 {len(other_patterns) - 5}件")
    else:
        print("すべての複雑パターンが修正されました")
    
    print(f"\\n🔧 ハムシの複雑な植物部位パターン修正が完了しました！")

if __name__ == "__main__":
    fix_hamushi_complex_plant_parts()