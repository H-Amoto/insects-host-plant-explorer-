#!/usr/bin/env python3
import csv
import re
import os

def fix_explanation_plant_names():
    """説明文が食草名になっているケースを修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 説明文が食草名になっているケース修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # パターン1: 「実際には野外での寄主植物は判明していない」
            if plant_name == '実際には野外での寄主植物は判明していない':
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: '不明', 備考: '実際には野外での寄主植物は判明していない'")
                
                row['plant_name'] = '不明'
                row['notes'] = '実際には野外での寄主植物は判明していない'
                fix_count += 1
            
            # パターン2: 「その後確認されていない」
            elif plant_name == 'その後確認されていない':
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: '不明', 備考: 'その後確認されていない'")
                
                row['plant_name'] = '不明'
                row['notes'] = 'その後確認されていない'
                fix_count += 1
            
            # パターン3: 推定・推測表現（科名が含まれている場合）
            elif any(pattern in plant_name for pattern in ['と推定される', 'と思われる']):
                if any(family in plant_name for family in ['科', '属']):
                    # 科名/属名を抽出
                    if 'マツ科と推定される' in plant_name:
                        print(f"修正: 行{row_num} {row['insect_id']}")
                        print(f"  元: '{plant_name}'")
                        print(f"  新: 'マツ科', 備考: '推定'")
                        
                        row['plant_name'] = 'マツ科'
                        row['notes'] = '推定'
                        fix_count += 1
                    elif 'ツヅラフジ科と思われる' in plant_name:
                        print(f"修正: 行{row_num} {row['insect_id']}")
                        print(f"  元: '{plant_name}'")
                        print(f"  新: 'ツヅラフジ科', 備考: '推定'")
                        
                        row['plant_name'] = 'ツヅラフジ科'
                        row['notes'] = '推定'
                        fix_count += 1
                    elif 'ツヅラフジ科を食していると思われる' in plant_name:
                        print(f"修正: 行{row_num} {row['insect_id']}")
                        print(f"  元: '{plant_name}'")
                        print(f"  新: 'ツヅラフジ科', 備考: '推定'")
                        
                        row['plant_name'] = 'ツヅラフジ科'
                        row['notes'] = '推定'
                        fix_count += 1
                    elif 'ヤナギ属につくものと思われる' in plant_name:
                        print(f"修正: 行{row_num} {row['insect_id']}")
                        print(f"  元: '{plant_name}'")
                        print(f"  新: 'ヤナギ属', 備考: '推定'")
                        
                        row['plant_name'] = 'ヤナギ属'
                        row['notes'] = '推定'
                        fix_count += 1
                    else:
                        new_data.append(row)
                        continue
                else:
                    # 一般的な推定表現（植物名が特定できない場合）
                    if any(keyword in plant_name for keyword in [
                        '前種と大差ない', '草地の草本類', '広葉樹を食す', 'だと思われる'
                    ]):
                        print(f"修正: 行{row_num} {row['insect_id']}")
                        print(f"  元: '{plant_name}'")
                        print(f"  新: '不明', 備考: '{plant_name}'")
                        
                        row['plant_name'] = '不明'
                        row['notes'] = plant_name
                        fix_count += 1
                    else:
                        new_data.append(row)
                        continue
            
            # パターン4: 単純な推定表現
            elif plant_name == 'と思われる':
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: '不明', 備考: '推定'")
                
                row['plant_name'] = '不明'
                row['notes'] = '推定'
                fix_count += 1
            
            # パターン5: 複雑な飼育記述
            elif '飼育されており野外でも利用していると思われる' in plant_name:
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: '不明', 備考: '飼育されており野外でも利用していると推定'")
                
                row['plant_name'] = '不明'
                row['notes'] = '飼育されており野外でも利用していると推定'
                fix_count += 1
            
            new_data.append(row)
    
    print(f"\\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  総エントリ数: {len(new_data)}件")
    
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
        
        # 「不明」に修正されたエントリの確認
        unknown_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (row['plant_name'] == '不明' and 
                    any(keyword in row.get('notes', '') for keyword in [
                        '判明していない', '確認されていない', '推定', '思われる'
                    ])):
                    unknown_entries.append(f"{row['insect_id']}: {row['notes'][:30]}...")
        
        if unknown_entries:
            print(f"「不明」に修正されたエントリ ({len(unknown_entries)}件):")
            for entry in unknown_entries[:5]:
                print(f"  {entry}")
        
        # 科名・属名に修正されたエントリの確認
        family_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (('科' in row['plant_name'] or '属' in row['plant_name']) and 
                    row.get('notes') == '推定'):
                    family_entries.append(f"{row['insect_id']}: {row['plant_name']}")
        
        if family_entries:
            print(f"\\n科名・属名に修正されたエントリ:")
            for entry in family_entries:
                print(f"  {entry}")
        
        # 残存する問題パターンをチェック
        remaining_issues = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if any(pattern in row['plant_name'] for pattern in [
                    '判明していない', '確認されていない', 'と思われる', 'と推定される'
                ]):
                    remaining_issues.append(row['plant_name'][:50])
        
        if remaining_issues:
            print(f"\\n残存する問題パターン:")
            for entry in list(set(remaining_issues))[:3]:
                print(f"  '{entry}...'")
        else:
            print("\\n✅ 説明文が食草名になっているケースの修正が完了しました")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_explanation_plant_names()