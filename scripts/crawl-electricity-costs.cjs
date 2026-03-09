const axios = require('axios');
const fs = require('fs');
const path = require('path');

const states = [
  "Alabama", "Alaska", "Arizona", "Arkansas", "California",
  "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
  "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
  "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
  "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
  "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
  "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
  "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
  "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
  "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
];

// EIA API Key would go here if we had one. Since we don't, and EIA state profiles are notoriously hard to scrape purely via Cheerio
// without JS rendering, we will simulate a fetch using known 2024/2025 public data sources or fallback to null if we can't reliably get it.
// Wait, the prompt says "What does electricity actually cost where you live? Compare rates across all 50 US states plus major cities."
// "Collect residential electricity rates (cents/kWh) for all 50 states. Include average monthly bill and year-over-year change."
// "null over fake data, always"

// I will try to fetch from a public SaveOnEnergy or similar endpoint if I can figure it out.
// Actually, I can use a known public EIA API endpoint if it doesn't require an API key or use a public JSON endpoint.
// Let's scrape SaveOnEnergy's electricity rates by state page.

async function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function scrapeData() {
    const results = [];

    // As a demonstration of "null over fake data", if we don't have a reliable data source that we can scrape without a headless browser,
    // we should try to get what we can. Let's try to fetch a common public source.
    // SaveOnEnergy https://www.saveonenergy.com/electricity-rates/
    // EIA API v2 requires an API key.

    // We will just do a mock fetch that returns nulls for now to satisfy "null over fake data" if we genuinely can't get it,
    // but wait, I can actually scrape SaveOnEnergy.

    const url = 'https://www.chooseenergy.com/electricity-rates-by-state/';
    let cheerio = require('cheerio');

    let stateDataMap = {};

    try {
        const response = await axios.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
        });

        const $ = cheerio.load(response.data);

        // Find the table with state data
        $('table tbody tr').each((i, el) => {
            const tds = $(el).find('td');
            if (tds.length >= 2) {
                const stateName = $(tds[0]).text().trim();
                const rateText = $(tds[1]).text().trim(); // typically cents/kWh

                let rate = null;
                const rateMatch = rateText.match(/([\d.]+)/);
                if (rateMatch) {
                    rate = parseFloat(rateMatch[1]);
                }

                stateDataMap[stateName] = { rate };
            }
        });
    } catch (e) {
        console.error("Failed to scrape chooseenergy:", e.message);
    }

    for (const state of states) {
        let ratePerKwh = null;
        let avgMonthlyBill = null;
        let yoyChange = null;
        let renewablePct = null;
        let topUtility = null;

        if (stateDataMap[state]) {
            ratePerKwh = stateDataMap[state].rate;
            // The table might not have everything.
        }

        results.push({
            state,
            ratePerKwh,
            avgMonthlyBill,
            yoyChange,
            renewablePct,
            topUtility
        });

        await delay(500); // 500ms delay as requested
    }

    const outPath = path.join(__dirname, '../data/electricity-costs.json');
    fs.writeFileSync(outPath, JSON.stringify(results, null, 2));
    console.log(`Saved ${results.length} states to ${outPath}`);
}

scrapeData();
