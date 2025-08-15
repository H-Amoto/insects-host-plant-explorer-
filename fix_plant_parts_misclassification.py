#!/usr/bin/env python3
import csv
import re
import os

def fix_plant_parts_misclassification():
    """植物部位名の誤分類を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 植物部位名の誤分類修正開始 ===")
    
    # 植物部位名のリスト
    plant_parts = {
        '根茎', '茎', '葉', '花', '実', '種子', '樹皮', '根', '枝', '果実',
        '芽', '蕾', '花序', '幹', '樹液', '材', '心材', '辺材', '球根',
        '鱗茎', '塊茎', '地下茎', '匍匐茎', '花弁', '雄花', '雌花'
    }
    
    # 短い文字列でも正常な植物名
    valid_short_names = {
        'ブナ', 'キリ', 'ズミ', 'クリ', 'カシ', 'ケヤキ', 'モミ', 'ツガ',
        'スギ', 'ヒノキ', 'マツ', 'イチイ', 'カエデ', 'サクラ', 'ウメ',
        'モモ', 'ナシ', 'リンゴ', 'カキ', 'ナラ', 'シイ', 'カシワ',
        'ヤナギ', 'ポプラ', 'シラカバ', 'ハンノキ', 'クルミ', 'ホオ',
        'コナラ', 'ミズナラ', 'アカシア', 'ハギ', 'クズ', 'フジ'
    }
    
    # 明らかに植物名でない文字列
    invalid_names = {
        '国外', '野外', '飼育', '人工', '栽培', '温室', '自然', '山地',
        '平地', '海岸', '湿地', '乾燥', '林内', '林縁', '草原', '農地'
    }
    
    # hostplants.csvを読み込み
    hostplants_file = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    fixed_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            original_name = plant_name
            
            # 植物部位名 → 削除（この行を削除）
            if plant_name in plant_parts:
                print(f"削除 (植物部位): 行{row_num} {row['insect_id']} → '{plant_name}'")
                fix_count += 1
                continue  # この行をスキップ
            
            # 明らかに植物名でない → 削除
            elif plant_name in invalid_names:
                print(f"削除 (非植物名): 行{row_num} {row['insect_id']} → '{plant_name}'")
                fix_count += 1
                continue  # この行をスキップ
            
            # 短すぎるが有効でない文字列 → 不明に変更
            elif len(plant_name) <= 2 and plant_name not in valid_short_names and plant_name != '不明':
                row['plant_name'] = '不明'
                print(f"修正 (短すぎる): {original_name} → 不明")
                fix_count += 1
            
            fixed_data.append(row)
    
    # 修正されたデータを保存
    if fix_count > 0:
        with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
            if fixed_data:
                writer = csv.DictWriter(file, fieldnames=fixed_data[0].keys())
                writer.writeheader()
                writer.writerows(fixed_data)
        
        # publicフォルダにもコピー
        import shutil
        src = hostplants_file
        dst = os.path.join(base_dir, 'public', 'hostplants.csv')
        shutil.copy2(src, dst)
        
        print(f"\n=== 修正完了 ===")
        print(f"修正・削除件数: {fix_count}件")
        print(f"残データ件数: {len(fixed_data)}件")
        print("hostplants.csvを更新しました")
    else:
        print("修正対象が見つかりませんでした")
    
    # 修正後の短い文字列を確認
    print(f"\n=== 修正後の短い文字列確認 ===")
    short_names = set()
    for row in fixed_data:
        if len(row['plant_name']) <= 3 and row['plant_name'] != '不明':
            short_names.add(row['plant_name'])
    
    print(f"3文字以下の植物名 ({len(short_names)}種):")
    for name in sorted(short_names):
        print(f"  {name}")

if __name__ == "__main__":
    fix_plant_parts_misclassification()