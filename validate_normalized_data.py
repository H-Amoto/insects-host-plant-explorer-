#!/usr/bin/env python3
import csv
import os
from collections import defaultdict, Counter

class DataValidator:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.insects = {}
        self.hostplants = []
        self.general_notes = []
        
    def load_data(self):
        """3つのCSVファイルを読み込み"""
        # insects.csv
        insects_file = os.path.join(self.data_dir, 'insects.csv')
        with open(insects_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.insects[row['insect_id']] = row
        
        # hostplants.csv  
        hostplants_file = os.path.join(self.data_dir, 'hostplants.csv')
        with open(hostplants_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            self.hostplants = list(reader)
        
        # general_notes.csv
        notes_file = os.path.join(self.data_dir, 'general_notes.csv')
        with open(notes_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            self.general_notes = list(reader)
        
        print(f"データ読み込み完了:")
        print(f"  昆虫: {len(self.insects)}件")
        print(f"  食草: {len(self.hostplants)}件")
        print(f"  総合備考: {len(self.general_notes)}件")
    
    def validate_referential_integrity(self):
        """外部キー整合性チェック"""
        print(f"\n=== 外部キー整合性チェック ===")
        
        # hostplantsの整合性
        orphaned_hostplants = []
        for hp in self.hostplants:
            if hp['insect_id'] not in self.insects:
                orphaned_hostplants.append(hp['insect_id'])
        
        # general_notesの整合性
        orphaned_notes = []
        for note in self.general_notes:
            if note['insect_id'] not in self.insects:
                orphaned_notes.append(note['insect_id'])
        
        print(f"食草データの孤児レコード: {len(orphaned_hostplants)}件")
        print(f"総合備考の孤児レコード: {len(orphaned_notes)}件")
        
        if orphaned_hostplants:
            print(f"孤児食草ID例: {orphaned_hostplants[:5]}")
        if orphaned_notes:
            print(f"孤児備考ID例: {orphaned_notes[:5]}")
        
        return len(orphaned_hostplants) == 0 and len(orphaned_notes) == 0
    
    def validate_data_quality(self):
        """データ品質チェック"""
        print(f"\n=== データ品質チェック ===")
        
        # 昆虫データの品質
        insects_without_name = sum(1 for insect in self.insects.values() if not insect['japanese_name'])
        insects_without_scientific = sum(1 for insect in self.insects.values() if not insect['scientific_name'])
        
        print(f"和名なし昆虫: {insects_without_name}件")
        print(f"学名なし昆虫: {insects_without_scientific}件")
        
        # 食草データの品質
        hostplants_without_name = sum(1 for hp in self.hostplants if not hp['plant_name'])
        empty_family_count = sum(1 for hp in self.hostplants if not hp['plant_family'])
        
        print(f"植物名なし食草: {hostplants_without_name}件")
        print(f"科名なし食草: {empty_family_count}件")
        
        # 総合備考の品質
        short_notes = sum(1 for note in self.general_notes if len(note['content']) < 30)
        print(f"短い総合備考: {short_notes}件")
        
        return hostplants_without_name == 0
    
    def analyze_hostplant_distribution(self):
        """食草分布の分析"""
        print(f"\n=== 食草分布分析 ===")
        
        # 昆虫あたりの食草数
        hostplant_counts = defaultdict(int)
        for hp in self.hostplants:
            hostplant_counts[hp['insect_id']] += 1
        
        count_distribution = Counter(hostplant_counts.values())
        
        print(f"昆虫あたりの食草数分布:")
        for count, insects in sorted(count_distribution.items()):
            print(f"  {count}種の食草: {insects}種の昆虫")
        
        # 最多食草の昆虫
        max_hostplants = max(hostplant_counts.values())
        max_insects = [insect_id for insect_id, count in hostplant_counts.items() if count == max_hostplants]
        
        print(f"\n最多食草数: {max_hostplants}種")
        for insect_id in max_insects[:3]:  # 上位3種まで表示
            insect_name = self.insects[insect_id]['japanese_name']
            print(f"  {insect_name} ({insect_id})")
    
    def check_specific_cases(self):
        """特定ケースの確認"""
        print(f"\n=== 特定ケース確認 ===")
        
        # アカキリバの確認
        akakilliba_id = 'catalog-4260'
        if akakilliba_id in self.insects:
            akakilliba_hostplants = [hp for hp in self.hostplants if hp['insect_id'] == akakilliba_id]
            print(f"アカキリバの食草数: {len(akakilliba_hostplants)}種")
            for hp in akakilliba_hostplants:
                family_info = f"({hp['plant_family']})" if hp['plant_family'] else ""
                print(f"  - {hp['plant_name']}{family_info}")
        
        # 総合備考のある昆虫例
        notes_insects = set(note['insect_id'] for note in self.general_notes)
        print(f"\n総合備考のある昆虫: {len(notes_insects)}種")
        
        for insect_id in list(notes_insects)[:3]:  # 上位3種の例
            insect_name = self.insects[insect_id]['japanese_name']
            notes = [note['content'][:50] + "..." for note in self.general_notes if note['insect_id'] == insect_id]
            print(f"  {insect_name}: {notes[0]}")
    
    def validate_conversion_accuracy(self):
        """変換精度の確認"""
        print(f"\n=== 変換精度確認 ===")
        
        # 科名抽出の確認
        family_patterns = defaultdict(int)
        for hp in self.hostplants:
            if hp['plant_family']:
                family_patterns[hp['plant_family']] += 1
        
        print(f"抽出された科名種類: {len(family_patterns)}")
        
        # よく出現する科名
        print(f"主要な科名:")
        for family, count in Counter(family_patterns).most_common(10):
            print(f"  {family}: {count}件")
    
    def run_all_validations(self):
        """全ての検証を実行"""
        print("=== 正規化データ検証開始 ===")
        
        self.load_data()
        
        integrity_ok = self.validate_referential_integrity()
        quality_ok = self.validate_data_quality()
        
        self.analyze_hostplant_distribution()
        self.check_specific_cases()
        self.validate_conversion_accuracy()
        
        print(f"\n=== 検証結果 ===")
        print(f"外部キー整合性: {'✅ OK' if integrity_ok else '❌ NG'}")
        print(f"データ品質: {'✅ OK' if quality_ok else '❌ NG'}")
        
        if integrity_ok and quality_ok:
            print(f"🎉 データ検証合格！正規化データは正常です。")
            return True
        else:
            print(f"⚠️  データに問題があります。修正が必要です。")
            return False

def main():
    validator = DataValidator('/Users/akimotohiroki/insects-host-plant-explorer/normalized_data')
    return validator.run_all_validations()

if __name__ == "__main__":
    main()