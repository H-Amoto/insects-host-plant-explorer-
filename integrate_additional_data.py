#!/usr/bin/env python3
import csv
import re
import os
from typing import List, Dict, Tuple

def clean_plant_name(name: str) -> str:
    """植物名をクリーンアップ"""
    if not name:
        return ""
    # 余分な空白を除去
    name = name.strip()
    # 空の場合は不明に
    if not name:
        return "不明"
    return name

def extract_family_from_complex_entry(plant_entry: str) -> Tuple[str, str]:
    """複雑な植物エントリから科名を抽出
    例: 'クスノキ科（クスノキ、タブノキ...）' -> ('クスノキ科', '')
    """
    # 科名パターンを検索
    family_match = re.search(r'([^（，、]+科)', plant_entry)
    if family_match:
        family = family_match.group(1)
        return family, ""
    return "", ""

def split_plant_entries(plant_text: str) -> List[Tuple[str, str, str]]:
    """植物エントリを分割して（植物名、科名、備考）のリストを返す"""
    if not plant_text or plant_text.strip() == "不明":
        return [("不明", "", "")]
    
    plants = []
    
    # 科レベルの記述を処理
    if re.search(r'科（[^）]+）', plant_text):
        # 例: ケマンソウ科のムラサキケマン、ジロボウエンゴサク...
        family_matches = re.finditer(r'([^，、]+科)(?:の|（)([^，、）]+)(?:，|、|）|$)', plant_text)
        for match in family_matches:
            family = match.group(1)
            species_list = match.group(2)
            # 個別種を分離
            species = re.split(r'[，、]', species_list)
            for sp in species:
                sp = sp.strip()
                if sp and sp != "など":
                    plants.append((sp, family, ""))
        
        # 追加の植物（科外）を処理
        remaining = re.sub(r'[^，、]+科(?:の|（)[^，、）]+(?:，|、|）)', '', plant_text)
        if remaining.strip():
            additional_plants = re.split(r'[，、]', remaining)
            for plant in additional_plants:
                plant = clean_plant_name(plant)
                if plant and plant != "など":
                    plants.append((plant, "", ""))
    else:
        # 通常の植物リスト（、で分割）
        plant_list = re.split(r'[，、]', plant_text)
        for plant in plant_list:
            plant = clean_plant_name(plant)
            if plant and plant != "など":
                # 属レベルの記述をチェック
                if "属" in plant and "（" in plant:
                    # 例: カンアオイ属（ミチノクサイシン、...）
                    genus_match = re.search(r'([^（]+属)（([^）]+)', plant)
                    if genus_match:
                        genus = genus_match.group(1)
                        species_in_genus = genus_match.group(2)
                        species_list = re.split(r'[，、]', species_in_genus)
                        for sp in species_list:
                            sp = sp.strip()
                            if sp and sp != "など":
                                plants.append((sp, "", f"{genus}の一種"))
                    else:
                        plants.append((plant, "", ""))
                else:
                    plants.append((plant, "", ""))
    
    # 空の結果の場合は不明を返す
    if not plants:
        return [("不明", "", "")]
    
    return plants

def create_insect_id_from_taxonomy(row: Dict, prefix: str) -> str:
    """分類情報からinsect_idを生成"""
    if prefix == "butterfly":
        # 蝶の場合: family-genus-species
        family = row.get('科', '').replace('科', '')
        genus = row.get('属', '')
        species = row.get('種小名', '')
        return f"butterfly-{family}-{genus}-{species}".lower()
    return f"{prefix}-unknown"

def integrate_buprestidae(base_dir: str) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """タマムシデータを統合"""
    print("=== buprestidae_host.csv の統合開始 ===")
    
    buprestidae_file = os.path.join(base_dir, 'public', 'buprestidae_host.csv')
    
    insects_data = []
    hostplants_data = []
    notes_data = []
    
    record_counter = 1
    
    with open(buprestidae_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            insect_id = f"species-{row['大図鑑カタログNo']}"
            
            # insects.csvエントリを作成
            insect_entry = {
                'insect_id': insect_id,
                'family': row['科名'],
                'family_jp': row['科和名'],
                'subfamily': row['亜科名'],
                'subfamily_jp': row['亜科和名'],
                'tribe': row['族名'],
                'tribe_jp': row['族和名'],
                'genus': row['属名'],
                'subgenus': row['亜属名'],
                'species': row['種小名'],
                'subspecies': row['亜種小名'],
                'author': row['著者'],
                'year': row['公表年'],
                'japanese_name': row['和名'],
                'old_japanese_name': row['旧和名'],
                'alternative_name': row['別名'],
                'other_names': row['その他の和名'],
                'scientific_name': row['学名'],
                'synonyms': '',
                'changes_since_standard': row['標準図鑑以後の変更'],
                'notes': ''
            }
            insects_data.append(insect_entry)
            
            # 食草データを処理
            plant_text = row['食草']
            reference = row['出典'] if row['出典'] else '日本産タマムシ大図鑑'
            
            if plant_text and plant_text.strip():
                plant_entries = split_plant_entries(plant_text)
                
                for i, (plant_name, plant_family, notes) in enumerate(plant_entries):
                    record_id = f"buprestidae-{row['大図鑑カタログNo']}-{i+1}"
                    
                    hostplant_entry = {
                        'record_id': record_id,
                        'insect_id': insect_id,
                        'plant_name': plant_name,
                        'plant_family': plant_family,
                        'observation_type': '',
                        'plant_part': '',
                        'life_stage': '',
                        'reference': reference,
                        'notes': notes
                    }
                    hostplants_data.append(hostplant_entry)
            
            # 備考を一般ノートとして追加
            if row['備考'] and row['備考'].strip():
                note_entry = {
                    'record_id': f"buprestidae-note-{row['大図鑑カタログNo']}",
                    'insect_id': insect_id,
                    'note_type': '生態情報',
                    'content': row['備考'],
                    'reference': reference,
                    'page': '',
                    'year': row['公表年']
                }
                notes_data.append(note_entry)
            
            # 成虫出現時期情報
            if row['成虫出現時期'] and row['成虫出現時期'].strip():
                note_entry = {
                    'record_id': f"buprestidae-period-{row['大図鑑カタログNo']}",
                    'insect_id': insect_id,
                    'note_type': '出現時期',
                    'content': row['成虫出現時期'],
                    'reference': row['成虫出現時期出典'] if row['成虫出現時期出典'] else reference,
                    'page': '',
                    'year': row['公表年']
                }
                notes_data.append(note_entry)
    
    print(f"  昆虫エントリ: {len(insects_data)}件")
    print(f"  食草エントリ: {len(hostplants_data)}件")
    print(f"  ノートエントリ: {len(notes_data)}件")
    
    return insects_data, hostplants_data, notes_data

def integrate_butterfly(base_dir: str) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """蝶データを統合"""
    print("=== butterfly_host.csv の統合開始 ===")
    
    butterfly_file = os.path.join(base_dir, 'public', 'butterfly_host.csv')
    
    insects_data = []
    hostplants_data = []
    notes_data = []
    
    with open(butterfly_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 1):
            insect_id = create_insect_id_from_taxonomy(row, "butterfly")
            
            # insects.csvエントリを作成
            insect_entry = {
                'insect_id': insect_id,
                'family': row['科'],
                'family_jp': row['科'],
                'subfamily': row['亜科'],
                'subfamily_jp': row['亜科'],
                'tribe': '',
                'tribe_jp': '',
                'genus': row['属'],
                'subgenus': '',
                'species': row['種小名'],
                'subspecies': '',
                'author': '',
                'year': '',
                'japanese_name': row['和名'],
                'old_japanese_name': '',
                'alternative_name': '',
                'other_names': '',
                'scientific_name': f"{row['属']} {row['種小名']}",
                'synonyms': '',
                'changes_since_standard': '',
                'notes': ''
            }
            insects_data.append(insect_entry)
            
            # 食草データを処理
            plant_text = row['食草']
            reference = row['文献名']
            
            if plant_text and plant_text.strip():
                plant_entries = split_plant_entries(plant_text)
                
                for i, (plant_name, plant_family, notes) in enumerate(plant_entries):
                    record_id = f"butterfly-{row_num}-{i+1}"
                    
                    hostplant_entry = {
                        'record_id': record_id,
                        'insect_id': insect_id,
                        'plant_name': plant_name,
                        'plant_family': plant_family,
                        'observation_type': '',
                        'plant_part': '',
                        'life_stage': '幼虫',
                        'reference': reference,
                        'notes': notes
                    }
                    hostplants_data.append(hostplant_entry)
            
            # 備考を追加
            if row['備考'] and row['備考'].strip():
                note_entry = {
                    'record_id': f"butterfly-note-{row_num}",
                    'insect_id': insect_id,
                    'note_type': '備考',
                    'content': row['備考'],
                    'reference': reference,
                    'page': '',
                    'year': ''
                }
                notes_data.append(note_entry)
    
    print(f"  昆虫エントリ: {len(insects_data)}件")
    print(f"  食草エントリ: {len(hostplants_data)}件")
    print(f"  ノートエントリ: {len(notes_data)}件")
    
    return insects_data, hostplants_data, notes_data

def integrate_hamushi(base_dir: str) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """ハムシデータを統合"""
    print("=== hamushi_integrated_master.csv の統合開始 ===")
    
    hamushi_file = os.path.join(base_dir, 'public', 'hamushi_integrated_master.csv')
    
    insects_data = []
    hostplants_data = []
    notes_data = []
    
    with open(hamushi_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            insect_id = f"species-{row['大図鑑カタログNo']}"
            
            # insects.csvエントリを作成
            insect_entry = {
                'insect_id': insect_id,
                'family': row['科名'],
                'family_jp': row['科和名'],
                'subfamily': row['亜科名'],
                'subfamily_jp': row['亜科和名'],
                'tribe': row['族名'],
                'tribe_jp': row['族和名'],
                'genus': row['属名'],
                'subgenus': row['亜属名'],
                'species': row['種小名'],
                'subspecies': row['亜種小名'],
                'author': row['著者'],
                'year': row['公表年'],
                'japanese_name': row['和名'],
                'old_japanese_name': row['旧和名'],
                'alternative_name': row['別名'],
                'other_names': row['その他の和名'],
                'scientific_name': row['学名'],
                'synonyms': '',
                'changes_since_standard': row['標準図鑑以後の変更'],
                'notes': ''
            }
            insects_data.append(insect_entry)
            
            # 食草データを処理
            plant_text = row['食草']
            reference = row['出典'] if row['出典'] else 'ハムシハンドブック'
            
            if plant_text and plant_text.strip() and plant_text.strip() != "不明":
                plant_entries = split_plant_entries(plant_text)
                
                for i, (plant_name, plant_family, notes) in enumerate(plant_entries):
                    record_id = f"hamushi-{row['大図鑑カタログNo']}-{i+1}"
                    
                    hostplant_entry = {
                        'record_id': record_id,
                        'insect_id': insect_id,
                        'plant_name': plant_name,
                        'plant_family': plant_family,
                        'observation_type': '',
                        'plant_part': '',
                        'life_stage': '',
                        'reference': reference,
                        'notes': notes
                    }
                    hostplants_data.append(hostplant_entry)
            elif plant_text and plant_text.strip() == "不明":
                # 不明エントリを明示的に追加
                record_id = f"hamushi-{row['大図鑑カタログNo']}-1"
                hostplant_entry = {
                    'record_id': record_id,
                    'insect_id': insect_id,
                    'plant_name': '不明',
                    'plant_family': '',
                    'observation_type': '',
                    'plant_part': '',
                    'life_stage': '',
                    'reference': reference,
                    'notes': ''
                }
                hostplants_data.append(hostplant_entry)
            
            # 備考を一般ノートとして追加
            if row['備考'] and row['備考'].strip():
                note_entry = {
                    'record_id': f"hamushi-note-{row['大図鑑カタログNo']}",
                    'insect_id': insect_id,
                    'note_type': '生態情報',
                    'content': row['備考'],
                    'reference': reference,
                    'page': '',
                    'year': row['公表年']
                }
                notes_data.append(note_entry)
            
            # 成虫出現時期情報
            if row['成虫出現時期'] and row['成虫出現時期'].strip():
                note_entry = {
                    'record_id': f"hamushi-period-{row['大図鑑カタログNo']}",
                    'insect_id': insect_id,
                    'note_type': '出現時期',
                    'content': row['成虫出現時期'],
                    'reference': row['成虫出現時期出典'] if row['成虫出現時期出典'] else reference,
                    'page': '',
                    'year': row['公表年']
                }
                notes_data.append(note_entry)
    
    print(f"  昆虫エントリ: {len(insects_data)}件")
    print(f"  食草エントリ: {len(hostplants_data)}件")
    print(f"  ノートエントリ: {len(notes_data)}件")
    
    return insects_data, hostplants_data, notes_data

def main():
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 追加データ統合スクリプト開始 ===")
    
    # 既存データを読み込み
    insects_file = os.path.join(base_dir, 'public', 'insects.csv')
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    notes_file = os.path.join(base_dir, 'public', 'general_notes.csv')
    
    # 既存のデータを保持
    existing_insects = []
    existing_hostplants = []
    existing_notes = []
    
    # 既存insects.csvを読み込み
    with open(insects_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        existing_insects = list(reader)
    
    # 既存hostplants.csvを読み込み
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        existing_hostplants = list(reader)
    
    # 既存general_notes.csvを読み込み
    with open(notes_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        existing_notes = list(reader)
    
    print(f"既存データ:")
    print(f"  昆虫: {len(existing_insects)}件")
    print(f"  食草: {len(existing_hostplants)}件")
    print(f"  ノート: {len(existing_notes)}件")
    
    # 新しいデータを統合
    all_new_insects = []
    all_new_hostplants = []
    all_new_notes = []
    
    # buprestidae統合
    bup_insects, bup_hostplants, bup_notes = integrate_buprestidae(base_dir)
    all_new_insects.extend(bup_insects)
    all_new_hostplants.extend(bup_hostplants)
    all_new_notes.extend(bup_notes)
    
    # butterfly統合
    but_insects, but_hostplants, but_notes = integrate_butterfly(base_dir)
    all_new_insects.extend(but_insects)
    all_new_hostplants.extend(but_hostplants)
    all_new_notes.extend(but_notes)
    
    # hamushi統合
    ham_insects, ham_hostplants, ham_notes = integrate_hamushi(base_dir)
    all_new_insects.extend(ham_insects)
    all_new_hostplants.extend(ham_hostplants)
    all_new_notes.extend(ham_notes)
    
    # 既存データと結合
    final_insects = existing_insects + all_new_insects
    final_hostplants = existing_hostplants + all_new_hostplants
    final_notes = existing_notes + all_new_notes
    
    print(f"\\n統合後のデータ:")
    print(f"  昆虫: {len(final_insects)}件 (+{len(all_new_insects)})")
    print(f"  食草: {len(final_hostplants)}件 (+{len(all_new_hostplants)})")
    print(f"  ノート: {len(final_notes)}件 (+{len(all_new_notes)})")
    
    # ファイルに保存
    print("\\n=== ファイル保存中 ===")
    
    # insects.csvを更新
    with open(insects_file, 'w', encoding='utf-8', newline='') as file:
        if final_insects:
            writer = csv.DictWriter(file, fieldnames=final_insects[0].keys())
            writer.writeheader()
            writer.writerows(final_insects)
    
    # hostplants.csvを更新
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if final_hostplants:
            writer = csv.DictWriter(file, fieldnames=final_hostplants[0].keys())
            writer.writeheader()
            writer.writerows(final_hostplants)
    
    # general_notes.csvを更新
    with open(notes_file, 'w', encoding='utf-8', newline='') as file:
        if final_notes:
            writer = csv.DictWriter(file, fieldnames=final_notes[0].keys())
            writer.writeheader()
            writer.writerows(final_notes)
    
    print("✅ 統合完了！")
    
    # 統合後の検証
    print("\\n=== 統合検証 ===")
    print("新規追加されたinsect_idのサンプル:")
    new_ids = [entry['insect_id'] for entry in all_new_insects[:5]]
    for id in new_ids:
        print(f"  {id}")

if __name__ == "__main__":
    main()