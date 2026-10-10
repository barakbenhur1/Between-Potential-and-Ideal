(() => {
  'use strict';

  const el = (id) => document.getElementById(id);
  const loginPanel = el('login-panel');
  const dashboardPanel = el('dashboard-panel');
  const loginForm = el('login-form');
  const tokenInput = el('admin-token');
  const loginError = el('login-error');
  const dashboardError = el('dashboard-error');
  const loading = el('loading');
  const refreshButton = el('refresh-button');
  const logoutButton = el('logout-button');
  const fmt = new Intl.NumberFormat('he-IL');
  const dateFmt = new Intl.DateTimeFormat('he-IL', { day:'numeric',month:'numeric',timeZone:'UTC' });

  function error(target, text) {
    target.textContent = text || '';
    target.hidden = !text;
  }

  function showLogin(message = '') {
    dashboardPanel.hidden = true;
    loginPanel.hidden = false;
    loading.hidden = true;
    error(loginError, message);
  }

  async function request(path, options = {}) {
    const res = await fetch(path, {
      credentials: 'same-origin',
      cache: 'no-store',
      referrerPolicy: 'no-referrer',
      ...options
    });
    if (res.status === 401) throw Object.assign(new Error('unauthorized'), {code:401});
    if (!res.ok) throw new Error('HTTP ' + res.status);
    return res.status === 204 ? null : res.json();
  }

  function populateDays(days) {
    const chart = el('chart');
    const tbody = el('daily-rows');
    chart.replaceChildren();
    tbody.replaceChildren();

    const max = Math.max(1, ...days.map(x => Math.max(0, Number(x.visits) || 0)));
    for (const day of days) {
      const count = Math.max(0, Number(day.visits) || 0);
      const date = dateFmt.format(new Date(day.date + 'T12:00:00Z'));
      const column = document.createElement('div');
      column.className = 'bar-column';
      const value = document.createElement('span');
      value.className = 'bar-value';
      value.textContent = fmt.format(count);
      const track = document.createElement('div');
      track.className = 'bar-track';
      const bar = document.createElement('div');
      bar.className = 'bar';
      bar.style.height = (count ? Math.max(3, Math.round(100 * count / max)) : 2) + '%';
      track.append(bar);
      const label = document.createElement('span');
      label.className = 'bar-date';
      label.textContent = date;
      column.append(value, track, label);
      chart.append(column);

      const row = document.createElement('tr');
      const dateCell = document.createElement('td');
      dateCell.textContent = day.date;
      const countCell = document.createElement('td');
      countCell.textContent = fmt.format(count);
      row.append(dateCell, countCell);
      tbody.append(row);
    }
    chart.setAttribute('aria-label', days.map(d => d.date + ': ' + d.visits).join('; '));
  }

  async function refresh() {
    refreshButton.disabled = true;
    error(dashboardError, '');
    try {
      const data = await request('/admin/stats');
      el('today-count').textContent = fmt.format(data.today);
      el('week-count').textContent = fmt.format(data.last7Days);
      el('total-count').textContent = fmt.format(data.totalSinceInstallation);
      populateDays(Array.isArray(data.days) ? data.days : []);
      el('last-updated').textContent = 'עודכן לאחרונה: ' + new Intl.DateTimeFormat('he-IL', {
        dateStyle:'medium',timeStyle:'short'
      }).format(new Date());
      dashboardPanel.hidden = false;
      loginPanel.hidden = true;
      loading.hidden = true;
    } catch (err) {
      if (err.code === 401) showLogin('יש להזין קוד ניהול כדי לצפות בנתונים.');
      else if (dashboardPanel.hidden) showLogin('לא ניתן לטעון נתונים כרגע. אפשר לנסות שוב.');
      else error(dashboardError, 'נכשלה טעינת הנתונים. נסה לרענן.');
    } finally {
      refreshButton.disabled = false;
      loading.hidden = true;
    }
  }

  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const token = tokenInput.value.trim();
    tokenInput.value = '';
    const button = el('login-button');
    button.disabled = true;
    error(loginError, '');
    try {
      await request('/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token })
      });
      await refresh();
    } catch (err) {
      error(loginError, err.code === 401 ? 'קוד הניהול שגוי.' : 'לא ניתן להתחבר כרגע. נסה שוב.');
    } finally {
      button.disabled = false;
    }
  });

  refreshButton.addEventListener('click', refresh);
  logoutButton.addEventListener('click', async () => {
    try { await request('/admin/logout', {method:'POST'}); }
    catch { /* Drop local dashboard regardless of network conditions. */ }
    showLogin('');
  });

  refresh();
})();
