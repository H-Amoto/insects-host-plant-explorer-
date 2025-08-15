#!/usr/bin/env python3
import csv
import re

def separate_combined_plants():
    """結合された食草を分離して新しい行を作成"""
    print("結合された食草を分離中...")
    
    input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master.csv'
    output_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master_separated.csv'
    
    new_rows = []
    separated_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        new_rows.append(header)  # ヘッダーを保持
        
        for row_num, row in enumerate(reader, start=2):
            if len(row) > 24:
                plant_data = row[24].strip() if len(row) > 24 else ""
                
                if plant_data and ';' in plant_data:
                    # セミコロンで分離
                    parts = plant_data.split(';')
                    
                    # 植物名らしいパーツを抽出（科名を含み、短すぎない）
                    plant_parts = []
                    for part in parts:
                        part = part.strip()
                        if ('科' in part and len(part) < 80 and 
                            not part.startswith(('飼育', '国外', 'ヨーロッパ', '自然', '報告', '幼虫'))):
                            # 簡単な植物名パターンをチェック
                            if (re.search(r'[ァ-ヺ]+.*科', part) or 
                                re.search(r'[a-zA-Z]+.*科', part)):
                                plant_parts.append(part)
                    
                    # 複数の植物に分離可能な場合
                    if len(plant_parts) > 1:
                        for i, plant in enumerate(plant_parts):
                            new_row = row.copy()
                            new_row[24] = plant.strip()
                            new_rows.append(new_row)
                            if i == 0:
                                print(f"分離: 行{row_num} - {row[18] if len(row) > 18 else '不明'}")
                                print(f"  元: {plant_data}")
                                for j, p in enumerate(plant_parts):
                                    print(f"  → {j+1}: {p}")
                        separated_count += 1
                    else:
                        # 分離できない場合はそのまま保持
                        new_rows.append(row)
                else:
                    # セミコロンがない場合はそのまま
                    new_rows.append(row)
            else:
                new_rows.append(row)
    
    # 結果を書き出し
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)
    
    print(f"\n分離完了: {separated_count}件の食草を分離")
    print(f"元の行数: {len(new_rows) - separated_count - 1}")  # ヘッダー除く
    print(f"新しい行数: {len(new_rows) - 1}")  # ヘッダー除く
    print(f"出力ファイル: {output_file}")

if __name__ == "__main__":
    separate_combined_plants()