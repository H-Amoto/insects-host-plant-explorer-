#!/usr/bin/env python3
"""
カメノコハムシ亜科の族名などの分類学的情報を文献に基づいて更新するスクリプト
"""

import csv
import re

def update_cassidinae_taxonomy():
    print("カメノコハムシ亜科の分類学的情報更新を開始します...")
    
    # 文献から抽出した族情報
    tribe_mapping = {
        # Tribe Aspidimorphini Chapuis, 1875
        'ジンガサハムシ': {'tribe': 'Aspidimorphini', 'tribe_author': 'Chapuis, 1875'},
        'ゴマダラジンガサハムシ': {'tribe': 'Aspidimorphini', 'tribe_author': 'Chapuis, 1875'},
        'スキバジンガサハムシ': {'tribe': 'Aspidimorphini', 'tribe_author': 'Chapuis, 1875'},
        'ヨツモンカメノコハムシ': {'tribe': 'Aspidimorphini', 'tribe_author': 'Chapuis, 1875'},
        
        # Tribe Cassidini Gyllenhal, 1813
        'タテスジヒメジンガサハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'キイロカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'セモンジンガサハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'ミドリカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'イカリアオカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'ヒメジンガサハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'イノコズチカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'クロスジカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'クロカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'ベニカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'ナミカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'スジキイロカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'ミカンカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'ヒメカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'アオカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'イカリヒメジンガサハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'チャイロカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'コガタカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'セスジカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'スジミドリカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'クロマダラカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'イチモンジカメノコハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        'ルイスジンガサハムシ': {'tribe': 'Cassidini', 'tribe_author': 'Gyllenhal, 1813'},
        
        # Tribe Cryptonychini Chapuis, 1875
        'ナガヒラタハムシ': {'tribe': 'Cryptonychini', 'tribe_author': 'Chapuis, 1875'},
        
        # Tribe Gonophorini Chapuis, 1875
        'オキナワホソヒラタハムシ': {'tribe': 'Gonophorini', 'tribe_author': 'Chapuis, 1875'},
        
        # Tribe Hispini Gyllenhal, 1813
        'ヨナグニトゲハムシ': {'tribe': 'Hispini', 'tribe_author': 'Gyllenhal, 1813'},
        'タケトゲハムシ': {'tribe': 'Hispini', 'tribe_author': 'Gyllenhal, 1813'},
        'イッシキトゲハムシ': {'tribe': 'Hispini', 'tribe_author': 'Gyllenhal, 1813'},
        'カタビロトゲハムシ': {'tribe': 'Hispini', 'tribe_author': 'Gyllenhal, 1813'},
        'ヒメキベリトゲハムシ': {'tribe': 'Hispini', 'tribe_author': 'Gyllenhal, 1813'},
        'ヒゴトゲハムシ': {'tribe': 'Hispini', 'tribe_author': 'Gyllenhal, 1813'},
        'イネトゲハムシ': {'tribe': 'Hispini', 'tribe_author': 'Gyllenhal, 1813'},
        'クロトゲハムシ': {'tribe': 'Hispini', 'tribe_author': 'Gyllenhal, 1813'},
        'ヘリビロトゲハムシ': {'tribe': 'Hispini', 'tribe_author': 'Gyllenhal, 1813'},
        'ツシマヘリビロトゲハムシ': {'tribe': 'Hispini', 'tribe_author': 'Gyllenhal, 1813'},
        'クロルリトゲハムシ': {'tribe': 'Hispini', 'tribe_author': 'Gyllenhal, 1813'},
        
        # Tribe Leptispini Fairmaire, 1868
        'ミヤモトホソヒラタハムシ': {'tribe': 'Leptispini', 'tribe_author': 'Fairmaire, 1868'},
        'タグチホソヒラタハムシ': {'tribe': 'Leptispini', 'tribe_author': 'Fairmaire, 1868'},
        
        # Tribe Notosacanthini Gressitt, 1952
        'アカヒラタカメノコハムシ': {'tribe': 'Notosacanthini', 'tribe_author': 'Gressitt, 1952'},
        'チャイロヒラタカメノコハムシ': {'tribe': 'Notosacanthini', 'tribe_author': 'Gressitt, 1952'},
        'キイロヒラタカメノコハムシ': {'tribe': 'Notosacanthini', 'tribe_author': 'Gressitt, 1952'}
    }
    
    # 別名マッピング（文献から確認できる別名）
    alternative_names = {
        'ナミカメノコハムシ': 'カメノコハムシ',  # 文献に記載
        'コガタカメノコハムシ': 'セダカカメノコハムシ',  # 文献に記載
        'スジキイロカメノコハムシ': 'チャイロカメノコハムシ',  # 文献に記載
        'タケトゲハムシ': 'イッシキトゲハムシ'  # 文献に記載
    }
    
    input_file = "public/hamushi_integrated_master.csv"
    output_file = "hamushi_integrated_master_cassidinae_updated.csv"
    
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
        # カメノコハムシ亜科の行を特定
        if row.get('亜科名') == 'Cassidinae' or row.get('亜科和名') == 'カメノコハムシ亜科':
            japanese_name = row.get('和名', '')
            line_number = i + 2
            
            if japanese_name in tribe_mapping:
                tribe_info = tribe_mapping[japanese_name]
                
                print(f"\\n行{line_number}: {japanese_name}")
                
                # 族名を追加
                if not row.get('族名'):
                    row['族名'] = tribe_info['tribe']
                    print(f"  族名追加: {tribe_info['tribe']}")
                
                # 族和名を追加（日本語名を作成）
                if not row.get('族和名'):
                    tribe_japanese = {
                        'Aspidimorphini': 'ジンガサハムシ族',
                        'Cassidini': 'カメノコハムシ族',
                        'Cryptonychini': 'ナガヒラタハムシ族',
                        'Gonophorini': 'ホソヒラタハムシ族',
                        'Hispini': 'トゲハムシ族',
                        'Leptispini': 'ホソヒラタハムシ族',
                        'Notosacanthini': 'ヒラタカメノコハムシ族'
                    }.get(tribe_info['tribe'], '')
                    
                    if tribe_japanese:
                        row['族和名'] = tribe_japanese
                        print(f"  族和名追加: {tribe_japanese}")
                
                # 別名を追加
                if japanese_name in alternative_names and not row.get('別名'):
                    row['別名'] = alternative_names[japanese_name]
                    print(f"  別名追加: {alternative_names[japanese_name]}")
                
                updated_count += 1
    
    # ファイル出力
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"\\n更新完了:")
    print(f"- 更新したカメノコハムシ亜科: {updated_count}種")
    print(f"- 出力ファイル: {output_file}")
    
    return output_file

if __name__ == "__main__":
    update_cassidinae_taxonomy()