#!/usr/bin/env python3
import csv
import os

def fix_remaining_geographic_patterns():
    """残っている地理的記述パターンを修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 残りの地理的記述パターン修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            notes = row.get('notes', '')
            
            # パターン1: 空の「ヨーロッパでは」エントリを削除
            if plant_name == 'ヨーロッパでは' and not row['plant_family']:
                print(f"削除: 行{row_num} {row['insect_id']}")
                print(f"  空の地理的記述エントリ '{plant_name}' を削除")
                fix_count += 1
                continue  # この行は追加しない
            
            # パターン2: 備考欄の「戦前から記録がある。ヨーロッパでは」を修正
            elif '戦前から記録がある。ヨーロッパでは' in notes:
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  備考の地理的記述を修正")
                
                row['notes'] = '戦前から記録がある'
                new_data.append(row)
                fix_count += 1
            
            # パターン3: 備考欄の「毛織物。ヨーロッパではハトの巣やモグラの巣からも見つかっている」
            elif '毛織物。ヨーロッパではハトの巣やモグラの巣からも見つかっている' in notes:
                print(f"修正: 行{row_num} {row['insect_id']}")
                print(f"  備考の地理的記述を分離")
                
                # 国内の記録
                row['notes'] = '毛織物'
                new_data.append(row)
                
                # ヨーロッパの記録を追加
                europe_row = row.copy()
                europe_row['plant_name'] = 'ハトの巣'
                europe_row['observation_type'] = '国外'
                europe_row['record_id'] = f"{row['record_id']}-2"
                europe_row['notes'] = 'ヨーロッパ'
                new_data.append(europe_row)
                
                # モグラの巣の記録を追加
                mole_row = row.copy()
                mole_row['plant_name'] = 'モグラの巣'
                mole_row['observation_type'] = '国外'
                mole_row['record_id'] = f"{row['record_id']}-3"
                mole_row['notes'] = 'ヨーロッパ'
                new_data.append(mole_row)
                
                fix_count += 1
            
            else:
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
        
        # 残存する地理的記述パターンをチェック
        remaining_geo = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if ('ヨーロッパでは' in row['plant_name'] or 
                    'ヨーロッパでは' in row.get('notes', '') or
                    any(geo in row['plant_name'] for geo in ['台湾では', '中国では', '北アメリカでは'])):
                    remaining_geo.append(row['plant_name'])
        
        if remaining_geo:
            print(f"残存する地理的記述パターン:")
            for pattern in list(set(remaining_geo))[:3]:
                print(f"  '{pattern}'")
        else:
            print("✅ 全ての地理的記述パターンの修正が完了しました")
        
        # 国外記録の総数確認
        foreign_count = 0
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['observation_type'] == '国外':
                    foreign_count += 1
        
        print(f"\\n国外記録の総数: {foreign_count}件")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_remaining_geographic_patterns()