#!/usr/bin/env python3
import csv
import os
import shutil

def verify_hamushi_handbook_entries():
    """ハムシハンドブックを出典とする「不明」エントリを元データと照合して検証"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== ハムシハンドブック出典「不明」エントリの検証 ===")
    
    # ファイル
    hamushi_file = os.path.join(base_dir, 'public', 'ハムシ.csv')
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    insects_file = os.path.join(base_dir, 'public', 'insects.csv')
    
    # 1. ハムシ.csvから種名リストを作成
    print("\n=== ハムシ.csvの種名リスト作成 ===")
    
    hamushi_species = set()
    hamushi_data = {}
    
    with open(hamushi_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダーをスキップ
        
        for row in reader:
            if len(row) >= 3:
                japanese_name = row[0].split('、')[0].strip()
                scientific_name = row[1].split('、')[0].strip() if len(row) > 1 else ""
                food_plants = row[2].strip().strip('""')
                
                hamushi_species.add(japanese_name)
                hamushi_data[japanese_name] = {
                    'scientific_name': scientific_name,
                    'food_plants': food_plants
                }
    
    print(f"ハムシ.csvの種数: {len(hamushi_species)}種")
    
    # 2. insects.csvからハムシ科の和名→IDマッピング
    print("\n=== ハムシ科昆虫IDマッピング作成 ===")
    
    hamushi_insects = {}
    
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['family'] == 'Chrysomelidae':  # ハムシ科
                japanese_name = row['japanese_name'].strip()
                insect_id = row['insect_id']
                hamushi_insects[japanese_name] = insect_id
    
    print(f"ハムシ科昆虫総数: {len(hamushi_insects)}種")
    
    # 3. hostplants.csvでハムシハンドブック出典の「不明」エントリを検索
    print("\n=== ハムシハンドブック出典「不明」エントリの検索 ===")
    
    unknown_entries = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if (row['reference'] == 'ハムシハンドブック' and 
                row['plant_name'] == '不明'):
                unknown_entries.append(row)
    
    print(f"ハムシハンドブック出典「不明」エントリ: {len(unknown_entries)}件")
    
    # 4. 各「不明」エントリの検証
    print("\n=== 詳細検証 ===")
    
    to_delete = []
    to_keep = []
    
    for entry in unknown_entries:
        insect_id = entry['insect_id']
        
        # insects.csvから和名を取得
        japanese_name = None
        for name, id_val in hamushi_insects.items():
            if id_val == insect_id:
                japanese_name = name
                break
        
        if japanese_name:
            print(f"\nID: {insect_id}")
            print(f"  和名: {japanese_name}")
            
            # ハムシ.csvに記載があるかチェック
            if japanese_name in hamushi_species:
                food_info = hamushi_data[japanese_name]
                print(f"  ハムシ.csvに記載あり")
                print(f"    食草: {food_info['food_plants']}")
                print(f"  → このエントリは保持すべき（元データに記載あり）")
                to_keep.append({
                    'entry': entry,
                    'japanese_name': japanese_name,
                    'food_plants': food_info['food_plants']
                })
            else:
                print(f"  ❌ ハムシ.csvに記載なし")
                print(f"  → このエントリは削除候補（元データに記載なし）")
                to_delete.append({
                    'entry': entry,
                    'japanese_name': japanese_name
                })
        else:
            print(f"\nID: {insect_id}")
            print(f"  ⚠️ insects.csvで和名が見つからない")
            to_delete.append({
                'entry': entry,
                'japanese_name': '不明'
            })
    
    # 5. 削除実行
    print(f"\n=== 削除実行 ===")
    print(f"削除対象: {len(to_delete)}件")
    print(f"保持対象: {len(to_keep)}件")
    
    if to_delete:
        print("\n削除対象の詳細:")
        for item in to_delete:
            print(f"  {item['entry']['insect_id']}: {item['japanese_name']}")
        
        # hostplants.csvから削除対象を除去
        hostplants_data = []
        deleted_count = 0
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                should_delete = False
                
                # 削除対象かチェック
                for item in to_delete:
                    if (row['record_id'] == item['entry']['record_id'] and
                        row['insect_id'] == item['entry']['insect_id'] and
                        row['plant_name'] == '不明' and
                        row['reference'] == 'ハムシハンドブック'):
                        should_delete = True
                        deleted_count += 1
                        print(f"削除: {row['record_id']} ({row['insect_id']})")
                        break
                
                if not should_delete:
                    hostplants_data.append(row)
        
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
        
        print(f"\n削除完了: {deleted_count}件のエントリを削除しました")
        print("hostplants.csvを更新しました")
    
    # 6. 保持されたエントリの確認
    if to_keep:
        print(f"\n=== 保持エントリの確認 ===")
        print("以下のエントリは元データに記載があるため保持されました:")
        for item in to_keep:
            print(f"\n{item['japanese_name']} ({item['entry']['insect_id']}):")
            print(f"  元データの食草: {item['food_plants']}")
            print(f"  → 「不明」のままでよいか要検討")
    
    # 7. 最終検証
    print(f"\n=== 最終検証 ===")
    
    remaining_unknown = []
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (row['reference'] == 'ハムシハンドブック' and 
                row['plant_name'] == '不明'):
                remaining_unknown.append(row)
    
    print(f"残存する「不明」エントリ: {len(remaining_unknown)}件")
    
    if remaining_unknown:
        print("残存エントリ:")
        for entry in remaining_unknown:
            print(f"  {entry['insect_id']}")
    
    print(f"\n✅ ハムシハンドブック出典「不明」エントリの検証が完了しました！")

if __name__ == "__main__":
    verify_hamushi_handbook_entries()