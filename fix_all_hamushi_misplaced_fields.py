#!/usr/bin/env python3
import csv
import re
import os

def fix_all_hamushi_misplaced_fields():
    """すべてのハムシデータの学名誤配置を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== すべてのハムシデータの学名誤配置修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # 元のhamushiデータをマッピング
    hamushi_file = os.path.join(base_dir, 'public', 'hamushi_integrated_master.csv')
    hamushi_lookup = {}
    
    with open(hamushi_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            catalog_no = row['大図鑑カタログNo']
            hamushi_lookup[catalog_no] = {
                'scientific_name': row['学名'],
                'japanese_name': row['和名'],
                'host_plants': row['食草'],
                'reference': row['出典'],
                'notes': row['備考'],
                'emergence_period': row['成虫出現時期']
            }
    
    new_data = []
    fix_count = 0
    scientific_name_in_plant_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            insect_id = row['insect_id']
            plant_name = row['plant_name']
            
            # CR系のIDで、plant_nameに学名（括弧を含む）が入っているケースを検出
            if insect_id.startswith('species-CR') and '(' in plant_name and ')' in plant_name:
                catalog_no = insect_id.replace('species-', '')
                
                if catalog_no in hamushi_lookup:
                    original_data = hamushi_lookup[catalog_no]
                    
                    print(f"\\n修正対象: 行{row_num} (ID: {insect_id})")
                    print(f"  誤配置された学名: '{plant_name}'")
                    
                    # 元データから正しい植物名と出典を取得
                    host_plants = original_data['host_plants']
                    reference = original_data['reference']
                    notes = original_data['notes']
                    
                    scientific_name_in_plant_count += 1
                    
                    if host_plants and host_plants.strip() and host_plants != '不明':
                        # 植物名が複数ある場合は分割
                        if '、' in host_plants:
                            plants = [p.strip() for p in host_plants.split('、') if p.strip()]
                            print(f"  正しい植物名: {plants} (分割)")
                            
                            for i, plant in enumerate(plants):
                                new_row = row.copy()
                                new_row['plant_name'] = plant
                                new_row['reference'] = reference
                                if notes:
                                    new_row['notes'] = notes
                                
                                # record_idを調整
                                if i == 0:
                                    # 最初のエントリは元のIDを維持
                                    pass
                                else:
                                    # 新しいレコードIDを生成
                                    new_row['record_id'] = f"temp-{row_num}-{i+1}"
                                
                                new_data.append(new_row)
                            
                            fix_count += 1
                        else:
                            # 単一の植物名
                            row['plant_name'] = host_plants
                            row['reference'] = reference
                            if notes:
                                row['notes'] = notes
                            new_data.append(row)
                            
                            print(f"  正しい植物名: '{host_plants}'")
                            fix_count += 1
                    else:
                        # 植物名が不明の場合
                        row['plant_name'] = '不明'
                        row['reference'] = reference
                        if notes:
                            row['notes'] = notes
                        new_data.append(row)
                        
                        print(f"  植物名: '不明' (元データにも植物名なし)")
                        fix_count += 1
                    
                    print(f"  出典: '{reference}'")
                else:
                    print(f"⚠️ 警告: {catalog_no} が元データで見つかりませんでした")
                    new_data.append(row)
            else:
                # 通常のレコードはそのまま保持
                new_data.append(row)
    
    print(f"\\n修正結果:")
    print(f"  学名が誤配置されていたエントリ: {scientific_name_in_plant_count}件")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  元のエントリ数: {row_num-1}件")
    print(f"  修正後のエントリ数: {len(new_data)}件")
    print(f"  増加したエントリ数: {len(new_data) - (row_num-1)}件")
    
    # record_idを正規化
    print("\\nrecord_idを正規化中...")
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
    print(f"\\n=== 検証 ===")
    
    # 残存する学名パターンをチェック
    remaining_scientific_names = []
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            plant_name = row['plant_name']
            insect_id = row['insect_id']
            if insect_id.startswith('species-CR') and '(' in plant_name and ')' in plant_name and any(c.isupper() for c in plant_name[:10]):
                remaining_scientific_names.append(f"{insect_id}: {plant_name[:50]}")
    
    if remaining_scientific_names:
        print(f"残存する学名パターン ({len(remaining_scientific_names)}件):")
        for pattern in remaining_scientific_names[:5]:
            print(f"  {pattern}...")
    else:
        print("✅ すべての学名誤配置が修正されました")
    
    # 修正された例の確認
    fixed_examples = []
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            if row['insect_id'].startswith('species-CR') and row['plant_name'] not in ['不明', '']:
                if not ('(' in row['plant_name'] and ')' in row['plant_name']):
                    fixed_examples.append(f"{row['insect_id']}: {row['plant_name']}")
                    count += 1
                    if count >= 10:
                        break
    
    print(f"\\n修正された例:")
    for example in fixed_examples:
        print(f"  {example}")
    
    print(f"\\n🔧 すべてのハムシデータの学名誤配置修正が完了しました！")

if __name__ == "__main__":
    fix_all_hamushi_misplaced_fields()