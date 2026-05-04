(function () {
  const KEY_SESSION = 'tapfo_onboarding_v2';
  const KEY_SKIPPED = 'tapfo_onboarding_skipped';
  const KEY_ROLE = 'tapfo_role_v2';
  const KEY_PROFILE = 'tapfo_active_profile_v2';

  function nowIso() {
    return new Date().toISOString();
  }

  function makeId() {
    return 'ob_' + Date.now() + '_' + Math.random().toString(16).slice(2, 8);
  }

  function defaultSession() {
    return {
      id: makeId(),
      startedAt: nowIso(),
      completedAt: null,
      role: null,
      stepsCompleted: [],
      profileData: {
        displayName: '',
        phone: '',
        avatar: null,
        location: null
      },
      businessData: {
        businessName: '',
        category: '',
        region: ''
      },
      designerData: {
        portfolio: null,
        specialty: '',
        commissionOptIn: false
      },
      featureTourCompleted: {
        search: false,
        notes: false,
        sums: false,
        trusted: false,
        location: false
      },
      skipped: false,
      version: 'v2'
    };
  }

  function parseJson(raw, fallback) {
    try {
      return raw ? JSON.parse(raw) : fallback;
    } catch (_) {
      return fallback;
    }
  }

  const FLOW_BY_ROLE = {
    browser: ['welcome', 'role', 'location', 'tour', 'done'],
    consumer: ['welcome', 'role', 'profile', 'location', 'tour', 'done'],
    business: ['welcome', 'role', 'profile', 'business', 'tour', 'done'],
    designer: ['welcome', 'role', 'profile', 'designer', 'tour', 'done'],
    staff: ['welcome', 'role', 'staff', 'done'],
    admin: ['welcome', 'role', 'admin', 'done']
  };

  const Onboarding = {
    keys: { KEY_SESSION, KEY_SKIPPED, KEY_ROLE, KEY_PROFILE },
    FLOW_BY_ROLE,

    getSession: function () {
      return parseJson(localStorage.getItem(KEY_SESSION), null);
    },

    saveSession: function (session) {
      localStorage.setItem(KEY_SESSION, JSON.stringify(session));
    },

    clearSession: function () {
      localStorage.removeItem(KEY_SESSION);
    },

    getOrCreateSession: function () {
      let session = this.getSession();
      if (!session || !session.id) {
        session = defaultSession();
        this.saveSession(session);
      }
      return session;
    },

    ensureRole: function (session) {
      if (!session.role) session.role = 'consumer';
      return session;
    },

    getFlow: function (session) {
      this.ensureRole(session);
      return FLOW_BY_ROLE[session.role] || FLOW_BY_ROLE.consumer;
    },

    markStepComplete: function (session, stepId) {
      if (!session.stepsCompleted.includes(stepId)) {
        session.stepsCompleted.push(stepId);
      }
      this.saveSession(session);
    },

    getResumeStepIndex: function (session) {
      const flow = this.getFlow(session);
      for (let i = 0; i < flow.length; i += 1) {
        if (!session.stepsCompleted.includes(flow[i])) return i;
      }
      return flow.length - 1;
    },

    isComplete: function () {
      const session = this.getSession();
      return !!(session && session.completedAt);
    },

    complete: function (session) {
      session.completedAt = nowIso();
      this.saveSession(session);
      localStorage.setItem(KEY_ROLE, session.role || 'consumer');
      localStorage.setItem(KEY_SKIPPED, session.skipped ? 'true' : 'false');
      localStorage.setItem(KEY_PROFILE, JSON.stringify({
        role: session.role || 'consumer',
        profileData: session.profileData,
        businessData: session.businessData,
        designerData: session.designerData,
        completedAt: session.completedAt
      }));
    },

    skip: function (session) {
      session.skipped = true;
      if (!session.role) session.role = 'browser';
      this.complete(session);
    },

    shouldResetFromQuery: function () {
      return new URLSearchParams(window.location.search).get('reset') === 'onboarding';
    },

    resetAll: function () {
      localStorage.removeItem(KEY_SESSION);
      localStorage.removeItem(KEY_SKIPPED);
      localStorage.removeItem(KEY_ROLE);
      localStorage.removeItem(KEY_PROFILE);
    }
  };

  window.TapFoOnboarding = Onboarding;
})();

