#!/usr/bin/env python3
import csv
import os
import shutil

def fix_remaining_hamushi_parts():
    """残りのハムシの複雑な植物部位パターンを修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 残りのハムシ植物部位パターン修正 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # 修正ルール
    fix_rules = [
        {
            'name': 'ナガハムシ (species-H627)',
            'insect_id': 'species-H627',
            'original': 'ハシドイ、オオカメノキの花など',
            'fixes': [
                {'plant': 'ハシドイ', 'from': '葉', 'to': '花', 'reason': '元データでは「オオカメノキの花など」とあり、ハシドイも花を食べる'},
            ]
        },
        {
            'name': 'スゲハムシ (species-LB007)', 
            'insect_id': 'species-LB007',
            'original': 'スゲ類、ハリイ類、各種の花',
            'fixes': [
                {'plant': 'スゲ類', 'from': '葉', 'to': '花', 'reason': '元データでは「各種の花」とあり、スゲ類も花を食べる'},
            ]
        },
        {
            'name': 'エンジュマメゾウムシ (species-H373)',
            'insect_id': 'species-H373', 
            'original': 'エンジュ、マユミなどの花',
            'fixes': [
                # エンジュマメゾウムシのデータを確認してから追加
            ]
        }
    ]
    
    # hostplants.csvを読み込み、修正
    hostplants_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            insect_id = row['insect_id']
            plant_name = row['plant_name']
            current_part = row['plant_part']
            
            # 修正ルールをチェック
            for rule in fix_rules:
                if insect_id == rule['insect_id']:
                    for fix in rule['fixes']:
                        if plant_name == fix['plant'] and current_part == fix['from']:
                            print(f"\\n修正: {rule['name']}")
                            print(f"  植物: {plant_name}")
                            print(f"  部位: '{fix['from']}' → '{fix['to']}'")
                            print(f"  理由: {fix['reason']}")
                            print(f"  元データ: {rule['original']}")
                            
                            row['plant_part'] = fix['to']
                            fix_count += 1
                            break
                    break
            
            hostplants_data.append(row)
    
    print(f"\\n修正結果: {fix_count}件")
    
    # ファイルを保存
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
    
    # エンジュマメゾウムシの確認
    print(f"\\n=== エンジュマメゾウムシの確認 ===")
    
    engyu_entries = []
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['insect_id'] == 'species-H373':
                engyu_entries.append(row)
    
    if engyu_entries:
        print(f"species-H373 (エンジュマメゾウムシ) の現在のエントリ:")
        for entry in engyu_entries:
            print(f"  {entry['plant_name']}: {entry['plant_part']}")
    else:
        print("⚠️ species-H373のエントリが見つかりません")
    
    # 検証
    print(f"\\n=== 修正結果検証 ===")
    
    for rule in fix_rules:
        if rule['fixes']:  # 修正があった場合のみ
            print(f"\\n{rule['name']}:")
            
            with open(hostplants_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['insect_id'] == rule['insect_id']:
                        print(f"  {row['plant_name']}: {row['plant_part']}")
    
    # 他の複雑パターンの検索
    print(f"\\n=== 他の複雑パターン検索 ===")
    
    # ハムシの元データから「の花」「の実」「の根」を含むパターンを検索
    hamushi_file = os.path.join(base_dir, 'public', 'ハムシ.csv')
    
    complex_patterns = []
    with open(hamushi_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダーをスキップ
        
        for row in reader:
            if len(row) >= 3:
                food_plants = row[2].strip().strip('""')
                
                # 複雑なパターンを検出
                if ('の花' in food_plants and '、' in food_plants) or \
                   ('の実' in food_plants and '、' in food_plants) or \
                   ('の根' in food_plants and '、' in food_plants):
                    
                    japanese_name = row[0].split('、')[0].strip()
                    complex_patterns.append({
                        'name': japanese_name,
                        'food_plants': food_plants
                    })
    
    if complex_patterns:
        print(f"他の複雑パターン ({len(complex_patterns)}件):")
        for pattern in complex_patterns[:5]:  # 最初の5件
            print(f"  {pattern['name']}: {pattern['food_plants']}")
    else:
        print("他の複雑パターンは見つかりませんでした")
    
    print(f"\\n🌸 残りのハムシ植物部位パターン修正が完了しました！")

if __name__ == "__main__":
    fix_remaining_hamushi_parts()