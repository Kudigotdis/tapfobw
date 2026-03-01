/**
 * Commission_Engine.js - Bothoflow Economy Logic
 * Handles 0.5% base triggers and Designer commission tracking.
 */

const CommissionEngine = {
    BASE_RATE: 0.005, // 0.5%
    DESIGNER_RATE: 0.20, // 20%

    // Calculate base commission for an interaction
    calculateTrigger: function (value) {
        return (value * this.BASE_RATE).toFixed(4);
    },

    // Calculate designer cut
    calculateDesignerCut: function (value) {
        return (value * this.DESIGNER_RATE).toFixed(2);
    },

    // Process a commission event
    processEvent: function (type, bizId, value = 0) {
        const commission = this.calculateTrigger(value);
        console.log(`[Commission] Triggered ${type} for Biz ${bizId}. System Fee: ${commission}`);

        if (window.PulseUpdater) {
            window.PulseUpdater.sync('commissions', { type, bizId, commission, value });
        }

        return commission;
    }
};

window.CommissionEngine = CommissionEngine;
