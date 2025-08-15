#!/usr/bin/env python3
import csv
import re
import os

def split_complex_plant_lists():
    """複雑な植物リストを個別のレコードに分割"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 複雑な植物リスト分割開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # パターン: 「植物名 (科名)の部位; 植物名 (科名)の部位; ...」
            if '; ' in plant_name and ' (' in plant_name and ')の' in plant_name:
                print(f"\n修正対象: 行{row_num}")
                print(f"  元: '{plant_name[:100]}...'")
                
                # セミコロンで分割
                plant_entries = [entry.strip() for entry in plant_name.split(';')]
                
                split_count = 0
                for i, entry in enumerate(plant_entries):
                    if not entry:
                        continue
                    
                    # パターンマッチング: 「植物名 (科名)の部位」
                    match = re.match(r'^([^(]+)\s+\(([^)]+)\)の(.+)$', entry.strip())
                    if match:
                        species_name = match.group(1).strip()
                        family_name = match.group(2).strip()
                        plant_part = match.group(3).strip()
                        
                        # 新しいレコードを作成
                        new_row = row.copy()
                        new_row['plant_name'] = species_name
                        new_row['plant_family'] = family_name
                        new_row['plant_part'] = plant_part
                        
                        # record_idを調整（最初のエントリは元のIDを保持、以降は新規生成）
                        if i == 0:
                            # 最初のエントリは元のレコードを更新
                            pass
                        else:
                            # 新しいレコードIDを生成（既存の最大ID+1から開始）
                            # 実際には後で正規化するので、一時的なIDを使用
                            new_row['record_id'] = f"temp-{row_num}-{i+1}"
                        
                        new_data.append(new_row)
                        split_count += 1
                        
                        print(f"    分割{i+1}: '{species_name}' ({family_name}) の{plant_part}")
                    else:
                        # パターンにマッチしない場合は元のエントリを保持
                        print(f"    パターン外: '{entry}'")
                        if i == 0:
                            new_data.append(row)
                        else:
                            # 予期しないケースなので元のレコードに追加情報として記録
                            new_row = row.copy()
                            new_row['plant_name'] = entry
                            new_row['record_id'] = f"temp-{row_num}-{i+1}"
                            new_data.append(new_row)
                
                print(f"  分割結果: {split_count}個のレコードに分割")
            else:
                # 通常のレコードはそのまま保持
                new_data.append(row)
    
    print(f"\n分割結果:")
    print(f"  元のエントリ数: {row_num-1}件")
    print(f"  分割後のエントリ数: {len(new_data)}件")
    print(f"  増加したエントリ数: {len(new_data) - (row_num-1)}件")
    
    # record_idを正規化
    print("\nrecord_idを正規化中...")
    for i, row in enumerate(new_data):
        row['record_id'] = f"hostplant-{i+1:06d}"
    
    # 修正されたデータを保存
    with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_data)
    
    # normalized_dataフォルダにもコピー
    import shutil
    src = hostplants_file
    dst = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    if os.path.exists(os.path.dirname(dst)):
        shutil.copy2(src, dst)
    
    print("hostplants.csvを更新しました")
    
    # 検証
    print(f"\n=== 検証 ===")
    
    # 残存する複雑なパターンをチェック
    remaining_complex = []
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            plant_name = row['plant_name']
            if '; ' in plant_name and ' (' in plant_name and ')の' in plant_name:
                remaining_complex.append(plant_name[:50])
    
    if remaining_complex:
        print(f"残存する複雑なパターン ({len(remaining_complex)}件):")
        for pattern in remaining_complex[:3]:
            print(f"  '{pattern}...'")
    else:
        print("✅ 複雑な植物リストパターンが全て分割されました")
    
    # 分割された例の確認
    split_examples = []
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['plant_family'] and row['plant_part']:
                if '科' in row['plant_family'] and row['plant_name'] != '不明':
                    split_examples.append(f"{row['plant_name']} ({row['plant_family']}) の{row['plant_part']}")
    
    print(f"\n分割された例:")
    for example in split_examples[-10:]:  # 最後の10件を表示
        print(f"  {example}")
    
    print(f"\n🌿 複雑な植物リスト分割が完了しました！")

if __name__ == "__main__":
    split_complex_plant_lists()