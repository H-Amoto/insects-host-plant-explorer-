#!/usr/bin/env python3
import csv
import os
import shutil

def fix_specific_winter_moth_records():
    """特定の冬尺蛾レコードの植物名・部位を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 特定冬尺蛾レコード修正 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # 修正ルール
    fixes = {
        'record-7412': {  # ヤマナラシ(ハコヤナギ)
            'plant_name': 'ヤマナラシ',
            'plant_part': '',
            'notes_add': 'ハコヤナギとも呼ばれる'
        },
        'record-7420': {  # ケヤキ(飼育)
            'plant_name': 'ケヤキ',
            'plant_part': '',
            'observation_type': '飼育記録'
        },
        'record-7549': {  # クローバー(シロツメクサ)
            'plant_name': 'シロツメクサ',
            'plant_part': ''
        },
        'record-7550': {  # レッドクローバー(ムラサキツメクサ)
            'plant_name': 'ムラサキツメクサ',
            'plant_part': ''
        },
        'record-7641': {  # ミヤマキリシマ(花・葉)
            'plant_name': 'ミヤマキリシマ',
            'plant_part': '花・葉'
        },
        'record-7701': {  # ヤマツツジ(花)
            'plant_name': 'ヤマツツジ',
            'plant_part': '花'
        }
    }
    
    hostplants_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            record_id = row['record_id']
            
            if record_id in fixes:
                fix_info = fixes[record_id]
                
                old_plant_name = row['plant_name']
                old_plant_part = row['plant_part']
                old_observation_type = row['observation_type']
                
                # 修正を適用
                row['plant_name'] = fix_info['plant_name']
                row['plant_part'] = fix_info['plant_part']
                
                if 'observation_type' in fix_info:
                    row['observation_type'] = fix_info['observation_type']
                
                if 'notes_add' in fix_info:
                    if row['notes']:
                        row['notes'] = f"{row['notes']}; {fix_info['notes_add']}"
                    else:
                        row['notes'] = fix_info['notes_add']
                
                print(f"修正 {record_id}:")
                print(f"  植物名: '{old_plant_name}' → '{row['plant_name']}'")
                print(f"  部位: '{old_plant_part}' → '{row['plant_part']}'")
                if 'observation_type' in fix_info:
                    print(f"  観察タイプ: '{old_observation_type}' → '{row['observation_type']}'")
                print()
                
                fix_count += 1
            
            hostplants_data.append(row)
    
    print(f"修正結果: {fix_count}件")
    
    # ファイルを保存
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if hostplants_data:
            writer = csv.DictWriter(file, fieldnames=hostplants_data[0].keys())
            writer.writeheader()
            writer.writerows(hostplants_data)
    
    # normalized_dataフォルダにもコピー
    src = hostplants_file
    dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    print("hostplants.csvを更新しました")
    
    # 修正結果の検証
    print(f"\n=== 修正結果検証 ===")
    
    winter_moth_entries = []
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['reference'] == '日本の冬尺蛾':
                winter_moth_entries.append(row)
    
    # 部位情報の分析
    part_counts = {}
    for entry in winter_moth_entries:
        part = entry['plant_part'] or '(なし)'
        part_counts[part] = part_counts.get(part, 0) + 1
    
    print("部位別エントリ数:")
    for part, count in sorted(part_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {part}: {count}件")
    
    # 飼育記録の確認
    breeding_count = sum(1 for e in winter_moth_entries if e['observation_type'] == '飼育記録')
    print(f"\n飼育記録として分類されたエントリ: {breeding_count}件")
    
    print(f"\n✅ 特定冬尺蛾レコードの修正が完了しました！")

if __name__ == "__main__":
    fix_specific_winter_moth_records()