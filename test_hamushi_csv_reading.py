#!/usr/bin/env python3
import csv
import os

def test_hamushi_csv_reading():
    """ハムシ.csvの読み込みテスト"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    hamushi_file = os.path.join(base_dir, 'public', 'ハムシ.csv')
    
    print("=== ハムシ.csv読み込みテスト ===")
    
    species_count = 0
    
    with open(hamushi_file, 'r', encoding='utf-8') as file:
        # ヘッダー行を読む
        header = file.readline().strip().strip('"')
        print(f"ヘッダー: {header}")
        
        # データ行を読む
        for line_num, line in enumerate(file, 2):
            line = line.strip()
            if not line:
                continue
                
            # 手動でCSV解析
            if line.startswith('"') and '","' in line:
                # クォートで囲まれた形式
                parts = []
                current = ""
                in_quotes = False
                
                i = 0
                while i < len(line):
                    char = line[i]
                    
                    if char == '"':
                        if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                            # エスケープされたクォート
                            current += '"'
                            i += 2
                        else:
                            in_quotes = not in_quotes
                            i += 1
                    elif char == ',' and not in_quotes:
                        parts.append(current)
                        current = ""
                        i += 1
                    else:
                        current += char
                        i += 1
                
                parts.append(current)
                
                if len(parts) >= 3:
                    name_part = parts[0].strip()
                    scientific_part = parts[1].strip()
                    food_part = parts[2].strip()
                    
                    # 和名を抽出
                    if '、' in name_part:
                        japanese_name = name_part.split('、')[0].strip()
                    elif '(' in name_part:
                        japanese_name = name_part.split('(')[0].strip()
                    else:
                        japanese_name = name_part.strip()
                    
                    species_count += 1
                    
                    if species_count <= 5:
                        print(f"行{line_num}: {japanese_name}")
                        print(f"  学名: {scientific_part}")
                        print(f"  食草: {food_part}")
    
    print(f"\n総種数: {species_count}種")
    print("✅ ハムシ.csvの読み込みテストが完了しました")

if __name__ == "__main__":
    test_hamushi_csv_reading()