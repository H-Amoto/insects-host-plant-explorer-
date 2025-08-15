#!/usr/bin/env python3
import csv
import os

def fix_comment_plant_names():
    """コメント様の文章が食草名になっているケースを修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== コメント様文章の食草名修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    rows_to_skip = set()
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    
    i = 0
    while i < len(rows):
        row = rows[i]
        
        if i in rows_to_skip:
            i += 1
            continue
        
        plant_name = row['plant_name']
        
        # パターン1: 「同科に固有とは考えがたい」を前の行の備考に移動
        if plant_name == '同科に固有とは考えがたい' and row['insect_id'] == 'species-3825':
            print(f"修正: 行{i+2} species-3825")
            print(f"  '{plant_name}' を前の行（ノイバラ）の備考に移動")
            
            # 前の行（ノイバラ）を探して備考を追加
            for j in range(len(new_data)-1, -1, -1):
                if (new_data[j]['insect_id'] == 'species-3825' and 
                    new_data[j]['plant_name'] == 'ノイバラ'):
                    new_data[j]['notes'] = 'バラ科に固有とは考えがたい'
                    print(f"  ノイバラの備考を更新: 'バラ科に固有とは考えがたい'")
                    break
            
            # この行は削除（追加しない）
            rows_to_skip.add(i)
            fix_count += 1
        
        # パターン2: 「同科に固有」を前の行の備考に移動
        elif plant_name == '同科に固有' and row['insect_id'] == 'species-3718':
            print(f"修正: 行{i+2} species-3718")
            print(f"  '{plant_name}' を前の行（シラカンバ）の備考に移動")
            
            # 前の行（シラカンバ）を探して備考を追加
            for j in range(len(new_data)-1, -1, -1):
                if (new_data[j]['insect_id'] == 'species-3718' and 
                    new_data[j]['plant_name'] == 'シラカンバ'):
                    new_data[j]['notes'] = 'カバノキ科に固有'
                    print(f"  シラカンバの備考を更新: 'カバノキ科に固有'")
                    break
            
            # この行は削除（追加しない）
            rows_to_skip.add(i)
            fix_count += 1
        
        # パターン3: 「ヨーロッパでは50種以上の草本が記録されている」を備考に変換
        elif plant_name == 'ヨーロッパでは50種以上の草本が記録されている' and row['insect_id'] == 'species-5601':
            print(f"修正: 行{i+2} species-5601")
            print(f"  '{plant_name}' を前の行の備考に移動")
            
            # 前の行を探して備考を追加
            for j in range(len(new_data)-1, -1, -1):
                if new_data[j]['insect_id'] == 'species-5601':
                    if new_data[j]['notes']:
                        new_data[j]['notes'] += f"; {plant_name}"
                    else:
                        new_data[j]['notes'] = plant_name
                    print(f"  前の行の備考を更新")
                    break
            
            # この行は削除（追加しない）
            rows_to_skip.add(i)
            fix_count += 1
        
        # その他の説明文的な食草名パターンをチェック
        elif (len(plant_name) > 15 and 
              any(phrase in plant_name for phrase in [
                  'では', 'されている', 'とは考え', 'である可能性', 
                  'に固有', 'を食べ', 'が記録', 'と推定'
              ]) and 
              not any(skip in plant_name for skip in ['科', '属', '類'])):
            
            print(f"修正: 行{i+2} {row['insect_id']}")
            print(f"  説明文的な食草名 '{plant_name}' を前の行の備考に移動")
            
            # 前の行を探して備考を追加
            for j in range(len(new_data)-1, -1, -1):
                if new_data[j]['insect_id'] == row['insect_id']:
                    if new_data[j]['notes']:
                        new_data[j]['notes'] += f"; {plant_name}"
                    else:
                        new_data[j]['notes'] = plant_name
                    print(f"  前の行の備考を更新")
                    break
            
            # この行は削除（追加しない）
            rows_to_skip.add(i)
            fix_count += 1
        
        else:
            new_data.append(row)
        
        i += 1
    
    print(f"\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  削除したエントリ: {len(rows_to_skip)}件")
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
        
        # species-3825の修正確認
        species_3825_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['insect_id'] == 'species-3825' and row['notes']:
                    species_3825_entries.append(f"{row['plant_name']} - 備考: {row['notes']}")
        
        if species_3825_entries:
            print("species-3825の修正例:")
            for entry in species_3825_entries:
                print(f"  {entry}")
        
        # species-3718の修正確認
        species_3718_entries = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['insect_id'] == 'species-3718' and row['notes']:
                    species_3718_entries.append(f"{row['plant_name']} - 備考: {row['notes']}")
        
        if species_3718_entries:
            print("\nspecies-3718の修正例:")
            for entry in species_3718_entries:
                print(f"  {entry}")
        
        print("\n✅ コメント様文章の食草名修正が完了しました")
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_comment_plant_names()