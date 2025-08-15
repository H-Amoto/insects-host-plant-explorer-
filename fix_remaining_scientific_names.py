#!/usr/bin/env python3
import csv
import re
import os

def fix_remaining_scientific_names():
    """残っている科学名関連の問題を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 残りの科学名関連問題の修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # パターン1: 植物名に学名が併記されている適切なケース（保持）
            if re.match(r'^[^(]+\\([A-Z][a-z]+ [a-z]+\\)$', plant_name):
                # 例: ムクゲ (Hibiscus syriacus) - これは適切なので保持
                new_data.append(row)
                continue
            
            # パターン2: 不完全な昆虫科学名（削除）
            elif any(pattern in plant_name for pattern in [
                'Callopistria placodoides (Guenée',
                'Protarchanara brevilinea (Fenn',
                'Nonagria puengeleri (Schawerda'
            ]):
                print(f"削除: 行{row_num} {row['insect_id']}")
                print(f"  不完全な昆虫科学名 '{plant_name[:50]}...' を削除")
                fix_count += 1
                continue  # この行は追加しない
            
            # パターン3: 学名で始まる植物名（植物学名として適切に処理）
            elif re.match(r'^[A-Z][a-z]+ [a-z]+ ', plant_name):
                # 例: "Calamagrostis canescens ヌマヤマアワ" → "ヌマヤマアワ"
                if ' ' in plant_name:
                    parts = plant_name.split(' ', 2)  # 最大3部分に分割
                    if len(parts) >= 3:
                        # 学名の後に和名がある場合
                        japanese_name = parts[2]
                        print(f"修正: 行{row_num} {row['insect_id']}")
                        print(f"  元: '{plant_name}'")
                        print(f"  新: '{japanese_name}'")
                        
                        row['plant_name'] = japanese_name
                        fix_count += 1
                    else:
                        # 学名のみの場合はそのまま保持
                        new_data.append(row)
                        continue
                else:
                    new_data.append(row)
                    continue
            
            # パターン4: 複雑な説明文が食草名になっているケース
            elif len(plant_name) > 50 and any(keyword in plant_name for keyword in [
                'リンネは', 'イネ科の', '現在は', 'から', 'が食草になっている'
            ]):
                # 説明文から植物名を抽出
                if 'リンネはイネ科の' in plant_name and 'Festuca fluitans' in plant_name:
                    print(f"修正: 行{row_num} {row['insect_id']}")
                    print(f"  元: '{plant_name[:50]}...'")
                    print(f"  新: 'ヒロハウキガヤ'")
                    
                    row['plant_name'] = 'ヒロハウキガヤ'
                    row['notes'] = 'リンネによる記載、現在は Glyceria fluitans'
                    fix_count += 1
                else:
                    # その他の複雑な説明文は削除
                    print(f"削除: 行{row_num} {row['insect_id']}")
                    print(f"  複雑な説明文 '{plant_name[:50]}...' を削除")
                    fix_count += 1
                    continue  # この行は追加しない
            
            new_data.append(row)
    
    print(f"\\n修正結果:")
    print(f"  修正・削除したエントリ: {fix_count}件")
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
        
        # 適切な学名併記の例を表示
        proper_scientific = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if re.match(r'^[^(]+\\([A-Z][a-z]+ [a-z]+\\)$', row['plant_name']):
                    proper_scientific.append(row['plant_name'])
        
        if proper_scientific:
            print(f"適切な学名併記の例 ({len(proper_scientific)}件):")
            for entry in list(set(proper_scientific))[:3]:
                print(f"  '{entry}'")
        
        # 残存する問題のある科学名パターンをチェック
        remaining_issues = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                plant_name = row['plant_name']
                if (len(plant_name) > 50 or 
                    any(pattern in plant_name for pattern in ['Callopistria', 'Protarchanara', 'Nonagria']) or
                    ('(' in plant_name and not plant_name.endswith(')'))):
                    remaining_issues.append(plant_name[:50])
        
        if remaining_issues:
            print(f"\\n残存する問題パターン:")
            for entry in list(set(remaining_issues))[:3]:
                print(f"  '{entry}...'")
        else:
            print("\\n✅ 科学名関連の問題修正が完了しました")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_remaining_scientific_names()