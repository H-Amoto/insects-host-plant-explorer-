#!/usr/bin/env python3
import csv
import re
import os

def remove_unnecessary_nado():
    """不要な「など」を除去して植物名を正規化"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 不要な「など」の除去開始 ===")
    
    hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
    
    new_data = []
    fix_count = 0
    
    # 「など」を除去すべき単独植物名のパターン
    # これらは元データで複数植物が列挙されているが、個別レコードに分割されているため「など」が不要
    single_plant_patterns = [
        'エノコログサなど',  # 元: メヒシバ、オイシバ、エノコログサなど → 個別レコード化済み
        'カノコユリなど',   # 元: オニユリ、テッポウユリ、カノコユリなど → 個別レコード化済み
        'マコモなど',       # 元: イネ、キタヨシ、カモガヤ、チガヤ、マコモなど → 個別レコード化済み
        'イボタノキなど',   # 元: ネズミモチ、コバノトネリコ、イボタノキなど → 個別レコード化済み
    ]
    
    # 「など」を保持すべきパターン（複数の類似種を表す有効な表現）
    valid_nado_patterns = [
        'タンポポなど',      # 複数のタンポポ種を表す有効な表現
        'イタドリなど',      # 複数のイタドリ種を表す有効な表現
        'ミズキなど',        # 複数のミズキ種を表す有効な表現
        'ニセアカシアなど',  # 複数のアカシア種を表す有効な表現
        'マユミなど',        # 複数のマユミ種を表す有効な表現
        'オオカメノキなど',  # 複数のカメノキ種を表す有効な表現
        'クロズルなど',      # 複数のズル種を表す有効な表現
        'キャベツなど',      # 複数のアブラナ科野菜を表す有効な表現
    ]
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            plant_name = row['plant_name']
            
            # 不要な「など」の除去対象かチェック
            if plant_name in single_plant_patterns:
                clean_name = plant_name.replace('など', '')
                print(f"\\n修正対象: 行{row_num}")
                print(f"  昆虫ID: {row['insect_id']}")
                print(f"  植物名: '{plant_name}' → '{clean_name}'")
                print(f"  理由: 個別レコード化により「など」が不要")
                
                row['plant_name'] = clean_name
                fix_count += 1
            
            # 有効な「など」の場合は保持（ログ出力のみ）
            elif plant_name in valid_nado_patterns:
                print(f"\\n保持: 行{row_num}")
                print(f"  昆虫ID: {row['insect_id']}")
                print(f"  植物名: '{plant_name}' (有効な「など」表現)")
            
            new_data.append(row)
    
    print(f"\\n修正結果:")
    print(f"  修正したエントリ: {fix_count}件")
    print(f"  元のエントリ数: {row_num-1}件")
    print(f"  修正後のエントリ数: {len(new_data)}件")
    
    # 修正されたデータを保存
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
    
    # 最終検証
    print(f"\\n=== 最終検証 ===")
    
    # 修正された植物名を確認
    fixed_plants = []
    remaining_nado = []
    
    with open(hostplants_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            plant_name = row['plant_name']
            
            # 修正されたものを確認
            if plant_name in ['エノコログサ', 'カノコユリ', 'マコモ', 'イボタノキ']:
                fixed_plants.append(f"{row['insect_id']}: {plant_name}")
            
            # 残存する「など」をカウント
            if 'など' in plant_name:
                remaining_nado.append(plant_name)
    
    print(f"修正された植物名:")
    for plant in fixed_plants:
        print(f"  {plant}")
    
    # 残存する「など」の統計
    nado_counts = {}
    for plant in remaining_nado:
        nado_counts[plant] = nado_counts.get(plant, 0) + 1
    
    print(f"\\n残存する「など」付き植物名:")
    for plant, count in sorted(nado_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {plant}: {count}件")
    
    print(f"\\n🌿 不要な「など」の除去が完了しました！")

if __name__ == "__main__":
    remove_unnecessary_nado()