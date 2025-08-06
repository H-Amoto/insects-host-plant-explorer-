# Legacy Hamushi Files

This directory contains the original hamushi and leafbeetle CSV files and previous versions that were consolidated and restructured.

## Files Moved Here (2025-08-05)

### Original Separate Files:
- `hamushi_species_integrated.csv` - 625 species from moth catalog database (28 columns)
- `hamushi_species.csv` - Duplicate of above file  
- `leafbeetle_hostplants.csv` - 119 species from handbook source (7 columns)
- `leafbeetle_hostplants_backup.csv` - Backup of handbook data
- `hamushi_species_integrated_before_cleanup.csv` - Pre-cleanup version

### Old Integrated Files (Replaced):
- `hamushi_integrated_master_old_10columns.csv` - First integration attempt (10 columns, 657 species)
- `public_hamushi_integrated_master_old_10columns.csv` - Public directory backup
- `hamushi_integrated_master_27columns.csv` - Second attempt without emergence time (27 columns, 670 species)
- `ListMJ_hostplants_master_27columns.csv` - Original ListMJ without emergence time (27 columns)

## Current Structure (With Emergence Time):
Both `hamushi_integrated_master.csv` and `ListMJ_hostplants_master.csv` format (30 columns):
- 大図鑑カタログNo,科名,科和名,亜科名,亜科和名,族名,族和名,亜族名,亜族和名,属名,亜属名,種小名,亜種小名,著者,公表年,類似種,和名,旧和名,別名,その他の和名,亜種範囲,標準図鑑ステータス,標準図鑑以後の変更,学名,食草,出典,備考,成虫出現時期,成虫出現時期出典,成虫出現時期備考

### Final Integration Result:
**ハムシファイル (670 unique species):**
- Quality A (handbook): 120 species  
- Quality B (catalog): 625 species
- Duplicates removed: 75 species
- Emergence time matches: 177 species

**ListMJファイル (6744 species):**
- Emergence time matches: 3 species (mostly キリガ moths)

### Data Sources:
- emergence_time_integrated.csv: 168 species (mostly leafbeetle handbook data)
- hamushi_species_integrated.csv: 177 species (catalog database data)
- Priority: handbook data > catalog database data

Both files now maintain identical structure and detailed taxonomic/temporal information.