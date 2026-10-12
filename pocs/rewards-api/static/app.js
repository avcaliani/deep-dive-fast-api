'use strict';

const $ = (id) => document.getElementById(id);
const state = { token: null, busy: false, history: [], selected: null, view: 'response', count: 0 };
let announcementTimer;

function hidePasswords() {
  document.querySelectorAll('[data-password-toggle]').forEach((button) => {
    $(button.dataset.passwordToggle).type = 'password';
    button.setAttribute('aria-label', 'Show password');
    button.setAttribute('aria-pressed', 'false');
    button.querySelector('span').textContent = 'visibility';
  });
}

document.querySelectorAll('[data-password-toggle]').forEach((button) => {
  button.addEventListener('click', () => {
    const input = $(button.dataset.passwordToggle);
    const visible = input.type === 'password';
    input.type = visible ? 'text' : 'password';
    button.setAttribute('aria-label', visible ? 'Hide password' : 'Show password');
    button.setAttribute('aria-pressed', String(visible));
    button.querySelector('span').textContent = visible ? 'visibility_off' : 'visibility';
  });
});

function announce(message) {
  $('announcement').textContent = message;
  $('announcement').classList.add('visible');
  clearTimeout(announcementTimer);
  announcementTimer = setTimeout(() => $('announcement').classList.remove('visible'), 3500);
}

function syncControls() {
  document.querySelectorAll('form button, [data-protected], [data-mood]').forEach((button) => {
    button.disabled = state.busy || (button.hasAttribute('data-protected') && !state.token);
  });
  $('logout').hidden = !state.token;
  $('logout').disabled = state.busy;
}

function setSession(token, name = '') {
  state.token = token;
  $('session-label').textContent = token ? 'Authenticated session' : 'Guest session';
  $('employee-status').textContent = token ? (name || 'Clocked in') : 'Not clocked in';
  $('employee-subtitle').textContent = token ? 'Your employee badge is active' : 'Sign in to get started';
  $('avatar').textContent = name ? name.split(/\s+/).map((part) => part[0]).join('').slice(0, 2).toUpperCase() : 'DM';
  $('login-hint').textContent = token ? 'Badge verified. You are ready to explore.' : 'Use an existing employee account.';
  $('mood-hint').textContent = token ? 'Pick a mood. Send a request. Earn a reward.' : 'Sign in, then pick your mood to check in.';
  if (!token) {
    $('balance').textContent = '···';
    $('catalog').replaceChildren();
    const empty = document.createElement('div');
    empty.className = 'catalog-empty';
    empty.textContent = 'Sign in and load the catalog to see what is in stock.';
    $('catalog').append(empty);
  }
  syncControls();
}

function redact(value) {
  if (Array.isArray(value)) return value.map(redact);
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.entries(value).map(([key, item]) => [
      key, /^(password|token|access_token|refresh_token|authorization)$/i.test(key) ? '[hidden]' : redact(item),
    ]));
  }
  return value;
}

function curlFor(record) {
  const lines = [`curl -X ${record.method} '${location.origin}${record.path}'`];
  if (record.authenticated) lines.push("  -H 'Authorization: Bearer <YOUR_TOKEN>'");
  if (record.request.body) {
    lines.push("  -H 'Content-Type: application/json'");
    const payload = JSON.stringify(record.request.body).replace(/'/g, "'\\''");
    lines.push(`  -d '${payload}'`);
  }
  return lines.join(' \\\n');
}

function codeText() {
  const record = state.selected;
  if (!record) return '// Choose an action to inspect a real API request.';
  if (state.view === 'curl') return curlFor(record);
  if (state.view === 'request') return JSON.stringify(record.request, null, 2);
  return typeof record.response === 'string' ? record.response : JSON.stringify(record.response, null, 2);
}

function renderCode() {
  const text = codeText();
  const code = $('response-code');
  code.replaceChildren();
  // Render only text nodes and fixed classes, including for server-controlled content.
  if (state.view === 'curl' || !state.selected || typeof state.selected.response === 'string' && state.view === 'response') {
    code.textContent = text;
    return;
  }
  const regex = /("(?:\\.|[^"\\])*"\s*:)|("(?:\\.|[^"\\])*")|\b(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\b|\b(true|false|null)\b/g;
  let last = 0;
  for (const match of text.matchAll(regex)) {
    code.append(document.createTextNode(text.slice(last, match.index)));
    const span = document.createElement('span');
    span.className = match[1] ? 'json-key' : match[2] ? 'json-string' : match[3] ? 'json-number' : 'json-literal';
    span.textContent = match[0];
    code.append(span);
    last = match.index + match[0].length;
  }
  code.append(document.createTextNode(text.slice(last)));
}

function selectRecord(record) {
  state.selected = record;
  $('inspect-method').textContent = record.method;
  $('inspect-path').textContent = record.path;
  $('response-status').textContent = record.status ? `${record.status} ${record.statusText}` : 'Network error';
  $('response-status').className = record.ok ? 'success' : 'error';
  $('response-time').textContent = `${record.duration} ms`;
  renderCode();
  renderHistory();
}

function renderHistory() {
  const container = $('request-history');
  container.replaceChildren();
  if (!state.history.length) {
    const empty = document.createElement('div');
    empty.className = 'history-empty';
    empty.textContent = 'Nothing on file. Yet.';
    container.append(empty);
  }
  state.history.forEach((record) => {
    const row = document.createElement('button');
    row.className = `history-row${record === state.selected ? ' current' : ''}`;
    row.setAttribute('aria-label', `${record.method} ${record.path}, status ${record.status || 'network error'}`);
    for (const [className, content] of [
      ['history-method', record.method], ['history-path', record.path],
      [`history-status${record.ok ? '' : ' error'}`, record.status || 'ERR'],
    ]) {
      const span = document.createElement('span');
      span.className = className;
      span.textContent = content;
      row.append(span);
    }
    row.addEventListener('click', () => selectRecord(record));
    container.append(row);
  });
}

async function request(method, path, body = null, authenticate = true) {
  $('inspect-method').textContent = method;
  $('inspect-path').textContent = path;
  $('response-status').textContent = 'Sending request…';
  $('response-status').className = '';
  $('response-time').textContent = '··· ms';
  const headers = {};
  const authenticated = authenticate && Boolean(state.token);
  if (authenticated) headers.Authorization = `Bearer ${state.token}`;
  if (body) headers['Content-Type'] = 'application/json';
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  const start = performance.now();
  const record = {
    method, path, authenticated,
    request: { method, path, headers: redact(headers), ...(body ? { body: redact(body) } : {}) },
  };
  let data;
  try {
    const response = await fetch(path, { method, headers, ...(body ? { body: JSON.stringify(body) } : {}), signal: controller.signal });
    const raw = await response.text();
    try { data = raw ? JSON.parse(raw) : null; } catch { data = raw; }
    Object.assign(record, { status: response.status, statusText: response.statusText, ok: response.ok, response: redact(data) });
    if (response.status === 401 && authenticated) setSession(null);
    if (!response.ok) announce(`Request returned ${response.status}. See the paper trail for details.`);
  } catch (error) {
    Object.assign(record, { status: 0, ok: false, response: { error: error.name === 'AbortError' ? 'Request timed out after 15 seconds.' : 'Could not reach the API. Check that the server is running.' } });
    announce(record.response.error);
  } finally {
    clearTimeout(timeout);
    record.duration = Math.round(performance.now() - start);
    state.count += 1;
    state.history.unshift(record);
    state.history = state.history.slice(0, 20);
    $('request-count').textContent = String(state.count).padStart(2, '0');
    $('last-request').textContent = `${method} ${decodeURI(path)}`;
    selectRecord(record);
  }
  return { ok: record.ok, data };
}

async function perform(action) {
  if (state.busy) return;
  state.busy = true;
  syncControls();
  try { await action(); } catch { announce('The API returned an unexpected response. Inspect the paper trail.'); }
  finally { state.busy = false; syncControls(); }
}

function updateBalance(data) {
  if (typeof data?.balance === 'number') $('balance').textContent = data.balance.toLocaleString();
  else if (typeof data?.points === 'number') $('balance').textContent = data.points.toLocaleString();
}

function renderCatalog(items) {
  const container = $('catalog');
  container.replaceChildren();
  if (!Array.isArray(items) || !items.length) {
    container.textContent = 'The shelves are empty. Check back after the catalog is configured.';
    return;
  }
  const grid = document.createElement('div');
  grid.className = 'catalog-grid';
  items.forEach((item, index) => {
    const product = document.createElement('div');
    product.className = 'catalog-product';
    const head = document.createElement('div');
    head.className = 'product-head';
    const emoji = document.createElement('span');
    emoji.textContent = item.emoji;
    const name = document.createElement('strong');
    name.textContent = item.name;
    head.append(emoji, name);
    const price = document.createElement('span');
    price.className = 'product-price';
    price.textContent = `${item.cost} SB`;
    const buttons = document.createElement('div');
    buttons.className = 'product-buttons';
    const inspect = document.createElement('button');
    inspect.className = 'button secondary';
    inspect.textContent = 'Inspect';
    inspect.setAttribute('data-protected', '');
    inspect.addEventListener('click', () => perform(() => request('GET', `/vending/${index}`)));
    const redeem = document.createElement('button');
    redeem.className = 'button primary';
    redeem.textContent = 'Redeem';
    const arrow = document.createElement('span');
    arrow.className = 'material-symbols-outlined';
    arrow.setAttribute('aria-hidden', 'true');
    arrow.textContent = 'arrow_outward';
    redeem.append(arrow);
    redeem.setAttribute('data-protected', '');
    redeem.addEventListener('click', () => perform(async () => {
      const result = await request('POST', `/vending/${index}`);
      if (result.ok) { updateBalance(result.data); announce('Redeemed. A little joy, on the company.'); }
    }));
    buttons.append(inspect, redeem);
    product.append(head, price, buttons);
    grid.append(product);
  });
  container.append(grid);
  syncControls();
}

$('login-form').addEventListener('submit', (event) => {
  event.preventDefault();
  perform(async () => {
    const result = await request('POST', '/auth', { username: $('login-email').value.trim(), password: $('login-password').value }, false);
    if (result.ok && typeof result.data?.token === 'string') {
      setSession(result.data.token);
      $('login-password').value = '';
      hidePasswords();
      announce('Welcome to the office. Your badge is ready.');
      const profile = await request('GET', '/users/me');
      if (profile.ok) { setSession(state.token, profile.data.name); updateBalance(profile.data); }
    } else setSession(null);
  });
});
$('logout').addEventListener('click', () => {
  setSession(null);
  state.history = [];
  state.selected = null;
  renderHistory();
  resetInspector();
  $('login-password').value = '';
  hidePasswords();
  announce('Signed out. Your badge and paper trail have been cleared.');
});
document.querySelectorAll('[data-mood]').forEach((button) => button.addEventListener('click', () => perform(async () => {
  const query = $('caps-mode').checked ? '?text_mode=CAPSLOCK' : '';
  const result = await request('POST', `/mood/${encodeURIComponent(button.dataset.mood)}${query}`);
  if (result.ok) { updateBalance(result.data); announce(`Check-in complete. +${result.data.schrute_bucks_earned} Schrute Bucks.`); }
})));
$('browse').addEventListener('click', () => perform(async () => {
  const result = await request('GET', '/vending/');
  if (result.ok) renderCatalog(result.data.items);
}));
$('my-profile').addEventListener('click', () => perform(async () => {
  const result = await request('GET', '/users/me');
  if (result.ok) { setSession(state.token, result.data.name); updateBalance(result.data); }
}));
$('lookup-form').addEventListener('submit', (event) => {
  event.preventDefault();
  if (!state.token) return;
  perform(() => request('GET', `/users/${encodeURIComponent($('lookup-id').value.trim())}`));
});
$('create-form').addEventListener('submit', (event) => {
  event.preventDefault();
  if (!state.token) return;
  perform(async () => {
    const result = await request('POST', '/users/', {
      name: $('new-name').value.trim(), email: $('new-email').value.trim(),
      birthdate: $('new-birthdate').value, password: $('new-password').value,
    });
    if (result.ok) { $('create-form').reset(); hidePasswords(); announce('Employee created. Welcome aboard.'); }
  });
});
document.querySelectorAll('[data-panel]').forEach((button) => button.addEventListener('click', () => {
  document.querySelectorAll('[data-panel]').forEach((item) => item.classList.toggle('active', item === button));
  $('office-panel').hidden = button.dataset.panel !== 'office';
  $('people-panel').hidden = button.dataset.panel !== 'people';
  $('page-label').textContent = button.dataset.panel === 'office' ? 'The office' : 'Employee directory';
}));
document.querySelectorAll('[data-view]').forEach((button) => button.addEventListener('click', () => {
  state.view = button.dataset.view;
  document.querySelectorAll('[data-view]').forEach((item) => {
    item.classList.toggle('selected', item === button);
    item.setAttribute('aria-selected', String(item === button));
  });
  $('inspector-output').setAttribute('aria-labelledby', button.id);
  renderCode();
}));
$('copy-output').addEventListener('click', async () => {
  try { await navigator.clipboard.writeText(codeText()); announce('Copied. Sensitive fields are masked.'); }
  catch { announce('Clipboard unavailable. Select the inspector text to copy it.'); }
});
function resetInspector() {
  $('inspect-method').textContent = 'READY';
  $('inspect-path').textContent = 'Waiting for a request';
  $('response-status').textContent = 'No request selected';
  $('response-status').className = '';
  $('response-time').textContent = '··· ms';
  renderCode();
}
$('clear-history').addEventListener('click', () => {
  state.history = [];
  state.selected = null;
  renderHistory();
  resetInspector();
});
syncControls();
