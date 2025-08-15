#!/usr/bin/env python3
import csv
import os

def fix_butterfly_duplicates():
    """蝶類データの重複を除去し、正しい食草名を保持"""
    input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master.csv'
    backup_file = input_file + '.backup'
    
    # バックアップ作成
    os.rename(input_file, backup_file)
    
    print("蝶類重複データの修正を開始...")
    
    # データを読み込み、重複除去
    seen_ids = set()
    fixed_rows = []
    
    with open(backup_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        fixed_rows.append(header)
        
        rows = list(reader)
        
        # 逆順で処理（新しいエントリを優先）
        butterfly_rows = {}
        other_rows = []
        
        for row in rows:
            if len(row) > 0:
                insect_id = row[0]
                classification = row[1] if len(row) > 1 else ''
                
                if classification == '蝶類' and insect_id.startswith('B'):
                    # 蝶類の場合、より完全な食草情報を持つものを保持
                    if insect_id in butterfly_rows:
                        current_plant = row[27] if len(row) > 27 else ''
                        existing_plant = butterfly_rows[insect_id][27] if len(butterfly_rows[insect_id]) > 27 else ''
                        
                        # より詳細な食草情報（括弧の中身が多い）を優先
                        if current_plant and ('、' in current_plant or '）' in current_plant):
                            butterfly_rows[insect_id] = row
                        # 既存の方が不完全な場合（「アズマザサ」で切れてるなど）は置き換える
                        elif existing_plant and not existing_plant.endswith('）') and current_plant.endswith('）'):
                            butterfly_rows[insect_id] = row
                    else:
                        butterfly_rows[insect_id] = row
                else:
                    # 蝶類以外はそのまま
                    if insect_id not in seen_ids:
                        other_rows.append(row)
                        seen_ids.add(insect_id)
        
        # 蝶類データを追加
        for butterfly_row in butterfly_rows.values():
            fixed_rows.append(butterfly_row)
        
        # その他のデータを追加
        for row in other_rows:
            fixed_rows.append(row)
    
    # 修正データを保存
    with open(input_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(fixed_rows)
    
    print(f"修正完了: 蝶類 {len(butterfly_rows)} 種、総計 {len(fixed_rows)-1} 種")

if __name__ == "__main__":
    fix_butterfly_duplicates()