# Cleanup Report Sample

Generated: 2025-08-08T12:00:00Z

## Statistics
- Total files analyzed: 1,234
- CSV files: 45
- Image files: 594
- Test/sample files: 23

## Files to Delete (Noise)
Count: 12
```
.DS_Store (Noise file (OS/build artifact))
public/.DS_Store (Noise file (OS/build artifact))
dist/.DS_Store (Noise file (OS/build artifact))
src/.DS_Store (Noise file (OS/build artifact))
.__MACOSX/image1.jpg (Noise file (OS/build artifact))
.__MACOSX/data.csv (Noise file (OS/build artifact))
app.css.map (Noise file (OS/build artifact))
bundle.js.map (Noise file (OS/build artifact))
vendor.js.map (Noise file (OS/build artifact))
styles.css.map (Noise file (OS/build artifact))
main.js.map (Noise file (OS/build artifact))
component.js.map (Noise file (OS/build artifact))
```

## Files to Archive

### Data Archive (CSV versions)
Count: 18
```
ListMJ_hostplants_master_final.csv
ListMJ_hostplants_master_fixed.csv
ListMJ_hostplants_master_corrected.csv
hamushi_integrated_master.csv
hamushi_species_integrated.csv
leafbeetle_hostplants_fixed.csv
日本のキリガ_fixed.csv
日本のキリガ_corrected.csv
日本のハマキガ1_fixed.csv
butterfly_host_final.csv
... and 8 more
```

### Misc Archive (test/sample files)
Count: 15
```
test-emergence.html
test-fuyushaku.cjs
test-fuyushaku.js
test-single-line.cjs
test-yakushima.html
icon-test.html
icon-test2.html
icon-test3.html
debug-parse.cjs
debug_csv_columns.py
sample-data.csv
trial-import.js
sandbox.html
temp-analysis.py
butterfly_test.csv
```

## Images

### Large Images (>2MB)
Count: 8
```
dist/images/insects/large_beetle_1.jpg (3.45 MB)
dist/images/insects/large_moth_2.jpg (2.87 MB)
dist/images/plants/oak_tree.jpg (4.12 MB)
public/images/banner_original.jpg (5.23 MB)
assets/hero_image.jpg (2.34 MB)
images/gallery/photo_001.jpg (2.98 MB)
images/gallery/photo_002.jpg (3.21 MB)
images/gallery/photo_003.jpg (2.45 MB)
```

### Images to Move to Originals
Count: 156
```
dist/images/insects/Abryna_regispetri.jpg
dist/images/insects/Acalolepta_fraudatrix.jpg
dist/images/insects/Acalolepta_luxuriosa.jpg
dist/images/insects/Agapanthia_daurica.jpg
dist/images/insects/Agnia_femorata.jpg
dist/images/insects/Alampyris_fumosa.jpg
dist/images/insects/Altica_lythri.jpg
dist/images/insects/Amphitrogia_amphidecta.jpg
dist/images/insects/Anoplophora_chinensis.jpg
dist/images/insects/Anoplophora_glabripennis.jpg
... and 146 more
```

## Summary

このレポートは、リポジトリクリーンアップツールによって生成されたサンプルです。実際の実行時には、以下の処理が行われます：

1. **ノイズファイルの削除**: OSやビルドツールが生成した不要ファイルを削除
2. **CSVアーカイブ**: 世代違いのCSVファイルを `/data/archive/` に移動
3. **テストファイルアーカイブ**: テスト・サンプルファイルを `/misc/archive/` に移動
4. **画像の整理**: 元画像を `/images/originals/` に移動し、最適化準備

実行後は、リポジトリがよりクリーンで管理しやすい状態になります。