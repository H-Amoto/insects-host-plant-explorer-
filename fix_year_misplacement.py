#!/usr/bin/env python3
import csv
import re
import os

def fix_year_misplacement():
    """公表年が植物名フィールドに誤って配置されている問題を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 公表年の誤配置修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    insects_file = os.path.join(base_dir, 'public', 'insects.csv')
    
    # 昆虫データを読み込んで公表年情報を取得
    insects_lookup = {}
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            insects_lookup[row['insect_id']] = {
                'year': row['year'],
                'scientific_name': row['scientific_name']
            }
    
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            insect_id = row['insect_id']
            plant_name = row['plant_name']
            reference = row['reference']
            
            # 植物名が4桁の年（1800-2099）で、referenceに実際の植物名がある場合
            year_pattern = re.match(r'^(18|19|20)\d{2}$', plant_name.strip())
            
            if year_pattern and reference.strip():
                # 昆虫データから正しい公表年を確認
                if insect_id in insects_lookup:
                    expected_year = insects_lookup[insect_id]['year']
                    
                    # 植物名フィールドの年が昆虫の公表年と一致する場合
                    if plant_name.strip() == expected_year:
                        print(f"\n修正対象: 行{row_num} (ID: {insect_id})")
                        print(f"  現在: plant_name='{plant_name}', reference='{reference}'")
                        
                        # referenceの内容を植物名に移動
                        correct_plant_names = reference.strip()
                        
                        # 複数の植物名がある場合は分割して複数レコードを作成
                        if '、' in correct_plant_names:
                            plants = [p.strip() for p in correct_plant_names.split('、') if p.strip()]
                            print(f"  修正: 複数植物に分割 {plants}")
                            
                            for i, plant in enumerate(plants):
                                if i == 0:
                                    # 最初のエントリは現在の行を更新
                                    row['plant_name'] = plant
                                    row['reference'] = 'ハムシハンドブック'  # 適切な出典に設定
                                    new_data.append(row)
                                else:
                                    # 追加エントリを作成
                                    new_row = row.copy()
                                    new_row['record_id'] = f"temp-{row_num}-{i+1}"
                                    new_row['plant_name'] = plant
                                    new_row['reference'] = 'ハムシハンドブック'
                                    new_data.append(new_row)
                            
                            fix_count += 1
                            continue  # 次のレコードへ
                        else:
                            # 単一植物の場合
                            row['plant_name'] = correct_plant_names
                            row['reference'] = 'ハムシハンドブック'
                            print(f"  修正: plant_name='{correct_plant_names}'")
                            fix_count += 1
                    else:
                        print(f"⚠️ 警告: {insect_id} の年 '{plant_name}' が期待される年 '{expected_year}' と一致しません")
                else:
                    print(f"⚠️ 警告: {insect_id} が昆虫データで見つかりませんでした")
            
            new_data.append(row)
    
    print(f"\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  元のエントリ数: {row_num-1}件")
    print(f"  修正後のエントリ数: {len(new_data)}件")
    
    # record_idを正規化
    print("\nrecord_idを正規化中...")
    for i, row in enumerate(new_data):
        row['record_id'] = f"hostplant-{i+1:06d}"
    
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
    print(f"\n=== 最終検証 ===")
    
    # 残存する年パターンをチェック
    remaining_year_patterns = []
    fixed_examples = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            plant_name = row['plant_name']
            insect_id = row['insect_id']
            
            # 4桁年パターンをチェック
            if re.match(r'^(18|19|20)\d{2}$', plant_name.strip()):
                remaining_year_patterns.append(f"{insect_id}: {plant_name}")
            # 修正されたH626エントリを確認
            elif insect_id == 'species-H626':
                fixed_examples.append(f"{insect_id}: {plant_name}")
    
    if remaining_year_patterns:
        print(f"残存する年パターン ({len(remaining_year_patterns)}件):")
        for pattern in remaining_year_patterns:
            print(f"  {pattern}")
    else:
        print("✅ すべての年の誤配置が修正されました")
    
    print(f"\n修正されたH626エントリ:")
    for example in fixed_examples:
        print(f"  {example}")
    
    print(f"\n🔧 公表年の誤配置修正が完了しました！")

if __name__ == "__main__":
    fix_year_misplacement()