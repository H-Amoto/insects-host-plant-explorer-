#!/usr/bin/env python3
import csv
import re
import os

def final_fix_hamushi_scientific_names():
    """ハムシの学名誤配置を最終修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== ハムシの学名誤配置最終修正開始 ===")
    
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
            
            # CR系のIDで、植物名に学名（括弧付き）が入っているケースを検出
            if insect_id.startswith('species-CR') and '(' in plant_name and ')' in plant_name:
                catalog_no = insect_id.replace('species-', '')
                
                if catalog_no in hamushi_lookup:
                    original_data = hamushi_lookup[catalog_no]
                    host_plants = original_data['host_plants']
                    reference = original_data['reference']
                    notes = original_data['notes']
                    
                    print(f"\\n修正対象: 行{row_num} (ID: {insect_id})")
                    print(f"  現在のplant_name: '{plant_name}'")
                    print(f"  元データの食草: '{host_plants}'")
                    print(f"  元データの出典: '{reference}'")
                    
                    # 食草データが学名と同じ（つまり元データも壊れている）場合は「不明」に
                    if host_plants == original_data['scientific_name'] or not host_plants:
                        row['plant_name'] = '不明'
                        row['reference'] = 'ハムシハンドブック'
                        print(f"  修正: plant_name='不明' (元データに有効な食草名なし)")
                    else:
                        # 有効な植物名がある場合はそれを使用
                        if '、' in host_plants:
                            # 複数植物の場合は分割
                            plants = [p.strip() for p in host_plants.split('、') if p.strip()]
                            print(f"  修正: 複数植物に分割 {plants}")
                            
                            for i, plant in enumerate(plants):
                                if i == 0:
                                    # 最初のエントリは現在の行を更新
                                    row['plant_name'] = plant
                                    row['reference'] = reference if reference else 'ハムシハンドブック'
                                    if notes:
                                        row['notes'] = notes
                                    new_data.append(row)
                                else:
                                    # 追加エントリを作成
                                    new_row = row.copy()
                                    new_row['record_id'] = f"temp-{row_num}-{i+1}"
                                    new_row['plant_name'] = plant
                                    new_row['reference'] = reference if reference else 'ハムシハンドブック'
                                    if notes:
                                        new_row['notes'] = notes
                                    new_data.append(new_row)
                            
                            fix_count += 1
                            continue  # 次のレコードへ
                        else:
                            # 単一植物の場合
                            row['plant_name'] = host_plants
                            row['reference'] = reference if reference else 'ハムシハンドブック'
                            if notes:
                                row['notes'] = notes
                            
                            print(f"  修正: plant_name='{host_plants}'")
                    
                    fix_count += 1
                else:
                    print(f"⚠️ 警告: {catalog_no} が元データで見つかりませんでした")
            
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
    correct_hamushi_entries = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            plant_name = row['plant_name']
            insect_id = row['insect_id']
            
            if insect_id.startswith('species-CR'):
                if '(' in plant_name and ')' in plant_name and any(c.isupper() for c in plant_name[:10]):
                    remaining_scientific_names.append(f"{insect_id}: {plant_name[:30]}...")
                else:
                    correct_hamushi_entries.append(f"{insect_id}: {plant_name}")
    
    if remaining_scientific_names:
        print(f"残存する学名パターン ({len(remaining_scientific_names)}件):")
        for pattern in remaining_scientific_names[:3]:
            print(f"  {pattern}")
    else:
        print("✅ すべての学名パターンが修正されました")
    
    print(f"\\n正しく修正されたハムシエントリ例 ({len(correct_hamushi_entries)}件):")
    for example in correct_hamushi_entries[:10]:
        print(f"  {example}")
    
    print(f"\\n🎯 ハムシの学名誤配置最終修正が完了しました！")

if __name__ == "__main__":
    final_fix_hamushi_scientific_names()