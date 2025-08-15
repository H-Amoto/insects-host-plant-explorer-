#!/usr/bin/env python3
import csv
import os

def fix_remaining_explanations():
    """残っている説明文パターンを修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 残りの説明文パターン修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # パターン1: 「と思われる」（単独）
            if plant_name == 'と思われる':
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: '不明', 備考: '推定'")
                
                row['plant_name'] = '不明'
                row['notes'] = '推定'
                fix_count += 1
            
            # パターン2: 「飼育されており野外でも利用していると思われる」
            elif plant_name == '飼育されており野外でも利用していると思われる':
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
        
        # 最終検証
        print(f"\\n=== 最終検証 ===")
        
        # 残存する問題パターンをチェック
        remaining_issues = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if any(pattern in row['plant_name'] for pattern in [
                    '判明していない', '確認されていない', 'と思われる', 'と推定される',
                    '飼育されており', 'だと思われる'
                ]):
                    remaining_issues.append(row['plant_name'][:50])
        
        if remaining_issues:
            print(f"残存する問題パターン:")
            for entry in list(set(remaining_issues))[:3]:
                print(f"  '{entry}...'")
        else:
            print("✅ 全ての説明文パターンの修正が完了しました")
        
        # 「不明」エントリの総数確認
        unknown_count = 0
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == '不明':
                    unknown_count += 1
        
        print(f"\\n「不明」エントリの総数: {unknown_count}件")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_remaining_explanations()