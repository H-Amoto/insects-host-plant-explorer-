#!/usr/bin/env python3
import csv
import re
import os

def parse_food_plants_with_dedup(text):
    """
    食草テキストを解析し、重複を除去する。
    例: "ヒイラギ (モクセイ科); ヤナギ類 (ヤナギ科); ヒイラギ (モクセイ科)" 
    → [{'name': 'ヒイラギ', 'family': 'モクセイ科'}, {'name': 'ヤナギ類', 'family': 'ヤナギ科'}]
    """
    if not text or text.strip() == '':
        return []
    
    # 「以上○○科」の処理
    text = re.sub(r'以上([^,;)]*科)', r'\1', text)
    
    # 分割パターン
    parts = re.split(r'[;；]', text)
    
    plants = []
    seen_plants = set()  # 重複チェック用
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # パターン1: "植物名 (科名)" 形式
        match = re.match(r'^([^()]+?)\s*\(([^)]+科)\)', part)
        if match:
            plant_name = match.group(1).strip()
            family_name = match.group(2).strip()
            
            # 重複チェック
            plant_key = (plant_name, family_name)
            if plant_key not in seen_plants:
                plants.append({'name': plant_name, 'family': family_name})
                seen_plants.add(plant_key)
            continue
        
        # パターン2: リスト形式 "植物1; 植物2; 植物3 (科名)"
        family_match = re.search(r'\(([^)]+科)\)', part)
        if family_match:
            family_name = family_match.group(1).strip()
            plant_part = part[:family_match.start()].strip()
            
            # セミコロンで分割
            plant_names = re.split(r'[;；]', plant_part)
            for plant_name in plant_names:
                plant_name = plant_name.strip()
                if plant_name:
                    # 重複チェック
                    plant_key = (plant_name, family_name)
                    if plant_key not in seen_plants:
                        plants.append({'name': plant_name, 'family': family_name})
                        seen_plants.add(plant_key)
            continue
        
        # パターン3: 科名なしの植物名
        plant_name = part.strip()
        if plant_name and '記録' not in plant_name:
            # 重複チェック
            plant_key = (plant_name, '')
            if plant_key not in seen_plants:
                plants.append({'name': plant_name, 'family': ''})
                seen_plants.add(plant_key)
    
    return plants[:10]  # 最大10個まで

def process_moth_data_dedup():
    """蛾類データを重複除去機能付きで処理"""
    input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master.csv'
    output_data = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        for row in reader:
            if len(row) < 26:
                continue
            
            # カタログ番号、分類群、学名、和名などの基本情報
            catalog_no = row[0]
            moth_id = f"M{catalog_no}"
            
            # 基本的な分類情報を取得
            taxon = "蛾類"
            family_latin = row[1] if len(row) > 1 else ""
            family_japanese = row[2] if len(row) > 2 else ""
            # ... その他の分類情報
            
            scientific_name = row[21] if len(row) > 21 else ""
            japanese_name = row[16] if len(row) > 16 else ""
            
            # 食草情報の解析（重複除去付き）
            food_plants_text = row[22] if len(row) > 22 else ""
            food_plants = parse_food_plants_with_dedup(food_plants_text)
            
            # 出典
            source = row[23] if len(row) > 23 else ""
            
            # 出力行を構築
            output_row = [
                moth_id, taxon, catalog_no, family_latin, family_japanese,
                "", "", "", "", "", "", "", "",  # 細分類は空白
                "", "", "", "", "", japanese_name, "", "", "", "", "", "",
                scientific_name
            ]
            
            # 食草データを追加（最大10個、各7列）
            for i, plant in enumerate(food_plants):
                if i >= 10:
                    break
                base_idx = 26 + i * 7
                while len(output_row) <= base_idx + 6:
                    output_row.append("")
                
                output_row[base_idx] = plant['name']      # 主要食草
                output_row[base_idx + 1] = plant['family'] # 科名
                output_row[base_idx + 2] = "野外（国内）"    # 観察タイプ
                output_row[base_idx + 3] = "葉"            # 利用部位
                output_row[base_idx + 4] = "幼虫"          # 利用ステージ
                output_row[base_idx + 5] = source         # 出典
                output_row[base_idx + 6] = ""             # 備考
            
            # 残りの列を埋める
            while len(output_row) < 111:
                output_row.append("")
            
            output_row[108] = "ListMJ_hostplants_master.csv"  # データソース
            
            output_data.append(output_row)
    
    return output_data

def integrate_csv_with_dedup():
    """重複除去機能付きCSV統合処理"""
    print("重複除去機能付きCSV統合処理を開始します...")
    
    # ヘッダー
    headers = [
        "昆虫ID", "分類群", "大図鑑カタログNo", "科名", "科和名", "亜科名", "亜科和名", "族名", "族和名",
        "亜族名", "亜族名_1", "属名", "亜属名", "種小名", "亜種小名", "著者", "公表年", "類似種", "和名",
        "旧和名", "別名", "その他の和名", "亜種範囲", "標準図鑑ステータス", "標準図鑑以後の変更", "学名"
    ]
    
    # 食草データ用ヘッダー（10食草×7列）
    for i in range(1, 11):
        headers.extend([
            f"主要食草{i}", f"主要食草科{i}", f"観察タイプ{i}", f"利用部位{i}", 
            f"利用ステージ{i}", f"出典{i}", f"食草備考{i}"
        ])
    
    # 追加ヘッダー
    headers.extend([
        "発生時期1", "発生時期出典1", "発生地域1", "発生時期備考1", "発生時期2", "発生時期出典2",
        "発生地域2", "発生時期備考2", "幼虫期1", "幼虫期出典1", "幼虫期備考1", "追加食草有無",
        "データソース", "総合備考", "亜族和名"
    ])
    
    # 蛾類データ処理
    print("蛾類データを重複除去機能付きで変換中...")
    moth_data = process_moth_data_dedup()
    print(f"蛾類データの重複除去変換完了: {len(moth_data)}件")
    
    # その他のデータは既存の統合ファイルから取得（蛾以外）
    existing_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master.csv'
    other_data = []
    
    if os.path.exists(existing_file):
        with open(existing_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # ヘッダーをスキップ
            for row in reader:
                if len(row) > 1 and not row[1] == "蛾類":  # 蛾類以外
                    other_data.append(row)
    
    # 統合データの書き出し
    output_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master.csv'
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        # 蛾類データ
        for row in moth_data:
            writer.writerow(row)
        
        # その他のデータ
        for row in other_data:
            writer.writerow(row)
    
    total_count = len(moth_data) + len(other_data)
    print(f"重複除去機能付きCSV統合処理が完了しました! 総計: {total_count}件")

if __name__ == "__main__":
    integrate_csv_with_dedup()