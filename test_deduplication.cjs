const fs = require('fs');
const Papa = require('papaparse');

// Simulate the deduplication logic
function cleanScientificNameForComparison(name) {
  if (!name) return '';
  return name.trim().replace(/\s+/g, ' ');
}

function testDeduplication() {
  // Read the main moth CSV
  const csvText = fs.readFileSync('public/ListMJ_hostplants_master.csv', 'utf8');
  const parsed = Papa.parse(csvText, { header: false });
  
  const moths = [];
  const header = parsed.data[0];
  
  // Process each row
  for (let i = 1; i < parsed.data.length; i++) {
    const row = parsed.data[i];
    if (row.length > 23) {
      const japaneseName = row[9] || '';
      const scientificName = row[23] || '';
      
      if (japaneseName) {
        moths.push({
          id: `moth-${i}`,
          name: japaneseName,
          scientificName: scientificName
        });
      }
    }
  }
  
  console.log(`Total moths before deduplication: ${moths.length}`);
  
  // Apply the new deduplication logic
  const uniqueMap = new Map();
  
  moths.forEach(moth => {
    const cleanScientificName = cleanScientificNameForComparison(moth.scientificName);
    const cleanJapaneseName = moth.name ? moth.name.trim() : '';
    
    // Determine if this has a complete species-level scientific name
    const hasSpeciesName = cleanScientificName && 
                           cleanScientificName.includes(' ') && 
                           !cleanScientificName.endsWith(' sp.') &&
                           !cleanScientificName.endsWith(' spp.');
    
    // Create unique key based on available information
    let uniqueKey;
    if (hasSpeciesName) {
      // If we have a full scientific name with species, use it as the primary key
      uniqueKey = cleanScientificName;
    } else if (cleanScientificName && cleanJapaneseName) {
      // For genus-only entries, combine scientific and Japanese names to make them unique
      uniqueKey = `${cleanScientificName}_${cleanJapaneseName}`;
    } else if (cleanJapaneseName) {
      // If only Japanese name exists, use it with ID to ensure uniqueness
      uniqueKey = `${cleanJapaneseName}_${moth.id}`;
    } else if (cleanScientificName) {
      // If only scientific name exists (genus-level), use it with ID
      uniqueKey = `${cleanScientificName}_${moth.id}`;
    } else {
      // Fallback to ID if nothing else is available
      uniqueKey = moth.id;
    }
    
    uniqueMap.set(uniqueKey, moth);
  });
  
  console.log(`Total unique moths after deduplication: ${uniqueMap.size}`);
  
  // Analyze the genus-only entries
  const genusOnlyEntries = [];
  const duplicateJapaneseNames = new Map();
  
  moths.forEach(moth => {
    const cleanScientificName = cleanScientificNameForComparison(moth.scientificName);
    const cleanJapaneseName = moth.name ? moth.name.trim() : '';
    
    if (!cleanScientificName || !cleanScientificName.includes(' ')) {
      genusOnlyEntries.push(moth);
    }
    
    if (!duplicateJapaneseNames.has(cleanJapaneseName)) {
      duplicateJapaneseNames.set(cleanJapaneseName, []);
    }
    duplicateJapaneseNames.get(cleanJapaneseName).push(moth);
  });
  
  console.log(`\nGenus-only entries: ${genusOnlyEntries.length}`);
  
  // Find Japanese names that appear multiple times
  const multipleOccurrences = [];
  duplicateJapaneseNames.forEach((moths, name) => {
    if (moths.length > 1) {
      multipleOccurrences.push({ name, count: moths.length });
    }
  });
  
  multipleOccurrences.sort((a, b) => b.count - a.count);
  
  console.log(`\nJapanese names appearing multiple times (top 10):`);
  multipleOccurrences.slice(0, 10).forEach(({ name, count }) => {
    console.log(`  ${name}: ${count} times`);
  });
  
  // Calculate expected vs actual
  console.log(`\n=== Summary ===`);
  console.log(`Moths in CSV: ${moths.length}`);
  console.log(`After deduplication: ${uniqueMap.size}`);
  console.log(`Removed as duplicates: ${moths.length - uniqueMap.size}`);
  
  // Add other insects
  const butterflies = 270;
  const beetles = 167;
  const leafbeetles = 668;
  
  const total = uniqueMap.size + butterflies + beetles + leafbeetles;
  console.log(`\nTotal with other insects:`);
  console.log(`  Moths: ${uniqueMap.size}`);
  console.log(`  Butterflies: ${butterflies}`);
  console.log(`  Beetles: ${beetles}`);
  console.log(`  Leafbeetles: ${leafbeetles}`);
  console.log(`  Expected total: ${total}`);
  console.log(`  Displayed: 7255`);
  console.log(`  Difference: ${total - 7255}`);
}

testDeduplication();