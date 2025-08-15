#!/usr/bin/env python3
import csv
import os

def fix_remaining_punct():
    """残っている句読点問題を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 残りの句読点問題修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # 「幼虫の記録がある。農作物の大害虫である」のような複雑な説明文を削除
            if ('の記録がある。' in plant_name and 
                ('害虫' in plant_name or '大害虫' in plant_name)):
                print(f"削除: 行{row_num} {row['insect_id']}")
                print(f"  説明文的な食草名 '{plant_name}' を削除")
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
        
        # 最終確認
        print(f"\\n=== 最終確認 ===")
        
        # 残存する句読点をチェック
        remaining_punct = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if any(punct in row['plant_name'] for punct in ['.', '。', '、', ';', ':', '!', '？']):
                    if len(row['plant_name']) <= 50:  # 表示用
                        remaining_punct.append(row['plant_name'])
        
        if remaining_punct:
            print(f"残存する句読点を含む食草名 ({len(remaining_punct)}件):")
            for entry in list(set(remaining_punct))[:3]:
                print(f"  '{entry}'")
        else:
            print("✅ 全ての不要な句読点の除去が完了しました")
            
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_remaining_punct()