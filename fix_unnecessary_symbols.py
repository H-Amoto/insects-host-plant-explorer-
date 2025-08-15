#!/usr/bin/env python3
import csv
import re
import os

def fix_unnecessary_symbols():
    """植物名の先頭についた不必要な記号を除去"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 不必要な記号の除去修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    # 除去対象の記号パターンを定義
    symbol_patterns = [
        r'^。(.+)$',      # 先頭の句点
        r'^、(.+)$',      # 先頭の読点
        r'^；(.+)$',      # 先頭のセミコロン（全角）
        r'^;(.+)$',       # 先頭のセミコロン（半角）
        r'^：(.+)$',      # 先頭のコロン（全角）
        r'^:(.+)$',       # 先頭のコロン（半角）
        r'^－(.+)$',      # 先頭のダッシュ（全角）
        r'^-(.+)$',       # 先頭のダッシュ（半角）
        r'^‐(.+)$',       # 先頭のハイフン
        r'^—(.+)$',       # 先頭のemダッシュ
        r'^_(.+)$',       # 先頭のアンダースコア
        r'^・(.+)$',      # 先頭の中点
        r'^\s+(.+)$',     # 先頭のスペース
    ]
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            original_name = plant_name
            
            # 各パターンをチェックして修正
            for pattern in symbol_patterns:
                match = re.match(pattern, plant_name)
                if match:
                    clean_name = match.group(1)
                    
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: '{plant_name}'")
                    print(f"  新: '{clean_name}'")
                    
                    row['plant_name'] = clean_name
                    fix_count += 1
                    break
            
            new_data.append(row)
    
    print(f"\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  総エントリ数: {len(new_data)}件")
    
    # 修正されたデータを保存
    if fix_count > 0:
        with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
            if new_data:
                writer = csv.DictWriter(file, fieldnames=new_data[0].keys())
                writer.writeheader()
                writer.writerows(new_data)
        
        # normalized_dataフォルダにもコピー
        import shutil
        src = hostplants_file
        dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
        shutil.copy2(src, dst)
        
        print("hostplants.csvを更新しました")
        
        # 検証
        print(f"\n=== 検証 ===")
        sakura_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == 'サクラ':
                    sakura_entries.append(f"{row['insect_id']}: {row['plant_name']}")
        
        if sakura_entries:
            print("サクラの修正例:")
            for entry in sakura_entries[:5]:
                print(f"  {entry}")
        
        # 残存する記号付きエントリをチェック
        remaining_symbols = []
        symbol_check_pattern = r'^[。、；;：:－\-‐—_・\s]'
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if re.match(symbol_check_pattern, row['plant_name']):
                    remaining_symbols.append(row['plant_name'])
        
        if remaining_symbols:
            print(f"\n残存する記号付きエントリ ({len(remaining_symbols)}件):")
            for entry in remaining_symbols[:10]:
                print(f"  '{entry}'")
        else:
            print("\n✅ 不必要な記号の除去が完了しました")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_unnecessary_symbols()