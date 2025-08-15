#!/usr/bin/env python3
import csv
import re
import json
from collections import defaultdict

class DataConverter:
    def __init__(self):
        self.insects_data = {}
        self.hostplants_data = []
        self.general_notes_data = []
        self.id_counter = defaultdict(int)
        self.used_ids = set()
        
    def generate_unique_id(self, catalog_no, scientific_name, japanese_name):
        """一意なinsect_idを生成"""
        if catalog_no:
            base_id = f"catalog-{catalog_no}"
            if base_id not in self.used_ids:
                self.used_ids.add(base_id)
                return base_id
        
        # カタログNoがない場合は代替ID生成
        self.id_counter['species'] += 1
        alt_id = f"species-{self.id_counter['species']:04d}"
        self.used_ids.add(alt_id)
        return alt_id
    
    def parse_hostplant_text(self, hostplant_text):
        """食草テキストを解析して個別食草リストに変換"""
        if not hostplant_text or hostplant_text.strip() in ['不明', '']:
            return []
        
        # セミコロンで分割
        plants = []
        raw_plants = re.split(r'[;；]', hostplant_text)
        
        for plant_text in raw_plants:
            plant_text = plant_text.strip()
            if not plant_text:
                continue
                
            # 科名の抽出
            plant_name = plant_text
            plant_family = ''
            
            # パターン1: "ムクゲ(アオイ科)" → "ムクゲ", "アオイ科"
            match = re.match(r'^([^(（]+)[(（]([^)）]*科)[)）]', plant_text)
            if match:
                plant_name = match.group(1).strip()
                plant_family = match.group(2).strip()
            else:
                # パターン2: "チチジマキイチゴ(以上バラ科)" → "チチジマキイチゴ", "バラ科"
                match = re.match(r'^([^(（]+)[(（]以上([^)）]*科)[)）]', plant_text)
                if match:
                    plant_name = match.group(1).strip()
                    plant_family = match.group(2).strip()
            
            if plant_name:
                plants.append({
                    'name': plant_name,
                    'family': plant_family,
                    'original_text': plant_text
                })
        
        return plants
    
    def is_general_note(self, note_text):
        """総合備考かどうかを判定"""
        if not note_text or len(note_text) < 50:
            return False
            
        # 出典のみの場合は除外
        if note_text in ['日本産蛾類標準図鑑2', '日本産蛾類標準図鑑3', '日本のハマキガ1']:
            return False
            
        # 生態的記述のキーワードをチェック
        ecological_keywords = [
            '広食性', '多食性', '世界的には', '国外では', '飼育下では', 
            '地域により', '季節により', '幼虫は', '成虫は'
        ]
        
        return any(keyword in note_text for keyword in ecological_keywords)
    
    def convert_data(self, input_file):
        """メインの変換処理"""
        print("データ変換開始...")
        
        record_counter = 0
        
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, 2):
                    try:
                        catalog_no = row.get('大図鑑カタログNo', '').strip()
                        scientific_name = row.get('学名', '').strip()
                        japanese_name = row.get('和名', '').strip()
                        
                        # 基本データが不完全な場合はスキップ
                        if not japanese_name:
                            print(f"警告: 行{row_num} - 和名が空白のためスキップ")
                            continue
                        
                        # 昆虫IDを生成
                        insect_id = self.generate_unique_id(catalog_no, scientific_name, japanese_name)
                        
                        # 昆虫基本情報を保存（重複チェック）
                        if insect_id not in self.insects_data:
                            self.insects_data[insect_id] = {
                                'insect_id': insect_id,
                                'catalog_no': catalog_no,
                                'family': row.get('科名', '').strip(),
                                'family_jp': row.get('科和名', '').strip(),
                                'subfamily': row.get('亜科名', '').strip(),
                                'subfamily_jp': row.get('亜科和名', '').strip(),
                                'tribe': row.get('族名', '').strip(),
                                'tribe_jp': row.get('族和名', '').strip(),
                                'genus': row.get('属名', '').strip(),
                                'subgenus': row.get('亜属名', '').strip(),
                                'species': row.get('種小名', '').strip(),
                                'subspecies': row.get('亜種小名', '').strip(),
                                'author': row.get('著者', '').strip(),
                                'year': row.get('公表年', '').strip(),
                                'japanese_name': japanese_name,
                                'old_japanese_name': row.get('旧和名', '').strip(),
                                'alternative_name': row.get('別名', '').strip(),
                                'other_names': row.get('その他の和名', '').strip(),
                                'scientific_name': scientific_name,
                                'synonyms': '',  # 今回のデータには含まれていない
                                'changes_since_standard': row.get('標準図鑑以後の変更', '').strip(),
                                'notes': ''  # 個別の備考は別途処理
                            }
                        
                        # 食草データの処理
                        hostplant_text = row.get('食草', '').strip()
                        reference = row.get('出典', '').strip()
                        
                        plants = self.parse_hostplant_text(hostplant_text)
                        for plant in plants:
                            record_counter += 1
                            self.hostplants_data.append({
                                'record_id': record_counter,
                                'insect_id': insect_id,
                                'plant_name': plant['name'],
                                'plant_family': plant['family'],
                                'observation_type': '野外（国内）',  # デフォルト値
                                'plant_part': '葉',  # デフォルト値
                                'life_stage': '幼虫',  # デフォルト値
                                'reference': reference,
                                'notes': ''  # 個別の食草備考
                            })
                        
                        # 総合備考の処理
                        note_text = row.get('備考', '').strip()
                        if self.is_general_note(note_text):
                            record_counter += 1
                            self.general_notes_data.append({
                                'record_id': record_counter,
                                'insect_id': insect_id,
                                'note_type': 'hostplants_general',
                                'content': note_text,
                                'reference': reference,
                                'page': '',
                                'year': ''
                            })
                    
                    except Exception as e:
                        print(f"エラー: 行{row_num} - {e}")
                        continue
            
            print(f"変換完了:")
            print(f"  昆虫基本情報: {len(self.insects_data)}件")
            print(f"  食草データ: {len(self.hostplants_data)}件")
            print(f"  総合備考: {len(self.general_notes_data)}件")
            
            return True
            
        except Exception as e:
            print(f"変換処理エラー: {e}")
            return False
    
    def save_to_csv(self, output_dir):
        """3つのCSVファイルに出力"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # insects.csv
        insects_file = os.path.join(output_dir, 'insects.csv')
        insects_fieldnames = [
            'insect_id', 'catalog_no', 'family', 'family_jp', 'subfamily', 'subfamily_jp',
            'tribe', 'tribe_jp', 'genus', 'subgenus', 'species', 'subspecies', 'author', 'year',
            'japanese_name', 'old_japanese_name', 'alternative_name', 'other_names',
            'scientific_name', 'synonyms', 'changes_since_standard', 'notes'
        ]
        
        with open(insects_file, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=insects_fieldnames)
            writer.writeheader()
            for insect in self.insects_data.values():
                writer.writerow(insect)
        
        # hostplants.csv
        hostplants_file = os.path.join(output_dir, 'hostplants.csv')
        hostplants_fieldnames = [
            'record_id', 'insect_id', 'plant_name', 'plant_family', 'observation_type',
            'plant_part', 'life_stage', 'reference', 'notes'
        ]
        
        with open(hostplants_file, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=hostplants_fieldnames)
            writer.writeheader()
            writer.writerows(self.hostplants_data)
        
        # general_notes.csv
        notes_file = os.path.join(output_dir, 'general_notes.csv')
        notes_fieldnames = [
            'record_id', 'insect_id', 'note_type', 'content', 'reference', 'page', 'year'
        ]
        
        with open(notes_file, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=notes_fieldnames)
            writer.writeheader()
            writer.writerows(self.general_notes_data)
        
        print(f"\n3つのCSVファイルを生成:")
        print(f"  {insects_file}")
        print(f"  {hostplants_file}")
        print(f"  {notes_file}")

def main():
    converter = DataConverter()
    
    # 変換実行
    input_file = '/Users/akimotohiroki/insects-host-plant-explorer/public/ListMJ_hostplants_master_backup_combined.csv'
    
    if converter.convert_data(input_file):
        # CSV出力
        output_dir = '/Users/akimotohiroki/insects-host-plant-explorer/normalized_data'
        converter.save_to_csv(output_dir)
        
        print("\n=== 変換完了 ===")
        print("データの整合性を確認してください。")
    else:
        print("変換に失敗しました。")

if __name__ == "__main__":
    main()