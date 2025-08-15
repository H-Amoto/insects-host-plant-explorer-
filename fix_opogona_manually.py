#!/usr/bin/env python3
import csv
import os

def fix_opogona_manually():
    """Opogona thiadelpha の記録を手動で正しく修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== Opogona thiadelpha の記録修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    # 元のファイルから得られる正しい食草リスト
    correct_plants = [
        'サトウキビ',
        'バナナ', 
        'ドラセナ',
        'ベンジャミン',
        'トウモロコシ',
        'サツマイモ'
    ]
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        found_species_0299 = False
        for row_num, row in enumerate(reader, 2):
            # species-0299の空のエントリや不正なエントリを探す
            if row['insect_id'] == 'species-0299':
                if not found_species_0299:
                    print(f"species-0299のエントリを正しい食草リストで置き換え")
                    
                    # 正しい食草エントリを作成
                    for i, plant in enumerate(correct_plants):
                        new_row = row.copy()
                        new_row['plant_name'] = plant
                        new_row['plant_family'] = ''  # 科名は不明
                        new_row['observation_type'] = '野外（国内）'
                        new_row['plant_part'] = '葉'
                        new_row['life_stage'] = '幼虫'
                        new_row['reference'] = '日本産蛾類標準図鑑3'
                        new_row['notes'] = ''
                        
                        # record_idを更新
                        if i == 0:
                            new_row['record_id'] = '291'  # 元の行の記録ID
                        else:
                            new_row['record_id'] = f"291-{i+1}"
                        
                        new_data.append(new_row)
                        print(f"  追加: {plant}")
                    
                    found_species_0299 = True
                    fix_count += 1
                # 他のspecies-0299エントリはスキップ
            else:
                new_data.append(row)
    
    if not found_species_0299:
        # species-0299が見つからない場合、新規作成
        print("species-0299が見つからないため、新規作成")
        
        for i, plant in enumerate(correct_plants):
            new_row = {
                'record_id': f'291-{i+1}' if i > 0 else '291',
                'insect_id': 'species-0299',
                'plant_name': plant,
                'plant_family': '',
                'observation_type': '野外（国内）',
                'plant_part': '葉',
                'life_stage': '幼虫',
                'reference': '日本産蛾類標準図鑑3',
                'notes': ''
            }
            new_data.append(new_row)
            print(f"  新規追加: {plant}")
        
        fix_count = 1
    
    print(f"\n修正結果:")
    print(f"  修正したspecies-0299: {fix_count}件")
    print(f"  追加した食草エントリ: {len(correct_plants)}件")
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
        species_0299_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['insect_id'] == 'species-0299':
                    species_0299_entries.append(row['plant_name'])
        
        print("species-0299の修正後食草リスト:")
        for entry in species_0299_entries:
            print(f"  {entry}")
        
        print("\n✅ Opogona thiadelpha の記録修正が完了しました")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_opogona_manually()