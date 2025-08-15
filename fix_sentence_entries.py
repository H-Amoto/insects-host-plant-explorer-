#!/usr/bin/env python3
import csv
import re
import os

def fix_sentence_entries():
    """文章形式のエントリを適切に分離"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 文章形式エントリの分離修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # 特定のパターンを修正
            if plant_name == "昆虫の死骸も与えれば食べる。":
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: 食草名='{plant_name}'")
                print(f"  新: 食草名='昆虫の死骸', 観察タイプ='飼育', 備考='与えれば食べる'")
                
                row['plant_name'] = '昆虫の死骸'
                row['observation_type'] = '飼育'
                row['notes'] = '与えれば食べる'
                fix_count += 1
                
            elif plant_name == "リョウメンシダの胞子を食する":
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: 食草名='{plant_name}'")
                print(f"  新: 食草名='リョウメンシダ', 部位='胞子'")
                
                row['plant_name'] = 'リョウメンシダ'
                row['plant_part'] = '胞子'
                fix_count += 1
                
            elif plant_name == "ケアリ属やアミメアリ属の幼虫を食する。また":
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: 食草名='{plant_name}'")
                print(f"  新: 食草名='アリ類幼虫', 観察タイプ='野外', 備考='ケアリ属やアミメアリ属'")
                
                row['plant_name'] = 'アリ類幼虫'
                row['observation_type'] = '野外（国内）'
                row['notes'] = 'ケアリ属やアミメアリ属'
                fix_count += 1
                
            elif plant_name == "アリの巣の中で":
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: 食草名='{plant_name}'")
                print(f"  新: 食草名='アリの巣', 観察タイプ='野外'")
                
                row['plant_name'] = 'アリの巣'
                row['observation_type'] = '野外（国内）'
                fix_count += 1
                
            elif plant_name == "枯れ葉も食べる":
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: 食草名='{plant_name}'")
                print(f"  新: 食草名='枯れ葉', 部位='枯れ葉'")
                
                row['plant_name'] = '枯れ葉'
                row['plant_part'] = '枯れ葉'
                fix_count += 1
                
            elif plant_name == "ギシギシなどの草本も食べる。":
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: 食草名='{plant_name}'")
                print(f"  新: 食草名='ギシギシ', 備考='草本も食べる'")
                
                row['plant_name'] = 'ギシギシ'
                row['notes'] = '草本も食べる'
                fix_count += 1
                
            # その他の文章形式パターン
            elif plant_name.endswith("を食する") and len(plant_name) > 10:
                # 「○○を食する」パターンの処理
                base_name = plant_name.replace("を食する", "")
                if "の" in base_name:
                    parts = base_name.split("の")
                    if len(parts) == 2:
                        plant_part = parts[0]
                        part_type = parts[1]
                        
                        print(f"修正: 行{row_num} {row['insect_id']}")
                        print(f"  元: 食草名='{plant_name}'")
                        print(f"  新: 食草名='{plant_part}', 部位='{part_type}'")
                        
                        row['plant_name'] = plant_part
                        row['plant_part'] = part_type
                        fix_count += 1
                    else:
                        new_data.append(row)
                else:
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: 食草名='{plant_name}'")
                    print(f"  新: 食草名='{base_name}'")
                    
                    row['plant_name'] = base_name
                    fix_count += 1
            
            new_data.append(row)
    
    print(f"\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  総エントリ数: {len(new_data)}件")
    
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
        
        # 昆虫の死骸の修正確認
        insect_carcass_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == '昆虫の死骸' and row['observation_type'] == '飼育':
                    insect_carcass_entries.append(f"{row['insect_id']}: {row['plant_name']} ({row['observation_type']}) - 備考: {row['notes']}")
        
        if insect_carcass_entries:
            print("昆虫の死骸修正例:")
            for entry in insect_carcass_entries:
                print(f"  {entry}")
        
        # その他の修正例
        other_fixes = ['リョウメンシダ', 'アリ類幼虫', 'アリの巣', 'ギシギシ']
        for plant in other_fixes:
            with open(hostplants_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['plant_name'] == plant and row['insect_id'] == 'species-0260':
                        print(f"\nその他修正例: {row['insect_id']} - {row['plant_name']}")
                        break
        
        # 残存する文章形式エントリをチェック
        remaining_sentences = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if any(pattern in row['plant_name'] for pattern in ['を食する', 'も食べる', '。また', 'の中で']):
                    remaining_sentences.append(row['plant_name'])
        
        if remaining_sentences:
            print(f"\n残存する文章形式エントリ ({len(remaining_sentences)}件):")
            for entry in list(set(remaining_sentences))[:5]:
                print(f"  '{entry}'")
        else:
            print("\n✅ 文章形式エントリの分離が完了しました")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_sentence_entries()