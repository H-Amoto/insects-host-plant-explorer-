#!/usr/bin/env python3
import csv
import os

def analyze_duplicate_sources():
    """重複する和名の原因を元ファイルから分析"""
    base_dir = '/Users/akimotohiroki/insects-host-plant-explorer'
    
    print("=== 重複和名の原因分析 ===")
    
    # 重複しているIDのペア
    duplicate_pairs = [
        ("species-1497", "species-1498", "ワタアカミムシガ"),
        ("species-1815", "species-1816", "カラマツイトヒキハマキ"),
        ("species-1972", "species-1973", "アカガネヒメハマキ"),
        ("species-2153", "species-2154", "フタシロモンヒメハマキ"),
        ("species-2155", "species-2156", "オオナガバヒメハマキ"),
        ("species-2157", "species-2158", "ダケカンバヒメハマキ"),
        ("species-5381", "species-6152", "オオアカキリバ"),
    ]
    
    insects_file = os.path.join(base_dir, 'public', 'insects.csv')
    
    # 各重複ペアの詳細を分析
    for id1, id2, japanese_name in duplicate_pairs:
        print(f"\n=== {japanese_name} ===")
        
        # insects.csvから詳細情報を取得
        with open(insects_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['insect_id'] in [id1, id2]:
                    print(f"ID: {row['insect_id']}")
                    print(f"  科: {row['family']}")
                    print(f"  属: {row['genus']}")
                    print(f"  種: {row['species']}")
                    print(f"  学名: {row['scientific_name']}")
                    print(f"  著者年: {row['author']} {row['year']}")
                    print(f"  旧和名: {row['old_japanese_name']}")
                    print(f"  別名: {row['alternative_name']}")
                    print(f"  その他名: {row['other_names']}")
                    print(f"  変更: {row['changes_since_standard']}")
                    print(f"  備考: {row['notes']}")
        
        # hostplants.csvでの使用状況を確認
        hostplants_file = os.path.join(base_dir, 'public', 'hostplants.csv')
        
        id1_records = 0
        id2_records = 0
        
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['insect_id'] == id1:
                    id1_records += 1
                elif row['insect_id'] == id2:
                    id2_records += 1
        
        print(f"\nhostplants.csvでの使用:")
        print(f"  {id1}: {id1_records}件")
        print(f"  {id2}: {id2_records}件")
        
        # どちらか一方しか使われていない場合は統合候補
        if id1_records == 0:
            print(f"  → {id1}は未使用、{id2}に統合可能")
        elif id2_records == 0:
            print(f"  → {id2}は未使用、{id1}に統合可能")
        elif id1_records > 0 and id2_records > 0:
            print(f"  → 両方使用されている、和名の区別が必要")
    
    print(f"\n=== 結論と推奨アクション ===")
    print("1. 学名が空欄のエントリが多く見られます")
    print("   - これらは不完全なデータとして扱う必要があります")
    print("2. 同じ和名で異なる学名を持つペアが存在します")
    print("   - 分類学的な確認が必要です")
    print("3. hostplants.csvで未使用のIDがある場合は削除候補です")
    print("4. 両方使用されている場合は和名に区別記号の追加を検討")
    
    # IDの連続性をチェック（統合時の問題を特定）
    print(f"\n=== ID連続性チェック ===")
    for id1, id2, japanese_name in duplicate_pairs:
        num1 = int(id1.split('-')[1])
        num2 = int(id2.split('-')[1])
        if abs(num1 - num2) == 1:
            print(f"{japanese_name}: 連続ID ({id1}, {id2}) - 統合時の重複エラーの可能性")

if __name__ == "__main__":
    analyze_duplicate_sources()