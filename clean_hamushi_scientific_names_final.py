#!/usr/bin/env python3
import csv
import re
import os

def clean_hamushi_scientific_names_final():
    """学名が植物名に誤って記録されているハムシエントリを最終修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== ハムシの学名誤記録最終クリーンアップ開始 ===")
    
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
                'host_plants': row['食草'].strip() if row['食草'] else '',
                'reference': row['出典'].strip() if row['出典'] else '',
                'notes': row['備考'].strip() if row['備考'] else ''
            }
    
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            insect_id = row['insect_id']
            plant_name = row['plant_name']
            
            # CR系のIDで、植物名に学名（括弧付き）が入っているケースを特定
            if insect_id.startswith('species-CR'):
                catalog_no = insect_id.replace('species-', '')
                
                if catalog_no in hamushi_lookup:
                    original_data = hamushi_lookup[catalog_no]
                    scientific_name = original_data['scientific_name']
                    host_plants = original_data['host_plants']
                    
                    # 植物名が学名と一致する場合は明らかに誤記録
                    if plant_name == scientific_name:
                        print(f"\\n修正対象: 行{row_num} (ID: {insect_id})")
                        print(f"  誤記録: plant_name='{plant_name}' (これは学名)")
                        print(f"  元データの食草: '{host_plants}'")
                        
                        if host_plants and host_plants != scientific_name:
                            # 有効な植物名がある場合
                            if '、' in host_plants:
                                # 複数植物の場合は分割
                                plants = [p.strip() for p in host_plants.split('、') if p.strip()]
                                print(f"  修正: 複数植物に分割 {plants}")
                                
                                for i, plant in enumerate(plants):
                                    if i == 0:
                                        # 最初のエントリは現在の行を更新
                                        row['plant_name'] = plant
                                        row['reference'] = 'ハムシハンドブック'
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
                                row['plant_name'] = host_plants
                                row['reference'] = 'ハムシハンドブック'
                                print(f"  修正: plant_name='{host_plants}'")
                        else:
                            # 植物名が不明の場合
                            row['plant_name'] = '不明'
                            row['reference'] = 'ハムシハンドブック'
                            print(f"  修正: plant_name='不明' (元データに植物情報なし)")
                        
                        fix_count += 1
                    
                    # 植物名に括弧がある場合も学名の可能性が高い
                    elif '(' in plant_name and ')' in plant_name and any(c.isupper() for c in plant_name[:10]):
                        print(f"\\n疑似学名パターン: 行{row_num} (ID: {insect_id})")
                        print(f"  疑似学名: plant_name='{plant_name}'")
                        print(f"  元データの食草: '{host_plants}'")
                        
                        if host_plants and host_plants != plant_name and host_plants != scientific_name:
                            # 元データに有効な植物名がある場合
                            row['plant_name'] = host_plants
                            row['reference'] = 'ハムシハンドブック'
                            print(f"  修正: plant_name='{host_plants}'")
                            fix_count += 1
                        else:
                            # 植物名が不明の場合
                            row['plant_name'] = '不明'
                            row['reference'] = 'ハムシハンドブック'
                            print(f"  修正: plant_name='不明'")
                            fix_count += 1
            
            new_data.append(row)
    
    print(f"\\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  元のエントリ数: {row_num-1}件")
    print(f"  修正後のエントリ数: {len(new_data)}件")
    
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
    
    # 最終検証
    print(f"\\n=== 最終検証 ===")
    
    # 残存する学名パターンをチェック
    remaining_scientific_names = []
    clean_hamushi_entries = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            plant_name = row['plant_name']
            insect_id = row['insect_id']
            
            if insect_id.startswith('species-CR'):
                # 学名パターンを検出
                if ('(' in plant_name and ')' in plant_name and 
                    any(c.isupper() for c in plant_name[:10]) and
                    len([c for c in plant_name if c.isupper()]) >= 2):
                    remaining_scientific_names.append(f"{insect_id}: {plant_name[:40]}...")
                else:
                    clean_hamushi_entries.append(f"{insect_id}: {plant_name}")
    
    if remaining_scientific_names:
        print(f"残存する学名パターン ({len(remaining_scientific_names)}件):")
        for pattern in remaining_scientific_names[:5]:
            print(f"  {pattern}")
    else:
        print("✅ すべての学名パターンがクリーンアップされました")
    
    print(f"\\nクリーンなハムシエントリ例 ({len(clean_hamushi_entries)}件):")
    for example in clean_hamushi_entries[:10]:
        print(f"  {example}")
    
    print(f"\\n🧹 ハムシの学名誤記録最終クリーンアップが完了しました！")

if __name__ == "__main__":
    clean_hamushi_scientific_names_final()