#!/usr/bin/env python3
import csv
import re
import os

def fix_plant_name_with_parts():
    """「植物名の部位」パターンを適切に分離"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 植物名の部位パターン分離修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    # 部位に関する語彙を定義
    plant_parts = ['花', '葉', '実', '種子', '果実', '根', '茎', '枝', '皮', '樹皮', '蕾', '新芽', '若葉', '花蕾', '花穂', '雄花']
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # 「植物名の部位」パターンをチェック
            for part in plant_parts:
                pattern = f'(.+)の{re.escape(part)}$'
                match = re.match(pattern, plant_name)
                
                if match:
                    base_plant_name = match.group(1).strip()
                    
                    # 複雑なケースをスキップ（後で個別対応）
                    if any(skip_word in base_plant_name for skip_word in [
                        '枯れ木', '朽ち木', 'コーラの原料となるヒメコラノキ', 
                        'ときには', '何らかの原因で', 'アキニレの花と若い', 
                        'クリの葉および', '多くのツツジ科植物'
                    ]):
                        new_data.append(row)
                        continue
                    
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: {plant_name}")
                    print(f"  新: 食草名='{base_plant_name}', 部位='{part}'")
                    
                    new_row = row.copy()
                    new_row['plant_name'] = base_plant_name
                    new_row['plant_part'] = part
                    new_data.append(new_row)
                    fix_count += 1
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
        kuwa_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == 'クワ類':
                    kuwa_entries.append(f"部位: {row['plant_part']}")
        
        if kuwa_entries:
            print("クワ類の修正例:")
            for entry in kuwa_entries:
                print(f"  {entry}")
        
        # 修正された他の例
        print("\nその他の修正例:")
        examples = ['ヤマハギ', 'ヌルデ', 'タラノキ', 'サンゴジュ', 'ツバキ']
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] in examples and row['plant_part'] in plant_parts:
                    print(f"  {row['plant_name']} - 部位: {row['plant_part']}")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_plant_name_with_parts()