#!/usr/bin/env python3
import csv
import os

def fix_ogasawara_plants():
    """小笠原諸島のギンネムとアメリカネムノキの記録を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 小笠原諸島のギンネム・アメリカネムノキ記録修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    rows_to_skip = set()
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    
    i = 0
    while i < len(rows):
        row = rows[i]
        
        if i in rows_to_skip:
            i += 1
            continue
        
        # species-3618の修正（行980-981）
        if row['insect_id'] == 'species-3618':
            # 現在の行が「小笠原諸島では」の場合
            if row['plant_name'] == '小笠原諸島では':
                print(f"修正: 行{i+2} species-3618の小笠原諸島記録を修正")
                
                # 次の行も確認
                if i + 1 < len(rows) and rows[i + 1]['insect_id'] == 'species-3618':
                    next_row = rows[i + 1]
                    if 'ギンネム' in next_row['plant_name'] and 'アメリカネムノキ' in next_row['plant_name']:
                        
                        # 1つ目のエントリ: ギンネム
                        new_row1 = row.copy()
                        new_row1['plant_name'] = 'ギンネム'
                        new_row1['plant_family'] = 'マメ科'
                        new_row1['notes'] = '小笠原諸島'
                        new_data.append(new_row1)
                        
                        # 2つ目のエントリ: アメリカネムノキ
                        new_row2 = row.copy()
                        new_row2['plant_name'] = 'アメリカネムノキ'
                        new_row2['plant_family'] = 'マメ科'
                        new_row2['record_id'] = f"{row['record_id']}-2"
                        new_row2['notes'] = '小笠原諸島'
                        new_data.append(new_row2)
                        
                        print(f"  修正: 'ギンネム' (小笠原諸島)")
                        print(f"  修正: 'アメリカネムノキ' (小笠原諸島)")
                        
                        # 次の行をスキップ
                        rows_to_skip.add(i + 1)
                        fix_count += 1
                    else:
                        new_data.append(row)
                else:
                    new_data.append(row)
            
            # 「ギンネム (ギンゴウカン) とアメリカネムノキ」の行の場合
            elif 'ギンネム' in row['plant_name'] and 'アメリカネムノキ' in row['plant_name']:
                # この行は前の行で処理済みなのでスキップされる
                pass
            
            else:
                new_data.append(row)
        
        else:
            new_data.append(row)
        
        i += 1
    
    print(f"\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  スキップしたエントリ: {len(rows_to_skip)}件")
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
        
        # species-3618の修正確認
        species_3618_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['insect_id'] == 'species-3618' and row['notes'] == '小笠原諸島':
                    species_3618_entries.append(f"{row['plant_name']} ({row['plant_family']})")
        
        if species_3618_entries:
            print("species-3618の小笠原諸島記録:")
            for entry in species_3618_entries:
                print(f"  {entry}")
        
        print("\n✅ 小笠原諸島のギンネム・アメリカネムノキ記録修正が完了しました")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_ogasawara_plants()