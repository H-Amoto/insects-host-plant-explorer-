#!/usr/bin/env python3
"""
フェモラータモモブトハムシとフェモラータオオモモブトハムシの重複を修正するスクリプト
"""

import csv

def fix_femorata_duplicate():
    print("フェモラータ種の重複修正を開始します...")
    
    input_file = "public/hamushi_integrated_master.csv"
    output_file = "hamushi_integrated_master_fixed_femorata.csv"
    
    data = []
    headers = []
    
    # CSVファイルを読み込み
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            data.append(row)
    
    print(f"読み込み完了: {len(data)}行")
    
    # 対象行を特定
    target_354 = None
    target_671 = None
    
    for i, row in enumerate(data):
        # 学名がSagra femorataで和名にフェモラータが含まれる行を特定
        if (row.get('学名') == 'Sagra femorata' and 
            'フェモラータ' in row.get('和名', '')):
            
            if row.get('和名') == 'フェモラータモモブトハムシ':
                target_354 = i
                print(f"354行目相当を特定: 行{i+2} - {row.get('和名')}")
            elif row.get('和名') == 'フェモラータオオモモブトハムシ':
                target_671 = i  
                print(f"671行目相当を特定: 行{i+2} - {row.get('和名')}")
    
    if target_354 is None or target_671 is None:
        print("対象行が見つかりませんでした")
        return
    
    # データを統合
    catalog_row = data[target_354]  # 目録データベース版
    handbook_row = data[target_671]  # ハンドブック版
    
    print("\n=== データ統合 ===")
    print(f"目録版: {catalog_row.get('和名')} - {catalog_row.get('食草')}")
    print(f"ハンドブック版: {handbook_row.get('和名')} - {handbook_row.get('食草')}")
    
    # 統合されたデータを作成（ハンドブック版をベースにする）
    merged_row = handbook_row.copy()
    
    # 正式名称を「フェモラータオオモモブトハムシ」に
    merged_row['和名'] = 'フェモラータオオモモブトハムシ'
    
    # 別名に「フェモラータモモブトハムシ」を設定
    merged_row['別名'] = 'フェモラータモモブトハムシ'
    
    # 目録データベースの詳細な分類学情報を取得
    taxonomic_fields = ['科名', '科和名', '亜科名', '亜科和名', '族名', '族和名', 
                       '亜族名', '亜族和名', '属名', '亜属名', '種小名', '亜種小名', 
                       '著者', '公表年']
    
    for field in taxonomic_fields:
        if catalog_row.get(field) and not merged_row.get(field):
            merged_row[field] = catalog_row.get(field)
    
    # カタログNoは目録データベース版を使用
    merged_row['大図鑑カタログNo'] = catalog_row.get('大図鑑カタログNo')
    
    # 食草情報を統合（より詳細な情報を優先）
    catalog_plants = catalog_row.get('食草', '').strip()
    handbook_plants = handbook_row.get('食草', '').strip()
    
    if len(catalog_plants) > len(handbook_plants):
        merged_row['食草'] = catalog_plants
        print(f"食草: 目録版を採用 ({catalog_plants})")
    else:
        merged_row['食草'] = handbook_plants
        print(f"食草: ハンドブック版を採用 ({handbook_plants})")
    
    # 成虫出現時期は目録版から取得
    if catalog_row.get('成虫出現時期'):
        merged_row['成虫出現時期'] = catalog_row.get('成虫出現時期')
        merged_row['成虫出現時期出典'] = catalog_row.get('成虫出現時期出典')
    
    # 出典情報を統合
    catalog_source = catalog_row.get('出典', '').strip()
    handbook_source = handbook_row.get('出典', '').strip()
    merged_row['出典'] = f"{handbook_source}; {catalog_source}" if catalog_source != handbook_source else handbook_source
    
    # 備考を統合
    merged_row['備考'] = '[品質A(ハンドブック統合)]'
    
    print(f"\n統合結果:")
    print(f"- 和名: {merged_row.get('和名')}")
    print(f"- 別名: {merged_row.get('別名')}")
    print(f"- 食草: {merged_row.get('食草')}")
    print(f"- 成虫出現時期: {merged_row.get('成虫出現時期')}")
    print(f"- 出典: {merged_row.get('出典')}")
    
    # データを更新（重複を削除し、統合版を挿入）
    updated_data = []
    
    for i, row in enumerate(data):
        if i == target_354:
            # 354行目は統合版で置換
            updated_data.append(merged_row)
        elif i == target_671:
            # 671行目は削除（スキップ）
            continue
        else:
            updated_data.append(row)
    
    # ファイル出力
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(updated_data)
    
    print(f"\n修正完了:")
    print(f"- 入力: {len(data)}行")
    print(f"- 出力: {len(updated_data)}行")
    print(f"- 削減: {len(data) - len(updated_data)}行")
    print(f"- ファイル: {output_file}")
    
    return output_file

if __name__ == "__main__":
    fix_femorata_duplicate()