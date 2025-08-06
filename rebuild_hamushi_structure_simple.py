#!/usr/bin/env python3
"""
ハムシファイルをListMJと同じ27列構造に統一するスクリプト (pandas不使用版)
"""

import csv
import os

def rebuild_hamushi_structure():
    print("ハムシファイル構造統一を開始します...")
    
    # ファイルパス
    legacy_hamushi_path = "legacy-local-hamushi-files/hamushi_species_integrated.csv"
    legacy_leafbeetle_path = "legacy-local-hamushi-files/leafbeetle_hostplants.csv"
    listmj_path = "public/ListMJ_hostplants_master.csv"
    output_path = "hamushi_integrated_master_listmj_structure.csv"
    
    # ListMJファイルから標準構造を取得
    with open(listmj_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        target_columns = next(reader)
    
    print(f"目標構造: {len(target_columns)}列")
    print(f"列名の一部: {target_columns[:5]}...")
    
    # 統合前hamushiファイル読み込み
    hamushi_data = []
    with open(legacy_hamushi_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        hamushi_columns = reader.fieldnames
        for row in reader:
            hamushi_data.append(row)
    
    print(f"統合前hamushi: {len(hamushi_data)}行, {len(hamushi_columns)}列")
    
    # leafbeetleファイル読み込み
    leafbeetle_data = []
    try:
        with open(legacy_leafbeetle_path, 'r', encoding='utf-8') as f:
            # BOMを除去
            content = f.read()
            if content.startswith('\ufeff'):
                content = content[1:]
            
            # 引用符で囲まれた行を処理
            lines = content.split('\n')
            if lines and lines[0].startswith('"'):
                # 最初の行から列名を抽出
                header_line = lines[0].strip('"')
                leafbeetle_columns = [col.strip() for col in header_line.split(',')]
                
                # データ行を処理
                for line in lines[1:]:
                    if line.strip() and line.startswith('"'):
                        # 引用符内のカンマを保護しながら分割
                        parts = []
                        in_quotes = False
                        current = ""
                        
                        for char in line:
                            if char == '"' and not in_quotes:
                                in_quotes = True
                            elif char == '"' and in_quotes:
                                in_quotes = False
                            elif char == ',' and not in_quotes:
                                parts.append(current.strip('"'))
                                current = ""
                                continue
                            current += char
                        
                        if current:
                            parts.append(current.strip('"'))
                        
                        if len(parts) >= len(leafbeetle_columns):
                            row_dict = {}
                            for i, col in enumerate(leafbeetle_columns):
                                if i < len(parts):
                                    # 内部の二重引用符を処理
                                    value = parts[i].replace('""', '"').strip()
                                    row_dict[col] = value
                                else:
                                    row_dict[col] = ''
                            leafbeetle_data.append(row_dict)
    except Exception as e:
        print(f"Leafbeetleファイル読み込みエラー: {e}")
        leafbeetle_data = []
        leafbeetle_columns = []
    
    print(f"Leafbeetle: {len(leafbeetle_data)}行")
    
    # 統合データ構築
    unified_data = []
    
    # hamushiデータを変換
    for row in hamushi_data:
        new_row = {}
        
        # 全ての目標列を初期化
        for col in target_columns:
            new_row[col] = ''
        
        # 直接マッピング
        column_mapping = {
            '大図鑑カタログNo': '大図鑑カタログNo',
            '科名': '科名',
            '科和名': '科和名',
            '亜科名': '亜科名',
            '亜科和名': '亜科和名',
            '族名': '族名',
            '族和名': '族和名',
            '亜族名': '亜族名',
            '亜族和名': '亜族和名',
            '属名': '属名',
            '亜属名': '亜属名',
            '種小名': '種小名',
            '亜種小名': '亜種小名',
            '著者': '著者',
            '公表年': '公表年',
            '類似種': '類似種',
            '和名': '和名',
            '旧和名': '旧和名',
            '別名': '別名',
            'その他の和名': 'その他の和名',
            '亜種範囲': '亜種範囲',
            '標準図鑑ステータス': '標準図鑑ステータス',
            '標準図鑑以後の変更': '標準図鑑以後の変更',
            '学名': '学名',
            '食草': '食草',
            '出典': '出典',
            '備考': '備考'
        }
        
        # データをマッピング
        for target_col, source_col in column_mapping.items():
            if source_col in row and row[source_col]:
                new_row[target_col] = row[source_col]
        
        # 品質情報を備考に追加
        source = new_row.get('出典', '')
        original_remarks = new_row.get('備考', '')
        quality = '品質B(目録データベース)'
        
        if original_remarks:
            new_row['備考'] = f"{original_remarks} [{quality}]"
        else:
            new_row['備考'] = f"[{quality}]"
        
        unified_data.append(new_row)
    
    # leafbeetleデータを変換
    for i, row in enumerate(leafbeetle_data):
        new_row = {}
        
        # 全ての目標列を初期化
        for col in target_columns:
            new_row[col] = ''
        
        # 基本情報をマッピング
        new_row['和名'] = row.get('和名', '')
        new_row['学名'] = row.get('学名', '')
        new_row['食草'] = row.get('食草', '')
        new_row['科和名'] = 'ハムシ科'
        new_row['科名'] = 'Chrysomelidae'
        new_row['大図鑑カタログNo'] = f"LB{i+1:03d}"
        
        # 出典情報を統合
        source_parts = []
        for key in ['書名', '著者', '出版社', '発行年']:
            if key in row and row[key]:
                if key == '書名':
                    source_parts.append(row[key])
                else:
                    source_parts.append(f"{key}: {row[key]}")
        
        new_row['出典'] = ', '.join(source_parts) if source_parts else 'ハムシハンドブック'
        new_row['備考'] = '[品質A(ハンドブック)]'
        
        unified_data.append(new_row)
    
    # 重複を除去（和名で判定）
    seen_names = set()
    unique_data = []
    for row in unified_data:
        name = row.get('和名', '')
        if name and name not in seen_names:
            seen_names.add(name)
            unique_data.append(row)
        elif not name:  # 和名が空の場合も含める
            unique_data.append(row)
    
    # ファイル出力
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=target_columns)
        writer.writeheader()
        writer.writerows(unique_data)
    
    print(f"\n統一構造ファイル生成完了:")
    print(f"- ファイル: {output_path}")
    print(f"- 総種数: {len(unique_data)}種")
    print(f"- 列数: {len(target_columns)}列")
    print(f"- ハムシ目録由来: {len(hamushi_data)}種")
    print(f"- ハンドブック由来: {len(leafbeetle_data)}種")
    
    # サンプルデータを表示
    print(f"\nサンプルデータ:")
    for i, row in enumerate(unique_data[:3]):
        print(f"{i+1}. {row.get('和名', 'N/A')} ({row.get('学名', 'N/A')}) - {row.get('食草', 'N/A')}")
    
    return output_path

if __name__ == "__main__":
    rebuild_hamushi_structure()