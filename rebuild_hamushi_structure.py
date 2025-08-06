#!/usr/bin/env python3
"""
ハムシファイルをListMJと同じ27列構造に統一するスクリプト
"""

import pandas as pd
import numpy as np
from pathlib import Path

def rebuild_hamushi_structure():
    print("ハムシファイル構造統一を開始します...")
    
    # ファイルパス
    legacy_hamushi_path = Path("legacy-local-hamushi-files/hamushi_species_integrated.csv")
    legacy_leafbeetle_path = Path("legacy-local-hamushi-files/leafbeetle_hostplants.csv")
    listmj_path = Path("public/ListMJ_hostplants_master.csv")
    output_path = Path("hamushi_integrated_master_listmj_structure.csv")
    
    # ListMJファイルから標準構造を取得
    listmj_df = pd.read_csv(listmj_path)
    target_columns = listmj_df.columns.tolist()
    print(f"目標構造: {len(target_columns)}列")
    print(f"列名: {target_columns}")
    
    # 統合前hamushiファイル読み込み (28列構造)
    hamushi_df = pd.read_csv(legacy_hamushi_path)
    print(f"統合前hamushi: {len(hamushi_df)}行, {len(hamushi_df.columns)}列")
    
    # leafbeetleファイル読み込み (7列構造)
    try:
        leafbeetle_df = pd.read_csv(legacy_leafbeetle_path)
        print(f"Leafbeetle: {len(leafbeetle_df)}行, {len(leafbeetle_df.columns)}列")
    except Exception as e:
        print(f"Leafbeetleファイル読み込みエラー: {e}")
        leafbeetle_df = pd.DataFrame()
    
    # hamushiデータをListMJ構造に変換
    hamushi_unified = pd.DataFrame(columns=target_columns)
    
    for _, row in hamushi_df.iterrows():
        new_row = {}
        
        # 直接マッピングできる列
        direct_mapping = {
            '大図鑑カタログNo': row.get('大図鑑カタログNo', ''),
            '科名': row.get('科名', ''),
            '科和名': row.get('科和名', ''),
            '亜科名': row.get('亜科名', ''),
            '亜科和名': row.get('亜科和名', ''),
            '族名': row.get('族名', ''),
            '族和名': row.get('族和名', ''),
            '亜族名': row.get('亜族名', ''),
            '亜族和名': row.get('亜族和名', ''),
            '属名': row.get('属名', ''),
            '亜属名': row.get('亜属名', ''),
            '種小名': row.get('種小名', ''),
            '亜種小名': row.get('亜種小名', ''),
            '著者': row.get('著者', ''),
            '公表年': row.get('公表年', ''),
            '類似種': row.get('類似種', ''),
            '和名': row.get('和名', ''),
            '旧和名': row.get('旧和名', ''),
            '別名': row.get('別名', ''),
            'その他の和名': row.get('その他の和名', ''),
            '亜種範囲': row.get('亜種範囲', ''),
            '標準図鑑ステータス': row.get('標準図鑑ステータス', ''),
            '標準図鑑以後の変更': row.get('標準図鑑以後の変更', ''),
            '学名': row.get('学名', ''),
            '食草': row.get('食草', ''),
            '出典': row.get('出典', ''),
            '備考': row.get('備考', '')
        }
        
        # NaN値を空文字に変換
        for key, value in direct_mapping.items():
            new_row[key] = '' if pd.isna(value) else str(value)
        
        hamushi_unified = pd.concat([hamushi_unified, pd.DataFrame([new_row])], ignore_index=True)
    
    # leafbeetleデータをListMJ構造に変換
    leafbeetle_unified = pd.DataFrame(columns=target_columns)
    
    if not leafbeetle_df.empty:
        for _, row in leafbeetle_df.iterrows():
            new_row = {}
            
            # leafbeetleの基本情報をマッピング
            for col in target_columns:
                new_row[col] = ''
            
            # 利用可能な情報をマッピング
            new_row['和名'] = str(row.get('和名', ''))
            new_row['学名'] = str(row.get('学名', ''))
            new_row['食草'] = str(row.get('食草', ''))
            new_row['科和名'] = 'ハムシ科'  # leafbeetleはハムシ科
            new_row['科名'] = 'Chrysomelidae'
            
            # 出典情報を統合
            if '書名' in row and '著者' in row:
                source_parts = []
                if not pd.isna(row.get('書名')):
                    source_parts.append(str(row['書名']))
                if not pd.isna(row.get('著者')):
                    source_parts.append(f"著者: {row['著者']}")
                if not pd.isna(row.get('出版社')):
                    source_parts.append(f"出版社: {row['出版社']}")
                if not pd.isna(row.get('発行年')):
                    source_parts.append(f"発行年: {row['発行年']}")
                new_row['出典'] = ', '.join(source_parts)
            
            # カタログNoを生成 (H + 連番)
            new_row['大図鑑カタログNo'] = f"LB{len(leafbeetle_unified) + 1:03d}"
            
            leafbeetle_unified = pd.concat([leafbeetle_unified, pd.DataFrame([new_row])], ignore_index=True)
    
    # 両データセットを統合
    final_df = pd.concat([hamushi_unified, leafbeetle_unified], ignore_index=True)
    
    # 重複を除去（和名と学名の組み合わせで判定）
    final_df = final_df.drop_duplicates(subset=['和名', '学名'], keep='first')
    
    # 品質情報を備考に追加
    for idx, row in final_df.iterrows():
        remarks = str(row.get('備考', ''))
        source = str(row.get('出典', ''))
        
        # 品質レベルを推定
        if 'ハムシハンドブック' in source:
            quality = '品質A(ハンドブック)'
        else:
            quality = '品質B(目録データベース)'
        
        if remarks and remarks != '':
            final_df.at[idx, '備考'] = f"{remarks} [{quality}]"
        else:
            final_df.at[idx, '備考'] = f"[{quality}]"
    
    # ファイル出力
    final_df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"\n統一構造ファイル生成完了:")
    print(f"- ファイル: {output_path}")
    print(f"- 総種数: {len(final_df)}種")
    print(f"- 列数: {len(final_df.columns)}列")
    print(f"- ハムシ目録由来: {len(hamushi_unified)}種")
    print(f"- ハンドブック由来: {len(leafbeetle_unified)}種")
    
    # サンプルデータを表示
    print(f"\nサンプルデータ:")
    print(final_df[['和名', '学名', '科和名', '食草', '出典']].head(3))
    
    return output_path

if __name__ == "__main__":
    rebuild_hamushi_structure()