#!/usr/bin/env python3
import csv
import re
import os

def fix_plant_part_states():
    """「植物名の状態+部位」パターンを適切に分離"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 植物名の状態+部位パターン分離修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    # 状態+部位の語彙を定義
    state_parts = [
        '枯れ葉', '枯れ枝', '枯れ木', 
        '若い葉', '若い枝', '若い果実',
        '古い葉', '古い枝',
        '新芽', '新葉',
        '乾燥葉', '湿った葉'
    ]
    
    # 状態と部位のマッピング
    state_part_mapping = {
        '枯れ葉': ('枯れ葉', '葉'),
        '枯れ枝': ('枯れ枝', '枝'),
        '枯れ木': ('枯れ木', '木'),
        '若い葉': ('若葉', '葉'),
        '若い枝': ('若枝', '枝'),
        '若い果実': ('若い果実', '果実'),
        '古い葉': ('古葉', '葉'),
        '古い枝': ('古枝', '枝'),
        '新芽': ('新芽', '芽'),
        '新葉': ('新葉', '葉'),
        '乾燥葉': ('乾燥葉', '葉'),
        '湿った葉': ('湿った葉', '葉')
    }
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # 「植物名の状態+部位」パターンをチェック
            for state_part in state_parts:
                pattern = f'(.+)の{re.escape(state_part)}(.*)$'
                match = re.match(pattern, plant_name)
                
                if match:
                    base_plant_name = match.group(1).strip()
                    suffix = match.group(2).strip()
                    
                    # 複雑なケースをスキップ
                    if any(skip_word in base_plant_name for skip_word in [
                        '枯れ木', '朽ち木', 'その', 'で飼育', 'も食べる', 'を食す'
                    ]):
                        new_data.append(row)
                        continue
                    
                    # 状態と部位を取得
                    if state_part in state_part_mapping:
                        part_state, part_type = state_part_mapping[state_part]
                    else:
                        part_state, part_type = state_part, state_part
                    
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: {plant_name}")
                    print(f"  新: 食草名='{base_plant_name}', 部位='{part_state}'")
                    
                    new_row = row.copy()
                    new_row['plant_name'] = base_plant_name + suffix
                    new_row['plant_part'] = part_state
                    new_data.append(new_row)
                    fix_count += 1
                    break
            else:
                # 「広葉樹の枯れ葉で飼育」のような特殊ケースを個別処理
                if plant_name.startswith('広葉樹の枯れ葉'):
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: {plant_name}")
                    print(f"  新: 食草名='広葉樹', 部位='枯れ葉'")
                    
                    new_row = row.copy()
                    new_row['plant_name'] = '広葉樹'
                    new_row['plant_part'] = '枯れ葉'
                    new_data.append(new_row)
                    fix_count += 1
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
        koyoju_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == '広葉樹' and '枯れ葉' in row['plant_part']:
                    koyoju_entries.append(f"{row['insect_id']}: {row['plant_name']} - 部位: {row['plant_part']}")
        
        if koyoju_entries:
            print("広葉樹の枯れ葉修正例:")
            for entry in koyoju_entries[:5]:
                print(f"  {entry}")
        
        # 修正された他の例
        yabu_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == 'ヤブニッケイ' and '枯れ枝' in row['plant_part']:
                    yabu_entries.append(f"{row['insect_id']}: {row['plant_name']} - 部位: {row['plant_part']}")
        
        if yabu_entries:
            print("\nヤブニッケイの枯れ枝修正例:")
            for entry in yabu_entries:
                print(f"  {entry}")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_plant_part_states()