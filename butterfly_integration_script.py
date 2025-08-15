#!/usr/bin/env python3
import csv
import re

def parse_hostplant_butterfly(hostplant_text):
    """蝶類の食草テキストを解析"""
    if not hostplant_text or hostplant_text.strip() == '不明':
        return '', ''
    
    # 括弧内のカンマは無視して分割
    # 「イネ科（アズマザサ、チマキザサ、ミヤコザサ、スズタケ）」のような場合は全体を一つの植物として扱う
    plants = []
    current = ""
    paren_level = 0
    
    for char in hostplant_text:
        if char in '（(':
            paren_level += 1
            current += char
        elif char in '）)':
            paren_level -= 1
            current += char
        elif char in '、,;' and paren_level == 0:
            if current.strip():
                plants.append(current.strip())
            current = ""
        else:
            current += char
    
    if current.strip():
        plants.append(current.strip())
    
    if plants:
        plant = plants[0].strip()
        # 科名を推定（カンアオイ属→ウマノスズクサ科など）
        if '属' in plant:
            if 'カンアオイ' in plant:
                return plant, 'ウマノスズクサ科'
            elif 'サイシン' in plant:
                return plant, 'ウマノスズクサ科'
            elif 'スミレ' in plant:
                return plant, 'スミレ科'
            else:
                return plant, ''
        else:
            return plant, ''
    
    return hostplant_text.strip(), ''

def convert_butterfly_data():
    """蝶類データを新形式に変換して統合ファイルに追記"""
    print("蝶類データを変換中...")
    
    input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/butterfly_host.csv'
    output_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master.csv'
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
    
    with open(output_file, 'a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        
        for i, row in enumerate(rows):
            # 昆虫IDを生成 (B + 4桁番号)
            insect_id = f"B{i+1:04d}"
            
            # 食草情報を解析
            hostplant_text = row.get('食草', '')
            plant_name, plant_family = parse_hostplant_butterfly(hostplant_text)
            
            # 学名を構築
            genus = row.get('属', '')
            species = row.get('種小名', '')
            scientific_name = f"{genus} {species}".strip()
            
            # 新しい行を構築
            new_row = [
                insect_id,                                      # 昆虫ID
                '蝶類',                                         # 分類群
                '',                                             # 大図鑑カタログNo
                row.get('科', ''),                             # 科名
                '',                                             # 科和名
                row.get('亜科', ''),                           # 亜科名
                '',                                             # 亜科和名
                '',                                             # 族名
                '',                                             # 族和名
                '',                                             # 亜族名
                '',                                             # 亜族名_1
                row.get('属', ''),                             # 属名
                '',                                             # 亜属名
                row.get('種小名', ''),                         # 種小名
                '',                                             # 亜種小名
                '',                                             # 著者
                '',                                             # 公表年
                '',                                             # 類似種
                row.get('和名', ''),                           # 和名
                '',                                             # 旧和名
                '',                                             # 別名
                '',                                             # その他の和名
                '',                                             # 亜種範囲
                '',                                             # 標準図鑑ステータス
                '',                                             # 標準図鑑以後の変更
                scientific_name,                                # 学名
                plant_name,                                     # 主要食草1
                plant_family,                                   # 主要食草科1
                '野外（国内）',                                # 観察タイプ1（デフォルト）
                '葉',                                          # 利用部位1（デフォルト）
                '幼虫',                                        # 利用ステージ1（デフォルト）
                row.get('文献名', ''),                         # 出典1
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
                '',                                             # 発生時期1
                '',                                             # 発生時期出典1
                '',                                             # 発生地域1
                '',                                             # 発生時期備考1
                '',                                             # 発生時期2
                '',                                             # 発生時期出典2
                '',                                             # 発生地域2
                '',                                             # 発生時期備考2
                '',                                             # 幼虫期1
                '',                                             # 幼虫期出典1
                '',                                             # 幼虫期備考1
                '',                                             # 追加食草有無
                'butterfly_host.csv',                          # データソース
                '',                                             # 総合備考
                '',                                             # 亜族和名
            ]
            
            writer.writerow(new_row)
    
    print(f"蝶類データの変換完了: {len(rows)}件")

if __name__ == "__main__":
    print("蝶類CSV統合処理を開始します...")
    convert_butterfly_data()
    print("蝶類CSV統合処理が完了しました!")