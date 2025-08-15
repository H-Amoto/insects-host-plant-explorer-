#!/usr/bin/env python3
import csv
import os
import shutil

def fix_remaining_family_pattern():
    """「(科名)」のみの植物名を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 残存科名パターン修正処理 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # データを読み込み・修正
    print("\n=== データ修正 ===")
    
    all_records = []
    fixed_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            plant_name = row['plant_name']
            
            # 「(科名)」のみのパターンをチェック
            if plant_name == '(アブラナ科)':
                # 植物名を「不明」に、科名を「アブラナ科」に設定
                row['plant_name'] = '不明'
                row['plant_family'] = 'アブラナ科'
                
                print(f"修正: {row['record_id']}")
                print(f"  元: '{plant_name}'")
                print(f"  植物名: '{row['plant_name']}'")
                print(f"  科名: '{row['plant_family']}'")
                print()
                fixed_count += 1
            
            all_records.append(row)
    
    print(f"修正したレコード数: {fixed_count}件")
    
    # ファイルを更新
    print("\n=== ファイル更新 ===")
    
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        if all_records:
            writer = csv.DictWriter(file, fieldnames=all_records[0].keys())
            writer.writeheader()
            writer.writerows(all_records)
    
    # normalized_dataフォルダにもコピー
    src = hostplants_file
    dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    print("hostplants.csvを更新しました")
    
    # 検証
    print(f"\n=== 検証 ===")
    
    remaining_issues = 0
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            plant_name = row['plant_name']
            
            # まだ問題のあるパターンが残っているかチェック
            if ('科)' in plant_name or '科）' in plant_name) and plant_name.startswith('('):
                remaining_issues += 1
                print(f"  残存問題: {row['record_id']} - '{plant_name}'")
    
    print(f"残存する問題パターン: {remaining_issues}件")
    
    # 修正結果の確認
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['record_id'] == 'hostplant-003519':
                print(f"\n修正結果確認:")
                print(f"  レコードID: {row['record_id']}")
                print(f"  植物名: '{row['plant_name']}'")
                print(f"  科名: '{row['plant_family']}'")
                break
    
    print(f"\n✅ 残存科名パターン修正処理が完了しました！")

if __name__ == "__main__":
    fix_remaining_family_pattern()