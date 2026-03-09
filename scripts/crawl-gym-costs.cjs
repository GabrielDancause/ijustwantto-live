const fs = require('fs');
const path = require('path');
const https = require('https');
const cheerio = require('cheerio');

const DATA_FILE = path.join(__dirname, '../data/gym-costs.json');

// Helper to delay execution
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

// Helper to fetch HTML from a URL
const fetchHtml = (url) => {
    return new Promise((resolve, reject) => {
        https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
            if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
                // follow simple redirect
                return fetchHtml(res.headers.location).then(resolve).catch(reject);
            }
            let data = '';
            res.on('data', chunk => { data += chunk; });
            res.on('end', () => resolve(data));
        }).on('error', err => reject(err));
    });
};

const predefinedData = [
    {
        gym: "Equinox",
        monthlyBase: 220,
        monthlyPremium: 300,
        initFee: 100,
        contractLength: "12 months",
        locations: 107,
        amenities: ["Pool", "Sauna", "Steam Room", "Towel Service", "Premium Toiletries", "Classes", "Eucalyptus Towels"]
    },
    {
        gym: "CrossFit",
        monthlyBase: 150,
        monthlyPremium: 250,
        initFee: null,
        contractLength: "Month-to-month",
        locations: 12000,
        amenities: ["Group Coaching", "Olympic Weights", "Specialized Equipment", "Community Events"]
    },
    {
        gym: "F45 Training",
        monthlyBase: 169,
        monthlyPremium: 199,
        initFee: null,
        contractLength: "Month-to-month",
        locations: 1750,
        amenities: ["Group Coaching", "Heart Rate Tracking", "Towels"]
    },
    {
        gym: "Anytime Fitness",
        monthlyBase: 41,
        monthlyPremium: null,
        initFee: 49,
        contractLength: "12 months",
        locations: 5000,
        amenities: ["24/7 Access", "Global Access", "Basic Equipment", "Showers"]
    },
    {
        gym: "24 Hour Fitness",
        monthlyBase: 35,
        monthlyPremium: 55,
        initFee: 49,
        contractLength: "Month-to-month",
        locations: 280,
        amenities: ["24/7 Access", "Pool", "Classes", "Basketball", "Sauna"]
    },
    {
        gym: "Gold's Gym",
        monthlyBase: 30,
        monthlyPremium: 40,
        initFee: 49,
        contractLength: "12 months",
        locations: 600,
        amenities: ["Heavy Weights", "Classes", "Cardio Cinema", "Pool"]
    },
    {
        gym: "Crunch Fitness",
        monthlyBase: 10,
        monthlyPremium: 25,
        initFee: 49,
        contractLength: "Month-to-month",
        locations: 400,
        amenities: ["Classes", "Tanning", "Hydromassage", "Guest Privileges"]
    },
    {
        gym: "YMCA",
        monthlyBase: 50,
        monthlyPremium: 75,
        initFee: 50,
        contractLength: "Month-to-month",
        locations: 2600,
        amenities: ["Pool", "Classes", "Childcare", "Basketball", "Community Events"]
    },
    {
        gym: "Orangetheory Fitness",
        monthlyBase: 159,
        monthlyPremium: 199,
        initFee: null,
        contractLength: "Month-to-month",
        locations: 1500,
        amenities: ["Heart Rate Monitored Training", "Coaches", "Towels"]
    },
    {
        gym: "Life Time",
        monthlyBase: 129,
        monthlyPremium: 249,
        initFee: 0,
        contractLength: "Month-to-month",
        locations: 160,
        amenities: ["Pools (Indoor/Outdoor)", "Tennis", "Spa", "Cafe", "Premium Childcare", "Classes"]
    },
    {
        gym: "Snap Fitness",
        monthlyBase: 40,
        monthlyPremium: null,
        initFee: 49,
        contractLength: "Month-to-month",
        locations: 1000,
        amenities: ["24/7 Access", "Global Access", "Myzone Integration"]
    },
    {
        gym: "Retro Fitness",
        monthlyBase: 20,
        monthlyPremium: 30,
        initFee: 99,
        contractLength: "12 months",
        locations: 120,
        amenities: ["Cardio Movie Theater", "Classes", "Tanning", "Smoothie Bar"]
    },
    {
        gym: "Blink Fitness",
        monthlyBase: 15,
        monthlyPremium: 30,
        initFee: 49,
        contractLength: "12 months",
        locations: 100,
        amenities: ["Clean Facilities", "Guest Privileges", "Basic Equipment"]
    },
    {
        gym: "World Gym",
        monthlyBase: 25,
        monthlyPremium: 45,
        initFee: 49,
        contractLength: "12 months",
        locations: 200,
        amenities: ["Heavy Weights", "Classes", "Barbell Club"]
    },
    {
        gym: "Vasa Fitness",
        monthlyBase: 10,
        monthlyPremium: 25,
        initFee: 49,
        contractLength: "Month-to-month",
        locations: 50,
        amenities: ["Pool", "Classes", "Childcare", "Basketball", "Massage"]
    },
    {
        gym: "EōS Fitness",
        monthlyBase: 10,
        monthlyPremium: 25,
        initFee: 49,
        contractLength: "Month-to-month",
        locations: 125,
        amenities: ["Pool", "Classes", "Turf Area", "Recovery Room"]
    },
    {
        gym: "Chuze Fitness",
        monthlyBase: 10,
        monthlyPremium: 22,
        initFee: 49,
        contractLength: "Month-to-month",
        locations: 30,
        amenities: ["Pool", "Classes", "Childcare", "Hydromassage"]
    },
    {
        gym: "Fit For Less",
        monthlyBase: 15,
        monthlyPremium: 25,
        initFee: 44,
        contractLength: "12 months",
        locations: 100,
        amenities: ["Basic Equipment", "Guest Privileges"]
    }
];

async function main() {
    console.log("Starting crawler...");
    let scrapedData = [];

    try {
        console.log("Fetching Planet Fitness data...");
        const pfHtml = await fetchHtml("https://gymmembershipfees.com/planet-fitness-prices/");
        const $pf = cheerio.load(pfHtml);

        let pfBase = null;
        let pfPremium = null;
        let pfInit = null;

        $pf('table tr').each((i, row) => {
            const text = $pf(row).text().replace(/\s+/g, ' ').trim();
            if (text.includes('Monthly Dues (One Person) (Classic)')) {
                const match = text.match(/\$(\d+\.\d+)/);
                if (match) pfBase = parseFloat(match[1]);
            }
            if (text.includes('Monthly Dues (One Person) (PF Black Card)')) {
                const match = text.match(/\$(\d+\.\d+)/);
                if (match) pfPremium = parseFloat(match[1]);
            }
            if (text.includes('Startup Fee (One Person) (Classic)')) {
                const match = text.match(/\$(\d+\.\d+)/);
                if (match) pfInit = parseFloat(match[1]);
            }
        });

        if (pfBase || pfPremium) {
            scrapedData.push({
                gym: "Planet Fitness",
                monthlyBase: pfBase || 10,
                monthlyPremium: pfPremium || 25,
                initFee: pfInit || 1,
                contractLength: "Month-to-month",
                locations: 2400,
                amenities: ["Tanning", "Massage Chairs", "Guest Privileges", "No Judgement Zone"]
            });
            console.log("Parsed Planet Fitness successfully");
        } else {
            console.log("Failed to parse Planet Fitness, using default");
            scrapedData.push({
                gym: "Planet Fitness",
                monthlyBase: 10,
                monthlyPremium: 24.99,
                initFee: 1,
                contractLength: "Month-to-month",
                locations: 2400,
                amenities: ["Tanning", "Massage Chairs", "Guest Privileges", "No Judgement Zone"]
            });
        }

    } catch (err) {
        console.error("Error fetching Planet Fitness:", err.message);
        scrapedData.push({
            gym: "Planet Fitness",
            monthlyBase: 10,
            monthlyPremium: 24.99,
            initFee: 1,
            contractLength: "Month-to-month",
            locations: 2400,
            amenities: ["Tanning", "Massage Chairs", "Guest Privileges", "No Judgement Zone"]
        });
    }

    await delay(500);

    try {
        console.log("Fetching LA Fitness data...");
        const laHtml = await fetchHtml("https://gymmembershipfees.com/la-fitness-prices/");
        const $la = cheerio.load(laHtml);

        let laBase = null;
        let laPremium = null;
        let laInit = null;

        $la('table tr').each((i, row) => {
            const text = $la(row).text().replace(/\s+/g, ' ').trim();
            if (text.includes('Monthly Fee (One Person) (Single Club)')) {
                const match = text.match(/\$(\d+\.\d+)/);
                if (match && !laBase) laBase = parseFloat(match[1]);
            }
            if (text.includes('Monthly Fee (1 Person) (Multi Club)')) {
                const match = text.match(/\$(\d+\.\d+)/);
                if (match && !laPremium) laPremium = parseFloat(match[1]);
            }
            if (text.includes('Initiation Fee (One Person) (Single Club)')) {
                const match = text.match(/\$(\d+\.\d+)/);
                if (match && laInit === null) laInit = parseFloat(match[1]);
            }
        });

        if (laBase || laPremium) {
            scrapedData.push({
                gym: "LA Fitness",
                monthlyBase: laBase || 34.99,
                monthlyPremium: laPremium || 49.99,
                initFee: laInit || 99,
                contractLength: "6 Month Term",
                locations: 700,
                amenities: ["Pool", "Basketball", "Racquetball", "Classes", "Sauna"]
            });
            console.log("Parsed LA Fitness successfully");
        } else {
             console.log("Failed to parse LA Fitness, using default");
             scrapedData.push({
                gym: "LA Fitness",
                monthlyBase: 34.99,
                monthlyPremium: 49.99,
                initFee: 99,
                contractLength: "6 Month Term",
                locations: 700,
                amenities: ["Pool", "Basketball", "Racquetball", "Classes", "Sauna"]
            });
        }
    } catch (err) {
        console.error("Error fetching LA Fitness:", err.message);
        scrapedData.push({
            gym: "LA Fitness",
            monthlyBase: 34.99,
            monthlyPremium: 49.99,
            initFee: 99,
            contractLength: "6 Month Term",
            locations: 700,
            amenities: ["Pool", "Basketball", "Racquetball", "Classes", "Sauna"]
        });
    }

    const finalData = [...scrapedData, ...predefinedData];

    fs.mkdirSync(path.dirname(DATA_FILE), { recursive: true });
    fs.writeFileSync(DATA_FILE, JSON.stringify(finalData, null, 2));

    console.log(`Saved ${finalData.length} gym records to ${DATA_FILE}`);
}

main().catch(console.error);
