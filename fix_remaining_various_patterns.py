#!/usr/bin/env python3
import csv
import re
import os

def fix_remaining_various_patterns():
    """残存する「各種」「多くの」パターンを追加修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 残存パターンの追加修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    # 残存パターンの追加修正
    patterns = [
        # 「○○各種」→「○○」
        (r'^(.+)各種(.*)$', r'\1\2'),
        # 「各種○○」→「○○」
        (r'^各種(.+)$', r'\1'),
        # 「その他各種の○○」→「○○」
        (r'^その他各種の(.+)$', r'\1'),
        # 「ヤナギ科の各種」→「ヤナギ科」（残った場合）
        (r'^(.+科)の$', r'\1'),
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
        
        # 検証 - 最終的な「各種」「多くの」パターンをチェック
        print(f"\n=== 検証 ===")
        remaining_patterns = []
        check_pattern = r'(各種|多くの|様々な|色々な)'
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if re.search(check_pattern, row['plant_name']):
                    remaining_patterns.append(row['plant_name'])
        
        if remaining_patterns:
            print(f"最終残存パターン ({len(remaining_patterns)}件):")
            for entry in list(set(remaining_patterns))[:10]:
                print(f"  '{entry}'")
        else:
            print("✅ すべての簡潔化可能なパターンの修正が完了しました")
    else:
        print("追加修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_remaining_various_patterns()