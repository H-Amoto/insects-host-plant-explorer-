#!/usr/bin/env python3
"""
Donacia属（ネクイハムシ類）の文献情報に基づく分類学的データの更新スクリプト
提供された文献：Tribe Donaciini Kirby, 1837の分類学的データ
"""

import csv
import re

def update_donacia_taxonomy():
    print("Donacia属の分類学的情報更新を開始します...")
    
    # 文献から抽出した分類学的データ
    donacia_literature_data = {
        # 族名を全てのDonaciaに適用
        'tribe': 'Donaciini',
        'tribe_author': 'Kirby, 1837',
        
        # 各種の詳細データ
        'species_data': {
            'Donacia aquatica': {
                'author': 'Linnaeus, 1758',
                'japanese_names': ['アオノネクイハムシ'],
                'conservation': None
            },
            'Donacia bicolora': {
                'author': 'Zschach, 1788',
                'japanese_names': ['アカガネネクイハムシ'],
                'conservation': None
            },
            'Donacia clavareaui': {
                'author': 'Jacobson, 1906',
                'japanese_names': ['カツラネクイハムシ'],
                'conservation': None
            },
            'Donacia crassipes': {
                'author': 'Fabricius, 1775',
                'japanese_names': ['フトネクイハムシ'],
                'conservation': None
            },
            'Donacia lenzi': {
                'author': 'Schönfeldt, 1888',
                'japanese_names': ['ガガブタネクイハムシ'],
                'conservation': None
            },
            'Donacia nitidior': {
                'author': 'Nakane, 1963',
                'japanese_names': ['ツヤネクイハムシ'],
                'conservation': None
            },
            'Donacia ozensis': {
                'author': 'Nakane, 1963',
                'japanese_names': ['キタヒラタネクイハムシ'],
                'subspecies': [
                    {
                        'subspecies': 'honshuensis',
                        'author': 'Hayashi, 1992',
                        'japanese_name': 'キタヒラタネクイハムシ本州亜種'
                    }
                ],
                'conservation': None
            },
            'Donacia provostii': {
                'author': 'Fairmaire, 1866',
                'japanese_names': ['イネネクイハムシ', 'ネクイハムシ'],
                'conservation': None
            },
            'Donacia semicuprea': {
                'author': 'Panzer, 1796',
                'japanese_names': ['クロガネネクイハムシ'],
                'conservation': None
            },
            'Donacia sparganii': {
                'author': 'Ahrens, 1810',
                'japanese_names': ['キンイロネクイハムシ'],
                'conservation': None
            },
            'Donacia thalassina': {
                'author': 'Germar, 1811',
                'japanese_names': ['キアシネクイハムシ'],
                'conservation': None
            },
            'Donacia tomentosa': {
                'author': 'Ahrens, 1810',
                'japanese_names': ['アシボソネクイハムシ'],
                'conservation': None
            },
            'Donacia vulgaris': {
                'author': 'Zschach, 1788',
                'japanese_names': ['コウホネネクイハムシ'],
                'conservation': None
            },
            'Donacia yersinensis': {
                'author': 'Pic, 1929',
                'japanese_names': ['ニセヒラタネクイハムシ'],
                'conservation': 'NT'  # Near Threatened
            },
            'Donacia hirashimai': {
                'author': 'Nakane, 1963',
                'japanese_names': ['ホソネクイハムシ'],
                'conservation': 'DD'  # Data Deficient
            },
            'Donacia sera': {
                'author': 'Jacobson, 1906',
                'japanese_names': ['セラネクイハムシ'],
                'conservation': None
            }
        }
    }
    
    input_file = "public/hamushi_integrated_master.csv"
    output_file = "hamushi_integrated_master_donacia_updated.csv"
    
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
        if row.get('属名') == 'Donacia':
            genus_species = f"Donacia"
            
            # 学名から種小名を抽出
            scientific_name = row.get('学名', '')
            species_match = re.search(r'Donacia\s+\(?[\w\s]*\)?\s*(\w+)', scientific_name)
            
            if species_match:
                species_name = species_match.group(1)
                full_species = f"Donacia {species_name}"
                
                print(f"\\n処理中: {row.get('和名')} ({scientific_name})")
                
                # 族情報を追加
                if not row.get('族名'):
                    row['族名'] = donacia_literature_data['tribe']
                    row['族和名'] = 'ネクイハムシ族'
                    print(f"  族名追加: {donacia_literature_data['tribe']}")
                
                # 文献データとマッチング（和名ベース）
                literature_match = None
                matched_species = None
                current_japanese_name = row.get('和名', '')
                
                # 亜種の場合は基本種で検索
                base_name = current_japanese_name.replace('本州亜種', '').strip()
                
                for lit_species, lit_data in donacia_literature_data['species_data'].items():
                    for jp_name in lit_data['japanese_names']:
                        if jp_name == current_japanese_name or jp_name == base_name:
                            literature_match = lit_data
                            matched_species = lit_species
                            break
                    if literature_match:
                        break
                
                if literature_match:
                    print(f"  文献データマッチ: {matched_species}")
                    
                    # 著者情報を更新
                    if not row.get('著者') and literature_match.get('author'):
                        row['著者'] = literature_match['author']
                        # 年を抽出
                        year_match = re.search(r'(\d{4})', literature_match['author'])
                        if year_match and not row.get('公表年'):
                            row['公表年'] = year_match.group(1)
                        print(f"  著者追加: {literature_match['author']}")
                    
                    # 亜種情報の処理
                    if '本州亜種' in current_japanese_name and 'subspecies' in literature_match:
                        for subspecies_info in literature_match['subspecies']:
                            if subspecies_info['japanese_name'] == current_japanese_name:
                                if not row.get('亜種小名'):
                                    row['亜種小名'] = subspecies_info['subspecies']
                                if not row.get('著者'):  # 既に基本種の著者が入っている場合は亜種著者で上書き
                                    row['著者'] = subspecies_info['author']
                                    year_match = re.search(r'(\d{4})', subspecies_info['author'])
                                    if year_match:
                                        row['公表年'] = year_match.group(1)
                                print(f"  亜種情報追加: {subspecies_info['subspecies']} ({subspecies_info['author']})")
                                break
                    
                    # 保全状況を備考に追加
                    if literature_match.get('conservation'):
                        current_remarks = row.get('備考', '')
                        conservation_note = f"保全状況: {literature_match['conservation']}"
                        if conservation_note not in current_remarks:
                            if current_remarks:
                                row['備考'] = f"{current_remarks}; {conservation_note}"
                            else:
                                row['備考'] = f"[品質B(目録データベース)]; {conservation_note}"
                        print(f"  保全状況追加: {literature_match['conservation']}")
                
                updated_count += 1
            
            else:
                print(f"\\n種小名抽出失敗: {row.get('和名')} ({scientific_name})")
    
    # ファイル出力
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"\\n更新完了:")
    print(f"- 処理したDonacia属: {updated_count}種")
    print(f"- 出力ファイル: {output_file}")
    
    return output_file

if __name__ == "__main__":
    update_donacia_taxonomy()