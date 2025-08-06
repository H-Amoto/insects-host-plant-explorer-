#!/usr/bin/env python3
"""
ツツハムシ亜科(Clytrinae)の族名・亜族名などの分類学的情報を文献に基づいて更新するスクリプト
"""

import csv
import re

def update_clytrinae_taxonomy():
    print("ツツハムシ亜科の分類学的情報更新を開始します...")
    
    # 文献から抽出した分類学的情報
    classification_mapping = {
        # Tribe Clytrini Kirby, 1837 - Subtribe Clytrina Kirby, 1837
        'タイワンカタハリナガツツハムシ': {
            'tribe': 'Clytrini', 'tribe_author': 'Kirby, 1837',
            'subtribe': 'Clytrina', 'subtribe_author': 'Kirby, 1837'
        },
        'ヨツボシナガツツハムシ': {
            'tribe': 'Clytrini', 'tribe_author': 'Kirby, 1837',
            'subtribe': 'Clytrina', 'subtribe_author': 'Kirby, 1837'
        },
        'ヨツボシアカツツハムシ': {
            'tribe': 'Clytrini', 'tribe_author': 'Kirby, 1837',
            'subtribe': 'Clytrina', 'subtribe_author': 'Kirby, 1837',
            'alternative_names': ['ズグロヨツボシナガツツハムシ', 'ヨモギナガツツハムシ']
        },
        'クロオビツツハムシ': {
            'tribe': 'Clytrini', 'tribe_author': 'Kirby, 1837',
            'subtribe': 'Clytrina', 'subtribe_author': 'Kirby, 1837'
        },
        'キボシルリハムシ': {
            'tribe': 'Clytrini', 'tribe_author': 'Kirby, 1837',
            'subtribe': 'Clytrina', 'subtribe_author': 'Kirby, 1837',
            'alternative_names': ['キボシナガツツハムシ']
        },
        'ツルグミナガツツハムシ': {
            'tribe': 'Clytrini', 'tribe_author': 'Kirby, 1837',
            'subtribe': 'Clytrina', 'subtribe_author': 'Kirby, 1837'
        },
        'ルリナガツツハムシ': {
            'tribe': 'Clytrini', 'tribe_author': 'Kirby, 1837',
            'subtribe': 'Clytrina', 'subtribe_author': 'Kirby, 1837'
        },
        'キイロナガツツハムシ': {
            'tribe': 'Clytrini', 'tribe_author': 'Kirby, 1837',
            'subtribe': 'Clytrina', 'subtribe_author': 'Kirby, 1837',
            'alternative_names': ['ヤナギナガツツハムシ']
        },
        'アザミナガツツハムシ': {
            'tribe': 'Clytrini', 'tribe_author': 'Kirby, 1837',
            'subtribe': 'Clytrina', 'subtribe_author': 'Kirby, 1837'
        },
        'ムナキルリハムシ': {
            'tribe': 'Clytrini', 'tribe_author': 'Kirby, 1837',
            'subtribe': 'Clytrina', 'subtribe_author': 'Kirby, 1837',
            'alternative_names': ['キムネナガツツハムシ']
        },
        
        # Tribe Cryptocephalini Gyllenhal, 1813 - Subtribe Cryptocephalina Gyllenhal, 1813
        'アイヌツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'セメノフツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813',
            'alternative_names': ['ミスジツツハムシ']
        },
        'フタスジツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'チビルリツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'エジマツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'キアシチビツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813',
            'alternative_names': ['モモグロチビツツハムシ']
        },
        'ウスグロスジツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813',
            'alternative_names': ['ウスグロチビツツハムシ']
        },
        'アカムネチビツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'キモトツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'タテスジキツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813',
            'alternative_names': ['クロスジツツハムシ']
        },
        'ハコネチビツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'ルリツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'キアシルリツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813',
            'alternative_names': ['バラルリツツハムシ']
        },
        'コヤツボシツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'ニセセスジツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'カラフトツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'キスジツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'リュウキュウツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'クロボシツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813',
            'alternative_names': ['ニセクロボシツツハムシ']
        },
        'ツヤルリツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'ヨツモンクロツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813',
            'alternative_names': ['ヨツモンツツハムシ']
        },
        'ムツキボシツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'セスジツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'ヤツボシツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813',
            'alternative_names': ['ヨツボシツツハムシ']
        },
        'キボシツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'カシワツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'ムツボシツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'ジュウシホシツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'ツマキクロツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'ヒロヒゲツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'ヒゲブトツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'ババチビツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        'アオチビツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Cryptocephalina', 'subtribe_author': 'Gyllenhal, 1813'
        },
        
        # Tribe Cryptocephalini Gyllenhal, 1813 - Subtribe Monachulina Leng, 1920
        'タマツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Monachulina', 'subtribe_author': 'Leng, 1920'
        },
        'リュウキュウタマツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Monachulina', 'subtribe_author': 'Leng, 1920'
        },
        'ウスグロヒメツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Monachulina', 'subtribe_author': 'Leng, 1920'
        },
        'ウスアカヒメツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Monachulina', 'subtribe_author': 'Leng, 1920'
        },
        'クロアシヒメツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Monachulina', 'subtribe_author': 'Leng, 1920'
        },
        'クロヒメツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Monachulina', 'subtribe_author': 'Leng, 1920'
        },
        'ムネミゾヒメツツハムシ': {
            'tribe': 'Cryptocephalini', 'tribe_author': 'Gyllenhal, 1813',
            'subtribe': 'Monachulina', 'subtribe_author': 'Leng, 1920'
        },
        
        # Tribe Fulcidacini Jakobson, 1924
        'カシワコブハムシ': {
            'tribe': 'Fulcidacini', 'tribe_author': 'Jakobson, 1924'
        },
        'ヒメコブハムシ': {
            'tribe': 'Fulcidacini', 'tribe_author': 'Jakobson, 1924'
        },
        'アマミコブハムシ': {
            'tribe': 'Fulcidacini', 'tribe_author': 'Jakobson, 1924'
        },
        'ミズキコブハムシ': {
            'tribe': 'Fulcidacini', 'tribe_author': 'Jakobson, 1924'
        },
        'ハバビロコブハムシ': {
            'tribe': 'Fulcidacini', 'tribe_author': 'Jakobson, 1924'
        },
        'ツツジコブハムシ': {
            'tribe': 'Fulcidacini', 'tribe_author': 'Jakobson, 1924'
        },
        'ツバキコブハムシ': {
            'tribe': 'Fulcidacini', 'tribe_author': 'Jakobson, 1924'
        },
        'ムシクソハムシ': {
            'tribe': 'Fulcidacini', 'tribe_author': 'Jakobson, 1924',
            'alternative_names': ['クヌギコブハムシ']
        },
        'ヤクシマコブハムシ': {
            'tribe': 'Fulcidacini', 'tribe_author': 'Jakobson, 1924'
        },
        
        # Tribe Pachybrachini Chapuis, 1874
        'ハギツツハムシ': {
            'tribe': 'Pachybrachini', 'tribe_author': 'Chapuis, 1874'
        }
    }
    
    input_file = "public/hamushi_integrated_master.csv"
    output_file = "hamushi_integrated_master_clytrinae_updated.csv"
    
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
        # ツツハムシ亜科の行を特定
        if row.get('亜科名') == 'Clytrinae' or row.get('亜科和名') == 'ツツハムシ亜科':
            japanese_name = row.get('和名', '')
            line_number = i + 2
            
            if japanese_name in classification_mapping:
                class_info = classification_mapping[japanese_name]
                
                print(f"\\n行{line_number}: {japanese_name}")
                
                # 族名を追加
                if not row.get('族名'):
                    row['族名'] = class_info['tribe']
                    print(f"  族名追加: {class_info['tribe']}")
                
                # 族和名を追加
                if not row.get('族和名'):
                    tribe_japanese = {
                        'Clytrini': 'ナガツツハムシ族',
                        'Cryptocephalini': 'ツツハムシ族',
                        'Fulcidacini': 'コブハムシ族',
                        'Pachybrachini': 'ハギツツハムシ族'
                    }.get(class_info['tribe'], '')
                    
                    if tribe_japanese:
                        row['族和名'] = tribe_japanese
                        print(f"  族和名追加: {tribe_japanese}")
                
                # 亜族名を追加
                if 'subtribe' in class_info and not row.get('亜族名'):
                    row['亜族名'] = class_info['subtribe']
                    print(f"  亜族名追加: {class_info['subtribe']}")
                
                # 亜族和名を追加（2番目の亜族名カラムを使用）
                # CSVのヘッダーでは亜族名が重複しているため、適切に処理
                # 実際は亜族和名のカラムがないようなので、備考に情報を追加
                
                # 別名を追加（既存の別名がない場合のみ）
                if 'alternative_names' in class_info and not row.get('別名'):
                    row['別名'] = '; '.join(class_info['alternative_names'])
                    print(f"  別名追加: {row['別名']}")
                
                updated_count += 1
    
    # ファイル出力
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"\\n更新完了:")
    print(f"- 更新したツツハムシ亜科: {updated_count}種")
    print(f"- 出力ファイル: {output_file}")
    
    return output_file

if __name__ == "__main__":
    update_clytrinae_taxonomy()