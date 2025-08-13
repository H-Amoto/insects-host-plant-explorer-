#!/usr/bin/env python3
import os
import re
import shutil

def extract_scientific_name(filename):
    """ファイル名から学名を抽出"""
    # パターン1: 和名 学名.jpg
    # パターン2: 和名亜種名 学名.jpg
    
    # 拡張子を除去
    name_without_ext = filename.replace('.jpg', '').replace('.JPG', '')
    
    # 特殊ケースの処理
    special_cases = {
        'オオチャバネセセリ': 'Polytremis_pellucida',
        'クズノチビタマムシ': 'Trachys_auricollis',
        'コキマエヤガ': 'Chilodes_pacifica',
        'サヌキキリガ': 'Conistra_flammatra',
        'ヤマトマダラメイガ': 'Nephopterix_angustella'
    }
    
    for japanese_name, scientific_name in special_cases.items():
        if japanese_name in filename:
            return scientific_name
    
    # 学名パターンを探す（属名は大文字始まり、種小名は小文字）
    # パターン: Genus species または Genus species subspecies
    pattern = r'([A-Z][a-z]+(?:\s+[a-z]+)+)'
    match = re.search(pattern, name_without_ext)
    
    if match:
        scientific_name = match.group(1)
        # 余分な情報を削除
        scientific_name = re.sub(r'\s*\([^)]*\)\s*', '', scientific_name)  # (Author, year)を削除
        scientific_name = re.sub(r'\s*\[[^\]]*\]\s*', '', scientific_name)  # [Author]を削除
        scientific_name = re.sub(r',.*$', '', scientific_name)  # カンマ以降を削除
        
        # 属名と種小名のみを抽出（亜種名は除く場合が多い）
        parts = scientific_name.split()
        if len(parts) >= 2:
            # 最初の2つの部分を取得（属名と種小名）
            return f"{parts[0]}_{parts[1]}"
    
    return None

def rename_japanese_images():
    """和名ファイルを学名にリネーム"""
    image_dir = 'public/images/insects'
    renamed_files = []
    failed_files = []
    
    # ディレクトリ内のファイルを取得
    for filename in os.listdir(image_dir):
        if not filename.endswith(('.jpg', '.JPG')):
            continue
            
        # 日本語文字が含まれているかチェック
        if not any(ord(char) > 0x3000 for char in filename):
            continue
            
        filepath = os.path.join(image_dir, filename)
        
        # 学名を抽出
        scientific_name = extract_scientific_name(filename)
        
        if scientific_name:
            new_filename = f"{scientific_name}.jpg"
            new_filepath = os.path.join(image_dir, new_filename)
            
            # 既存ファイルがある場合は番号を付ける
            counter = 2
            while os.path.exists(new_filepath):
                new_filename = f"{scientific_name}_{counter}.jpg"
                new_filepath = os.path.join(image_dir, new_filename)
                counter += 1
            
            # リネーム実行
            try:
                shutil.move(filepath, new_filepath)
                renamed_files.append((filename, new_filename))
                print(f"✓ {filename} → {new_filename}")
            except Exception as e:
                failed_files.append((filename, str(e)))
                print(f"✗ {filename}: {e}")
        else:
            failed_files.append((filename, "学名を抽出できませんでした"))
            print(f"✗ {filename}: 学名を抽出できませんでした")
    
    # 結果を表示
    print(f"\n=== リネーム結果 ===")
    print(f"成功: {len(renamed_files)} ファイル")
    print(f"失敗: {len(failed_files)} ファイル")
    
    if failed_files:
        print("\n=== 失敗したファイル ===")
        for filename, reason in failed_files:
            print(f"  - {filename}: {reason}")
    
    return renamed_files, failed_files

if __name__ == "__main__":
    renamed_files, failed_files = rename_japanese_images()