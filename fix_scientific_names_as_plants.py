#!/usr/bin/env python3
import csv
import re
import os

def fix_scientific_names_as_plants():
    """科学名が食草名になっているケースを修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 科学名が食草名になっているケース修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # パターン1: Acronicta の科学名
            if re.match(r'^"?Acronicta [a-z]+ \\([A-Za-z& ,]+, [0-9]{4}\\)"?$', plant_name):
                print(f"削除: 行{row_num} {row['insect_id']}")
                print(f"  昆虫の科学名 '{plant_name[:50]}...' を削除")
                fix_count += 1
                continue  # この行は追加しない
            
            # パターン2: 一般的な昆虫科学名パターン（引用符付き）
            elif plant_name.startswith('"') and plant_name.endswith('"'):
                inner_name = plant_name[1:-1]  # 引用符を除去
                # 科学名パターンをチェック
                if re.match(r'^[A-Z][a-z]+ [a-z]+ \\([A-Za-z& ,]+, [0-9]{4}\\)$', inner_name):
                    print(f"削除: 行{row_num} {row['insect_id']}")
                    print(f"  昆虫の科学名 '{plant_name[:50]}...' を削除")
                    fix_count += 1
                    continue  # この行は追加しない
            
            # パターン3: 引用符なしの科学名パターン
            elif re.match(r'^[A-Z][a-z]+ [a-z]+ \\([A-Za-z& ,]+, [0-9]{4}\\)$', plant_name):
                print(f"削除: 行{row_num} {row['insect_id']}")
                print(f"  昆虫の科学名 '{plant_name[:50]}...' を削除")
                fix_count += 1
                continue  # この行は追加しない
            
            # パターン4: その他の明らかに昆虫名のパターン
            elif any(genus in plant_name for genus in [
                'Lepidoptera', 'Coleoptera', 'Diptera', 'Hymenoptera',
                'Hemiptera', 'Orthoptera', 'Neuroptera'
            ]):
                print(f"削除: 行{row_num} {row['insect_id']}")
                print(f"  昆虫の分類名 '{plant_name}' を削除")
                fix_count += 1
                continue  # この行は追加しない
            
            new_data.append(row)
    
    print(f"\\n修正結果:")
    print(f"  削除したエントリ: {fix_count}件")
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
        print(f"\\n=== 検証 ===")
        
        # 残存する科学名パターンをチェック
        remaining_scientific = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_name = row['plant_name']
                if (re.search(r'\\([A-Za-z& ,]+, [0-9]{4}\\)', plant_name) or
                    any(genus in plant_name for genus in ['Acronicta', 'Lepidoptera', 'Coleoptera'])):
                    remaining_scientific.append(plant_name)
        
        if remaining_scientific:
            print(f"残存する科学名パターン ({len(remaining_scientific)}件):")
            for entry in list(set(remaining_scientific))[:3]:
                print(f"  '{entry[:50]}...'")
        else:
            print("✅ 昆虫科学名の食草名からの除去が完了しました")
        
        # 削除前後のspecies-5713～5722の確認
        target_species = []
        for i in range(5713, 5723):
            species_id = f"species-{i}"
            with open(hostplants_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['insect_id'] == species_id:
                        target_species.append(f"{species_id}: {row['plant_name']}")
                        break
        
        if target_species:
            print(f"\\n対象種の残存食草例:")
            for entry in target_species[:5]:
                print(f"  {entry}")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_scientific_names_as_plants()