#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys

# データ辞書を作成（和名をキーとする）
data_updates = {
    "キボシフナガタタマムシ": {
        "族名": "フナガタタマムシ族",
        "著者": "Nonfried",
        "公表年": "1895",
        "学名": "Acmaeodera (Cobosiella) luzonica Nonfried, 1895",
        "備考": "成虫はハマボウの花弁を後食する。アデクから羽化脱出した記録あり。",
        "成虫出現時期": "不明"
    },
    "モンキタマムシ": {
        "族名": "ツツタマムシ族",
        "著者": "Marseul",
        "公表年": "1867",
        "学名": "Prosima chinensis Marseul, 1867",
        "備考": "成虫はモモなどを後食する。本来の分布は中国大陸で、人為的に分布が拡大した外来種の可能性が推察される。",
        "成虫出現時期": "5~6月"
    },
    "ケシツブタマムシ": {
        "族名": "ケシツブタマムシ族",
        "著者": "Y. Kurosawa",
        "公表年": "1972",
        "学名": "Mastogenius insperatus Y. Kurosawa, 1972",
        "備考": "沖縄島ではマルバニッケイの枯れ枝から羽化。",
        "成虫出現時期": "4月上旬~6月上旬"
    },
    "ミスジツブタマムシ": {
        "族名": "ツブタマムシ族",
        "著者": "E. Saunders",
        "公表年": "1873",
        "学名": "Paratrachys hederae E. Saunders, 1873",
        "備考": "幼虫はクワ科イチジク属植物の潜葉虫として葉裏に潜り込み、内部組織を食害する。",
        "成虫出現時期": "3~6月"
    },
    "ダイトウツブタマムシ": {
        "族名": "ツブタマムシ族",
        "著者": "Y. Kurosawa",
        "公表年": "1985",
        "学名": "Paratrachys mixtipubescens Y. Kurosawa, 1985",
        "備考": "北大東島の固有種。オオイタビの葉より成虫を羽化脱出させた記録あり。",
        "成虫出現時期": "3~6月頃 (秋期に発生している可能性もあり)"
    },
    "オオシマツブタマムシ": {
        "族名": "ツブタマムシ族",
        "著者": "Y. Kurosawa",
        "公表年": "1976",
        "学名": "Paratrachys princeps Y. Kurosawa, 1976",
        "備考": "幼虫はイチジク属植物の潜葉虫。",
        "成虫出現時期": "3~6月"
    },
    "タマムシ": {
        "族名": "ルリタマムシ族",
        "著者": "(Schönherr)",
        "公表年": "1817",
        "学名": "Chrysochroa fulgidissima (Schönherr, 1817)",
        "食草": "エノキ、リュウキュウエノキ、ケヤキ、サクラ類、カシ類、カキ、クワ、ハリエンジュ (ニセアカシア)",
        "備考": "成虫はエノキ、ケヤキ、サクラ類などの太めの枯れ枝に集まる。",
        "成虫出現時期": "6~8月"
    },
    "オガサワラタマムシ": {
        "族名": "ルリタマムシ族",
        "著者": "Waterhouse",
        "公表年": "1890",
        "学名": "Chrysochroa holstii Waterhouse, 1890",
        "食草": "ムニンエノキ、ヤシマシャリンバイ",
        "備考": "成虫はムニンエノキに集まる。",
        "成虫出現時期": "6~8月"
    },
    "アオムネスジタマムシ": {
        "族名": "ルリタマムシ族",
        "著者": "(Eschscholtz)",
        "公表年": "1837",
        "学名": "Chrysodema dalmanni (Eschscholtz, 1837)",
        "備考": "成虫はマテバシイ、ウバメガシ、スダジイ、ホルトノキ、カシ類などに集まる。",
        "成虫出現時期": "5~8月"
    }
}

# CSVファイルを読み込み
input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/buprestidae_host.csv'
output_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/buprestidae_host_updated.csv'

# Set maximum field size limit
csv.field_size_limit(sys.maxsize)

rows = []
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    header = reader.fieldnames
    
    for row in reader:
        # 和名に基づいて更新
        if row.get('和名') in data_updates:
            updates = data_updates[row['和名']]
            for key, value in updates.items():
                if key in row:
                    row[key] = value
        
        rows.append(row)

# 更新したCSVを書き出し
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated {len(data_updates)} species records")
print(f"Output saved to: {output_file}")