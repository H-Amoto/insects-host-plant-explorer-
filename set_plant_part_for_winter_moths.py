#!/usr/bin/env python3
import csv
import os
import shutil

def set_plant_part_for_winter_moths():
    """日本の冬尺蛾と日本の冬夜蛾を出典とするレコードのplant_partを「葉」に設定"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 冬季蛾類植物部位設定処理 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    # データを読み込み・修正
    print("\n=== データ修正 ===")
    
    all_records = []
    winter_geometridae_count = 0
    winter_noctuidae_count = 0
    updated_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            reference = row['reference']
            original_plant_part = row['plant_part']
            
            # 日本の冬尺蛾または日本の冬夜蛾を出典とするレコードを処理
            if reference in ['日本の冬尺蛾', '日本の冬夜蛾']:
                if reference == '日本の冬尺蛾':
                    winter_geometridae_count += 1
                else:
                    winter_noctuidae_count += 1
                
                # plant_partが空または既に「葉」でない場合に「葉」を設定
                if not original_plant_part or original_plant_part.strip() == '':
                    row['plant_part'] = '葉'
                    updated_count += 1
                    
                    if updated_count <= 10:  # 最初の10件のみ表示
                        print(f"更新: {row['record_id']} ({reference}) - plant_part: '' → '葉'")
            
            all_records.append(row)
    
    print(f"\n処理結果:")
    print(f"日本の冬尺蛾レコード: {winter_geometridae_count}件")
    print(f"日本の冬夜蛾レコード: {winter_noctuidae_count}件")
    print(f"plant_part更新: {updated_count}件")
    
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
    
    verification_counts = {
        '日本の冬尺蛾': {'total': 0, 'with_leaf': 0, 'empty': 0},
        '日本の冬夜蛾': {'total': 0, 'with_leaf': 0, 'empty': 0}
    }
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            reference = row['reference']
            plant_part = row['plant_part']
            
            if reference in verification_counts:
                verification_counts[reference]['total'] += 1
                
                if plant_part == '葉':
                    verification_counts[reference]['with_leaf'] += 1
                elif not plant_part or plant_part.strip() == '':
                    verification_counts[reference]['empty'] += 1
    
    for ref, counts in verification_counts.items():
        print(f"{ref}:")
        print(f"  総レコード数: {counts['total']}件")
        print(f"  plant_part='葉': {counts['with_leaf']}件")
        print(f"  plant_part空: {counts['empty']}件")
    
    # サンプル表示
    print(f"\n更新済みサンプル:")
    sample_count = 0
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (row['reference'] in ['日本の冬尺蛾', '日本の冬夜蛾'] and 
                row['plant_part'] == '葉'):
                print(f"  {row['record_id']}: {row['plant_name']} - {row['plant_part']} ({row['reference']})")
                sample_count += 1
                if sample_count >= 5:
                    break
    
    print(f"\n✅ 冬季蛾類植物部位設定処理が完了しました！")

if __name__ == "__main__":
    set_plant_part_for_winter_moths()