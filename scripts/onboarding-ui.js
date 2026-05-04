(function () {
  const O = window.TapFoOnboarding;
  if (!O) return;

  if (O.shouldResetFromQuery()) O.resetAll();

  let session = O.getOrCreateSession();
  session = O.ensureRole(session);
  O.saveSession(session);

  const screenEl = document.getElementById('ob-screen');
  const statusEl = document.getElementById('ob-status');
  const progressEl = document.getElementById('ob-progress');
  const backBtn = document.getElementById('ob-back-btn');
  const nextBtn = document.getElementById('ob-next-btn');
  const skipBtn = document.getElementById('ob-skip-btn');

  let currentFlow = O.getFlow(session);
  let currentStepIndex = O.getResumeStepIndex(session);

  function optionsFromLocations() {
    const locations = (window.BIZ_DATABASE && window.BIZ_DATABASE.locations) || {};
    return Object.keys(locations);
  }

  function getAreasForCity(city) {
    const locations = (window.BIZ_DATABASE && window.BIZ_DATABASE.locations) || {};
    return locations[city] || ['All Areas'];
  }

  function normalizePhone(value) {
    const v = (value || '').replace(/\s+/g, '');
    if (!v) return '';
    if (v.startsWith('+267')) return v;
    if (v.startsWith('267')) return '+' + v;
    if (v.startsWith('0')) return '+267' + v.slice(1);
    return v;
  }

  function roleLabel(role) {
    const labels = {
      browser: 'Guest Browser',
      consumer: 'Consumer',
      business: 'Business Owner',
      designer: 'Designer',
      staff: 'Staff',
      admin: 'Admin'
    };
    return labels[role] || role;
  }

  function setStatus(text) {
    statusEl.textContent = text || '';
  }

  function renderProgress() {
    const pct = ((currentStepIndex + 1) / currentFlow.length) * 100;
    progressEl.style.width = Math.max(4, Math.min(100, pct)) + '%';
    setStatus(`Step ${currentStepIndex + 1} of ${currentFlow.length} - ${roleLabel(session.role)}`);
  }

  function updateNavButtons() {
    backBtn.disabled = currentStepIndex <= 0;
    nextBtn.textContent = currentFlow[currentStepIndex] === 'done' ? 'Finish' : 'Next';
  }

  function save() {
    O.saveSession(session);
  }

  function renderWelcome() {
    screenEl.innerHTML = `
      <h1>Welcome to TapFo</h1>
      <p>Discover Botswana businesses faster, even with low connectivity.</p>
      <div class="hint">Setup takes under 3 minutes.</div>
    `;
  }

  function renderRole() {
    const role = session.role || 'consumer';
    screenEl.innerHTML = `
      <h2>Choose your path</h2>
      <div class="stack">
        <button class="role-btn ${role === 'browser' ? 'active' : ''}" data-role="browser">Browse only (Guest)</button>
        <button class="role-btn ${role === 'consumer' ? 'active' : ''}" data-role="consumer">I want to find businesses</button>
        <button class="role-btn ${role === 'business' ? 'active' : ''}" data-role="business">I own/manage a business</button>
        <button class="role-btn ${role === 'designer' ? 'active' : ''}" data-role="designer">I am a designer</button>
        <button class="role-btn ${role === 'staff' ? 'active' : ''}" data-role="staff">TapFo Staff</button>
        <button class="role-btn ${role === 'admin' ? 'active' : ''}" data-role="admin">TapFo Admin</button>
      </div>
    `;
    screenEl.querySelectorAll('.role-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        session.role = btn.dataset.role;
        currentFlow = O.getFlow(session);
        currentStepIndex = 1;
        save();
        render();
      });
    });
  }

  function renderProfile() {
    const p = session.profileData;
    const locations = optionsFromLocations();
    const locationOptions = locations.map(l => `<option value="${l}" ${p.location === l ? 'selected' : ''}>${l}</option>`).join('');
    screenEl.innerHTML = `
      <h2>About you</h2>
      <div class="stack">
        <div>
          <label for="ob-name">Display Name *</label>
          <input id="ob-name" maxlength="60" value="${p.displayName || ''}" />
          <div class="error hidden" id="ob-err-name">Display name is required (min 2 chars).</div>
        </div>
        <div>
          <label for="ob-phone">Phone (optional)</label>
          <input id="ob-phone" placeholder="+267..." value="${p.phone || ''}" />
        </div>
        <div>
          <label for="ob-region">Region *</label>
          <select id="ob-region">
            <option value="">Select region</option>
            ${locationOptions}
          </select>
          <div class="error hidden" id="ob-err-region">Please select a region.</div>
        </div>
      </div>
    `;
  }

  function renderLocation() {
    const locations = optionsFromLocations();
    const city = session.profileData.location || locations[0] || 'Gaborone';
    const areas = getAreasForCity(city);
    const areaCurrent = session.profileData.area || 'All Areas';

    const cityOptions = locations.map(c => `<option value="${c}" ${c === city ? 'selected' : ''}>${c}</option>`).join('');
    const areaOptions = areas.map(a => `<option value="${a}" ${a === areaCurrent ? 'selected' : ''}>${a}</option>`).join('');

    screenEl.innerHTML = `
      <h2>Set location</h2>
      <p>Used to personalize business and promo results.</p>
      <div class="stack">
        <div>
          <label for="ob-city">City / Town *</label>
          <select id="ob-city">${cityOptions}</select>
        </div>
        <div>
          <label for="ob-area">Area / Neighbourhood</label>
          <select id="ob-area">${areaOptions}</select>
        </div>
      </div>
    `;

    const cityEl = document.getElementById('ob-city');
    cityEl.addEventListener('change', function () {
      const nextAreas = getAreasForCity(cityEl.value);
      const areaEl = document.getElementById('ob-area');
      areaEl.innerHTML = nextAreas.map(a => `<option value="${a}">${a}</option>`).join('');
    });
  }

  function renderBusiness() {
    const b = session.businessData;
    const locations = optionsFromLocations();
    const locOptions = locations.map(l => `<option value="${l}" ${b.region === l ? 'selected' : ''}>${l}</option>`).join('');
    screenEl.innerHTML = `
      <h2>Your business</h2>
      <div class="stack">
        <div>
          <label for="ob-biz-name">Business Name *</label>
          <input id="ob-biz-name" maxlength="100" value="${b.businessName || ''}" />
          <div class="error hidden" id="ob-err-biz-name">Business name is required.</div>
        </div>
        <div>
          <label for="ob-biz-cat">Category *</label>
          <input id="ob-biz-cat" maxlength="80" placeholder="e.g. Groceries, Finance" value="${b.category || ''}" />
          <div class="error hidden" id="ob-err-biz-cat">Category is required.</div>
        </div>
        <div>
          <label for="ob-biz-region">Region *</label>
          <select id="ob-biz-region">
            <option value="">Select region</option>
            ${locOptions}
          </select>
          <div class="error hidden" id="ob-err-biz-region">Region is required.</div>
        </div>
      </div>
    `;
  }

  function renderDesigner() {
    const d = session.designerData;
    screenEl.innerHTML = `
      <h2>Designer setup</h2>
      <div class="stack">
        <div>
          <label for="ob-specialty">Specialty *</label>
          <select id="ob-specialty">
            <option value="">Select specialty</option>
            ${['Logo', 'Brand', 'UI/UX', 'Print', 'Packaging', 'Other']
              .map(s => `<option value="${s}" ${d.specialty === s ? 'selected' : ''}>${s}</option>`).join('')}
          </select>
          <div class="error hidden" id="ob-err-specialty">Specialty is required.</div>
        </div>
        <div>
          <label for="ob-portfolio">Portfolio URL (optional)</label>
          <input id="ob-portfolio" placeholder="https://..." value="${d.portfolio || ''}" />
        </div>
        <div>
          <label><input type="checkbox" id="ob-commission-optin" ${d.commissionOptIn ? 'checked' : ''}> I agree to designer commission terms *</label>
          <div class="error hidden" id="ob-err-optin">You must agree before continuing.</div>
        </div>
      </div>
    `;
  }

  function renderTour() {
    screenEl.innerHTML = `
      <h2>Quick feature tour</h2>
      <div class="stack">
        <button class="choice-btn" data-ft="search">Search and discover businesses</button>
        <button class="choice-btn" data-ft="location">City and area personalization</button>
        <button class="choice-btn" data-ft="trusted">Trusted list and fast re-access</button>
        <button class="choice-btn" data-ft="notes">Notes and tracked items</button>
        <button class="choice-btn" data-ft="sums">Sums and grouped insights</button>
      </div>
      <div class="hint">Tap each item once to mark as seen.</div>
    `;
    screenEl.querySelectorAll('.choice-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        const key = btn.dataset.ft;
        session.featureTourCompleted[key] = true;
        btn.classList.add('active');
        save();
      });
    });
  }

  function renderStaff() {
    screenEl.innerHTML = `
      <h2>Staff onboarding</h2>
      <p>You will receive staff capabilities and operational views after completion.</p>
      <div class="hint">Use this flow only for authorized TapFo staff.</div>
    `;
  }

  function renderAdmin() {
    screenEl.innerHTML = `
      <h2>Admin onboarding</h2>
      <p>Admin mode enables high-impact controls. Proceed only with authorization.</p>
      <div class="hint">All admin actions should be auditable.</div>
    `;
  }

  function renderDone() {
    screenEl.innerHTML = `
      <h2>You're ready</h2>
      <p>Your setup is complete. We will open TapFo now with your selected role.</p>
      <div class="hint">Role: ${roleLabel(session.role)}</div>
    `;
  }

  function render() {
    const step = currentFlow[currentStepIndex];
    renderProgress();
    updateNavButtons();
    if (step === 'welcome') return renderWelcome();
    if (step === 'role') return renderRole();
    if (step === 'profile') return renderProfile();
    if (step === 'location') return renderLocation();
    if (step === 'business') return renderBusiness();
    if (step === 'designer') return renderDesigner();
    if (step === 'tour') return renderTour();
    if (step === 'staff') return renderStaff();
    if (step === 'admin') return renderAdmin();
    return renderDone();
  }

  function validateCurrentStep() {
    const step = currentFlow[currentStepIndex];

    if (step === 'profile') {
      const nameEl = document.getElementById('ob-name');
      const phoneEl = document.getElementById('ob-phone');
      const regionEl = document.getElementById('ob-region');
      const errName = document.getElementById('ob-err-name');
      const errRegion = document.getElementById('ob-err-region');

      const name = (nameEl.value || '').trim();
      const region = regionEl.value;
      const okName = name.length >= 2;
      const okRegion = !!region;

      errName.classList.toggle('hidden', okName);
      errRegion.classList.toggle('hidden', okRegion);
      if (!okName || !okRegion) return false;

      session.profileData.displayName = name;
      session.profileData.phone = normalizePhone(phoneEl.value || '');
      session.profileData.location = region;
      save();
      return true;
    }

    if (step === 'location') {
      const cityEl = document.getElementById('ob-city');
      const areaEl = document.getElementById('ob-area');
      session.profileData.location = cityEl.value;
      session.profileData.area = areaEl.value || 'All Areas';
      save();
      return true;
    }

    if (step === 'business') {
      const nameEl = document.getElementById('ob-biz-name');
      const catEl = document.getElementById('ob-biz-cat');
      const regionEl = document.getElementById('ob-biz-region');

      const errName = document.getElementById('ob-err-biz-name');
      const errCat = document.getElementById('ob-err-biz-cat');
      const errRegion = document.getElementById('ob-err-biz-region');

      const okName = (nameEl.value || '').trim().length > 0;
      const okCat = (catEl.value || '').trim().length > 0;
      const okRegion = !!regionEl.value;

      errName.classList.toggle('hidden', okName);
      errCat.classList.toggle('hidden', okCat);
      errRegion.classList.toggle('hidden', okRegion);
      if (!okName || !okCat || !okRegion) return false;

      session.businessData.businessName = nameEl.value.trim();
      session.businessData.category = catEl.value.trim();
      session.businessData.region = regionEl.value;
      save();
      return true;
    }

    if (step === 'designer') {
      const specialtyEl = document.getElementById('ob-specialty');
      const portfolioEl = document.getElementById('ob-portfolio');
      const optInEl = document.getElementById('ob-commission-optin');
      const errSpecialty = document.getElementById('ob-err-specialty');
      const errOptIn = document.getElementById('ob-err-optin');

      const okSpecialty = !!specialtyEl.value;
      const okOptIn = !!optInEl.checked;

      errSpecialty.classList.toggle('hidden', okSpecialty);
      errOptIn.classList.toggle('hidden', okOptIn);
      if (!okSpecialty || !okOptIn) return false;

      session.designerData.specialty = specialtyEl.value;
      session.designerData.portfolio = (portfolioEl.value || '').trim() || null;
      session.designerData.commissionOptIn = true;
      save();
      return true;
    }

    return true;
  }

  function completeAndExit() {
    O.complete(session);
    try {
      if (window.PulseUpdater && typeof window.PulseUpdater.logSentiment === 'function') {
        window.PulseUpdater.logSentiment('onboarding_complete');
      }
    } catch (_) {}
    window.location.href = 'index.html';
  }

  backBtn.addEventListener('click', function () {
    if (currentStepIndex <= 0) return;
    currentStepIndex -= 1;
    render();
  });

  nextBtn.addEventListener('click', function () {
    if (!validateCurrentStep()) return;

    const step = currentFlow[currentStepIndex];
    O.markStepComplete(session, step);

    if (step === 'role') {
      currentFlow = O.getFlow(session);
    }

    if (currentStepIndex >= currentFlow.length - 1) {
      return completeAndExit();
    }

    currentStepIndex += 1;
    render();
  });

  skipBtn.addEventListener('click', function () {
    session.skipped = true;
    if (!session.role) session.role = 'browser';
    O.skip(session);
    window.location.href = 'index.html';
  });

  render();
})();

