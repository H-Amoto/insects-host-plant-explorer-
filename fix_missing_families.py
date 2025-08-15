#!/usr/bin/env python3
import csv
import os

def fix_missing_families():
    """科名が空白の植物を適切な科名に修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 科名補完処理 ===")
    
    # 植物名から科名へのマッピング（主要なもの）
    plant_to_family = {
        # バラ科
        'ウラジロノキ': 'バラ科',
        'クロツバラ': 'バラ科',
        
        # カバノキ科
        'ケヤマハンノキ': 'カバノキ科',
        'ハンノキ': 'カバノキ科',
        'アカシデ': 'カバノキ科',
        'イヌシデ': 'カバノキ科',
        'シラカンパ': 'カバノキ科',
        'ヤマハンノキ': 'カバノキ科',
        'ツノハシパミ': 'カバノキ科',
        
        # ムクロジ科（旧カエデ科）
        'ウリカエデ': 'ムクロジ科',
        'ウリハダカエデ': 'ムクロジ科',
        'ミネカエデ': 'ムクロジ科',
        'イタヤカエデ': 'ムクロジ科',
        
        # イラクサ科
        'コアカソ': 'イラクサ科',
        
        # ヤナギ科
        'ネコヤナギ': 'ヤナギ科',
        'バッコヤナギ': 'ヤナギ科',
        'シバヤナギ': 'ヤナギ科',
        
        # ツツジ科
        'ヤマツツジ': 'ツツジ科',
        'レンゲツツジ': 'ツツジ科',
        'ミツバツツジ': 'ツツジ科',
        'シャクナゲ': 'ツツジ科',
        'アセビ': 'ツツジ科',
        'ブルーベリー': 'ツツジ科',
        
        # ブナ科
        'ナラガシワ': 'ブナ科',
        'アラカシ': 'ブナ科',
        'カシワ': 'ブナ科',
        'ミズナラ': 'ブナ科',
        'クリ': 'ブナ科',
        'シイ': 'ブナ科',
        'コナラ': 'ブナ科',
        'ウバメガシ': 'ブナ科',
        'クヌギ': 'ブナ科',
        'シラカシ': 'ブナ科',
        
        # キク科
        'ヨモギ': 'キク科',
        'フキ': 'キク科',
        'タンポポ': 'キク科',
        'ノコンギク': 'キク科',
        'イナカギク': 'キク科',
        
        # イネ科
        'ススキ': 'イネ科',
        'チガヤ': 'イネ科',
        'アシ': 'イネ科',
        'ヨシ': 'イネ科',
        'ムギ': 'イネ科',
        'イネ': 'イネ科',
        
        # クワ科
        'クワ': 'クワ科',
        'イチジク': 'クワ科',
        
        # ニレ科
        'ハルニレ': 'ニレ科',
        'ケヤキ': 'ニレ科',
        'エノキ': 'ニレ科',
        
        # タデ科
        'イタドリ': 'タデ科',
        'ミゾソバ': 'タデ科',
        'オオイヌタデ': 'タデ科',
        
        # マメ科
        'ハギ': 'マメ科',
        'クズ': 'マメ科',
        'フジ': 'マメ科',
        'ヤマハギ': 'マメ科',
        'エンドウ': 'マメ科',
        'ダイズ': 'マメ科',
        
        # アブラナ科
        'ダイコン': 'アブラナ科',
        'キャベツ': 'アブラナ科',
        'ナズナ': 'アブラナ科',
        
        # ナス科
        'トマト': 'ナス科',
        'ジャガイモ': 'ナス科',
        'ナス': 'ナス科',
        'タバコ': 'ナス科',
        
        # その他の重要な科
        'サクラ': 'バラ科',
        'ウメ': 'バラ科',
        'モモ': 'バラ科',
        'リンゴ': 'バラ科',
        'ナシ': 'バラ科',
        
        'スギ': 'ヒノキ科',
        'ヒノキ': 'ヒノキ科',
        
        'ブドウ': 'ブドウ科',
        'ヤマブドウ': 'ブドウ科',
        
        'ツバキ': 'ツバキ科',
        'サザンカ': 'ツバキ科',
        'チャ': 'ツバキ科',
        
        'カキ': 'カキノキ科',
        
        'クルミ': 'クルミ科',
        'オニグルミ': 'クルミ科',
        
        'モチノキ': 'モチノキ科',
        'ソヨゴ': 'モチノキ科',
        
        'クスノキ': 'クスノキ科',
        'タブノキ': 'クスノキ科',
        'シロダモ': 'クスノキ科',
        
        'トチノキ': 'ムクロジ科',
        
        'ニシキギ': 'ニシキギ科',
        'マユミ': 'ニシキギ科',
        'ツリバナ': 'ニシキギ科',
        
        'ミズキ': 'ミズキ科',
        'ヤマボウシ': 'ミズキ科',
        
        'スイカズラ': 'スイカズラ科',
        'タニウツギ': 'スイカズラ科',
        
        'アジサイ': 'アジサイ科',
        'ウツギ': 'アジサイ科',
        
        'ゴマ': 'ゴマ科',
        'クコ': 'ナス科',
        
        'アケビ': 'アケビ科',
        'ミツバアケビ': 'アケビ科',
        
        'アサ': 'アサ科',
        'カラムシ': 'イラクサ科',
        
        'メギ': 'メギ科',
        'ナンテン': 'メギ科',
        
        'ケシ': 'ケシ科',
        'ヤマブキソウ': 'ケシ科',
        
        'キンポウゲ': 'キンポウゲ科',
        'オキナグサ': 'キンポウゲ科',
        
        'ツヅラフジ': 'ツヅラフジ科',
        'アオツヅラフジ': 'ツヅラフジ科',
        
        'アオイ': 'アオイ科',
        'オクラ': 'アオイ科',
        'ムクゲ': 'アオイ科',
        
        'シソ': 'シソ科',
        'エゴマ': 'シソ科',
        'ミント': 'シソ科',
        
        'トウダイグサ': 'トウダイグサ科',
        'エノキグサ': 'トウダイグサ科',
        
        'ユリ': 'ユリ科',
        'ギボウシ': 'ユリ科',
        
        'サクラソウ': 'サクラソウ科',
        'オカトラノオ': 'サクラソウ科',
        
        'アカネ': 'アカネ科',
        'ヤエムグラ': 'アカネ科',
        
        'オオバコ': 'オオバコ科',
        'ヘラオオバコ': 'オオバコ科',
        
        'スミレ': 'スミレ科',
        'タチツボスミレ': 'スミレ科',
        
        'ウリ': 'ウリ科',
        'キュウリ': 'ウリ科',
        'メロン': 'ウリ科',
        'カボチャ': 'ウリ科',
        
        'セリ': 'セリ科',
        'ニンジン': 'セリ科',
        'ウド': 'ウコギ科',
        
        'ムラサキ': 'ムラサキ科',
        'ワスレナグサ': 'ムラサキ科',
        
        'キョウチクトウ': 'キョウチクトウ科',
        'テイカカズラ': 'キョウチクトウ科',
        
        'モクセイ': 'モクセイ科',
        'キンモクセイ': 'モクセイ科',
        'トネリコ': 'モクセイ科',
        
        'エゴノキ': 'エゴノキ科',
        'ハクウンボク': 'エゴノキ科',
    }
    
    print(f"植物-科名マッピング: {len(plant_to_family)}件")
    
    # 両方のファイルを修正
    files_to_fix = [
        os.path.join(base_dir, 'public', 'hostplants.csv'),
        os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    ]
    
    for hostplants_file in files_to_fix:
        if not os.path.exists(hostplants_file):
            print(f"ファイルが見つかりません: {hostplants_file}")
            continue
            
        print(f"\n=== {hostplants_file} の修正 ===")
        
        all_records = []
        fixed_count = 0
        fixes_by_family = {}
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_name = row['plant_name']
                plant_family = row['plant_family']
                
                # 科名が空白で、マッピングに存在する植物の場合に修正
                if not plant_family and plant_name in plant_to_family:
                    correct_family = plant_to_family[plant_name]
                    print(f"修正: {row['record_id']} - '{plant_name}' に科名 '{correct_family}' を追加")
                    row['plant_family'] = correct_family
                    fixed_count += 1
                    
                    if correct_family not in fixes_by_family:
                        fixes_by_family[correct_family] = 0
                    fixes_by_family[correct_family] += 1
                
                all_records.append(row)
        
        print(f"修正したレコード数: {fixed_count}件")
        if fixes_by_family:
            print("科別追加数:")
            for family, count in sorted(fixes_by_family.items(), key=lambda x: x[1], reverse=True):
                print(f"  {family}: {count}件")
        
        # ファイルを更新
        print(f"\n=== ファイル更新 ===")
        
        with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
            if all_records:
                writer = csv.DictWriter(file, fieldnames=all_records[0].keys())
                writer.writeheader()
                writer.writerows(all_records)
        
        print(f"{hostplants_file} を更新しました")
    
    # 検証 - 残存する空白科名をチェック
    print(f"\n=== 検証 ===")
    
    for hostplants_file in files_to_fix:
        if not os.path.exists(hostplants_file):
            continue
            
        print(f"\n{hostplants_file}:")
        
        empty_families = {}
        total_records = 0
        empty_count = 0
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                total_records += 1
                plant_name = row['plant_name']
                plant_family = row['plant_family']
                
                if not plant_family:
                    empty_count += 1
                    if plant_name not in empty_families:
                        empty_families[plant_name] = 0
                    empty_families[plant_name] += 1
        
        print(f"  総レコード数: {total_records}件")
        print(f"  科名空白レコード数: {empty_count}件")
        print(f"  科名空白植物種数: {len(empty_families)}種")
        
        if empty_families:
            print(f"  残存する科名空白植物（上位10種）:")
            for plant, count in sorted(empty_families.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"    {plant}: {count}件")
    
    print(f"\n✅ 科名補完処理が完了しました！")

if __name__ == "__main__":
    fix_missing_families()