#!/usr/bin/env python3
import csv
import re
import os

def fix_final_problematic_entries():
    """最後の問題エントリを修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 最終問題エントリ修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # パターン1: 「神保 (1962) は母娘より採卵し...」のような文献情報
            if '神保 (1962)' in plant_name and '母娘より採卵し' in plant_name:
                print(f"削除: 行{row_num} {row['insect_id']}")
                print(f"  文献情報 '{plant_name[:50]}...' を削除")
                fix_count += 1
                continue  # この行は追加しない
            
            # パターン2: その他の文献・研究情報が食草名になっているケース
            elif any(pattern in plant_name for pattern in [
                'は母娘より', 'より採卵し', '研究により', '調査により', '報告により'
            ]):
                print(f"削除: 行{row_num} {row['insect_id']}")
                print(f"  研究情報 '{plant_name[:50]}...' を削除")
                fix_count += 1
                continue  # この行は追加しない
            
            # パターン3: 長すぎる説明文
            elif len(plant_name) > 80:
                print(f"削除: 行{row_num} {row['insect_id']}")
                print(f"  長すぎる説明文 '{plant_name[:50]}...' を削除")
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
        
        # 最終検証
        print(f"\\n=== 最終検証 ===")
        
        # 長い食草名や問題のあるパターンをチェック
        problematic_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_name = row['plant_name']
                if (len(plant_name) > 60 or
                    any(pattern in plant_name for pattern in [
                        '神保', '採卵', '研究', '調査', '報告', '文献'
                    ])):
                    problematic_entries.append(plant_name[:60])
        
        if problematic_entries:
            print(f"残存する問題エントリ ({len(problematic_entries)}件):")
            for entry in list(set(problematic_entries))[:3]:
                print(f"  '{entry}...'")
        else:
            print("✅ 全ての問題エントリの修正が完了しました")
        
        # 総エントリ数の確認
        total_entries = len(new_data)
        print(f"\\n最終総エントリ数: {total_entries}件")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_final_problematic_entries()