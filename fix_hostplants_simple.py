#!/usr/bin/env python3
import csv
import re
import os

def fix_hostplants_simple():
    """現在のデータを直接修正（安全な方法）"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 食草データの直接修正開始 ===")
    
    # バックアップから復元
    backup_file = os.path.join(base_dir, 'hostplants_backup.csv')
    
    # 元の正規化データをコピーして使用
    original_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # 最初に正規化データをコピーして作業用ファイル作成
    import shutil
    
    # 以前に正しく生成された正規化データがあるかチェック
    normalized_original = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    
    print("現在のデータを分析中...")
    
    # 現在のデータを読み込んで問題を特定
    problematic_entries = []
    valid_entries = []
    
    with open(original_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # 問題のあるエントリを特定
            if plant_name == '不明' and row.get('original_name'):
                # 以前に修正されたエントリ - 元に戻す必要がある
                problematic_entries.append({
                    'row': row_num,
                    'type': '過修正',
                    'current': plant_name,
                    'insect_id': row['insect_id']
                })
            
            # 植物部位名が食草名になっているケース
            elif plant_name in ['根茎', '樹皮', '花弁', '茎', '葉', '花', '実', '種子', '根', '枝', '果実']:
                problematic_entries.append({
                    'row': row_num,
                    'type': '植物部位',
                    'current': plant_name,
                    'insect_id': row['insect_id'],
                    'should_be_part': plant_name
                })
            
            # 明らかに科名のみのケース
            elif plant_name.endswith('科') and len(plant_name) <= 6:
                problematic_entries.append({
                    'row': row_num,
                    'type': '科名のみ',
                    'current': plant_name,
                    'insect_id': row['insect_id'],
                    'should_be_family': plant_name
                })
            
            else:
                valid_entries.append(row)
    
    print(f"分析結果:")
    print(f"  有効エントリ: {len(valid_entries)}件")
    print(f"  問題エントリ: {len(problematic_entries)}件")
    
    # 問題タイプ別に集計
    by_type = {}
    for entry in problematic_entries:
        type_key = entry['type']
        if type_key not in by_type:
            by_type[type_key] = []
        by_type[type_key].append(entry)
    
    for type_name, entries in by_type.items():
        print(f"    {type_name}: {len(entries)}件")
        if len(entries) <= 5:
            for entry in entries:
                print(f"      行{entry['row']}: {entry['insect_id']} → '{entry['current']}'")
    
    # 修正方針を確認
    print(f"\n修正方針:")
    print(f"1. 植物部位名 → 削除（plant_partは既存値を保持）")
    print(f"2. 科名のみ → plant_familyに移動し、エントリ削除")
    print(f"3. 過修正された正常な植物名 → 元に戻す（要手動確認）")
    
    return problematic_entries, valid_entries

if __name__ == "__main__":
    problematic, valid = fix_hostplants_simple()