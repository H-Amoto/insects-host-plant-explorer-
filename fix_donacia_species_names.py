#!/usr/bin/env python3
"""
Donacia属の種小名を正しく修正するスクリプト
"""

import csv

def fix_donacia_species_names():
    print("Donacia属の種小名修正を開始します...")
    
    # 正しい種小名のマッピング
    species_mapping = {
        'ガガブタネクイハムシ': 'lenzi',
        'イネネクイハムシ': 'provostii', 
        'セラネクイハムシ': 'sera',
        'コウホネネクイハムシ': 'vulgaris',
        'キアシネクイハムシ': 'thalassina',
        'フトネクイハムシ': 'crassipes',
        'クロガネネクイハムシ': 'semicuprea',
        'アオノネクイハムシ': 'aquatica',
        'アカガネネクイハムシ': 'bicolora',
        'キンイロネクイハムシ': 'sparganii',
        'カツラネクイハムシ': 'clavareaui',
        'ツヤネクイハムシ': 'nitidior',
        'アシボソネクイハムシ': 'tomentosa',
        'キタヒラタネクイハムシ': 'ozensis',
        'キタヒラタネクイハムシ 本州亜種': 'ozensis',  # 基本種と同じ
        'ニセヒラタネクイハムシ': 'yersinensis',
        'ホソネクイハムシ': 'hirashimai',
        'ネクイハムシ': 'provostii'  # LB005行用
    }
    
    # 亜種小名のマッピング
    subspecies_mapping = {
        'キタヒラタネクイハムシ 本州亜種': 'honshuensis'
    }
    
    input_file = "public/hamushi_integrated_master.csv"
    output_file = "hamushi_integrated_master_species_fixed.csv"
    
    data = []
    headers = []
    
    # CSVファイルを読み込み
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            data.append(row)
    
    print(f"読み込み完了: {len(data)}行")
    
    updated_count = 0
    
    for i, row in enumerate(data):
        # Donacia属の行を特定
        if row.get('属名') == 'Donacia' or 'Donacia' in row.get('学名', ''):
            japanese_name = row.get('和名', '')
            
            if japanese_name in species_mapping:
                species_name = species_mapping[japanese_name]
                
                # 種小名を更新
                row['種小名'] = species_name
                
                # 亜種小名を更新（該当する場合）
                if japanese_name in subspecies_mapping:
                    row['亜種小名'] = subspecies_mapping[japanese_name]
                
                # 学名も正しく更新
                if row.get('亜属名'):
                    if row.get('亜種小名'):
                        row['学名'] = f"Donacia ({row['亜属名']}) {species_name} {row['亜種小名']}"
                    else:
                        row['学名'] = f"Donacia ({row['亜属名']}) {species_name}"
                else:
                    if row.get('亜種小名'):
                        row['学名'] = f"Donacia {species_name} {row['亜種小名']}"
                    else:
                        row['学名'] = f"Donacia {species_name}"
                
                print(f"修正: {japanese_name} → 種小名: {species_name}, 学名: {row['学名']}")
                updated_count += 1
    
    # ファイル出力
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"\\n修正完了:")
    print(f"- 更新したDonacia属: {updated_count}種")
    print(f"- 出力ファイル: {output_file}")
    
    return output_file

if __name__ == "__main__":
    fix_donacia_species_names()