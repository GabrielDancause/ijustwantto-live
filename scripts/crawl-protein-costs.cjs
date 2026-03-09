const fs = require('fs');
const path = require('path');

// Raw data based on US retail prices (average/realistic estimates for 2026) and USDA food database
const rawData = [
  { name: "Chicken Breast", category: "poultry", servingSize: "100g", proteinGrams: 31, caloriesPerServing: 165, priceUSD: 0.88, isPlantBased: false, prepRequired: "cooking required" },
  { name: "Chicken Thighs", category: "poultry", servingSize: "100g", proteinGrams: 24, caloriesPerServing: 209, priceUSD: 0.65, isPlantBased: false, prepRequired: "cooking required" },
  { name: "Whole Chicken", category: "poultry", servingSize: "100g", proteinGrams: 27, caloriesPerServing: 239, priceUSD: 0.45, isPlantBased: false, prepRequired: "cooking required" },
  { name: "Ground Beef (80/20)", category: "beef", servingSize: "100g", proteinGrams: 25, caloriesPerServing: 254, priceUSD: 1.10, isPlantBased: false, prepRequired: "cooking required" },
  { name: "Ground Beef (90/10)", category: "beef", servingSize: "100g", proteinGrams: 26, caloriesPerServing: 176, priceUSD: 1.45, isPlantBased: false, prepRequired: "cooking required" },
  { name: "Ground Turkey", category: "poultry", servingSize: "100g", proteinGrams: 27, caloriesPerServing: 149, priceUSD: 1.05, isPlantBased: false, prepRequired: "cooking required" },
  { name: "Pork Chops", category: "pork", servingSize: "100g", proteinGrams: 25, caloriesPerServing: 196, priceUSD: 0.95, isPlantBased: false, prepRequired: "cooking required" },
  { name: "Pork Tenderloin", category: "pork", servingSize: "100g", proteinGrams: 26, caloriesPerServing: 143, priceUSD: 1.25, isPlantBased: false, prepRequired: "cooking required" },
  { name: "Eggs", category: "eggs", servingSize: "1 large egg (50g)", proteinGrams: 6, caloriesPerServing: 72, priceUSD: 0.25, isPlantBased: false, prepRequired: "cooking required" },
  { name: "Egg Whites (Liquid)", category: "eggs", servingSize: "46g (3 tbsp)", proteinGrams: 5, caloriesPerServing: 25, priceUSD: 0.22, isPlantBased: false, prepRequired: "cooking required" },
  { name: "Canned Tuna (Water)", category: "seafood", servingSize: "1 can (142g)", proteinGrams: 29, caloriesPerServing: 130, priceUSD: 1.15, isPlantBased: false, prepRequired: "none" },
  { name: "Canned Salmon", category: "seafood", servingSize: "1 can (147g)", proteinGrams: 30, caloriesPerServing: 210, priceUSD: 2.80, isPlantBased: false, prepRequired: "none" },
  { name: "Tilapia", category: "seafood", servingSize: "100g", proteinGrams: 26, caloriesPerServing: 128, priceUSD: 0.90, isPlantBased: false, prepRequired: "cooking required" },
  { name: "Shrimp", category: "seafood", servingSize: "100g", proteinGrams: 24, caloriesPerServing: 99, priceUSD: 1.80, isPlantBased: false, prepRequired: "cooking required" },
  { name: "Tofu (Firm)", category: "legume", servingSize: "100g", proteinGrams: 17, caloriesPerServing: 144, priceUSD: 0.55, isPlantBased: true, prepRequired: "minimal" },
  { name: "Tempeh", category: "legume", servingSize: "100g", proteinGrams: 19, caloriesPerServing: 192, priceUSD: 0.95, isPlantBased: true, prepRequired: "minimal" },
  { name: "Black Beans (Canned)", category: "legume", servingSize: "1/2 cup (130g)", proteinGrams: 7, caloriesPerServing: 114, priceUSD: 0.40, isPlantBased: true, prepRequired: "none" },
  { name: "Black Beans (Dry)", category: "legume", servingSize: "1/4 cup dry (35g)", proteinGrams: 8, caloriesPerServing: 114, priceUSD: 0.15, isPlantBased: true, prepRequired: "cooking required" },
  { name: "Lentils (Dry)", category: "legume", servingSize: "1/4 cup dry (50g)", proteinGrams: 12, caloriesPerServing: 170, priceUSD: 0.18, isPlantBased: true, prepRequired: "cooking required" },
  { name: "Chickpeas (Canned)", category: "legume", servingSize: "1/2 cup (125g)", proteinGrams: 6, caloriesPerServing: 120, priceUSD: 0.45, isPlantBased: true, prepRequired: "none" },
  { name: "Peanut Butter", category: "legume", servingSize: "2 tbsp (32g)", proteinGrams: 8, caloriesPerServing: 190, priceUSD: 0.15, isPlantBased: true, prepRequired: "none" },
  { name: "Greek Yogurt (Nonfat)", category: "dairy", servingSize: "3/4 cup (170g)", proteinGrams: 17, caloriesPerServing: 100, priceUSD: 1.10, isPlantBased: false, prepRequired: "none" },
  { name: "Cottage Cheese (2%)", category: "dairy", servingSize: "1/2 cup (113g)", proteinGrams: 12, caloriesPerServing: 90, priceUSD: 0.85, isPlantBased: false, prepRequired: "none" },
  { name: "Milk (2%)", category: "dairy", servingSize: "1 cup (244g)", proteinGrams: 8, caloriesPerServing: 122, priceUSD: 0.25, isPlantBased: false, prepRequired: "none" },
  { name: "Whey Protein Powder", category: "supplement", servingSize: "1 scoop (30g)", proteinGrams: 24, caloriesPerServing: 120, priceUSD: 0.95, isPlantBased: false, prepRequired: "none" },
  { name: "Casein Protein Powder", category: "supplement", servingSize: "1 scoop (33g)", proteinGrams: 24, caloriesPerServing: 120, priceUSD: 1.25, isPlantBased: false, prepRequired: "none" },
  { name: "Edamame", category: "legume", servingSize: "1/2 cup (75g)", proteinGrams: 9, caloriesPerServing: 94, priceUSD: 0.65, isPlantBased: true, prepRequired: "minimal" },
  { name: "Quinoa", category: "other", servingSize: "1/4 cup dry (43g)", proteinGrams: 6, caloriesPerServing: 156, priceUSD: 0.55, isPlantBased: true, prepRequired: "cooking required" },
  { name: "Oats", category: "other", servingSize: "1/2 cup dry (40g)", proteinGrams: 5, caloriesPerServing: 150, priceUSD: 0.12, isPlantBased: true, prepRequired: "minimal" },
  { name: "Almonds", category: "other", servingSize: "1 oz (28g)", proteinGrams: 6, caloriesPerServing: 164, priceUSD: 0.50, isPlantBased: true, prepRequired: "none" },
  { name: "Cheese (Cheddar)", category: "dairy", servingSize: "1 oz (28g)", proteinGrams: 7, caloriesPerServing: 115, priceUSD: 0.35, isPlantBased: false, prepRequired: "none" },
  { name: "Turkey Breast Deli Meat", category: "poultry", servingSize: "2 oz (56g)", proteinGrams: 10, caloriesPerServing: 60, priceUSD: 0.95, isPlantBased: false, prepRequired: "none" },
  { name: "Beef Jerky", category: "beef", servingSize: "1 oz (28g)", proteinGrams: 9, caloriesPerServing: 80, priceUSD: 1.80, isPlantBased: false, prepRequired: "none" },
  { name: "Sardines (Oil)", category: "seafood", servingSize: "1 can (106g)", proteinGrams: 23, caloriesPerServing: 191, priceUSD: 1.25, isPlantBased: false, prepRequired: "none" },
  { name: "Protein Bars", category: "supplement", servingSize: "1 bar (60g)", proteinGrams: 20, caloriesPerServing: 200, priceUSD: 2.50, isPlantBased: false, prepRequired: "none" }
];

const processedData = rawData.map(item => {
  // Validate data
  if (item.proteinGrams < 1 || item.proteinGrams > 80) throw new Error(`Invalid proteinGrams for ${item.name}`);
  if (item.priceUSD < 0.05 || item.priceUSD > 15) throw new Error(`Invalid priceUSD for ${item.name}`);

  // Calculate proteinPerDollar
  let proteinPerDollar = item.proteinGrams / item.priceUSD;
  // Round to 1 decimal place
  proteinPerDollar = Math.round(proteinPerDollar * 10) / 10;

  if (proteinPerDollar < 1 || proteinPerDollar > 200) throw new Error(`Invalid proteinPerDollar for ${item.name}: ${proteinPerDollar}`);

  return {
    ...item,
    proteinPerDollar
  };
});

// Sort by protein per dollar descending
processedData.sort((a, b) => b.proteinPerDollar - a.proteinPerDollar);

const outPath = path.join(__dirname, '../data/protein-per-dollar.json');
fs.writeFileSync(outPath, JSON.stringify(processedData, null, 2));

console.log(`Successfully generated data for ${processedData.length} protein sources.`);
console.log(`Top source: ${processedData[0].name} (${processedData[0].proteinPerDollar}g/$1)`);
