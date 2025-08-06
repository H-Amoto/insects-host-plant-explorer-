#!/usr/bin/env python3
"""
ハムシファイルをListMJと同じ27列構造に統一するスクリプト (修正版)
"""

import csv
import io

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
    
    # 統合前hamushiファイル読み込み
    hamushi_data = []
    with open(legacy_hamushi_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            hamushi_data.append(row)
    
    print(f"統合前hamushi: {len(hamushi_data)}行")
    
    # leafbeetleファイル読み込み (修正版)
    leafbeetle_data = []
    try:
        with open(legacy_leafbeetle_path, 'r', encoding='utf-8-sig') as f:  # BOMを自動除去
            # 全行読み込み 
            lines = f.readlines()
            
            if lines:
                # ヘッダー行を処理
                header_line = lines[0].strip()
                if header_line.startswith('"') and header_line.endswith('"'):
                    header_line = header_line[1:-1]  # 外側の引用符を除去
                leafbeetle_columns = [col.strip() for col in header_line.split(',')]
                print(f"Leafbeetle列名: {leafbeetle_columns}")
                
                # データ行を処理
                for line_num, line in enumerate(lines[1:], 2):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        # csvモジュールで1行をパース
                        reader = csv.reader([line])
                        parts = next(reader)
                        
                        if len(parts) >= len(leafbeetle_columns):
                            row_dict = {}
                            for i, col in enumerate(leafbeetle_columns):
                                if i < len(parts):
                                    row_dict[col] = parts[i].strip()
                                else:
                                    row_dict[col] = ''
                            leafbeetle_data.append(row_dict)
                    except Exception as e:
                        print(f"行 {line_num} 処理エラー: {e}")
                        
    except Exception as e:
        print(f"Leafbeetleファイル読み込みエラー: {e}")
    
    print(f"Leafbeetle: {len(leafbeetle_data)}行")
    
    # 統合データ構築
    unified_data = []
    
    # hamushiデータを変換
    for row in hamushi_data:
        new_row = {}
        
        # 全ての目標列を初期化
        for col in target_columns:
            new_row[col] = ''
        
        # 直接マッピング可能な列
        for col in target_columns:
            if col in row and row[col]:
                new_row[col] = str(row[col]).strip()
        
        # 品質情報を備考に追加
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
        new_row['和名'] = row.get('和名', '').strip()
        new_row['学名'] = row.get('学名', '').strip()
        new_row['食草'] = row.get('食草', '').strip()
        new_row['科和名'] = 'ハムシ科'
        new_row['科名'] = 'Chrysomelidae'
        new_row['大図鑑カタログNo'] = f"LB{i+1:03d}"
        
        # 出典情報を統合
        source_parts = []
        if row.get('書名'):
            source_parts.append(row['書名'])
        if row.get('著者'):
            source_parts.append(f"著者: {row['著者']}")
        if row.get('出版社'):
            source_parts.append(f"出版社: {row['出版社']}")
        if row.get('発行年'):
            source_parts.append(f"発行年: {row['発行年']}")
        
        new_row['出典'] = ', '.join(source_parts) if source_parts else 'ハムシハンドブック'
        new_row['備考'] = '[品質A(ハンドブック)]'
        
        unified_data.append(new_row)
    
    # 重複を除去（和名で判定）
    seen_names = set()
    unique_data = []
    for row in unified_data:
        name = row.get('和名', '').strip()
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
    
    # ハンドブックデータのサンプルも表示
    handbook_samples = [row for row in unique_data if '[品質A(ハンドブック)]' in row.get('備考', '')]
    if handbook_samples:
        print(f"\nハンドブックデータサンプル:")
        for i, row in enumerate(handbook_samples[:3]):
            print(f"{i+1}. {row.get('和名', 'N/A')} ({row.get('学名', 'N/A')}) - {row.get('食草', 'N/A')}")
    
    return output_path

if __name__ == "__main__":
    rebuild_hamushi_structure()