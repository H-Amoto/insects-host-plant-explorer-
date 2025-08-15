#!/usr/bin/env python3
import csv

def regenerate_integrated_csv():
    """修正された学名で統合CSVを再生成"""
    print("統合CSVを再生成中...")
    
    input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master.csv'
    output_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/insects_integrated_master_fixed.csv'
    fixed_master = '/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master_fixed.csv'
    
    # 修正された学名をマッピング
    fixes = {
        'Anapamea incerta (Staudinger,': 'Anapamea incerta (Staudinger, 1892)',
        'Buzara onelia (Guenée,': 'Buzara onelia (Guenée, 1852)',
        'Macaldenia palumba (Guenée,': 'Macaldenia palumba (Guenée, 1852)',
        'Mocis dolosa (Butler,': 'Mocis dolosa (Butler, 1880)',
        'Oxyodes scrobiculatus (Fabricius,': 'Oxyodes scrobiculatus (Fabricius, 1775)',
        'Blasticorhinus rivulosa (Walker,': 'Blasticorhinus rivulosa (Walker, 1865)',
        'Mecodina albodentata (Swinhoe,': 'Mecodina albodentata (Swinhoe, 1895)',
        'Mecodina praecipua (Walker,': 'Mecodina praecipua (Walker, 1865)',
        'Bocula diffusa (Swinhoe,': 'Bocula diffusa (Swinhoe, 1890)',
        'Hulodes caranea (Cramer,': 'Hulodes caranea (Cramer, 1780)',
        'Lacera noctilio (Fabricius,': 'Lacera noctilio (Fabricius, 1794)',
        'Ericeia inangulata (Guenée,': 'Ericeia inangulata (Guenée, 1852)',
        'Avatha discolor (Fabricius,': 'Avatha discolor (Fabricius, 1794)',
        'Aegilia describens (Walker,': 'Aegilia describens (Walker, 1858)',
        'Lophoptera anthyalus (Hampson,': 'Lophoptera anthyalus (Hampson, 1894)',
        'Lophoptera acuda (Swinhoe,': 'Lophoptera acuda (Swinhoe, 1906)',
        'Phalga clarirena (Sugi,': 'Phalga clarirena (Sugi, 1982)',
        'Eutelia cuneades (Draudt,': 'Eutelia cuneades (Draudt, 1950)',
        'Atacira melanephra (Hampson,': 'Atacira melanephra (Hampson, 1912)',
        'Targalla delatrix (Guenée,': 'Targalla delatrix (Guenée, 1852)',
        'Thysanoplusia lectula (Walker,': 'Thysanoplusia lectula (Walker, 1858)',
    }
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixed_count = 0
    for old, new in fixes.items():
        if old in content:
            content = content.replace(old, new)
            fixed_count += 1
            print(f"統合CSV修正: {old} → {new}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n統合CSV修正完了: {fixed_count}件の学名を修正")
    print(f"出力ファイル: {output_file}")

if __name__ == "__main__":
    regenerate_integrated_csv()