#!/usr/bin/env python3
import csv
import os
import shutil

def fix_winter_moth_life_stage():
    """冬尺蛾データの生活段階を成虫から幼虫に修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 冬尺蛾データ生活段階修正 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # 1. 現在のデータを読み込み
    print("\n=== 現在の冬尺蛾データ確認 ===")
    
    winter_moth_records = []
    other_records = []
    adult_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['reference'] == '日本の冬尺蛾':
                winter_moth_records.append(row)
                if row['life_stage'] == '成虫':
                    adult_count += 1
            else:
                other_records.append(row)
    
    print(f"冬尺蛾関連レコード数: {len(winter_moth_records)}件")
    print(f"うち成虫記録: {adult_count}件")
    
    # 2. 成虫を幼虫に修正
    print("\n=== 生活段階修正 ===")
    
    fixed_count = 0
    for record in winter_moth_records:
        if record['life_stage'] == '成虫':
            record['life_stage'] = '幼虫'
            fixed_count += 1
            if fixed_count <= 5:  # 最初の5件のみ表示
                print(f"修正: {record['record_id']} - {record['insect_id']} ({record['plant_name']})")
    
    print(f"修正されたレコード数: {fixed_count}件")
    
    # 3. ファイルを更新
    print("\n=== ファイル更新 ===")
    
    all_records = other_records + winter_moth_records
    
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
    
    # 4. 修正結果の検証
    print(f"\n=== 修正結果検証 ===")
    
    verification_records = []
    adult_remaining = 0
    larva_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['reference'] == '日本の冬尺蛾':
                verification_records.append(row)
                if row['life_stage'] == '成虫':
                    adult_remaining += 1
                elif row['life_stage'] == '幼虫':
                    larva_count += 1
    
    print(f"修正後の冬尺蛾レコード数: {len(verification_records)}件")
    print(f"  幼虫記録: {larva_count}件")
    print(f"  成虫記録: {adult_remaining}件")
    
    if adult_remaining > 0:
        print(f"⚠️  まだ成虫記録が{adult_remaining}件残っています")
    else:
        print("✅ すべての冬尺蛾食草記録が幼虫記録に修正されました")
    
    # サンプル表示
    print(f"\n修正後サンプル（最初の3件）:")
    for i, record in enumerate(verification_records[:3]):
        print(f"  {record['record_id']}: {record['plant_name']} - {record['life_stage']}")
    
    print(f"\n✅ 冬尺蛾データの生活段階修正が完了しました！")

if __name__ == "__main__":
    fix_winter_moth_life_stage()