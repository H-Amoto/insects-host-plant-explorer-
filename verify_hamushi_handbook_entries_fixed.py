#!/usr/bin/env python3
import csv
import os
import shutil

def verify_hamushi_handbook_entries_fixed():
    """ハムシハンドブックを出典とする「不明」エントリを元データと照合して検証（修正版）"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== ハムシハンドブック出典「不明」エントリの検証（修正版） ===")
    
    # ファイル
    hamushi_file = os.path.join(base_dir, 'public', 'ハムシ.csv')
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    insects_file = os.path.join(base_dir, 'public', 'insects.csv')
    
    # 1. ハムシ.csvから種名リストを作成（正しい解析）
    print("\n=== ハムシ.csvの種名リスト作成 ===")
    
    hamushi_species = set()
    hamushi_data = {}
    
    with open(hamushi_file, 'r', encoding='utf-8') as file:
        # 最初の行をヘッダーとして読み飛ばし
        header = file.readline().strip()
        print(f"ヘッダー: {header}")
        
        for line_num, line in enumerate(file, 2):
            line = line.strip()
            if line:
                # ダブルクォートで囲まれた部分を正しく解析
                # CSVライブラリを使わず手動で解析
                parts = []
                current_part = ""
                in_quotes = False
                i = 0
                
                while i < len(line):
                    char = line[i]
                    
                    if char == '"':
                        if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                            # ダブルクォートのエスケープ
                            current_part += '"'
                            i += 2
                        else:
                            in_quotes = not in_quotes
                            i += 1
                    elif char == ',' and not in_quotes:
                        parts.append(current_part.strip())
                        current_part = ""
                        i += 1
                    else:
                        current_part += char
                        i += 1
                
                # 最後の部分を追加
                parts.append(current_part.strip())
                
                if len(parts) >= 3:
                    japanese_name_full = parts[0]
                    scientific_name = parts[1]
                    food_plants = parts[2]
                    
                    # 和名から最初の部分を抽出（括弧内は除く）
                    if '(' in japanese_name_full:
                        japanese_name = japanese_name_full.split('(')[0].strip()
                    else:
                        japanese_name = japanese_name_full.split('、')[0].strip()
                    
                    hamushi_species.add(japanese_name)
                    hamushi_data[japanese_name] = {
                        'scientific_name': scientific_name,
                        'food_plants': food_plants,
                        'full_name': japanese_name_full
                    }
                    
                    if line_num <= 5:  # 最初の数行をデバッグ表示
                        print(f"行{line_num}: {japanese_name} -> {food_plants}")
    
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
    
    for entry in unknown_entries[:10]:  # 最初の10件をテスト
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
                print(f"  ✅ ハムシ.csvに記載あり")
                print(f"    完全名: {food_info['full_name']}")
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
    
    print(f"\n=== サンプル結果 ===")
    print(f"削除候補: {len(to_delete)}件（サンプル10件中）")
    print(f"保持候補: {len(to_keep)}件（サンプル10件中）")
    
    # 5. 利用可能な種名の例
    print(f"\n=== ハムシ.csvに記載されている種名の例 ===")
    sample_names = list(hamushi_species)[:10]
    for name in sample_names:
        print(f"  {name}: {hamushi_data[name]['food_plants']}")
    
    print(f"\n📋 検証スクリプトのテストが完了しました！")
    print(f"実際の削除を実行する場合は、全データで処理してください。")

if __name__ == "__main__":
    verify_hamushi_handbook_entries_fixed()