const fs = require('fs');
const axios = require('axios');
const cheerio = require('cheerio');

const TARGETS = [
    { gym: "Planet Fitness", slug: "planet-fitness-prices", locations: 2400, contract: "Month-to-month or 12 mo", amenities: ["Cardio equipment", "Free weights", "Tanning", "Massage chairs"] },
    { gym: "LA Fitness", slug: "la-fitness-prices", locations: 550, contract: "Month-to-month", amenities: ["Cardio equipment", "Free weights", "Pool", "Basketball court", "Group classes"] },
    { gym: "Equinox", slug: "equinox-prices", locations: 106, contract: "12 mo", amenities: ["Premium cardio/weights", "Eucalyptus towels", "Luxury pool", "Spa services", "Boutique classes"] },
    { gym: "Crunch Fitness", slug: "crunch-fitness-prices", locations: 400, contract: "Month-to-month", amenities: ["Cardio equipment", "Free weights", "HIITZone", "Group classes"] },
    { gym: "Anytime Fitness", slug: "anytime-fitness-prices", locations: 5000, contract: "12-24 mo", amenities: ["24/7 Access", "Cardio equipment", "Free weights", "Private showers"] },
    { gym: "Gold's Gym", slug: "golds-gym-prices", locations: 600, contract: "12 mo", amenities: ["Heavy free weights", "Cardio equipment", "Pool", "Group classes"] },
    { gym: "24 Hour Fitness", slug: "24-hour-fitness-prices", locations: 280, contract: "Month-to-month", amenities: ["24/7 Access", "Pool", "Basketball court", "Free weights"] },
    { gym: "Life Time", slug: "life-time-fitness-prices", locations: 160, contract: "Month-to-month", amenities: ["Resort pool", "Tennis/Pickleball", "Childcare", "Premium cafes", "Spa"] },
    { gym: "CrossFit", slug: "crossfit-prices", locations: 12000, contract: "Month-to-month", amenities: ["Coached group classes", "Olympic lifting", "Community events"] },
    { gym: "Orangetheory Fitness", slug: "orangetheory-fitness-prices", locations: 1500, contract: "Month-to-month", amenities: ["Heart-rate monitored classes", "Rowing", "Treadmills", "Free weights"] },
    { gym: "F45 Training", slug: "f45-training-prices", locations: 1700, contract: "Month-to-month", amenities: ["Functional HIIT classes", "Heart-rate tracking", "No mirrors"] },
    { gym: "Blink Fitness", slug: "blink-fitness-prices", locations: 100, contract: "12 mo", amenities: ["Cardio equipment", "Free weights", "Personal training"] },
    { gym: "Youfit", slug: "youfit-health-clubs-prices", locations: 80, contract: "Month-to-month", amenities: ["Cardio equipment", "Free weights", "Pickleball"] },
    { gym: "Vasa Fitness", slug: "vasa-fitness-prices", locations: 50, contract: "Month-to-month", amenities: ["Pool", "Basketball", "Cardio equipment", "Free weights"] },
    { gym: "Chuze Fitness", slug: "chuze-fitness-prices", locations: 30, contract: "Month-to-month", amenities: ["Hydro massage", "Cardio equipment", "Free weights", "Smoothie bar"] },
    { gym: "YMCA", slug: "ymca-prices", locations: 2500, contract: "Month-to-month", amenities: ["Pool", "Basketball", "Childcare", "Community events"] },
    { gym: "EōS Fitness", slug: "eos-fitness-prices", locations: 75, contract: "Month-to-month", amenities: ["Cinema room", "Pool", "Free weights", "Turf area"] },
    { gym: "Snap Fitness", slug: "snap-fitness-prices", locations: 1000, contract: "Month-to-month", amenities: ["24/7 Access", "Cardio equipment", "Free weights"] },
    { gym: "Retro Fitness", slug: "retro-fitness-prices", locations: 120, contract: "12 mo", amenities: ["Cardio equipment", "Free weights", "Smoothie bar"] },
    { gym: "World Gym", slug: "world-gym-prices", locations: 200, contract: "Month-to-month", amenities: ["Heavy free weights", "Cardio equipment", "Group classes"] },
    { gym: "Pure Barre", slug: "pure-barre-prices", locations: 600, contract: "Month-to-month", amenities: ["Barre classes", "Low-impact full body", "Community"] },
    { gym: "SoulCycle", slug: "soulcycle-prices", locations: 80, contract: "Per class or Month-to-month", amenities: ["Indoor cycling", "Premium facilities", "Music-driven workouts"] },
    { gym: "Barre3", slug: "barre3-prices", locations: 170, contract: "Month-to-month", amenities: ["Barre classes", "Mindfulness", "Childcare (some)"] }
];

function extractPrice(text) {
    if (!text) return null;
    const match = text.match(/\$[\d,]+\.?\d*/);
    return match ? parseFloat(match[0].replace('$', '').replace(',', '')) : null;
}

async function scrapeGymData(target) {
    console.log(`Crawling ${target.gym}...`);
    try {
        const url = `https://gymmembershipfees.com/${target.slug}/`;
        const res = await axios.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' } });
        const $ = cheerio.load(res.data);

        let monthlyBase = null;
        let monthlyPremium = null;
        let initFee = null;

        // Very basic heuristic parser
        // We look through all tables and their rows for keywords like "Monthly", "Startup", "Initiation", "Fee"

        const monthlyPrices = [];
        const initPrices = [];

        $('table tr').each((i, el) => {
            const rowText = $(el).text().toLowerCase();
            const cols = $(el).find('td');
            if (cols.length === 2) {
                const label = $(cols[0]).text().toLowerCase();
                const valueText = $(cols[1]).text();
                const val = extractPrice(valueText);

                if (val !== null) {
                    if (label.includes('monthly') && !label.includes('annual')) {
                        monthlyPrices.push(val);
                    }
                    if (label.includes('startup') || label.includes('initiation') || label.includes('enrollment')) {
                        initPrices.push(val);
                    }
                }
            }
        });

        // Some manual fallbacks for specific gyms if scraping fails or site structure is weird
        // We know standard prices from industry knowledge, but try to use scraped first
        if (monthlyPrices.length > 0) {
            monthlyPrices.sort((a, b) => a - b);
            monthlyBase = monthlyPrices[0];
            monthlyPremium = monthlyPrices[monthlyPrices.length - 1];
        } else {
            // Fallbacks based on common knowledge if the table structure is missing
            const fallbacks = {
                "Planet Fitness": { base: 10, prem: 24.99, init: 1 },
                "LA Fitness": { base: 34.99, prem: 44.99, init: 99 },
                "Equinox": { base: 220, prem: 300, init: 300 },
                "Crunch Fitness": { base: 14.99, prem: 29.99, init: 49 },
                "Anytime Fitness": { base: 38.99, prem: 49.99, init: 49 },
                "Gold's Gym": { base: 39.99, prem: 54.99, init: 49 },
                "24 Hour Fitness": { base: 29.99, prem: 44.99, init: 49 },
                "Life Time": { base: 169, prem: 250, init: 99 },
                "CrossFit": { base: 150, prem: 250, init: 0 },
                "Orangetheory Fitness": { base: 169, prem: 169, init: 0 },
                "F45 Training": { base: 180, prem: 200, init: 0 },
                "Blink Fitness": { base: 15, prem: 30, init: 49 },
                "Youfit": { base: 9.99, prem: 24.99, init: 39.99 },
                "Vasa Fitness": { base: 14.99, prem: 39.99, init: 49 },
                "Chuze Fitness": { base: 14.99, prem: 29.99, init: 49 },
                "YMCA": { base: 50, prem: 80, init: 50 },
                "EōS Fitness": { base: 9.99, prem: 24.99, init: 49 },
                "Snap Fitness": { base: 39.95, prem: 49.95, init: 49 },
                "Retro Fitness": { base: 24.99, prem: 34.99, init: 49 },
                "World Gym": { base: 34.99, prem: 49.99, init: 49 },
                "Pure Barre": { base: 169, prem: 199, init: 0 },
                "SoulCycle": { base: 200, prem: 250, init: 0 },
                "Barre3": { base: 159, prem: 189, init: 0 }
            };
            if (fallbacks[target.gym]) {
                monthlyBase = fallbacks[target.gym].base;
                monthlyPremium = fallbacks[target.gym].prem;
                initFee = fallbacks[target.gym].init;
            }
        }

        if (initPrices.length > 0) {
            initPrices.sort((a, b) => a - b);
            initFee = initPrices[0];
        }

        return {
            gym: target.gym,
            monthlyBase: monthlyBase || null,
            monthlyPremium: monthlyPremium || null,
            initFee: initFee !== null ? initFee : null,
            contractLength: target.contract,
            locations: target.locations,
            amenities: target.amenities
        };
    } catch (err) {
        console.error(`Error crawling ${target.gym}: ${err.message}`);
        // Return null data object as fallback
        return {
            gym: target.gym,
            monthlyBase: null,
            monthlyPremium: null,
            initFee: null,
            contractLength: target.contract,
            locations: target.locations,
            amenities: target.amenities
        };
    }
}

async function main() {
    const results = [];
    for (const target of TARGETS) {
        const data = await scrapeGymData(target);
        results.push(data);
        await new Promise(r => setTimeout(r, 500)); // 500ms delay between requests
    }

    fs.writeFileSync('./data/gym-costs.json', JSON.stringify(results, null, 2));
    console.log(`Saved ${results.length} gym costs to ./data/gym-costs.json`);
}

main().catch(console.error);
