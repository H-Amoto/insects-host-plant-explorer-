#!/usr/bin/env python3
import csv
import os

def fix_reference_quotes():
    """referenceフィールドの引用符を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== referenceフィールドの引用符修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            reference = row.get('reference', '')
            
            # referenceフィールドに不正な引用符がある場合（例: "1954"""）
            if reference.endswith('""'):
                new_reference = reference.rstrip('"')  # 末尾の"を全て除去
                print(f"修正: 行{row_num} {row['insect_id']} (reference)")
                print(f"  元: reference='{reference}'")
                print(f"  新: reference='{new_reference}'")
                
                row['reference'] = new_reference
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
        print("✅ 全ての引用符問題の修正が完了しました")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_reference_quotes()