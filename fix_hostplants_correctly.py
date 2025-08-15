#!/usr/bin/env python3
import csv
import re
import os

def fix_hostplants_correctly():
    """食草データを正しく修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 食草データの正しい修正開始 ===")
    
    # 植物部位名のリスト
    plant_parts = {
        '根茎': '根茎',
        '樹皮': '樹皮', 
        '花弁': '花弁',
        '茎': '茎',
        '葉': '葉',
        '花': '花',
        '実': '実',
        '種子': '種子',
        '根': '根',
        '枝': '枝',
        '果実': '果実',
        '芽': '芽',
        '蕾': '蕾',
        '花序': '花序',
        '幹': '幹',
        '樹液': '樹液',
        '材': '材',
        '心材': '心材',
        '辺材': '辺材'
    }
    
    # 科名パターン（末尾が「科」）
    family_pattern = re.compile(r'^(.+科)$')
    
    # 元データを復元してから正しく修正
    print("元データから再変換します...")
    
    # 元の統合CSVから再度hostplantsデータを抽出
    source_file = os.path.join(base_dir, 'public', 'ListMJ_hostplants_master_backup_combined.csv')
    hostplants_data = []
    insect_counter = 1
    
    with open(source_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            japanese_name = row.get('和名', '').strip()
            hostplant_text = row.get('食草', '').strip()
            
            if not japanese_name or not hostplant_text or hostplant_text == '不明':
                continue
            
            insect_id = f"species-{insect_counter:04d}"
            insect_counter += 1
            
            # 食草テキストを解析
            plants = parse_hostplant_text(hostplant_text)
            
            for plant_info in plants:
                plant_name = plant_info['name']
                plant_family = plant_info['family']
                
                # 植物部位名チェック
                if plant_name in plant_parts:
                    # この食草エントリを削除し、前のエントリのplant_partを更新
                    if hostplants_data:
                        hostplants_data[-1]['plant_part'] = plant_parts[plant_name]
                    continue
                
                # 科名チェック
                family_match = family_pattern.match(plant_name)
                if family_match and not plant_family:
                    plant_family = family_match.group(1)
                    continue  # 科名のみの場合は食草エントリとして追加しない
                
                # 正常な食草エントリを追加
                hostplants_data.append({
                    'record_id': len(hostplants_data) + 1,
                    'insect_id': insect_id,
                    'plant_name': plant_name,
                    'plant_family': plant_family,
                    'observation_type': '野外（国内）',
                    'plant_part': '葉',
                    'life_stage': '幼虫',
                    'reference': row.get('出典', ''),
                    'notes': ''
                })
    
    print(f"再抽出完了: {len(hostplants_data)}件")
    
    # 新しいhostplants.csvを保存
    hostplants_file = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if hostplants_data:
            writer = csv.DictWriter(file, fieldnames=hostplants_data[0].keys())
            writer.writeheader()
            writer.writerows(hostplants_data)
    
    # publicフォルダにもコピー
    import shutil
    src = hostplants_file
    dst = os.path.join(base_dir, 'public', 'hostplants.csv')
    shutil.copy2(src, dst)
    
    print("正しい修正完了")
    return hostplants_data

def parse_hostplant_text(hostplant_text):
    """食草テキストを解析して個別食草リストに変換"""
    if not hostplant_text or hostplant_text.strip() in ['不明', '']:
        return []
    
    plants = []
    raw_plants = re.split(r'[;；]', hostplant_text)
    
    for plant_text in raw_plants:
        plant_text = plant_text.strip()
        if not plant_text:
            continue
            
        # 科名の抽出
        plant_name = plant_text
        plant_family = ''
        
        # パターン1: "ムクゲ(アオイ科)" → "ムクゲ", "アオイ科"
        match = re.match(r'^([^(（]+)[(（]([^)）]*科)[)）]', plant_text)
        if match:
            plant_name = match.group(1).strip()
            plant_family = match.group(2).strip()
        else:
            # パターン2: "チチジマキイチゴ(以上バラ科)" → "チチジマキイチゴ", "バラ科"
            match = re.match(r'^([^(（]+)[(（]以上([^)）]*科)[)）]', plant_text)
            if match:
                plant_name = match.group(1).strip()
                plant_family = match.group(2).strip()
        
        if plant_name:
            plants.append({
                'name': plant_name,
                'family': plant_family,
                'original_text': plant_text
            })
    
    return plants

if __name__ == "__main__":
    fix_hostplants_correctly()