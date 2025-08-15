#!/usr/bin/env python3
import csv
import re
import os

def fix_integration_issues():
    """統合後のデータ品質問題を修正"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 統合後データ品質問題修正開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    new_data = []
    fix_count = 0
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            record_id = row['record_id']
            
            # 統合データのみ対象（buprestidae, butterfly, hamushi）
            if any(prefix in record_id for prefix in ['buprestidae-', 'butterfly-', 'hamushi-']):
                
                # パターン1: 不明（説明文）形式
                if plant_name.startswith('不明（'):
                    print(f"修正: {record_id}")
                    print(f"  元: '{plant_name}'")
                    
                    # 括弧内の説明を抽出（閉じ括弧があってもなくても対応）
                    if plant_name.endswith('）'):
                        explanation = plant_name[3:-1]  # "不明（" と "）" を除去
                    else:
                        explanation = plant_name[3:]  # "不明（" を除去
                    
                    row['plant_name'] = '不明'
                    row['notes'] = explanation
                    
                    print(f"  新: plant_name='不明', notes='{explanation}'")
                    fix_count += 1
                
                # パターン2: 「○○など）」で終わる残留パターン
                elif plant_name.endswith('など）'):
                    print(f"修正: {record_id}")
                    print(f"  元: '{plant_name}'")
                    
                    # 「など）」を除去
                    clean_name = plant_name[:-3]  # "など）" を除去
                    row['plant_name'] = clean_name
                    
                    print(f"  新: plant_name='{clean_name}'")
                    fix_count += 1
                
                # パターン3: 空の植物名
                elif not plant_name or plant_name.strip() == '':
                    print(f"修正: {record_id}")
                    print(f"  元: 空の植物名")
                    
                    row['plant_name'] = '不明'
                    
                    print(f"  新: plant_name='不明'")
                    fix_count += 1
                
                # パターン4: 科レベルエントリの残存パターン「○○科（」で始まって適切に閉じられていない
                elif '科（' in plant_name and not plant_name.endswith('）'):
                    print(f"修正: {record_id}")
                    print(f"  元: '{plant_name}'")
                    
                    # 科名を抽出
                    family_match = re.search(r'([^（]+科)', plant_name)
                    if family_match:
                        family_name = family_match.group(1)
                        row['plant_name'] = family_name
                        row['plant_family'] = family_name
                        row['notes'] = '科レベルの記録'
                        
                        print(f"  新: plant_name='{family_name}', plant_family='{family_name}'")
                        fix_count += 1
            
            new_data.append(row)
    
    print(f"\\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  総エントリ数: {len(new_data)}件")
    
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
        if os.path.exists(os.path.dirname(dst)):
            shutil.copy2(src, dst)
        
        print("hostplants.csvを更新しました")
        
        # 検証
        print(f"\\n=== 検証 ===")
        
        # 残存する問題パターンをチェック
        remaining_issues = []
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                record_id = row['record_id']
                plant_name = row['plant_name']
                
                # 統合データのみ対象
                if any(prefix in record_id for prefix in ['buprestidae-', 'butterfly-', 'hamushi-']):
                    if any(pattern in plant_name for pattern in [
                        'など）', '不明（', '科（', 'と思われる', '判明していない'
                    ]):
                        remaining_issues.append(f"{record_id}: {plant_name[:30]}...")
        
        if remaining_issues:
            print(f"残存する問題パターン ({len(remaining_issues)}件):") 
            for issue in remaining_issues[:5]:
                print(f"  {issue}")
        else:
            print("✅ 統合データの品質問題修正が完了しました")
        
        # 「不明」エントリの統計
        unknown_count = 0
        unknown_new = 0
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['plant_name'] == '不明':
                    unknown_count += 1
                    if any(prefix in row['record_id'] for prefix in ['buprestidae-', 'butterfly-', 'hamushi-']):
                        unknown_new += 1
        
        print(f"\\n「不明」エントリ統計:")
        print(f"  全体: {unknown_count}件")
        print(f"  新規統合データ: {unknown_new}件")
        
    else:
        print("修正対象が見つかりませんでした")

if __name__ == "__main__":
    fix_integration_issues()