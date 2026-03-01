/**
 * TapFo History Tracker (Bothoflow Protocol)
 * Persists user interaction history to localStorage with a 88-item cap.
 * Part of the 3.5D Navigation Engine.
 */

const HistoryTracker = {
    MAX_ITEMS: 88,
    STORAGE_KEY: 'tapfo_history',

    /**
     * Log a new interaction
     * @param {string} pageId - The internal page ID
     * @param {string} label - The human-readable label
     * @param {object} meta - Optional metadata (bizId, promoId, etc)
     */
    log: function (pageId, label, meta = {}) {
        if (pageId === 'home' || pageId === 'history') return;

        let history = this.get();

        const entry = {
            pageId,
            label,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            isoDate: new Date().toISOString(),
            ...meta
        };

        // Enforce FIFO limit
        if (history.length >= this.MAX_ITEMS) {
            history.shift();
        }

        history.push(entry);
        this.save(history);

        console.log(`[History] Logged: ${label} (${pageId})`);
    },

    /**
     * Save history to localStorage
     */
    save: function (data) {
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(data));
    },

    /**
     * Retrieve history from localStorage
     */
    get: function () {
        try {
            return JSON.parse(localStorage.getItem(this.STORAGE_KEY)) || [];
        } catch (e) {
            return [];
        }
    },

    /**
     * Clear the history
     */
    clear: function () {
        localStorage.removeItem(this.STORAGE_KEY);
        console.log('[History] Cleared');
        return [];
    },

    /**
     * Calculate interaction insights
     */
    getInsights: function () {
        const history = this.get();
        if (history.length === 0) return null;

        const counts = {};
        history.forEach(h => {
            const key = h.label || h.pageId;
            counts[key] = (counts[key] || 0) + 1;
        });

        // Get top 3
        const sorted = Object.entries(counts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 3)
            .map(([label, count]) => ({ label, count }));

        return {
            topVisits: sorted,
            totalInteractions: history.length
        };
    }
};

window.HistoryTracker = HistoryTracker;
