#!/usr/bin/env python3
import csv
import re
import os

def fix_detailed_feeding_info():
    """元ファイルの詳細情報を参照して正確に修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 詳細摂食情報の修正開始 ===")
    
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
            
        # species-0317の修正（アマリチビミノガ）
        if row['insect_id'] == 'species-0317':
            # 現在の行が「飼育条件下では緑色藻類」の場合
            if '飼育条件下では緑色藻類' in row['plant_name']:
                print(f"修正: species-0317の飼育情報を元ファイルに基づき再構成")
                
                # 1つ目のエントリ: 陸生緑色藻類
                new_row1 = row.copy()
                new_row1['plant_name'] = '緑色藻類'
                new_row1['observation_type'] = '飼育'
                new_row1['notes'] = '古い木材に生える陸生緑色藻類'
                new_data.append(new_row1)
                
                # 2つ目のエントリ: 昆虫の死骸
                new_row2 = row.copy()
                new_row2['plant_name'] = '昆虫の死骸'
                new_row2['observation_type'] = '飼育'
                new_row2['record_id'] = f"{row['record_id']}-2"
                new_row2['notes'] = '乾燥した昆虫の死骸'
                new_data.append(new_row2)
                
                # 次の関連行をスキップ対象にする
                for j in range(i + 1, min(i + 4, len(rows))):
                    if rows[j]['insect_id'] == 'species-0317':
                        if any(keyword in rows[j]['plant_name'] for keyword in [
                            'エノキタケ', '乾燥した小昆虫の死骸', '不明'
                        ]):
                            rows_to_skip.add(j)
                
                fix_count += 1
                
            else:
                new_data.append(row)
        
        # species-0322の修正（地表の有機物を食べる種）
        elif row['insect_id'] == 'species-0322':
            if '自然状態では地表のさまざまな有機物を食べていると推定される。' in row['plant_name']:
                print(f"修正: species-0322の摂食情報を整理")
                
                new_row = row.copy()
                new_row['plant_name'] = '地表有機物'
                new_row['observation_type'] = '野外（国内）'
                new_row['notes'] = '地表のさまざまな有機物を食べていると推定される'
                new_data.append(new_row)
                fix_count += 1
                
            elif '自然状態では地表近くや朽ち木下面などに生じるキノコ類（担子体）' in row['plant_name']:
                print(f"修正: species-0322のキノコ類情報を整理")
                
                new_row = row.copy()
                new_row['plant_name'] = 'キノコ類'
                new_row['observation_type'] = '野外（国内）'
                new_row['notes'] = '地表近くや朽ち木下面などに生じるキノコ類（担子体）'
                new_data.append(new_row)
                fix_count += 1
                
            elif 'カビ類（糸状体）などを食べているのが観察されている。' in row['plant_name']:
                print(f"修正: species-0322のカビ類情報を整理")
                
                new_row = row.copy()
                new_row['plant_name'] = 'カビ類'
                new_row['observation_type'] = '野外（国内）'
                new_row['notes'] = 'カビ類（糸状体）などを食べているのが観察されている'
                new_data.append(new_row)
                fix_count += 1
                
            else:
                new_data.append(row)
        
        # その他の長い説明文の処理
        elif len(row['plant_name']) > 30 and ('を食べて' in row['plant_name'] or 'が観察されている' in row['plant_name']):
            # 長い文章を簡潔に
            if 'その表面で羽化殻が確認されている' in row['plant_name']:
                new_row = row.copy()
                new_row['plant_name'] = 'ツリガネタケ'
                new_row['notes'] = 'その表面で羽化殻が確認されている'
                new_data.append(new_row)
                fix_count += 1
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
        
        # species-0317の修正確認
        species_0317_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['insect_id'] == 'species-0317' and row['observation_type'] == '飼育':
                    species_0317_entries.append(f"{row['plant_name']} - 備考: {row['notes']}")
        
        if species_0317_entries:
            print("species-0317の飼育記録修正例:")
            for entry in species_0317_entries:
                print(f"  {entry}")
        
        # species-0322の修正確認
        species_0322_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['insect_id'] == 'species-0322':
                    species_0322_entries.append(f"{row['plant_name']}")
        
        if species_0322_entries:
            print(f"\nspecies-0322の修正例: {', '.join(species_0322_entries)}")
        
        print("\n✅ 詳細摂食情報の修正が完了しました")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_detailed_feeding_info()