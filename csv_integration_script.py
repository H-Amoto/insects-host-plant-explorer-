#!/usr/bin/env python3
import csv
import re
import sys

def parse_hostplant(hostplant_text):
    """食草テキストを解析して、植物名と科名を抽出"""
    if not hostplant_text or hostplant_text.strip() == '不明':
        return '', ''
    
    # パターン1: 植物名（科名）形式
    pattern1 = r'([^（）]+)（([^（）]+科)）'
    match = re.search(pattern1, hostplant_text)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    
    # パターン2: 科名が含まれていない場合
    # セミコロンやカンマで区切られた最初の植物名を取得
    plants = re.split(r'[;、,]', hostplant_text)
    if plants:
        return plants[0].strip(), ''
    
    return hostplant_text.strip(), ''

def convert_moth_data():
    """蛾類データを新形式に変換"""
    print("蛾類データを変換中...")
    
    input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master.csv'
    output_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master.csv'
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
    
    with open(output_file, 'a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        
        for i, row in enumerate(rows):
            # 昆虫IDを生成 (M + 4桁番号)
            insect_id = f"M{i+1:04d}"
            
            # 食草情報を解析
            hostplant_text = row.get('食草', '')
            plant_name, plant_family = parse_hostplant(hostplant_text)
            
            # 新しい行を構築
            new_row = [
                insect_id,                                      # 昆虫ID
                '蛾類',                                         # 分類群
                row.get('大図鑑カタログNo', ''),               # 大図鑑カタログNo
                row.get('科名', ''),                           # 科名
                row.get('科和名', ''),                         # 科和名
                row.get('亜科名', ''),                         # 亜科名
                row.get('亜科和名', ''),                       # 亜科和名
                row.get('族名', ''),                           # 族名
                row.get('族和名', ''),                         # 族和名
                row.get('亜族名', ''),                         # 亜族名
                row.get('亜族名_1', ''),                       # 亜族名_1
                row.get('属名', ''),                           # 属名
                row.get('亜属名', ''),                         # 亜属名
                row.get('種小名', ''),                         # 種小名
                row.get('亜種小名', ''),                       # 亜種小名
                row.get('著者', ''),                           # 著者
                row.get('公表年', ''),                         # 公表年
                row.get('類似種', ''),                         # 類似種
                row.get('和名', ''),                           # 和名
                row.get('旧和名', ''),                         # 旧和名
                row.get('別名', ''),                           # 別名
                row.get('その他の和名', ''),                   # その他の和名
                row.get('亜種範囲', ''),                       # 亜種範囲
                row.get('標準図鑑ステータス', ''),             # 標準図鑑ステータス
                row.get('標準図鑑以後の変更', ''),             # 標準図鑑以後の変更
                row.get('学名', ''),                           # 学名
                plant_name,                                     # 主要食草1
                plant_family,                                   # 主要食草科1
                '野外（国内）',                                # 観察タイプ1（デフォルト）
                '葉',                                          # 利用部位1（デフォルト）
                '幼虫',                                        # 利用ステージ1（デフォルト）
                row.get('出典', ''),                           # 出典1
                row.get('備考', ''),                           # 食草備考1
                '',                                             # 主要食草2
                '',                                             # 主要食草科2
                '',                                             # 観察タイプ2
                '',                                             # 利用部位2
                '',                                             # 利用ステージ2
                '',                                             # 出典2
                '',                                             # 食草備考2
                '',                                             # 主要食草3
                '',                                             # 主要食草科3
                '',                                             # 観察タイプ3
                '',                                             # 利用部位3
                '',                                             # 利用ステージ3
                '',                                             # 出典3
                '',                                             # 食草備考3
                row.get('成虫出現時期', ''),                   # 発生時期1
                row.get('成虫出現時期出典', ''),               # 発生時期出典1
                '',                                             # 発生地域1
                row.get('成虫出現時期備考', ''),               # 発生時期備考1
                '',                                             # 発生時期2
                '',                                             # 発生時期出典2
                '',                                             # 発生地域2
                '',                                             # 発生時期備考2
                row.get('幼虫期', ''),                         # 幼虫期1
                '',                                             # 幼虫期出典1
                row.get('幼虫期に関する備考', ''),             # 幼虫期備考1
                '',                                             # 追加食草有無
                'ListMJ_hostplants_master.csv',                # データソース
                '',                                             # 総合備考
                '',                                             # 亜族和名
            ]
            
            writer.writerow(new_row)
    
    print(f"蛾類データの変換完了: {len(rows)}件")

def convert_hamushi_data():
    """ハムシデータを新形式に変換（追記）"""
    print("ハムシデータを変換中...")
    
    input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/hamushi_integrated_master.csv'
    output_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master.csv'
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
    
    with open(output_file, 'a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        
        for i, row in enumerate(rows):
            # 昆虫IDを生成 (H + 4桁番号)
            insect_id = f"H{i+1:04d}"
            
            # 食草情報を解析
            hostplant_text = row.get('食草', '')
            plant_name, plant_family = parse_hostplant(hostplant_text)
            
            # 新しい行を構築
            new_row = [
                insect_id,                                      # 昆虫ID
                'ハムシ類',                                     # 分類群
                row.get('大図鑑カタログNo', ''),               # 大図鑑カタログNo
                row.get('科名', ''),                           # 科名
                row.get('科和名', ''),                         # 科和名
                row.get('亜科名', ''),                         # 亜科名
                row.get('亜科和名', ''),                       # 亜科和名
                row.get('族名', ''),                           # 族名
                row.get('族和名', ''),                         # 族和名
                row.get('亜族名', ''),                         # 亜族名
                row.get('亜族名_1', ''),                       # 亜族名_1
                row.get('属名', ''),                           # 属名
                row.get('亜属名', ''),                         # 亜属名
                row.get('種小名', ''),                         # 種小名
                row.get('亜種小名', ''),                       # 亜種小名
                row.get('著者', ''),                           # 著者
                row.get('公表年', ''),                         # 公表年
                row.get('類似種', ''),                         # 類似種
                row.get('和名', ''),                           # 和名
                row.get('旧和名', ''),                         # 旧和名
                row.get('別名', ''),                           # 別名
                row.get('その他の和名', ''),                   # その他の和名
                row.get('亜種範囲', ''),                       # 亜種範囲
                row.get('標準図鑑ステータス', ''),             # 標準図鑑ステータス
                row.get('標準図鑑以後の変更', ''),             # 標準図鑑以後の変更
                row.get('学名', ''),                           # 学名
                plant_name,                                     # 主要食草1
                plant_family,                                   # 主要食草科1
                '野外（国内）',                                # 観察タイプ1（デフォルト）
                '葉',                                          # 利用部位1（デフォルト）
                '幼虫',                                        # 利用ステージ1（デフォルト）
                row.get('出典', ''),                           # 出典1
                row.get('備考', ''),                           # 食草備考1
                '',                                             # 主要食草2
                '',                                             # 主要食草科2
                '',                                             # 観察タイプ2
                '',                                             # 利用部位2
                '',                                             # 利用ステージ2
                '',                                             # 出典2
                '',                                             # 食草備考2
                '',                                             # 主要食草3
                '',                                             # 主要食草科3
                '',                                             # 観察タイプ3
                '',                                             # 利用部位3
                '',                                             # 利用ステージ3
                '',                                             # 出典3
                '',                                             # 食草備考3
                row.get('成虫出現時期', ''),                   # 発生時期1
                row.get('成虫出現時期出典', ''),               # 発生時期出典1
                '',                                             # 発生地域1
                row.get('成虫出現時期備考', ''),               # 発生時期備考1
                '',                                             # 発生時期2
                '',                                             # 発生時期出典2
                '',                                             # 発生地域2
                '',                                             # 発生時期備考2
                row.get('幼虫期', ''),                         # 幼虫期1
                '',                                             # 幼虫期出典1
                row.get('幼虫期に関する備考', ''),             # 幼虫期備考1
                '',                                             # 追加食草有無
                'hamushi_integrated_master.csv',               # データソース
                '',                                             # 総合備考
                row.get('亜族和名', ''),                       # 亜族和名
            ]
            
            writer.writerow(new_row)
    
    print(f"ハムシデータの変換完了: {len(rows)}件")

def convert_beetle_data():
    """タマムシデータを新形式に変換（追記）"""
    print("タマムシデータを変換中...")
    
    input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/buprestidae_host.csv'
    output_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master.csv'
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
    
    with open(output_file, 'a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        
        for i, row in enumerate(rows):
            # 昆虫IDを生成 (T + 4桁番号)
            insect_id = f"T{i+1:04d}"
            
            # 食草情報を解析
            hostplant_text = row.get('食草', '')
            plant_name, plant_family = parse_hostplant(hostplant_text)
            
            # 新しい行を構築
            new_row = [
                insect_id,                                      # 昆虫ID
                'タマムシ類',                                   # 分類群
                row.get('大図鑑カタログNo', ''),               # 大図鑑カタログNo
                row.get('科名', ''),                           # 科名
                row.get('科和名', ''),                         # 科和名
                row.get('亜科名', ''),                         # 亜科名
                row.get('亜科和名', ''),                       # 亜科和名
                row.get('族名', ''),                           # 族名
                row.get('族和名', ''),                         # 族和名
                row.get('亜族名', ''),                         # 亜族名
                row.get('亜族名_1', ''),                       # 亜族名_1
                row.get('属名', ''),                           # 属名
                row.get('亜属名', ''),                         # 亜属名
                row.get('種小名', ''),                         # 種小名
                row.get('亜種小名', ''),                       # 亜種小名
                row.get('著者', ''),                           # 著者
                row.get('公表年', ''),                         # 公表年
                row.get('類似種', ''),                         # 類似種
                row.get('和名', ''),                           # 和名
                row.get('旧和名', ''),                         # 旧和名
                row.get('別名', ''),                           # 別名
                row.get('その他の和名', ''),                   # その他の和名
                row.get('亜種範囲', ''),                       # 亜種範囲
                row.get('標準図鑑ステータス', ''),             # 標準図鑑ステータス
                row.get('標準図鑑以後の変更', ''),             # 標準図鑑以後の変更
                row.get('学名', ''),                           # 学名
                plant_name,                                     # 主要食草1
                plant_family,                                   # 主要食草科1
                '野外（国内）',                                # 観察タイプ1（デフォルト）
                '葉',                                          # 利用部位1（デフォルト）
                '幼虫',                                        # 利用ステージ1（デフォルト）
                row.get('出典', ''),                           # 出典1
                row.get('備考', ''),                           # 食草備考1
                '',                                             # 主要食草2
                '',                                             # 主要食草科2
                '',                                             # 観察タイプ2
                '',                                             # 利用部位2
                '',                                             # 利用ステージ2
                '',                                             # 出典2
                '',                                             # 食草備考2
                '',                                             # 主要食草3
                '',                                             # 主要食草科3
                '',                                             # 観察タイプ3
                '',                                             # 利用部位3
                '',                                             # 利用ステージ3
                '',                                             # 出典3
                '',                                             # 食草備考3
                row.get('成虫出現時期', ''),                   # 発生時期1
                row.get('成虫出現時期出典', ''),               # 発生時期出典1
                '',                                             # 発生地域1
                row.get('成虫出現時期備考', ''),               # 発生時期備考1
                '',                                             # 発生時期2
                '',                                             # 発生時期出典2
                '',                                             # 発生地域2
                '',                                             # 発生時期備考2
                row.get('幼虫期', ''),                         # 幼虫期1
                '',                                             # 幼虫期出典1
                row.get('幼虫期に関する備考', ''),             # 幼虫期備考1
                '',                                             # 追加食草有無
                'buprestidae_host.csv',                        # データソース
                '',                                             # 総合備考
                '',                                             # 亜族和名
            ]
            
            writer.writerow(new_row)
    
    print(f"タマムシデータの変換完了: {len(rows)}件")

if __name__ == "__main__":
    print("CSV統合処理を開始します...")
    
    # 蛾類データの変換
    convert_moth_data()
    
    # ハムシデータの変換  
    convert_hamushi_data()
    
    # タマムシデータの変換
    convert_beetle_data()
    
    print("CSV統合処理が完了しました!")