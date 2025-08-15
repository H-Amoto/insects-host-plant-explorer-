#!/usr/bin/env python3
import csv
import os

def fix_remaining_comment_entries():
    """残っているコメント様エントリを修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 残りのコメント様エントリ修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # 「中国ではムクロジ科植物が知られている」を削除
            if plant_name == '中国ではムクロジ科植物が知られている':
                print(f"削除: 行{row_num} {row['insect_id']}")
                print(f"  '{plant_name}' はコメント的内容のため削除")
                fix_count += 1
                continue  # この行は追加しない
            
            new_data.append(row)
    
    print(f"\\n修正結果:")
    print(f"  削除したエントリ: {fix_count}件")
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
        
        # 残存する「植物」パターンをチェック
        remaining_patterns = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if ('科植物' in row['plant_name'] or '属植物' in row['plant_name'] or 
                    'が知られている' in row['plant_name'] or 'が記録されている' in row['plant_name']):
                    remaining_patterns.append(row['plant_name'])
        
        if remaining_patterns:
            print(f"残存するパターン:")
            for pattern in list(set(remaining_patterns))[:3]:
                print(f"  '{pattern}'")
        else:
            print("✅ コメント様エントリの修正が完了しました")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_remaining_comment_entries()