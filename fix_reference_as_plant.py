#!/usr/bin/env python3
import csv
import re
import os

def fix_reference_as_plant():
    """参考文献が食草名になっている問題を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 参考文献が食草名になっている問題の修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            notes = row.get('notes', '')
            
            # ケース1: species-5522の修正
            if row['insect_id'] == 'species-5522' and plant_name == '日本産蛾類標準図鑑2':
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: 食草名='{plant_name}', 備考='{notes}'")
                print(f"  新: 食草名='ネムノキ類', 科名='マメ科', 観察タイプ='国外', 参考文献='日本産蛾類標準図鑑2', 備考='インドでは'")
                
                row['plant_name'] = 'ネムノキ類'
                row['plant_family'] = 'マメ科'
                row['observation_type'] = '国外'
                row['reference'] = '日本産蛾類標準図鑑2'
                row['notes'] = 'インドでは'
                fix_count += 1
                
            # ケース2: species-4074とspecies-4277の修正（備考が空の場合は削除）
            elif plant_name in ['日本産蛾類標準図鑑1', '日本産蛾類標準図鑑2', '日本産蛾類標準図鑑3']:
                if not notes or notes.strip() == '':
                    print(f"削除: 行{row_num} {row['insect_id']} - 参考文献のみで食草情報なし")
                    fix_count += 1
                    continue  # この行をスキップ（削除）
                else:
                    print(f"要確認: 行{row_num} {row['insect_id']} - 参考文献が食草名: '{plant_name}', 備考: '{notes}'")
            
            new_data.append(row)
    
    print(f"\n修正結果:")
    print(f"  修正・削除したエントリ: {fix_count}件")
    print(f"  新しい総エントリ数: {len(new_data)}件")
    
    # 修正されたデータを保存
    if fix_count > 0:
        with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
            if new_data:
                writer = csv.DictWriter(file, fieldnames=new_data[0].keys())
                writer.writeheader()
                writer.writerows(new_data)
        
        # normalized_dataフォルダにもコピー
        import shutil
        src = hostplants_file
        dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
        shutil.copy2(src, dst)
        
        print("hostplants.csvを更新しました")
        
        # 検証
        print(f"\n=== 検証 ===")
        nemunoki_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == 'ネムノキ類' and row['observation_type'] == '国外':
                    nemunoki_entries.append(f"{row['insect_id']}: {row['plant_name']} ({row['observation_type']}) - {row['plant_family']}")
        
        if nemunoki_entries:
            print("ネムノキ類の国外記録修正例:")
            for entry in nemunoki_entries:
                print(f"  {entry}")
        
        # 残存する参考文献が食草名になっているケースをチェック
        remaining_references = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if '日本産蛾類標準図鑑' in row['plant_name']:
                    remaining_references.append(f"行{reader.line_num}: {row['insect_id']} - {row['plant_name']}")
        
        if remaining_references:
            print(f"\n残存する参考文献が食草名のケース ({len(remaining_references)}件):")
            for entry in remaining_references:
                print(f"  {entry}")
        else:
            print("\n✅ 参考文献が食草名になっている問題の修正が完了しました")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_reference_as_plant()