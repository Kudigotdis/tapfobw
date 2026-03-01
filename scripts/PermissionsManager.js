/**
 * PermissionsManager.js - TapFo Permissions Engine
 * Controls feature visibility and access based on user capabilities.
 */

const PermissionsManager = {
    // Mock data for profiles (to be synced with TAPFO_USER_PROFILES.md)
    // Maps simple types to default capabilities
    DEFAULT_CAPS: {
        'browser': [],
        'user': ['Player'],
        'business-unvalidated': ['Player'],
        'business-validated': ['Player', 'BusinessOwner'],
        'business-validated-senior': ['Player', 'BusinessOwner', 'Creator'],
        'designer': ['Player', 'Designer', 'Creator'],
        'designer-senior': ['Player', 'Designer', 'Creator', 'Admin'],
        'staff': ['Player', 'Staff', 'Admin'],
        'admin': ['Player', 'Staff', 'Admin', 'Root']
    },

    // Check if current account has a capability
    check: function (account, capability) {
        if (!account) return false;

        // 1. Check default caps for type
        const caps = this.DEFAULT_CAPS[account.type] || [];
        if (caps.includes(capability) || caps.includes('Root')) return true;

        // 2. Add specific logic for profile capabilities if present
        if (account.capabilities && account.capabilities.includes(capability)) return true;

        return false;
    },

    // Helper for UI visibility
    getVisibility: function (account, capability) {
        return this.check(account, capability) ? 'flex' : 'none';
    }
};

window.PermissionsManager = PermissionsManager;
