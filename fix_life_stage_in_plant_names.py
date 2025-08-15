#!/usr/bin/env python3
import csv
import re
import os

def fix_life_stage_in_plant_names():
    """植物名に含まれるライフステージ情報を適切なフィールドに分離"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 植物名のライフステージ情報分離開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    hamushi_handbook_fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            life_stage = row['life_stage']
            reference = row['reference']
            
            # パターン1: 植物名に含まれるライフステージ情報（成虫、幼虫、卵、蛹）
            life_stage_match = re.search(r'(.*?)（(成虫|幼虫|卵|蛹)）$', plant_name)
            if life_stage_match:
                clean_plant_name = life_stage_match.group(1).strip()
                extracted_life_stage = life_stage_match.group(2)
                
                print(f"\\n修正対象: 行{row_num}")
                print(f"  元: plant_name='{plant_name}', life_stage='{life_stage}'")
                
                row['plant_name'] = clean_plant_name
                row['life_stage'] = extracted_life_stage
                
                print(f"  新: plant_name='{clean_plant_name}', life_stage='{extracted_life_stage}'")
                fix_count += 1
            
            # パターン2: ハムシハンドブックが出典で、life_stageが空欄の場合は「成虫」に設定
            elif reference == 'ハムシハンドブック' and not life_stage.strip():
                print(f"\\nハムシハンドブック修正: 行{row_num}")
                print(f"  植物名: '{plant_name}'")
                print(f"  life_stage: '{life_stage}' → '成虫'")
                
                row['life_stage'] = '成虫'
                hamushi_handbook_fix_count += 1
            
            new_data.append(row)
    
    print(f"\\n修正結果:")
    print(f"  ライフステージ分離: {fix_count}件")
    print(f"  ハムシハンドブック成虫設定: {hamushi_handbook_fix_count}件")
    print(f"  総修正: {fix_count + hamushi_handbook_fix_count}件")
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
    
    # 検証
    print(f"\\n=== 検証 ===")
    
    # 残存するライフステージパターンをチェック
    remaining_patterns = []
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            plant_name = row['plant_name']
            if re.search(r'（(成虫|幼虫|卵|蛹)）', plant_name):
                remaining_patterns.append(plant_name[:50])
    
    if remaining_patterns:
        print(f"残存するライフステージパターン ({len(remaining_patterns)}件):")
        for pattern in remaining_patterns[:3]:
            print(f"  '{pattern}...'")
    else:
        print("✅ 植物名のライフステージパターンが全て分離されました")
    
    # 修正された例の確認
    fixed_examples = []
    hamushi_handbook_examples = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['life_stage'] in ['成虫', '幼虫', '卵', '蛹']:
                if row['plant_name'] in ['枯れ葉', 'タンポポなどの花', 'スギゴケ類', 'ブナ', 'ヤマアリ類の巣材の一部']:
                    fixed_examples.append(f"{row['plant_name']} ({row['life_stage']})")
                elif row['reference'] == 'ハムシハンドブック' and row['life_stage'] == '成虫':
                    hamushi_handbook_examples.append(f"{row['plant_name']} ({row['life_stage']})")
    
    print(f"\\n分離された例:")
    for example in fixed_examples:
        print(f"  {example}")
    
    print(f"\\nハムシハンドブック（成虫設定）例:")
    for example in hamushi_handbook_examples[:5]:
        print(f"  {example}")
    
    print(f"\\n🔬 植物名のライフステージ情報分離が完了しました！")

if __name__ == "__main__":
    fix_life_stage_in_plant_names()