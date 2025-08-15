#!/usr/bin/env python3
import csv
import re
import os

def fix_wood_parts():
    """「植物名の部位」パターンを適切に分離（木材関連）"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 植物名の部位パターン分離修正開始（木材関連） ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    # 木材関連の部位パターンを定義
    wood_parts = ['樹皮', '根', '茎', '枝', '幹', '材']
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # 「植物名の部位」パターンをチェック
            for part in wood_parts:
                pattern = f'(.+)の{re.escape(part)}(.*)$'
                match = re.match(pattern, plant_name)
                
                if match:
                    base_plant_name = match.group(1).strip()
                    suffix = match.group(2).strip()
                    
                    # 複雑なケースや説明文をスキップ
                    if any(skip_word in base_plant_name for skip_word in [
                        '木材となる', 'コーラの原料となる', '若い枝', '果実'
                    ]):
                        new_data.append(row)
                        continue
                    
                    # 特殊なケースの処理
                    if '。古くなった竹の柵でも幼虫を採集' in suffix:
                        # 「枯れ木の樹皮。古くなった竹の柵でも幼虫を採集」の場合
                        print(f"修正: 行{row_num} {row['insect_id']}")
                        print(f"  元: {plant_name}")
                        print(f"  新: 食草名='{base_plant_name}', 部位='{part}', 備考='古くなった竹の柵でも幼虫を採集'")
                        
                        row['plant_name'] = base_plant_name
                        row['plant_part'] = part
                        row['notes'] = '古くなった竹の柵でも幼虫を採集'
                        fix_count += 1
                    else:
                        print(f"修正: 行{row_num} {row['insect_id']}")
                        print(f"  元: {plant_name}")
                        print(f"  新: 食草名='{base_plant_name}', 部位='{part}'")
                        
                        row['plant_name'] = base_plant_name + suffix
                        row['plant_part'] = part
                        fix_count += 1
                    
                    new_data.append(row)
                    break
            else:
                # パターンにマッチしない場合はそのまま
                new_data.append(row)
    
    print(f"\n修正結果:")
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
        print(f"\n=== 検証 ===")
        
        # 朽ち木の修正例
        kuchiki_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == '朽ち木' and row['plant_part'] == '樹皮':
                    kuchiki_entries.append(f"{row['insect_id']}: {row['plant_name']} - 部位: {row['plant_part']}")
        
        if kuchiki_entries:
            print("朽ち木の樹皮修正例:")
            for entry in kuchiki_entries:
                print(f"  {entry}")
        
        # 枯れ木の修正例
        kareki_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == '枯れ木' and row['plant_part'] == '樹皮':
                    kareki_entries.append(f"{row['insect_id']}: {row['plant_name']} - 部位: {row['plant_part']}")
        
        if kareki_entries:
            print("\n枯れ木の樹皮修正例:")
            for entry in kareki_entries[:3]:
                print(f"  {entry}")
        
        # 残存する「の樹皮」パターンをチェック
        remaining_bark = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'の樹皮' in row['plant_name']:
                    remaining_bark.append(row['plant_name'])
        
        if remaining_bark:
            print(f"\n残存する「の樹皮」パターン ({len(remaining_bark)}件):")
            for entry in list(set(remaining_bark)):
                print(f"  '{entry}'")
        else:
            print("\n✅ 植物名の部位パターン分離が完了しました")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_wood_parts()