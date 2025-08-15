#!/usr/bin/env python3
import csv
import os

def fix_final_comment_patterns():
    """最後の残っているコメント様パターンを修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 最終コメント様パターン修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # 「アカバナ科が記録されている。」→「アカバナ科」
            if plant_name == 'アカバナ科が記録されている。':
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: 'アカバナ科'、備考: '記録されている'")
                
                row['plant_name'] = 'アカバナ科'
                row['notes'] = '記録されている'
                fix_count += 1
            
            # 「バラ科が記録されているが」→「バラ科」
            elif plant_name == 'バラ科が記録されているが':
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  新: 'バラ科'、備考: '記録されている'")
                
                row['plant_name'] = 'バラ科'
                row['notes'] = '記録されている'
                fix_count += 1
            
            # 「植物で飼育が可能」→削除してキク科のnotesに統合
            elif plant_name == '植物で飼育が可能':
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  '{plant_name}' を前の行の備考に移動")
                
                # 前の行を探してnotesに追加
                if new_data:
                    last_entry = new_data[-1]
                    if last_entry['insect_id'] == row['insect_id']:
                        existing_notes = last_entry.get('notes', '')
                        if existing_notes:
                            last_entry['notes'] = f"{existing_notes}; 植物で飼育が可能"
                        else:
                            last_entry['notes'] = '植物で飼育が可能'
                        print(f"  前の行の備考を更新")
                        fix_count += 1
                        continue  # この行は追加しない
                
                # 前の行が見つからない場合はそのまま
                new_data.append(row)
                continue
            
            new_data.append(row)
    
    print(f"\\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
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
        
        # アカバナ科とバラ科の修正確認
        family_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if ((row['plant_name'] == 'アカバナ科' and row['notes'] == '記録されている') or
                    (row['plant_name'] == 'バラ科' and row['notes'] == '記録されている')):
                    family_entries.append(f"{row['plant_name']} - 備考: {row['notes']}")
        
        if family_entries:
            print("科名の修正例:")
            for entry in family_entries:
                print(f"  {entry}")
        
        # 残存するコメント様パターンをチェック
        remaining_patterns = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if ('が記録されている' in row['plant_name'] or 
                    'が知られている' in row['plant_name'] or
                    '科植物' in row['plant_name']):
                    remaining_patterns.append(row['plant_name'])
        
        if remaining_patterns:
            print(f"\\n残存するパターン:")
            for pattern in list(set(remaining_patterns))[:3]:
                print(f"  '{pattern}'")
        else:
            print("\\n✅ 全てのコメント様パターンの修正が完了しました")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_final_comment_patterns()