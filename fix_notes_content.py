#!/usr/bin/env python3
import csv
import re
import os

def fix_notes_content():
    """備考欄の内容を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 備考欄内容の修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            # species-5522の備考を完全な文章に修正
            if row['insect_id'] == 'species-5522' and row['notes'] == 'インドでは':
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: 備考='{row['notes']}'")
                print(f"  新: 備考='インドではマメ科ネムノキ類が知られる'")
                
                row['notes'] = 'インドではマメ科ネムノキ類が知られる'
                fix_count += 1
            
            new_data.append(row)
    
    print(f"\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    
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
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['insect_id'] == 'species-5522':
                    print(f"修正確認: {row['insect_id']}")
                    print(f"  食草名: {row['plant_name']}")
                    print(f"  科名: {row['plant_family']}")
                    print(f"  観察タイプ: {row['observation_type']}")
                    print(f"  参考文献: {row['reference']}")
                    print(f"  備考: {row['notes']}")
                    break
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_notes_content()