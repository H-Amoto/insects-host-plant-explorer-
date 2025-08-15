#!/usr/bin/env python3
import csv
import re
import os

def fix_punctuation_in_plant_names():
    """食草名の不要な句読点を除去"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 食草名の句読点除去開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            original_plant_name = plant_name
            
            # 不要な句読点や記号をチェックして除去
            if any(punct in plant_name for punct in ['.', '。', '、', ';', ':', '!', '？']):
                
                # 特定の修正パターン
                fixes_made = []
                
                # パターン1: ". エゾトリカブト" → "エゾトリカブト"
                if plant_name.startswith('. '):
                    new_name = plant_name[2:]  # ". " を除去
                    fixes_made.append(f"先頭の '. ' を除去")
                
                # パターン2: 文章の断片が食草名になっている場合
                elif any(phrase in plant_name for phrase in [
                    'コルクの害虫。野外ではサルノコシカケ類のキノコも食する。また',
                    '腐朽木。また',
                    'これらの加工品。他にもフクロウの羽やハイタカのペリット',
                    '乾燥して茶色くかたくなったものを好む。他にも国外で',
                    'ときにはスギなど針葉樹の葉など。何らかの原因で樹木から離れ',
                    'アヤメ科などの葉を食べる。ザクロ'
                ]):
                    # これらは文章なので削除または備考に移動
                    print(f"削除: 行{row_num} {row['insect_id']}")
                    print(f"  文章的な食草名 '{plant_name[:30]}...' を削除")
                    fix_count += 1
                    continue  # この行は追加しない
                
                # パターン3: 末尾の句読点を除去
                elif plant_name.endswith(('。', '.', '、', ';', ':', '!', '？')):
                    new_name = plant_name.rstrip('.。、;:!？')
                    fixes_made.append(f"末尾の句読点を除去")
                
                # パターン4: 「コケ植物の一種の記録がある。」のような説明文
                elif any(phrase in plant_name for phrase in [
                    'の記録がある。', 'として有名。', 'で確認されている。',
                    'の害虫として', 'を主に食す。', 'で飼育できる。',
                    'からも幼虫が見つかっている。', 'を食す。', 'の害虫。',
                    'との区別はついていない。', 'の種名とした。'
                ]):
                    print(f"削除: 行{row_num} {row['insect_id']}")
                    print(f"  説明文的な食草名 '{plant_name[:30]}...' を削除")
                    fix_count += 1
                    continue  # この行は追加しない
                
                # パターン5: 単純な植物名で末尾に句読点がある場合
                elif len(plant_name) <= 20 and plant_name.endswith(('。', '、')):
                    new_name = plant_name.rstrip('。、')
                    if new_name and len(new_name) > 2:  # 有意義な名前が残る場合のみ
                        fixes_made.append(f"末尾の句読点を除去")
                    else:
                        # 句読点を除去すると意味がなくなる場合は削除
                        print(f"削除: 行{row_num} {row['insect_id']}")
                        print(f"  無意味な食草名 '{plant_name}' を削除")
                        fix_count += 1
                        continue
                
                # パターン6: 中間の不適切な句読点
                elif '。' in plant_name and len(plant_name.split('。')) == 2:
                    parts = plant_name.split('。')
                    if len(parts[1]) <= 5 and parts[1] in ['また', 'ツゲ科', '']:
                        new_name = parts[0]  # 前半部分のみ使用
                        fixes_made.append(f"中間の句読点と後半部分を除去")
                    else:
                        # 複雑な場合は削除
                        print(f"削除: 行{row_num} {row['insect_id']}")
                        print(f"  複雑な食草名 '{plant_name[:30]}...' を削除")
                        fix_count += 1
                        continue
                
                else:
                    # その他の場合はそのまま
                    new_data.append(row)
                    continue
                
                # 修正を適用
                if fixes_made:
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: '{original_plant_name}'")
                    print(f"  新: '{new_name}'")
                    print(f"  修正: {', '.join(fixes_made)}")
                    
                    row['plant_name'] = new_name
                    fix_count += 1
            
            new_data.append(row)
    
    print(f"\\n修正結果:")
    print(f"  修正・削除したエントリ: {fix_count}件")
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
        
        # エゾトリカブトの修正確認
        ezotorikabuto_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'エゾトリカブト' in row['plant_name']:
                    ezotorikabuto_entries.append(row['plant_name'])
        
        if ezotorikabuto_entries:
            print("エゾトリカブトの修正例:")
            for entry in ezotorikabuto_entries:
                print(f"  '{entry}'")
        
        # 残存する句読点をチェック
        remaining_punct = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if any(punct in row['plant_name'] for punct in ['.', '。', '、', ';', ':', '!', '？']):
                    if len(row['plant_name']) <= 30:  # 短いもののみ表示
                        remaining_punct.append(row['plant_name'])
        
        if remaining_punct:
            print(f"\\n残存する句読点を含む食草名 ({len(remaining_punct)}件):")
            for entry in list(set(remaining_punct))[:5]:
                print(f"  '{entry}'")
        else:
            print("\\n✅ 不要な句読点の除去が完了しました")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_punctuation_in_plant_names()