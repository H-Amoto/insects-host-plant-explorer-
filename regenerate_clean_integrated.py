#!/usr/bin/env python3
import csv
import re
import os

def parse_hostplant_butterfly_fixed(hostplant_text):
    """蝶類の食草テキストを解析（修正版）"""
    if not hostplant_text or hostplant_text.strip() == '不明':
        return '', ''
    
    # 括弧内のカンマは無視して分割
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
        return plant, ''
    
    return hostplant_text.strip(), ''

def add_hostplant_to_entry(entry_data, plant_name, plant_family='', obs_type='野外（国内）', 
                          part='葉', stage='幼虫', source='', remark=''):
    """エントリに食草データを追加"""
    if not plant_name or plant_name == '不明':
        return False
        
    # 空いている食草スロットを探す（主要食草1-5）
    for i in range(1, 6):
        plant_idx = 25 + (i-1) * 7  # 主要食草のインデックス
        if not entry_data[plant_idx]:  # 空のスロットを見つけた
            entry_data[plant_idx] = plant_name        # 主要食草
            entry_data[plant_idx + 1] = plant_family  # 主要食草科
            entry_data[plant_idx + 2] = obs_type      # 観察タイプ
            entry_data[plant_idx + 3] = part          # 利用部位
            entry_data[plant_idx + 4] = stage         # 利用ステージ
            entry_data[plant_idx + 5] = source        # 出典
            entry_data[plant_idx + 6] = remark        # 食草備考
            return True
    
    return False  # すべてのスロットが埋まっている

def create_species_key(scientific_name, japanese_name, classification):
    """種を一意に識別するキーを作成"""
    # 学名と和名の組み合わせで一意キーを作る
    sci_name = scientific_name.strip() if scientific_name else ""
    jp_name = japanese_name.strip() if japanese_name else ""
    class_name = classification.strip() if classification else ""
    
    if sci_name and jp_name:
        return f"{class_name}|{sci_name}|{jp_name}"
    elif sci_name:
        return f"{class_name}|{sci_name}|"
    elif jp_name:
        return f"{class_name}||{jp_name}"
    else:
        return None  # 学名も和名もない場合は処理しない

def get_preferred_insect_id(catalog_no, scientific_name, japanese_name, classification, counter_dict, used_ids):
    """最適な昆虫IDを取得"""
    if catalog_no:
        preferred_id = f"catalog-{catalog_no}"
        if preferred_id not in used_ids:
            used_ids.add(preferred_id)
            return preferred_id
    
    # カタログ番号がない場合や重複している場合は代替IDを生成
    if classification == '蛾類':
        prefix = 'moth'
    elif classification == '蝶類':
        prefix = 'butterfly'
    elif classification == 'ハムシ類':
        prefix = 'beetle'
    else:
        prefix = 'insect'
    
    if prefix not in counter_dict:
        counter_dict[prefix] = 1
    
    while True:
        alt_id = f"{prefix}-{counter_dict[prefix]:04d}"
        counter_dict[prefix] += 1
        if alt_id not in used_ids:
            used_ids.add(alt_id)
            return alt_id

def regenerate_clean_integrated():
    """クリーンな統合CSVを再生成（重複除去付き）"""
    print("クリーンな統合CSVファイルを再生成中...（重複除去機能付き）")
    
    # 出力ファイル
    output_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master.csv'
    backup_file = output_file + '.backup_' + str(int(__import__('time').time()))
    
    # 既存ファイルをバックアップ
    if os.path.exists(output_file):
        os.rename(output_file, backup_file)
        print(f"既存ファイルをバックアップ: {backup_file}")
    
    # ヘッダー
    header = [
        '昆虫ID', '分類群', '大図鑑カタログNo', '科名', '科和名', '亜科名', '亜科和名', 
        '族名', '族和名', '亜族名', '亜族名_1', '属名', '亜属名', '種小名', '亜種小名', 
        '著者', '公表年', '類似種', '和名', '旧和名', '別名', 'その他の和名', 'その他の和名_1', 
        '標準図鑑以後の変更', '学名', '主要食草1', '主要食草科1', '観察タイプ1', '利用部位1', 
        '利用ステージ1', '出典1', '食草備考1', '主要食草2', '主要食草科2', '観察タイプ2', 
        '利用部位2', '利用ステージ2', '出典2', '食草備考2', '主要食草3', '主要食草科3', 
        '観察タイプ3', '利用部位3', '利用ステージ3', '出典3', '食草備考3', 
        '主要食草4', '主要食草科4', '観察タイプ4', '利用部位4', '利用ステージ4', '出典4', '食草備考4',
        '主要食草5', '主要食草科5', '観察タイプ5', '利用部位5', '利用ステージ5', '出典5', '食草備考5',
        'データソース', '備考'
    ]
    
    # 重複除去のための辞書（種キーに基づく）
    insect_data = {}
    # 使用済みIDを追跡
    used_ids = set()
    # IDカウンター
    id_counters = {}
    
    # 1. 蛾類データ (ListMJ_hostplants_master.csv)
    print("蛾類データを処理中...")
    moth_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master.csv'
    try:
        with open(moth_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                catalog_no = row.get('大図鑑カタログNo', '').strip()
                scientific_name = row.get('学名', '').strip()
                japanese_name = row.get('和名', '').strip()
                
                # 種キーを作成
                species_key = create_species_key(scientific_name, japanese_name, '蛾類')
                if not species_key:
                    continue  # 学名も和名もない場合はスキップ
                
                # 既存エントリがあるかチェック
                if species_key not in insect_data:
                    # 最適なIDを取得
                    insect_id = get_preferred_insect_id(catalog_no, scientific_name, japanese_name, '蛾類', id_counters, used_ids)
                    
                    # 新しいエントリを作成
                    new_row = [insect_id, '蛾類'] + [''] * (len(header) - 2)
                    
                    # 基本情報
                    new_row[2] = catalog_no  # 大図鑑カタログNo
                    new_row[3] = row.get('科名', '')  # 科名
                    new_row[4] = row.get('科和名', '')  # 科和名
                    new_row[5] = row.get('亜科名', '')  # 亜科名
                    new_row[6] = row.get('亜科和名', '')  # 亜科和名
                    new_row[11] = row.get('属名', '')  # 属名
                    new_row[13] = row.get('種小名', '')  # 種小名
                    new_row[18] = row.get('和名', '')  # 和名
                    new_row[24] = row.get('学名', '')  # 学名
                    new_row[56] = 'ListMJ_hostplants_master.csv'  # データソース
                    new_row[57] = row.get('備考', '')  # 備考
                    
                    insect_data[species_key] = new_row
                
                # 食草情報を追加
                hostplant = row.get('食草', '').strip()
                if hostplant and hostplant != '不明':
                    add_hostplant_to_entry(
                        insect_data[species_key], 
                        hostplant, 
                        '',  # 科名なし
                        '野外（国内）', 
                        '葉', 
                        '幼虫', 
                        'ListMJ_hostplants_master'
                    )
    except FileNotFoundError:
        print(f"警告: {moth_file} が見つかりません")
    
    # 2. 蝶類データ (butterfly_host.csv)
    print("蝶類データを処理中...")
    butterfly_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/butterfly_host.csv'
    try:
        with open(butterfly_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                japanese_name = row.get('和名', '').strip()
                
                # 学名構築
                genus = row.get('属', '').strip()
                species = row.get('種小名', '').strip()
                scientific_name = f"{genus} {species}" if genus and species else ""
                
                # 種キーを作成
                species_key = create_species_key(scientific_name, japanese_name, '蝶類')
                if not species_key:
                    continue  # 学名も和名もない場合はスキップ
                
                # 既存エントリがあるかチェック
                if species_key not in insect_data:
                    # 最適なIDを取得
                    insect_id = get_preferred_insect_id('', scientific_name, japanese_name, '蝶類', id_counters, used_ids)
                    
                    # 新しいエントリを作成
                    new_row = [insect_id, '蝶類'] + [''] * (len(header) - 2)
                    
                    # 基本情報
                    new_row[3] = row.get('科', '')  # 科名
                    new_row[11] = genus  # 属名
                    new_row[13] = species  # 種小名
                    new_row[18] = japanese_name  # 和名
                    new_row[24] = scientific_name  # 学名
                    new_row[56] = 'butterfly_host.csv'  # データソース
                    
                    insect_data[species_key] = new_row
                
                # 食草情報を追加（修正版パーサーを使用）
                hostplant_text = row.get('食草', '').strip()
                if hostplant_text and hostplant_text != '不明':
                    plant_name, plant_family = parse_hostplant_butterfly_fixed(hostplant_text)
                    if plant_name:
                        add_hostplant_to_entry(
                            insect_data[species_key],
                            plant_name,
                            plant_family,
                            '野外（国内）',
                            '葉',
                            '幼虫',
                            row.get('出典', '日本産蝶類標準図鑑')
                        )
    except FileNotFoundError:
        print(f"警告: {butterfly_file} が見つかりません")
    
    # 3. ハムシ類データ (hamushi_integrated_master.csv)
    print("ハムシ類データを処理中...")
    leafbeetle_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/hamushi_integrated_master.csv'
    try:
        with open(leafbeetle_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                catalog_no = row.get('大図鑑カタログNo', '').strip()
                scientific_name = row.get('学名', '').strip()
                japanese_name = row.get('和名', '').strip()
                
                # 種キーを作成
                species_key = create_species_key(scientific_name, japanese_name, 'ハムシ類')
                if not species_key:
                    continue  # 学名も和名もない場合はスキップ
                
                # 既存エントリがあるかチェック
                if species_key not in insect_data:
                    # 最適なIDを取得
                    insect_id = get_preferred_insect_id(catalog_no, scientific_name, japanese_name, 'ハムシ類', id_counters, used_ids)
                    
                    # 新しいエントリを作成
                    new_row = [insect_id, 'ハムシ類'] + [''] * (len(header) - 2)
                    
                    # 基本情報
                    new_row[2] = catalog_no  # 大図鑑カタログNo
                    new_row[3] = row.get('科名', '')  # 科名
                    new_row[4] = row.get('科和名', '')  # 科和名
                    new_row[5] = row.get('亜科名', '')  # 亜科名
                    new_row[6] = row.get('亜科和名', '')  # 亜科和名
                    new_row[7] = row.get('族名', '')  # 族名
                    new_row[8] = row.get('族和名', '')  # 族和名
                    new_row[11] = row.get('属名', '')  # 属名
                    new_row[12] = row.get('亜属名', '')  # 亜属名
                    new_row[13] = row.get('種小名', '')  # 種小名
                    new_row[14] = row.get('亜種小名', '')  # 亜種小名
                    new_row[15] = row.get('著者', '')  # 著者
                    new_row[16] = row.get('公表年', '')  # 公表年
                    new_row[18] = row.get('和名', '')  # 和名
                    new_row[19] = row.get('旧和名', '')  # 旧和名
                    new_row[20] = row.get('別名', '')  # 別名
                    new_row[21] = row.get('その他の和名', '')  # その他の和名
                    new_row[23] = row.get('標準図鑑以後の変更', '')  # 標準図鑑以後の変更
                    new_row[24] = row.get('学名', '')  # 学名
                    new_row[56] = 'hamushi_integrated_master.csv'  # データソース
                    new_row[57] = row.get('備考', '')  # 備考
                    
                    insect_data[species_key] = new_row
                
                # 食草情報を追加
                hostplant = row.get('食草', '').strip()
                if hostplant and hostplant != '不明':
                    add_hostplant_to_entry(
                        insect_data[species_key],
                        hostplant,
                        '',  # 科名なし
                        '野外（国内）',
                        '葉',
                        '成虫・幼虫',
                        row.get('出典', 'ハムシハンドブック')
                    )
    except FileNotFoundError:
        print(f"警告: {leafbeetle_file} が見つかりません")
    
    # 4. 冬夜蛾データ (日本の冬夜蛾.csv) - 追加の食草情報
    print("冬夜蛾データを処理中...")
    winter_moth_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/日本の冬夜蛾.csv'
    try:
        with open(winter_moth_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                japanese_name = row.get('和名', '').strip()
                scientific_name = row.get('学名', '').strip()
                
                if not japanese_name and not scientific_name:
                    continue
                
                # 種キーを作成
                species_key = create_species_key(scientific_name, japanese_name, '蛾類')
                if not species_key:
                    continue
                
                # 既存エントリがある場合のみ食草情報を追加（新規エントリは作成しない）
                if species_key in insect_data:
                    hostplant = row.get('食草', '').strip()
                    if hostplant and hostplant != '不明':
                        add_hostplant_to_entry(
                            insect_data[species_key],
                            hostplant,
                            '',
                            '野外（国内）',
                            '葉',
                            '幼虫',
                            '日本の冬夜蛾'
                        )
    except FileNotFoundError:
        print(f"警告: {winter_moth_file} が見つかりません")
    
    # 5. 冬尺蛾データ (日本の冬尺蛾.csv) - 追加の食草情報
    print("冬尺蛾データを処理中...")
    winter_geometer_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/日本の冬尺蛾.csv'
    try:
        with open(winter_geometer_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                japanese_name = row.get('和名', '').strip()
                scientific_name = row.get('学名', '').strip()
                
                if not japanese_name and not scientific_name:
                    continue
                
                # 種キーを作成
                species_key = create_species_key(scientific_name, japanese_name, '蛾類')
                if not species_key:
                    continue
                
                # 既存エントリがある場合のみ食草情報を追加
                if species_key in insect_data:
                    hostplant = row.get('食草', '').strip()
                    if hostplant and hostplant != '不明':
                        add_hostplant_to_entry(
                            insect_data[species_key],
                            hostplant,
                            '',
                            '野外（国内）',
                            '葉',
                            '幼虫',
                            '日本の冬尺蛾'
                        )
    except FileNotFoundError:
        print(f"警告: {winter_geometer_file} が見つかりません")
    
    # 辞書のデータをリストに変換して出力
    all_rows = [header]
    for species_key, row_data in insect_data.items():
        all_rows.append(row_data)
    
    # CSVファイルに出力
    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(all_rows)
    
    print(f"重複除去後の統合CSVファイルを生成: {len(all_rows)-1}件のレコード")
    print(f"出力ファイル: {output_file}")
    
    # 統計情報を表示
    moth_count = sum(1 for row in all_rows[1:] if row[1] == '蛾類')
    butterfly_count = sum(1 for row in all_rows[1:] if row[1] == '蝶類')
    beetle_count = sum(1 for row in all_rows[1:] if row[1] == 'ハムシ類')
    
    print(f"内訳: 蛾類={moth_count}種, 蝶類={butterfly_count}種, ハムシ類={beetle_count}種")

if __name__ == "__main__":
    regenerate_clean_integrated()