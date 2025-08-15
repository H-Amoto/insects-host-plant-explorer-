#!/usr/bin/env python3
import csv
import re
import os

def fix_various_patterns():
    """「各種の○○」「多くの○○」パターンを簡潔に修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 「各種の」「多くの」パターン簡潔化修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    # 修正パターンを定義
    patterns = [
        # 「各種の○○」→「○○」
        (r'^各種の(.+)$', r'\1'),
        # 「多くの○○」→「○○」
        (r'^多くの(.+)$', r'\1'),
        # 「様々な○○」→「○○」
        (r'^様々な(.+)$', r'\1'),
        # 「色々な○○」→「○○」
        (r'^色々な(.+)$', r'\1'),
        # 「○○各種」→「○○」
        (r'^(.+)各種$', r'\1'),
        # 「○○属各種」→「○○属」
        (r'^(.+属)各種(.*)$', r'\1\2'),
        # 「ヤナギ科の各種」→「ヤナギ科」
        (r'^(.+科)の各種$', r'\1'),
        # 「その他○○」→「○○」（キイチゴなどの具体名の場合）
        (r'^その他([ァ-ヶ一-龯]+)$', r'\1'),
    ]
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            original_name = plant_name
            
            # 各パターンをチェックして修正
            for pattern, replacement in patterns:
                new_name = re.sub(pattern, replacement, plant_name)
                if new_name != plant_name:
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: '{plant_name}'")
                    print(f"  新: '{new_name}'")
                    
                    row['plant_name'] = new_name
                    fix_count += 1
                    break
            
            new_data.append(row)
    
    print(f"\n修正結果:")
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
        print(f"\n=== 検証 ===")
        konara_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == 'コナラ属':
                    konara_entries.append(f"{row['insect_id']}: {row['plant_name']}")
        
        if konara_entries:
            print("コナラ属の修正例:")
            for entry in konara_entries:
                print(f"  {entry}")
        
        # 残存する「各種」「多くの」パターンをチェック
        remaining_patterns = []
        check_pattern = r'(各種|多くの|様々な|色々な)'
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if re.search(check_pattern, row['plant_name']):
                    remaining_patterns.append(row['plant_name'])
        
        if remaining_patterns:
            print(f"\n残存する「各種」「多くの」パターン ({len(remaining_patterns)}件):")
            for entry in list(set(remaining_patterns))[:10]:  # 重複除去して表示
                print(f"  '{entry}'")
        else:
            print("\n✅ 「各種の」「多くの」パターンの簡潔化が完了しました")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_various_patterns()