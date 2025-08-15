#!/usr/bin/env python3
import csv
import re
import os

def fix_hamushi_plant_parts():
    """ハムシの植物名に含まれる部位情報を適切なフィールドに分離"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== ハムシの植物部位情報分離開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # 植物部位のパターンを定義
    part_patterns = [
        ('花', 'flower'),
        ('花序', 'inflorescence'),
        ('蕾', 'bud'),
        ('実', 'fruit'),
        ('果実', 'fruit'),
        ('種子', 'seed'),
        ('茎', 'stem'),
        ('根', 'root'),
        ('葉', 'leaf'),
        ('芽', 'bud'),
        ('新芽', 'young_shoot'),
    ]
    
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            insect_id = row['insect_id']
            plant_name = row['plant_name']
            plant_part = row['plant_part']
            
            # ハムシ（H系とCR系）のエントリのみ処理
            if insect_id.startswith('species-H') or insect_id.startswith('species-CR'):
                
                # 「植物名の部位」パターンを検出
                for part_jp, part_en in part_patterns:
                    pattern = rf'^(.+?)(?:など)?の{re.escape(part_jp)}$'
                    match = re.match(pattern, plant_name)
                    
                    if match:
                        clean_plant_name = match.group(1).strip()
                        
                        # 「など」がある場合は植物名に戻す
                        if 'など' in plant_name:
                            # 「タンポポなどの花」→「タンポポなど」（植物名）、「花」（部位）
                            if 'などの' in plant_name:
                                clean_plant_name = plant_name.split('などの')[0] + 'など'
                            else:
                                clean_plant_name = clean_plant_name + 'など'
                        
                        print(f"\\n修正対象: 行{row_num} (ID: {insect_id})")
                        print(f"  元: plant_name='{plant_name}', plant_part='{plant_part}'")
                        print(f"  新: plant_name='{clean_plant_name}', plant_part='{part_jp}'")
                        
                        row['plant_name'] = clean_plant_name
                        row['plant_part'] = part_jp
                        fix_count += 1
                        break  # 最初にマッチしたパターンで処理
                
                # 特殊ケース: 「オオカメノキなどの白色の花」のような複雑なパターン
                complex_pattern = r'^(.+?)の([^の]+)の(花|実|果実|種子|茎|根|葉|芽|新芽|蕾|花序)$'
                complex_match = re.match(complex_pattern, plant_name)
                if complex_match and not any(re.match(rf'^(.+?)(?:など)?の{re.escape(part_jp)}$', plant_name) for part_jp, _ in part_patterns):
                    plant_base = complex_match.group(1).strip()
                    descriptor = complex_match.group(2).strip()
                    part = complex_match.group(3).strip()
                    
                    print(f"\\n複雑パターン修正: 行{row_num} (ID: {insect_id})")
                    print(f"  元: plant_name='{plant_name}'")
                    print(f"  新: plant_name='{plant_base}', plant_part='{descriptor}の{part}'")
                    
                    row['plant_name'] = plant_base
                    row['plant_part'] = f"{descriptor}の{part}"
                    fix_count += 1
            
            new_data.append(row)
    
    print(f"\\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  元のエントリ数: {row_num-1}件")
    print(f"  修正後のエントリ数: {len(new_data)}件")
    
    # 修正されたデータを保存
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if new_data:
            writer = csv.DictWriter(file, fieldnames=new_data[0].keys())
            writer.writeheader()
            writer.writerows(new_data)
    
    # normalized_dataフォルダにもコピー
    import shutil
    src = hostplants_file
    dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    print("hostplants.csvを更新しました")
    
    # 最終検証
    print(f"\\n=== 最終検証 ===")
    
    # 残存する「植物名の部位」パターンをチェック
    remaining_patterns = []
    fixed_examples = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            insect_id = row['insect_id']
            plant_name = row['plant_name']
            plant_part = row['plant_part']
            
            # ハムシエントリで残存パターンをチェック
            if (insect_id.startswith('species-H') or insect_id.startswith('species-CR')):
                # 部位パターンが残っているかチェック
                if re.search(r'の(花|実|果実|種子|茎|根|葉|芽|新芽|蕾|花序)$', plant_name):
                    remaining_patterns.append(f"{insect_id}: {plant_name}")
                
                # 修正された例を収集
                if plant_part and plant_part in ['花', '実', '果実', '種子', '茎', '根', '葉', '芽', '新芽', '蕾', '花序']:
                    fixed_examples.append(f"{insect_id}: {plant_name} → {plant_part}")
    
    if remaining_patterns:
        print(f"残存する植物名+部位パターン ({len(remaining_patterns)}件):")
        for pattern in remaining_patterns[:5]:
            print(f"  {pattern}")
    else:
        print("✅ すべての植物名+部位パターンが分離されました")
    
    print(f"\\n修正された例 ({len(fixed_examples)}件):")
    for example in fixed_examples[:10]:
        print(f"  {example}")
    
    # 部位統計
    part_counts = {}
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (row['insect_id'].startswith('species-H') or row['insect_id'].startswith('species-CR')) and row['plant_part']:
                part = row['plant_part']
                part_counts[part] = part_counts.get(part, 0) + 1
    
    print(f"\\n植物部位の統計:")
    for part, count in sorted(part_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {part}: {count}件")
    
    print(f"\\n🌿 ハムシの植物部位情報分離が完了しました！")

if __name__ == "__main__":
    fix_hamushi_plant_parts()