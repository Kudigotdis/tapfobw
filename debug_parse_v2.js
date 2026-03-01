const fs = require('fs');
const path = 'c:/Users/Kudzanai/Documents/2025/App Developments/TapFo/data/Directory_ Categories_V1.json';

try {
    const rawData = JSON.parse(fs.readFileSync(path, 'utf8'));
    const items = [];
    let currentSectionHeader = 'General';

    for (const entry of rawData) {
        const text = (entry.raw_text || '').trim();
        if (!text) continue;

        const isSeparator = text.includes('---');
        const isNote = text.includes('Architect’s Note') || text.includes('(Used In:');
        const isHeader = text.includes('Value (Internal Key)');

        if (!text.includes(',') && !isSeparator && !isNote && !isHeader && text.length < 100) {
            currentSectionHeader = text;
            continue;
        }

        if (text.includes(',') && !isNote && !isHeader) {
            const parts = text.split(',');
            if (parts.length >= 2) {
                const key = parts[0].trim();
                const display = parts[1].trim();
                if (!key || !display) continue;

                let mainCat = currentSectionHeader;
                if (parts[2]) {
                    const context = parts[2].trim();
                    if (context.includes(':')) {
                        mainCat = context.split(':')[0].trim();
                    }
                }

                items.push({ key, display, mainCat });
            }
        }
    }

    console.log(`Total categories found: ${items.length}`);
    const mainCats = [...new Set(items.map(i => i.mainCat))].sort();
    console.log(`Unique Main categories (${mainCats.length}):`);
    console.log(JSON.stringify(mainCats, null, 2));

    // Sample businesses matching
    const businesses = [
        { name: "A Team Shopfitters", sub: ["Shop Fitting", "Interior"] },
        { name: "American Express", sub: ["Finance"] }
    ];

    console.log('\nMatching simulation:');
    businesses.forEach(b => {
        const match = items.find(cat => {
            const cleanDisplay = cat.display.replace(/(\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f]|\ud83d[\ude80-\udeff]|[\u2600-\u26FF\u2700-\u27BF])\s*/, '').trim();
            return b.sub.some(s => s.toLowerCase().includes(cleanDisplay.toLowerCase()) || cleanDisplay.toLowerCase().includes(s.toLowerCase()));
        });
        console.log(`${b.name} matches: ${match ? match.display : 'NONE'}`);
    });

} catch (err) {
    console.error(err);
}
