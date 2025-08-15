#!/usr/bin/env python3
import csv
import re
import os

def fix_hamushi_field_mixup():
    """ハムシデータのフィールド混在を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== ハムシデータのフィールド混在修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    # まず元のhamushiデータを読み込んでマッピングを作成
    hamushi_file = os.path.join(base_dir, 'public', 'hamushi_integrated_master.csv')
    hamushi_data = {}
    
    with open(hamushi_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            catalog_no = row['大図鑑カタログNo']
            hamushi_data[catalog_no] = {
                'scientific_name': row['学名'],
                'japanese_name': row['和名'],
                'host_plants': row['食草'],
                'reference': row['出典']
            }
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            insect_id = row['insect_id']
            plant_name = row['plant_name']
            reference = row['reference']
            
            # CR系のinsect_idかつ、plant_nameに学名が入っているケースを検出
            if insect_id.startswith('species-CR') and '(' in plant_name and ')' in plant_name:
                # CR001 -> CR001の形でカタログ番号を抽出
                catalog_no = insect_id.replace('species-', '')
                
                if catalog_no in hamushi_data:
                    original_data = hamushi_data[catalog_no]
                    
                    print(f"\n修正対象: 行{row_num} (insect_id: {insect_id})")
                    print(f"  元plant_name: '{plant_name}' (学名)")
                    print(f"  元reference: '{reference}' (植物名)")
                    
                    # 正しい植物名を設定
                    correct_plant_name = original_data['host_plants']
                    correct_reference = original_data['reference']
                    
                    # 植物名が複数ある場合は分割
                    if '、' in correct_plant_name:
                        plants = [p.strip() for p in correct_plant_name.split('、') if p.strip()]
                        # 最初の植物を現在のレコードに設定
                        row['plant_name'] = plants[0]
                        row['reference'] = correct_reference
                        new_data.append(row)
                        
                        # 残りの植物を追加レコードとして作成
                        for i, plant in enumerate(plants[1:], 1):
                            new_row = row.copy()
                            new_row['record_id'] = f"temp-{row_num}-{i+1}"
                            new_row['plant_name'] = plant
                            new_row['reference'] = correct_reference
                            new_data.append(new_row)
                        
                        print(f"  新plant_name: {plants} (分割)")
                        print(f"  新reference: '{correct_reference}'")
                        fix_count += 1
                    else:
                        row['plant_name'] = correct_plant_name if correct_plant_name else '不明'
                        row['reference'] = correct_reference
                        new_data.append(row)
                        
                        print(f"  新plant_name: '{row['plant_name']}'")
                        print(f"  新reference: '{correct_reference}'")
                        fix_count += 1
                else:
                    print(f"⚠️ カタログ番号 {catalog_no} が元データで見つかりませんでした")
                    new_data.append(row)
            else:
                # 通常のレコードはそのまま保持
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
    
    # 検証
    print(f"\n=== 検証 ===")
    
    # 残存する学名パターンをチェック
    remaining_scientific_names = []
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            plant_name = row['plant_name']
            insect_id = row['insect_id']
            # 学名パターンを検出
            if insect_id.startswith('species-CR') and ('(' in plant_name and ')' in plant_name) and any(c.isupper() for c in plant_name[:5]):
                remaining_scientific_names.append(f"{insect_id}: {plant_name[:50]}")
    
    if remaining_scientific_names:
        print(f"残存する学名パターン ({len(remaining_scientific_names)}件):")
        for pattern in remaining_scientific_names[:5]:
            print(f"  {pattern}...")
    else:
        print("✅ ハムシデータの学名パターンが全て修正されました")
    
    # 修正された例の確認
    fixed_examples = []
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['insect_id'].startswith('species-CR'):
                if row['plant_name'] not in ['不明', ''] and not ('(' in row['plant_name'] and ')' in row['plant_name']):
                    fixed_examples.append(f"{row['insect_id']}: {row['plant_name']}")
    
    print(f"\n修正された例:")
    for example in fixed_examples[:5]:
        print(f"  {example}")
    
    print(f"\n🔧 ハムシデータのフィールド混在修正が完了しました！")

if __name__ == "__main__":
    fix_hamushi_field_mixup()