/**
 * PulseUpdater.js - Bothoflow Protocol KPI Tracking
 * Tracks user interactions and updates internal KPIs (Offline-First)
 */

const PulseUpdater = {
    // Sync pulse to local storage for offline retrieval
    sync: function (key, data) {
        let pulseData = JSON.parse(localStorage.getItem('tapfo_pulse')) || {};
        if (!pulseData[key]) pulseData[key] = [];

        pulseData[key].push({
            timestamp: new Date().toISOString(),
            ...data
        });

        localStorage.setItem('tapfo_pulse', JSON.stringify(pulseData));
        console.log(`[Pulse] Logged ${key}:`, data);
    },

    // Track business visit
    logVisit: function (bizId, bizName) {
        this.sync('visits', { bizId, bizName });
    },

    // Track contact action (Phone, WhatsApp, FB)
    logContact: function (bizId, type) {
        this.sync('contacts', { bizId, type });
    },

    // Track sentiment (Trust/Favourite)
    logSentiment: function (bizId, action) {
        this.sync('sentiment', { bizId, action });
    },

    // Get current session stats
    getPulseStats: function () {
        return JSON.parse(localStorage.getItem('tapfo_pulse')) || {};
    }
};

window.PulseUpdater = PulseUpdater;
