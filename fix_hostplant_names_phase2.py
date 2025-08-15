#!/usr/bin/env python3
import csv
import re
import os

def fix_remaining_hostplant_issues():
    """残りの食草名問題を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 残りの食草名問題の修正開始 ===")
    
    # hostplants.csvを読み込み
    hostplants_file = os.path.join(base_dir, 'normalized_data', 'hostplants.csv')
    fixed_data = []
    fix_count = 0
    suspicious_cases = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            original_name = plant_name
            
            # パターン1: 数字のみ (年号) → "不明"に変更
            if re.match(r'^\d{4}$', plant_name):
                row['plant_name'] = '不明'
                fix_count += 1
                print(f"修正 (数字のみ): {original_name} → 不明")
            
            # パターン2: "年号)" → "不明"に変更
            elif re.match(r'^\d{4}\)$', plant_name):
                row['plant_name'] = '不明'
                fix_count += 1
                print(f"修正 (年号括弧): {original_name} → 不明")
            
            # パターン3の候補を収集（特殊ケース）
            else:
                # 学名らしき文字列が含まれている
                if re.search(r'\([A-Z][a-z]+\)', plant_name):
                    suspicious_cases.append({
                        'row': row_num,
                        'insect_id': row['insect_id'],
                        'plant_name': plant_name,
                        'type': '学名らしき文字列'
                    })
                
                # ピリオドで始まる
                elif plant_name.startswith('.'):
                    suspicious_cases.append({
                        'row': row_num,
                        'insect_id': row['insect_id'],
                        'plant_name': plant_name,
                        'type': 'ピリオドで始まる'
                    })
                
                # 特殊記号や文字列
                elif any(char in plant_name for char in [')', '(', 'Moor', '泥炭地']):
                    suspicious_cases.append({
                        'row': row_num,
                        'insect_id': row['insect_id'],
                        'plant_name': plant_name,
                        'type': '特殊記号/文字列'
                    })
                
                # 明らかに植物名でない文字列
                elif re.search(r'^[A-Z][a-z]+ [a-z]+', plant_name):  # 学名パターン
                    suspicious_cases.append({
                        'row': row_num,
                        'insect_id': row['insect_id'],
                        'plant_name': plant_name,
                        'type': '学名パターン'
                    })
                
                # 短すぎる/意味不明な文字列
                elif len(plant_name) <= 2 and plant_name not in ['不明', '未記録']:
                    suspicious_cases.append({
                        'row': row_num,
                        'insect_id': row['insect_id'],
                        'plant_name': plant_name,
                        'type': '短すぎる文字列'
                    })
            
            fixed_data.append(row)
    
    # 修正されたデータを保存
    if fix_count > 0:
        with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
            if fixed_data:
                writer = csv.DictWriter(file, fieldnames=fixed_data[0].keys())
                writer.writeheader()
                writer.writerows(fixed_data)
        
        # publicフォルダにもコピー
        import shutil
        src = hostplants_file
        dst = os.path.join(base_dir, 'public', 'hostplants.csv')
        shutil.copy2(src, dst)
        
        print(f"\n=== 修正完了 ===")
        print(f"修正件数: {fix_count}件")
        print("hostplants.csvを更新しました")
    
    # パターン3の候補を表示
    print(f"\n=== パターン3: 要確認ケース ({len(suspicious_cases)}件) ===")
    
    # タイプ別に整理して表示
    by_type = {}
    for case in suspicious_cases:
        type_key = case['type']
        if type_key not in by_type:
            by_type[type_key] = []
        by_type[type_key].append(case)
    
    for type_name, cases in by_type.items():
        print(f"\n【{type_name}】({len(cases)}件)")
        for i, case in enumerate(cases[:10]):  # 各タイプ最大10件表示
            print(f"  {i+1}. 行{case['row']}: {case['insect_id']} → '{case['plant_name']}'")
        if len(cases) > 10:
            print(f"  ... (他{len(cases)-10}件)")
    
    return suspicious_cases

if __name__ == "__main__":
    suspicious_cases = fix_remaining_hostplant_issues()