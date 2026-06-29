/* =============================================
   Blinx Generator — Frontend Logic
   ============================================= */

'use strict';

// ─── State ──────────────────────────────────────────────────────────────────
const state = {
  accounts: [],
  filter: 'all',
  search: '',
  activeSession: null,
  pollInterval: null,
  elapsedTimer: null,
  elapsedSec: 0,
  selectedRegion: 'ID',
  generating: false
};

// ─── DOM refs ────────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const loginScreen   = $('loginScreen');
const dashboard     = $('dashboard');
const loginForm     = $('loginForm');
const loginError    = $('loginError');
const loginBtn      = $('loginBtn');
const logoutBtn     = $('logoutBtn');
const adminPassword = $('adminPassword');
const togglePass    = $('togglePass');
const generateForm  = $('generateForm');
const generateBtn   = $('generateBtn');
const generateLoader= $('generateLoader');
const generateBtnText = $('generateBtnText');
const regionGrid    = $('regionGrid');
const selectedRegionDisplay = $('selectedRegionDisplay');
const accountCount  = $('accountCount');
const namePrefix    = $('namePrefix');
const nameSample    = $('nameSample');
const filterInput   = $('filterInput');
const accountsList  = $('accountsList');
const emptyState    = $('emptyState');
const totalBadge    = $('totalBadge');
const copyAllBtn    = $('copyAllBtn');
const downloadBtn   = $('downloadBtn');
const clearBtn      = $('clearBtn');
const progressPanel = $('progressPanel');
const progressBar   = $('progressBar');
const progressCount = $('progressCount');
const successCount  = $('successCount');
const elapsedTime   = $('elapsedTime');

// ─── Particle background ─────────────────────────────────────────────────────
(function initParticles() {
  const canvas = $('particleCanvas');
  const ctx = canvas.getContext('2d');
  let particles = [];
  let W, H;

  function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }

  function createParticle() {
    return {
      x: Math.random() * W,
      y: Math.random() * H,
      r: Math.random() * 1.5 + 0.3,
      vx: (Math.random() - 0.5) * 0.3,
      vy: -Math.random() * 0.4 - 0.1,
      alpha: Math.random() * 0.5 + 0.1,
      color: Math.random() > 0.5 ? '0,245,160' : '0,217,245'
    };
  }

  function initParticles() {
    particles = Array.from({ length: 80 }, createParticle);
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    particles.forEach((p, i) => {
      p.x += p.vx;
      p.y += p.vy;
      if (p.y < -5 || p.x < -5 || p.x > W + 5) {
        particles[i] = { ...createParticle(), x: Math.random() * W, y: H + 5 };
      }
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${p.color},${p.alpha})`;
      ctx.fill();
    });

    // Draw lines between nearby particles
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 100) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(0,245,160,${0.04 * (1 - dist / 100)})`;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', () => { resize(); initParticles(); });
  resize();
  initParticles();
  draw();
})();

// ─── Screen management ───────────────────────────────────────────────────────
function showScreen(screenEl) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  screenEl.classList.add('active');
}

// ─── Toast ───────────────────────────────────────────────────────────────────
function toast(msg, type = 'info', dur = 3000) {
  const icons = { success: '✓', error: '✕', info: 'ℹ' };
  const tc = $('toastContainer');
  const el = document.createElement('div');
  el.className = `toast toast-${type}`;
  el.innerHTML = `<span class="toast-icon">${icons[type]}</span><span class="toast-msg">${msg}</span>`;
  tc.appendChild(el);
  setTimeout(() => {
    el.style.opacity = '0';
    el.style.transform = 'translateX(20px)';
    el.style.transition = '0.3s ease';
    setTimeout(() => el.remove(), 350);
  }, dur);
}

// ─── Auth ────────────────────────────────────────────────────────────────────
async function checkAuth() {
  try {
    const res = await fetch('/api/check_auth');
    const data = await res.json();
    if (data.authenticated) {
      showScreen(dashboard);
      loadRegions();
    } else {
      showScreen(loginScreen);
    }
  } catch {
    showScreen(loginScreen);
  }
}

togglePass.addEventListener('click', () => {
  const isPass = adminPassword.type === 'password';
  adminPassword.type = isPass ? 'text' : 'password';
  $('eyeIcon').innerHTML = isPass
    ? '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/>'
    : '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
});

loginForm.addEventListener('submit', async e => {
  e.preventDefault();
  loginError.textContent = '';
  const pw = adminPassword.value.trim();
  if (!pw) {
    loginError.textContent = 'Password tidak boleh kosong';
    return;
  }
  loginBtn.disabled = true;
  loginBtn.querySelector('.btn-text').textContent = 'Memeriksa...';
  loginBtn.querySelector('.btn-loader').classList.remove('hidden');

  try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: pw })
    });
    const data = await res.json();
    if (data.success) {
      toast('Login berhasil!', 'success');
      showScreen(dashboard);
      loadRegions();
    } else {
      loginError.textContent = data.message || 'Password salah';
      adminPassword.value = '';
      adminPassword.focus();
    }
  } catch {
    loginError.textContent = 'Koneksi gagal. Coba lagi.';
  } finally {
    loginBtn.disabled = false;
    loginBtn.querySelector('.btn-text').textContent = 'Masuk';
    loginBtn.querySelector('.btn-loader').classList.add('hidden');
  }
});

logoutBtn.addEventListener('click', async () => {
  await fetch('/api/logout', { method: 'POST' });
  state.accounts = [];
  state.activeSession = null;
  clearInterval(state.pollInterval);
  clearInterval(state.elapsedTimer);
  showScreen(loginScreen);
  toast('Berhasil logout', 'info');
});

// ─── Regions ─────────────────────────────────────────────────────────────────
async function loadRegions() {
  try {
    const res = await fetch('/api/regions');
    const data = await res.json();
    renderRegions(data.regions);
  } catch {
    toast('Gagal memuat region', 'error');
  }
}

function renderRegions(regions) {
  regionGrid.innerHTML = '';
  regions.forEach(r => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'region-btn' + (r.code === state.selectedRegion ? ' active' : '');
    btn.dataset.code = r.code;
    btn.innerHTML = `
      <span class="rflag">${r.flag}</span>
      <span class="rcode">${r.code}</span>
      <span class="rname">${r.name}</span>
    `;
    btn.addEventListener('click', () => selectRegion(r, regions));
    regionGrid.appendChild(btn);
  });
}

function selectRegion(r, regions) {
  state.selectedRegion = r.code;
  // Update selected display
  selectedRegionDisplay.innerHTML = `
    <span class="region-flag">${r.flag}</span>
    <span class="region-name-selected">${r.name}</span>
    <span class="region-code-selected">${r.code}</span>
  `;
  // Update buttons
  document.querySelectorAll('.region-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.code === r.code);
  });
}

// ─── Count controls ──────────────────────────────────────────────────────────
$('countMinus').addEventListener('click', () => {
  const v = parseInt(accountCount.value) || 1;
  accountCount.value = Math.max(1, v - 1);
});

$('countPlus').addEventListener('click', () => {
  const v = parseInt(accountCount.value) || 1;
  accountCount.value = Math.min(50, v + 1);
});

document.querySelectorAll('.preset-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    accountCount.value = btn.dataset.val;
  });
});

// Name prefix preview
namePrefix.addEventListener('input', updateNameSample);
function updateNameSample() {
  const p = namePrefix.value.trim() || 'Blinx';
  nameSample.textContent = `${p}_1, ${p}_2, ...`;
}

// ─── Generate ─────────────────────────────────────────────────────────────────
generateForm.addEventListener('submit', async e => {
  e.preventDefault();
  if (state.generating) return;

  const count  = parseInt(accountCount.value) || 1;
  const region = state.selectedRegion;
  const prefix = namePrefix.value.trim() || 'Blinx';

  if (count < 1 || count > 1500) {
    toast('Jumlah akun harus 1-1500', 'error');
    return;
  }

  startGenerating(count, region, prefix);
});

async function startGenerating(count, region, prefix) {
  state.generating = true;
  generateBtn.disabled = true;
  generateBtnText.textContent = 'Sedang generate...';
  generateLoader.classList.remove('hidden');
  generateBtn.querySelector('svg').style.display = 'none';

  progressPanel.classList.remove('hidden');
  progressBar.style.width = '0%';
  progressCount.textContent = `0 / ${count}`;
  successCount.textContent = '0';
  state.elapsedSec = 0;
  elapsedTime.textContent = '0s';

  // Start elapsed timer
  clearInterval(state.elapsedTimer);
  state.elapsedTimer = setInterval(() => {
    state.elapsedSec++;
    elapsedTime.textContent = state.elapsedSec < 60
      ? `${state.elapsedSec}s`
      : `${Math.floor(state.elapsedSec / 60)}m ${state.elapsedSec % 60}s`;
  }, 1000);

  try {
    const res = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ count, region, name_prefix: prefix })
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || 'Gagal memulai generate');
    }
    state.activeSession = data.session_id;
    pollStatus(data.session_id, count);
  } catch (err) {
    toast(err.message, 'error');
    stopGenerating();
  }
}

function pollStatus(sessionId, total) {
  let prevSuccess = 0;
  let rendered = 0;

  clearInterval(state.pollInterval);
  state.pollInterval = setInterval(async () => {
    try {
      const res = await fetch(`/api/status/${sessionId}`);
      const data = await res.json();
      if (!res.ok) throw new Error();

      // Update progress
      const done = data.done || 0;
      const success = data.success || 0;
      const pct = total > 0 ? (done / total * 100) : 0;
      progressBar.style.width = `${pct}%`;
      progressCount.textContent = `${done} / ${total}`;
      successCount.textContent = success;

      // Render new accounts
      if (data.accounts && data.accounts.length > rendered) {
        const newAccs = data.accounts.slice(rendered);
        newAccs.forEach((acc, i) => {
          const isFirst = rendered === 0 && i === 0;
          addAccountCard(acc, isFirst);
          state.accounts.push(acc);
        });
        rendered = data.accounts.length;
        updateResultsUI();
      }

      // Check done
      if (data.status === 'done' || data.status === 'error') {
        clearInterval(state.pollInterval);
        clearInterval(state.elapsedTimer);
        stopGenerating();
        if (data.status === 'error') {
          toast(`Error: ${data.error}`, 'error');
        } else {
          toast(`${success} akun berhasil dibuat! 🎉`, 'success', 5000);
        }
        progressPanel.classList.add('hidden');
      }
    } catch {
      // keep polling
    }
  }, 1000);
}

function stopGenerating() {
  state.generating = false;
  generateBtn.disabled = false;
  generateBtnText.textContent = 'Generate Sekarang';
  generateLoader.classList.add('hidden');
  generateBtn.querySelector('svg').style.display = '';
}

// ─── Account Cards ────────────────────────────────────────────────────────────
function addAccountCard(acc, isNew = true) {
  emptyState.classList.add('hidden');
  const card = buildCard(acc, state.accounts.length, isNew);
  accountsList.prepend(card);

  if (isNew) {
    setTimeout(() => card.classList.remove('new-card'), 3000);
  }
}

function buildCard(acc, index, isNew = false) {
  const div = document.createElement('div');
  div.className = 'account-card' + (acc.is_rare ? ' rare' : '') + (isNew ? ' new-card' : '');

  const idx = index + 1;
  const timeStr = acc.created_at || '';

  div.innerHTML = `
    <div class="card-index">${idx}</div>
    <div class="card-body">
      <div class="card-top">
        <span class="card-name">${escHtml(acc.name)}</span>
        <span class="card-badge badge-region">${escHtml(acc.region)}</span>
        ${acc.is_rare ? '<span class="card-badge badge-rare">⭐ Rare</span>' : ''}
        ${isNew ? '<span class="card-badge badge-new">New</span>' : ''}
      </div>
      <div class="card-fields">
        <div class="card-field">
          <span class="field-label">UID</span>
          <span class="field-value mono-text">${escHtml(acc.uid)}</span>
        </div>
        <div class="card-field">
          <span class="field-label">Account ID</span>
          <span class="field-value ${acc.is_rare ? 'rare-color' : 'accent'}">${escHtml(acc.account_id)}</span>
        </div>
        <div class="card-field">
          <span class="field-label">Password</span>
          <span class="field-value mono-text">${escHtml(acc.password)}</span>
        </div>
        <div class="card-field">
          <span class="field-label">Dibuat</span>
          <span class="field-value" style="color:var(--text-muted);font-size:11px">${escHtml(timeStr)}</span>
        </div>
      </div>
      ${timeStr ? `<div class="card-time"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12,6 12,12 16,14"/></svg>${timeStr}</div>` : ''}
    </div>
    <div class="card-actions">
      <button class="btn-copy" title="Copy data akun" data-acc='${JSON.stringify(acc)}'>
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
        </svg>
      </button>
    </div>
  `;

  // Copy button
  div.querySelector('.btn-copy').addEventListener('click', function() {
    const acc = JSON.parse(this.dataset.acc);
    const text = `Name: ${acc.name}\nUID: ${acc.uid}\nPassword: ${acc.password}\nAccount ID: ${acc.account_id}\nRegion: ${acc.region}`;
    copyText(text, this);
  });

  return div;
}

function escHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function copyText(text, btn) {
  navigator.clipboard.writeText(text).then(() => {
    if (btn) {
      btn.classList.add('copied');
      btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20,6 9,17 4,12"/></svg>`;
      setTimeout(() => {
        btn.classList.remove('copied');
        btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>`;
      }, 2000);
    }
    toast('Disalin!', 'success', 1500);
  }).catch(() => {
    toast('Gagal menyalin', 'error');
  });
}

// ─── Filter ───────────────────────────────────────────────────────────────────
filterInput.addEventListener('input', () => {
  state.search = filterInput.value.toLowerCase();
  reRenderFiltered();
});

document.querySelectorAll('.filter-tab').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
    state.filter = btn.dataset.filter;
    reRenderFiltered();
  });
});

function reRenderFiltered() {
  accountsList.innerHTML = '';
  let filtered = state.accounts;
  if (state.filter === 'rare') filtered = filtered.filter(a => a.is_rare);
  if (state.search) {
    filtered = filtered.filter(a =>
      (a.uid && a.uid.toLowerCase().includes(state.search)) ||
      (a.account_id && a.account_id.toLowerCase().includes(state.search)) ||
      (a.name && a.name.toLowerCase().includes(state.search))
    );
  }
  if (filtered.length === 0) {
    emptyState.classList.remove('hidden');
  } else {
    emptyState.classList.add('hidden');
    filtered.forEach((acc, i) => {
      const card = buildCard(acc, i, false);
      accountsList.appendChild(card);
    });
  }
}

// ─── Results actions ──────────────────────────────────────────────────────────
function updateResultsUI() {
  const total = state.accounts.length;
  totalBadge.textContent = `${total} akun`;
  const hasAccs = total > 0;
  copyAllBtn.disabled = !hasAccs;
  downloadBtn.disabled = !hasAccs;
  clearBtn.disabled    = !hasAccs;
  if (hasAccs) emptyState.classList.add('hidden');
}

copyAllBtn.addEventListener('click', () => {
  const text = state.accounts.map((a, i) =>
    `[${i+1}] Name: ${a.name} | UID: ${a.uid} | Pass: ${a.password} | ID: ${a.account_id} | Region: ${a.region}`
  ).join('\n');
  copyText(text, null);
  toast(`${state.accounts.length} akun disalin!`, 'success');
});

downloadBtn.addEventListener('click', () => {
  const blob = new Blob([JSON.stringify(state.accounts, null, 2)], { type: 'application/json' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href = url;
  a.download = `blinx-accounts-${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(url);
  toast('Download dimulai', 'success');
});

clearBtn.addEventListener('click', () => {
  if (!confirm('Hapus semua hasil generate?')) return;
  state.accounts = [];
  accountsList.innerHTML = '';
  emptyState.classList.remove('hidden');
  updateResultsUI();
  toast('Semua akun dihapus', 'info');
});

// ─── Init ─────────────────────────────────────────────────────────────────────
checkAuth();
updateNameSample();
  
