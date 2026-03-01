const fs = require('fs');
const path = 'c:/Users/Kudzanai/Documents/2025/App Developments/TapFo/data/Directory_ Categories_V1.json';

try {
    const rawData = JSON.parse(fs.readFileSync(path, 'utf8'));
    const items = [];
    let currentMainCat = 'Other';

    for (const entry of rawData) {
        const text = entry.raw_text || '';

        // Detect section headers (they usually aren't comma separated and preceded/followed by separators)
        if (text.length > 0 && !text.includes(',') && !text.includes('---') && !text.includes('Architect’s Note') && !text.includes('(Used In:')) {
            // Potential Section Header
            currentMainCat = text.trim();
        }

        if (text.includes(',')) {
            const parts = text.split(',');
            if (parts.length >= 2) {
                const key = parts[0].trim();
                const display = parts[1].trim();

                if (key === 'Value (Internal Key)') continue;

                let mainCat = currentMainCat;
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

    console.log(`Total items parsed: ${items.length}`);
    console.log('Sample items (first 10):');
    console.log(JSON.stringify(items.slice(0, 10), null, 2));

    const mainCats = [...new Set(items.map(i => i.mainCat))];
    console.log(`Unique Main Categories (${mainCats.length}):`);
    console.log(mainCats.join(', '));

} catch (err) {
    console.error(err);
}
