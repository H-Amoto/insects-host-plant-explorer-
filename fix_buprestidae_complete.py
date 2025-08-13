#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys

# 完全なデータ辞書（提供されたテキストから）
complete_data = [
    {"和名": "キボシフナガタタマムシ", "学名": "Acmaeodera (Cobosiella) luzonica Nonfried, 1895", "族名": "フナガタタマムシ族", "食草": "アデク、ハマボウ", "備考": "成虫はハマボウの花弁を後食する。アデクから羽化脱出した記録あり。", "成虫出現時期": "不明"},
    {"和名": "モンキタマムシ", "学名": "Prosima chinensis Marseul, 1867", "族名": "ツツタマムシ族", "食草": "モモ", "備考": "成虫はモモなどを後食する。本来の分布は中国大陸で、人為的に分布が拡大した外来種の可能性が推察される。", "成虫出現時期": "5~6月"},
    {"和名": "ケシツブタマムシ", "学名": "Mastogenius insperatus Y. Kurosawa, 1972", "族名": "ケシツブタマムシ族", "食草": "シバニッケイ、マルバニッケイ", "備考": "沖縄島ではマルバニッケイの枯れ枝から羽化。", "成虫出現時期": "4月上旬~6月上旬"},
    {"和名": "ミスジツブタマムシ", "学名": "Paratrachys hederae E. Saunders, 1873", "族名": "ツブタマムシ族", "食草": "オオイタビ、イタビカズラ", "備考": "幼虫はクワ科イチジク属植物の潜葉虫として葉裏に潜り込み、内部組織を食害する。", "成虫出現時期": "3~6月"},
    {"和名": "ダイトウツブタマムシ", "学名": "Paratrachys mixtipubescens Y. Kurosawa, 1985", "族名": "ツブタマムシ族", "食草": "オオイタビ", "備考": "北大東島の固有種。オオイタビの葉より成虫を羽化脱出させた記録あり。", "成虫出現時期": "3~6月頃 (秋期に発生している可能性もあり)"},
    {"和名": "オオシマツブタマムシ (原名亜種)", "学名": "Paratrachys princeps princeps Y. Kurosawa, 1976", "族名": "ツブタマムシ族", "食草": "オオイタビ、イタビカズラ、ヒメイタビ", "備考": "幼虫はイチジク属植物の潜葉虫。", "成虫出現時期": "3~6月"},
    {"和名": "オオシマツブタマムシ (沖縄亜種)", "学名": "Paratrachys princeps chujoi Y. Kurosawa, 1976", "族名": "ツブタマムシ族", "食草": "オオイタビ、イタビカズラ、ヒメイタビ", "備考": "幼虫はイチジク属植物の潜葉虫。", "成虫出現時期": "3~6月"},
    {"和名": "オオシマツブタマムシ (与那国島亜種)", "学名": "Paratrachys princeps kasaharai Y. Kurosawa, 1985", "族名": "ツブタマムシ族", "食草": "オオイタビ、イタビカズラ、ヒメイタビ", "備考": "幼虫はイチジク属植物の潜葉虫。", "成虫出現時期": "3~6月"},
    {"和名": "タマムシ (ヤマトタマムシ) (原名亜種)", "学名": "Chrysochroa fulgidissima fulgidissima (Schönherr, 1817)", "族名": "ルリタマムシ族", "食草": "エノキ、リュウキュウエノキ、ケヤキ、サクラ類、カシ類、カキ、クワ、ハリエンジュ (ニセアカシア)", "備考": "成虫はエノキ、ケヤキ、サクラ類などの太めの枯れ枝に集まる。", "成虫出現時期": "6~8月"},
    {"和名": "タマムシ (ヤマトタマムシ) (対馬亜種)", "学名": "Chrysochroa fulgidissima coeruleocephala Motschulsky, 1861", "族名": "ルリタマムシ族", "食草": "エノキ、リュウキュウエノキ、ケヤキ、サクラ類、カシ類、カキ、クワ、ハリエンジュ (ニセアカシア)", "備考": "成虫はエノキ、ケヤキ、サクラ類などの太めの枯れ枝に集まる。", "成虫出現時期": "6~8月"},
    {"和名": "タマムシ (ヤマトタマムシ) (男女亜種)", "学名": "Chrysochroa fulgidissima adachii Akiyama and Ohmomo, 1998", "族名": "ルリタマムシ族", "食草": "エノキ、リュウキュウエノキ、ケヤキ、サクラ類、カシ類、カキ、クワ、ハリエンジュ (ニセアカシア)", "備考": "成虫はエノキ、ケヤキ、サクラ類などの太めの枯れ枝に集まる。", "成虫出現時期": "6~8月"},
    {"和名": "タマムシ (ヤマトタマムシ) (奄美・沖縄亜種)", "学名": "Chrysochroa fulgidissima alternans Waterhouse, 1888", "族名": "ルリタマムシ族", "食草": "エノキ、リュウキュウエノキ、ケヤキ、サクラ類、カシ類、カキ、クワ、ハリエンジュ (ニセアカシア)", "備考": "成虫はエノキ、ケヤキ、サクラ類などの太めの枯れ枝に集まる。", "成虫出現時期": "6~8月"},
    {"和名": "オガサワラタマムシ", "学名": "Chrysochroa holstii Waterhouse, 1890", "族名": "ルリタマムシ族", "食草": "ムニンエノキ、ヤシマシャリンバイ", "備考": "成虫はムニンエノキに集まる。", "成虫出現時期": "6~8月"},
    {"和名": "アオムネスジタマムシ", "学名": "Chrysodema dalmanni (Eschscholtz, 1837)", "族名": "ルリタマムシ族", "食草": "モモタマナ", "備考": "成虫はマテバシイ、ウバメガシ、スダジイ、ホルトノキ、カシ類などに集まる。", "成虫出現時期": "5~8月"},
    {"和名": "アヤムネスジタマムシ", "学名": "Chrysodema lewisii E. Saunders, 1873", "族名": "ルリタマムシ族", "食草": "スダジイ、マテバシイ、ウバメガシ、カシ類、タブノキ、モモタマナ", "備考": "タブノキやモモタマナなどを食害する。", "成虫出現時期": "4~8月"},
    {"和名": "ツマベニタマムシ (原名亜種)", "学名": "Tamamushia virida virida Miwa et Chûjô, 1935", "族名": "ルリタマムシ族", "食草": "シマシャリンバイ、アデク、ヤシマシャリンバイ", "備考": "成虫はアデクやシマシャリンバイに集まる。", "成虫出現時期": "5~7月"},
    {"和名": "ツマベニタマムシ (聟島亜種)", "学名": "Tamamushia virida fujitai Ohmomo and Karube, 2004", "族名": "ルリタマムシ族", "食草": "シマシャリンバイ、アデク、ヤシマシャリンバイ", "備考": "成虫はアデクやシマシャリンバイに集まる。", "成虫出現時期": "5~7月"},
    {"和名": "ウバタマムシ (原名亜種)", "学名": "Chalcophora japonica japonica (Gory, 1840)", "族名": "ルリタマムシ族", "食草": "アカマツ、クロマツ、リュウキュウマツ", "備考": "マツ類を食害する。", "成虫出現時期": "4月頃 (2~3月の暖かい日に発見されることもある)"},
    {"和名": "ウバタマムシ (宝島亜種)", "学名": "Chalcophora japonica takarajimana Y. Kurosawa, 1974", "族名": "ルリタマムシ族", "食草": "アカマツ、クロマツ、リュウキュウマツ", "備考": "マツ類を食害する。", "成虫出現時期": "4月頃 (2~3月の暖かい日に発見されることもある)"},
    {"和名": "ウバタマムシ (奄美・沖縄亜種)", "学名": "Chalcophora japonica oshimana Schönfeldt, 1890", "族名": "ルリタマムシ族", "食草": "アカマツ、クロマツ、リュウキュウマツ", "備考": "マツ類を食害する。", "成虫出現時期": "4月頃 (2~3月の暖かい日に発見されることもある)"},
]

# CSVファイルを読み込み
input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/buprestidae_host.csv'

# Set maximum field size limit
csv.field_size_limit(sys.maxsize)

rows = []
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    header = reader.fieldnames
    
    # 提供されたデータを辞書形式に変換
    update_dict = {item["和名"]: item for item in complete_data}
    
    for row in reader:
        # 和名に基づいて更新
        if row.get('和名') in update_dict:
            updates = update_dict[row['和名']]
            # 学名から著者と年を抽出
            if "学名" in updates:
                row["学名"] = updates["学名"]
                # 学名から著者情報を抽出
                parts = updates["学名"].split(" ")
                if len(parts) > 2:
                    # 属名と種小名の後が著者
                    author_parts = " ".join(parts[2:])
                    # 年を分離
                    if "," in author_parts:
                        row["著者"] = author_parts.rsplit(",", 1)[0].strip()
                        row["公表年"] = author_parts.rsplit(",", 1)[1].strip()
                    elif author_parts.endswith(")"):
                        # 括弧付きの場合
                        if "(" in author_parts:
                            row["著者"] = author_parts.rsplit(" ", 1)[0].strip()
                            row["公表年"] = author_parts.rsplit(" ", 1)[1].strip()
                    else:
                        # 年だけの場合
                        row["著者"] = author_parts.rsplit(" ", 1)[0].strip() if " " in author_parts else ""
                        row["公表年"] = author_parts.rsplit(" ", 1)[1].strip() if " " in author_parts else author_parts
            
            # その他のフィールドを更新
            for key in ["族名", "食草", "備考", "成虫出現時期"]:
                if key in updates and key in row:
                    row[key] = updates[key]
            
            # 出典を正しく設定
            row["出典"] = "日本産タマムシ大図鑑"
        
        rows.append(row)

# 更新したCSVを元のファイルに上書き
with open(input_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated {len(complete_data)} species records in buprestidae_host.csv")