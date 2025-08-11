const fs = require('fs');
const Papa = require('papaparse');

// Test exact moth counting logic
function testMothCount() {
  // Read the main moth CSV
  const csvText = fs.readFileSync('public/ListMJ_hostplants_master.csv', 'utf8');
  const parsed = Papa.parse(csvText, { header: false });
  
  let totalRows = 0;
  let rowsWithJapaneseName = 0;
  let rowsWithoutJapaneseName = 0;
  const japaneseNames = new Set();
  const scientificNames = new Set();
  
  // Process each row (skip header)
  for (let i = 1; i < parsed.data.length; i++) {
    const row = parsed.data[i];
    if (row.length > 23) {
      totalRows++;
      const japaneseName = row[9] || '';
      const scientificName = row[23] || '';
      
      if (japaneseName && japaneseName.trim()) {
        rowsWithJapaneseName++;
        japaneseNames.add(japaneseName.trim());
      } else {
        rowsWithoutJapaneseName++;
        console.log(`Row ${i+1} missing Japanese name: ${scientificName}`);
      }
      
      if (scientificName && scientificName.trim()) {
        scientificNames.add(scientificName.trim());
      }
    }
  }
  
  console.log('\n=== Moth CSV Analysis ===');
  console.log(`Total data rows: ${totalRows}`);
  console.log(`Rows with Japanese name: ${rowsWithJapaneseName}`);
  console.log(`Rows without Japanese name: ${rowsWithoutJapaneseName}`);
  console.log(`Unique Japanese names: ${japaneseNames.size}`);
  console.log(`Unique scientific names: ${scientificNames.size}`);
  
  // Simulate what App.jsx does
  console.log('\n=== Expected in App ===');
  console.log(`Moths array length should be: ${rowsWithJapaneseName}`);
  
  // Other insects from the code
  const butterflies = 270;
  const beetles = 167;
  const leafbeetles = 668;
  
  const expectedTotal = rowsWithJapaneseName + butterflies + beetles + leafbeetles;
  console.log(`\n=== Total Expected ===`);
  console.log(`Moths: ${rowsWithJapaneseName}`);
  console.log(`Butterflies: ${butterflies}`);
  console.log(`Beetles: ${beetles}`);
  console.log(`Leafbeetles: ${leafbeetles}`);
  console.log(`Total: ${expectedTotal}`);
  console.log(`Currently displayed: 7255`);
  console.log(`Difference: ${expectedTotal - 7255}`);
}

testMothCount();