#!/usr/bin/env python3
import csv
import re
import sys

def parse_hostplant_multiple(hostplant_text):
    """食草テキストを解析して、複数の植物名と科名を抽出"""
    if not hostplant_text or hostplant_text.strip() == '不明':
        return []
    
    hostplants = []
    
    # まず「以上○○科」パターンを特別に処理
    if '以上' in hostplant_text and '科' in hostplant_text:
        # セミコロンで大まかに分割してから処理
        segments = re.split(r'[;；]', hostplant_text)
        temp_plants = []
        
        for segment in segments:
            segment = segment.strip()
            if not segment:
                continue
                
            # 「(以上○○科)」パターンがある場合
            family_match = re.search(r'\(以上([^（）]+科)\)', segment)
            if family_match:
                # 前のセグメントから植物名を抽出
                plant_part = re.sub(r'\(以上[^（）]+科\)', '', segment).strip()
                if plant_part:
                    # この部分をさらに細かく分割
                    sub_plants = re.split(r'[、,]', plant_part)
                    for sub_plant in sub_plants:
                        sub_plant = sub_plant.strip()
                        if sub_plant:
                            temp_plants.append(sub_plant)
                
                # 蓄積した植物に共通科名を設定
                family_name = family_match.group(1)
                for plant_name in temp_plants:
                    if plant_name and plant_name != '不明':
                        hostplants.append({
                            'name': plant_name,
                            'family': family_name
                        })
                temp_plants = []  # リセット
                
            else:
                # 個別の科名がある場合
                individual_family_match = re.search(r'([^（）(]+)[（(]([^（）()]+科)[）)]', segment)
                if individual_family_match:
                    plant_name = individual_family_match.group(1).strip()
                    individual_family = individual_family_match.group(2).strip()
                    if plant_name and plant_name != '不明':
                        hostplants.append({
                            'name': plant_name,
                            'family': individual_family
                        })
                else:
                    # 科名指定なしの場合、カンマや読点で分割
                    plants_in_segment = re.split(r'[、,]', segment)
                    for plant in plants_in_segment:
                        plant_name = re.sub(r'[（(][^)）]*[）)]', '', plant).strip()
                        if plant_name and plant_name != '不明':
                            temp_plants.append(plant_name)
        
        # 最後に残った植物（科名なし）を処理
        for plant_name in temp_plants:
            if plant_name and plant_name != '不明':
                hostplants.append({
                    'name': plant_name,
                    'family': ''
                })
    
    else:
        # 「以上○○科」パターンがない場合は、全体をセミコロン、コンマ、読点で分割
        segments = re.split(r'[;；、,]', hostplant_text)
        
        for segment in segments:
            segment = segment.strip()
            if not segment:
                continue
                
            # 個別の科名がある場合
            individual_family_match = re.search(r'([^（）(]+)[（(]([^（）()]+科)[）)]', segment)
            if individual_family_match:
                plant_name = individual_family_match.group(1).strip()
                individual_family = individual_family_match.group(2).strip()
                if plant_name and plant_name != '不明':
                    hostplants.append({
                        'name': plant_name,
                        'family': individual_family
                    })
            else:
                # 科名指定なしの場合
                plant_name = re.sub(r'[（(][^)）]*[）)]', '', segment).strip()
                if plant_name and plant_name != '不明':
                    hostplants.append({
                        'name': plant_name,
                        'family': ''
                    })
    
    return hostplants

def convert_moth_data_fixed():
    """蛾類データを修正版で新形式に変換"""
    print("蛾類データを修正版で変換中...")
    
    input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master.csv'
    output_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master_fixed.csv'
    
    # ヘッダーを書き込み
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        header = [
            '昆虫ID', '分類群', '大図鑑カタログNo', '科名', '科和名', '亜科名', '亜科和名', '族名', '族和名', '亜族名', '亜族名_1', 
            '属名', '亜属名', '種小名', '亜種小名', '著者', '公表年', '類似種', '和名', '旧和名', '別名', 'その他の和名', 
            '亜種範囲', '標準図鑑ステータス', '標準図鑑以後の変更', '学名',
            '主要食草1', '主要食草科1', '観察タイプ1', '利用部位1', '利用ステージ1', '出典1', '食草備考1',
            '主要食草2', '主要食草科2', '観察タイプ2', '利用部位2', '利用ステージ2', '出典2', '食草備考2',
            '主要食草3', '主要食草科3', '観察タイプ3', '利用部位3', '利用ステージ3', '出典3', '食草備考3',
            '主要食草4', '主要食草科4', '観察タイプ4', '利用部位4', '利用ステージ4', '出典4', '食草備考4',
            '主要食草5', '主要食草科5', '観察タイプ5', '利用部位5', '利用ステージ5', '出典5', '食草備考5',
            '主要食草6', '主要食草科6', '観察タイプ6', '利用部位6', '利用ステージ6', '出典6', '食草備考6',
            '主要食草7', '主要食草科7', '観察タイプ7', '利用部位7', '利用ステージ7', '出典7', '食草備考7',
            '主要食草8', '主要食草科8', '観察タイプ8', '利用部位8', '利用ステージ8', '出典8', '食草備考8',
            '主要食草9', '主要食草科9', '観察タイプ9', '利用部位9', '利用ステージ9', '出典9', '食草備考9',
            '主要食草10', '主要食草科10', '観察タイプ10', '利用部位10', '利用ステージ10', '出典10', '食草備考10',
            '発生時期1', '発生時期出典1', '発生地域1', '発生時期備考1',
            '発生時期2', '発生時期出典2', '発生地域2', '発生時期備考2',
            '幼虫期1', '幼虫期出典1', '幼虫期備考1',
            '追加食草有無', 'データソース', '総合備考', '亜族和名'
        ]
        writer.writerow(header)
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
    
    with open(output_file, 'a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        
        for i, row in enumerate(rows):
            # 昆虫IDを生成 (M + 4桁番号)
            insect_id = f"M{i+1:04d}"
            
            # 食草情報を解析（複数対応）
            hostplant_text = row.get('食草', '')
            hostplants = parse_hostplant_multiple(hostplant_text)
            
            # デバッグ用：アオバシャチホコの食草処理を表示
            japanese_name = row.get('和名', '')
            if 'アオバシャチホコ' in japanese_name:
                print(f"DEBUG アオバシャチホコの食草処理:")
                print(f"  元テキスト: {hostplant_text}")
                print(f"  解析結果: {hostplants}")
            
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
            ]
            
            # 主要食草1-10を追加（最大10種まで対応）
            for j in range(10):
                if j < len(hostplants):
                    hp = hostplants[j]
                    new_row.extend([
                        hp['name'],                             # 主要食草N
                        hp['family'],                           # 主要食草科N
                        '野外（国内）',                         # 観察タイプN（デフォルト）
                        '葉',                                   # 利用部位N（デフォルト）
                        '幼虫',                                 # 利用ステージN（デフォルト）
                        row.get('出典', ''),                   # 出典N
                        ''                                      # 食草備考N
                    ])
                else:
                    new_row.extend(['', '', '', '', '', '', ''])  # 空の食草情報
            
            # 残りの列を追加
            new_row.extend([
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
                'はい' if len(hostplants) > 10 else '',        # 追加食草有無
                'ListMJ_hostplants_master.csv',                # データソース
                row.get('備考', ''),                           # 総合備考
                '',                                             # 亜族和名
            ])
            
            writer.writerow(new_row)
    
    print(f"蛾類データの修正版変換完了: {len(rows)}件")

def convert_hamushi_data_fixed():
    """ハムシデータを修正版で新形式に変換（追記）"""
    print("ハムシデータを修正版で変換中...")
    
    input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/hamushi_integrated_master.csv'
    output_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master_fixed.csv'
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
    
    with open(output_file, 'a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        
        for i, row in enumerate(rows):
            # 昆虫IDを生成 (H + 4桁番号)
            insect_id = f"H{i+1:04d}"
            
            # 食草情報を解析（複数対応）
            hostplant_text = row.get('食草', '')
            hostplants = parse_hostplant_multiple(hostplant_text)
            
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
            ]
            
            # 主要食草1-10を追加（最大10種まで対応）
            for j in range(10):
                if j < len(hostplants):
                    hp = hostplants[j]
                    new_row.extend([
                        hp['name'],                             # 主要食草N
                        hp['family'],                           # 主要食草科N
                        '野外（国内）',                         # 観察タイプN（デフォルト）
                        '葉',                                   # 利用部位N（デフォルト）
                        '幼虫',                                 # 利用ステージN（デフォルト）
                        row.get('出典', ''),                   # 出典N
                        ''                                      # 食草備考N
                    ])
                else:
                    new_row.extend(['', '', '', '', '', '', ''])  # 空の食草情報
            
            # 残りの列を追加
            new_row.extend([
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
                'はい' if len(hostplants) > 10 else '',        # 追加食草有無
                'hamushi_integrated_master.csv',               # データソース
                '',                                             # 総合備考
                row.get('亜族和名', ''),                       # 亜族和名
            ])
            
            writer.writerow(new_row)
    
    print(f"ハムシデータの修正版変換完了: {len(rows)}件")

def convert_beetle_data_fixed():
    """タマムシデータを修正版で新形式に変換（追記）"""
    print("タマムシデータを修正版で変換中...")
    
    input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/buprestidae_host.csv'
    output_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master_fixed.csv'
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
    
    with open(output_file, 'a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        
        for i, row in enumerate(rows):
            # 昆虫IDを生成 (T + 4桁番号)
            insect_id = f"T{i+1:04d}"
            
            # 食草情報を解析（複数対応）
            hostplant_text = row.get('食草', '')
            hostplants = parse_hostplant_multiple(hostplant_text)
            
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
            ]
            
            # 主要食草1-10を追加（最大10種まで対応）
            for j in range(10):
                if j < len(hostplants):
                    hp = hostplants[j]
                    new_row.extend([
                        hp['name'],                             # 主要食草N
                        hp['family'],                           # 主要食草科N
                        '野外（国内）',                         # 観察タイプN（デフォルト）
                        '葉',                                   # 利用部位N（デフォルト）
                        '幼虫',                                 # 利用ステージN（デフォルト）
                        row.get('出典', ''),                   # 出典N
                        ''                                      # 食草備考N
                    ])
                else:
                    new_row.extend(['', '', '', '', '', '', ''])  # 空の食草情報
            
            # 残りの列を追加
            new_row.extend([
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
                'はい' if len(hostplants) > 10 else '',        # 追加食草有無
                'buprestidae_host.csv',                        # データソース
                '',                                             # 総合備考
                '',                                             # 亜族和名
            ])
            
            writer.writerow(new_row)
    
    print(f"タマムシデータの修正版変換完了: {len(rows)}件")

def convert_butterfly_data_fixed():
    """蝶類データを修正版で新形式に変換して統合ファイルに追記"""
    print("蝶類データを修正版で変換中...")
    
    input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/butterfly_host.csv'
    output_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master_fixed.csv'
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
    
    with open(output_file, 'a', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        
        for i, row in enumerate(rows):
            # 昆虫IDを生成 (B + 4桁番号)
            insect_id = f"B{i+1:04d}"
            
            # 食草情報を解析（複数対応）
            hostplant_text = row.get('食草', '')
            hostplants = parse_hostplant_multiple(hostplant_text)
            
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
            ]
            
            # 主要食草1-3を追加
            for j in range(3):
                if j < len(hostplants):
                    hp = hostplants[j]
                    new_row.extend([
                        hp['name'],                             # 主要食草N
                        hp['family'],                           # 主要食草科N
                        '野外（国内）',                         # 観察タイプN（デフォルト）
                        '葉',                                   # 利用部位N（デフォルト）
                        '幼虫',                                 # 利用ステージN（デフォルト）
                        row.get('文献名', ''),                 # 出典N
                        ''                                      # 食草備考N
                    ])
                else:
                    new_row.extend(['', '', '', '', '', '', ''])  # 空の食草情報
            
            # 残りの列を追加
            new_row.extend([
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
                'はい' if len(hostplants) > 10 else '',        # 追加食草有無
                'butterfly_host.csv',                          # データソース
                row.get('備考', ''),                           # 総合備考
                '',                                             # 亜族和名
            ])
            
            writer.writerow(new_row)
    
    print(f"蝶類データの修正版変換完了: {len(rows)}件")

if __name__ == "__main__":
    print("修正版CSV統合処理を開始します...")
    
    # 蛾類データの変換
    convert_moth_data_fixed()
    
    # ハムシデータの変換  
    convert_hamushi_data_fixed()
    
    # タマムシデータの変換
    convert_beetle_data_fixed()
    
    # 蝶類データの変換
    convert_butterfly_data_fixed()
    
    print("修正版CSV統合処理が完了しました!")