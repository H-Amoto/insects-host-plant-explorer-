#!/usr/bin/env python3
import csv
import os

def fix_acronicta_scientific_names():
    """Acronicta の科学名が食草名になっているケースを修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== Acronicta 科学名の修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    # 削除対象の科学名リスト
    target_scientific_names = [
        '"Acronicta strigosa (Denis & Schiffermüller, 1775)"',
        '"Acronicta jozana (Matsumura, 1926)"',
        '"Acronicta omorii (Matsumura, 1926)"',
        '"Acronicta albistigma (Hampson, 1909)"',
        '"Acronicta subpurpurea (Matsumura, 1926)"',
        '"Acronicta sugii (Kinoshita, 1990)"'
    ]
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # 対象の科学名かチェック
            if plant_name in target_scientific_names:
                print(f"削除: 行{row_num} {row['insect_id']}")
                print(f"  昆虫の科学名 '{plant_name}' を削除")
                fix_count += 1
                continue  # この行は追加しない
            
            # その他のAcronictl関連パターン
            elif 'Acronicta' in plant_name and ('1775' in plant_name or '1926' in plant_name or '1909' in plant_name or '1990' in plant_name):
                print(f"削除: 行{row_num} {row['insect_id']}")
                print(f"  Acronicta科学名 '{plant_name}' を削除")
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
        
        # 残存するAcronicta科学名をチェック
        remaining_acronicta = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'Acronicta' in row['plant_name']:
                    remaining_acronicta.append(row['plant_name'])
        
        if remaining_acronicta:
            print(f"残存するAcronicta科学名:")
            for entry in remaining_acronicta:
                print(f"  '{entry}'")
        else:
            print("✅ Acronicta科学名の除去が完了しました")
        
        # species-5713～5722の現在の食草を確認
        target_species_plants = []
        for i in range(5713, 5723):
            species_id = f"species-{i}"
            with open(hostplants_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                plants_for_species = []
                for row in reader:
                    if row['insect_id'] == species_id:
                        plants_for_species.append(row['plant_name'])
                if plants_for_species:
                    target_species_plants.append(f"{species_id}: {', '.join(plants_for_species[:3])}")
        
        print(f"\\n科学名削除後の対象種の食草:")
        for entry in target_species_plants:
            print(f"  {entry}")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_acronicta_scientific_names()