const params = new URLSearchParams(location.search);
const target = params.get('target');
const demo = params.get('demo');
const summary = document.getElementById('summary');
const findings = document.getElementById('findings');
const targetText = document.getElementById('targetText');
const surfaceMapEl = document.getElementById('surfaceMap');

function t(key) {
  const lang = getLang();
  return (HF_LANGS[lang] && HF_LANGS[lang][key]) || HF_LANGS.en[key] || key;
}

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>'"]/g, (char) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    "'": '&#39;',
    '"': '&quot;',
  }[char]));
}

function translateKind(kind) {
  const lang = getLang();
  const map = {
    es: { Confirmed: 'Confirmado', Review: 'Revisar', Informational: 'Informativo' },
    en: { Confirmed: 'Confirmed', Review: 'Review', Informational: 'Informational' },
    pt: { Confirmed: 'Confirmado', Review: 'Revisar', Informational: 'Informativo' },
    ja: { Confirmed: '確認済み', Review: '要確認', Informational: '情報' },
    zh: { Confirmed: '已确认', Review: '需复核', Informational: '信息' },
    ar: { Confirmed: 'مؤكد', Review: 'مراجعة', Informational: 'معلومة' },
    hi: { Confirmed: 'Confirmed', Review: 'Review', Informational: 'Informational' },
  };
  return map[lang]?.[kind] || kind;
}

function translateConfidence(value) {
  const lang = getLang();
  const map = {
    es: { high: 'alta', medium: 'media', low: 'baja' },
    en: { high: 'high', medium: 'medium', low: 'low' },
    pt: { high: 'alta', medium: 'média', low: 'baixa' },
    ja: { high: '高', medium: '中', low: '低' },
    zh: { high: '高', medium: '中', low: '低' },
    ar: { high: 'مرتفعة', medium: 'متوسطة', low: 'منخفضة' },
    hi: { high: 'high', medium: 'medium', low: 'low' },
  };
  return map[lang]?.[String(value).toLowerCase()] || value;
}

function translateSeverity(value) {
  const lang = getLang();
  const map = {
    es: { critical: 'CRÍTICO', high: 'ALTO', medium: 'MEDIO', low: 'BAJO', info: 'INFORMACIÓN' },
    en: { critical: 'CRITICAL', high: 'HIGH', medium: 'MEDIUM', low: 'LOW', info: 'INFO' },
    pt: { critical: 'CRÍTICO', high: 'ALTO', medium: 'MÉDIO', low: 'BAIXO', info: 'INFORMAÇÃO' },
    ja: { critical: '重大', high: '高', medium: '中', low: '低', info: '情報' },
    zh: { critical: '严重', high: '高', medium: '中', low: '低', info: '信息' },
    ar: { critical: 'حرج', high: 'مرتفع', medium: 'متوسط', low: 'منخفض', info: 'معلومة' },
    hi: { critical: 'CRITICAL', high: 'HIGH', medium: 'MEDIUM', low: 'LOW', info: 'INFO' },
  };
  return map[lang]?.[String(value).toLowerCase()] || String(value).toUpperCase();
}

function translateFinding(finding) {
  const lang = getLang();
  const translated = FINDING_TRANSLATIONS[lang]?.[finding.id];
  if (!translated) return finding;
  return {
    ...finding,
    title: translated[0] || finding.title,
    description: translated[1] || finding.description,
    recommendation: translated[2] || finding.recommendation,
  };
}

function metric(label, value, hint = '') {
  return `
    <div class="metric">
      <span>${escapeHtml(label)}</span>
      <b>${escapeHtml(value)}</b>
      ${hint ? `<small>${escapeHtml(hint)}</small>` : ''}
    </div>
  `;
}

function renderSummary(data) {
  const severity = data.summary?.severity_counts || {};
  summary.innerHTML = [
    metric(t('riskScore'), data.summary?.risk_score ?? '0', data.summary?.posture || t('review')),
    metric(t('findings'), data.count ?? 0, t('total')),
    metric(t('high'), severity.high ?? 0, 'confirmed/review'),
    metric(t('precision'), data.summary?.precision_mode || 'low-noise', t('passive')),
  ].join('');
}

function renderTags(items) {
  if (!items || !items.length) return `<div class="empty">${escapeHtml(t('emptySurface'))}</div>`;
  return `<div class="tag-list">${items.map((item) => `<span class="tag">${escapeHtml(item)}</span>`).join('')}</div>`;
}

function renderForms(forms) {
  if (!forms || !forms.length) return `<div class="empty">${escapeHtml(t('emptySurface'))}</div>`;
  return `
    <div class="form-list">
      ${forms.map((form) => `
        <div class="form-chip">
          <div>
            <b>${escapeHtml(form.path || form.action || '/')}</b>
            <small>${escapeHtml(t('formMethod'))}: ${escapeHtml(form.method || 'GET')} · ${escapeHtml(t('fields'))}: ${escapeHtml(form.field_count ?? 0)}</small>
          </div>
          <small>${escapeHtml((form.fields || []).map((field) => field.name).filter(Boolean).slice(0, 6).join(', '))}</small>
        </div>
      `).join('')}
    </div>
  `;
}

function renderSurfaceMap(data) {
  const surface = data.surface_map || {};
  const blocks = [
    {
      title: t('routesLabel'),
      subtitle: `${t('pagesCrawled')}: ${surface.pages_crawled || 1}`,
      body: renderTags(surface.routes || []),
    },
    {
      title: t('apiRoutesLabel'),
      subtitle: `${t('scriptsLabel')}: ${(surface.scripts || []).length}`,
      body: renderTags(surface.api_routes || []),
    },
    {
      title: t('paramsLabel'),
      subtitle: '',
      body: renderTags(surface.parameters || []),
    },
    {
      title: t('formsLabel'),
      subtitle: '',
      body: renderForms(surface.forms || []),
    },
  ];
  surfaceMapEl.innerHTML = blocks.map((block) => `
    <article class="surface-card">
      <h3>${escapeHtml(block.title)}</h3>
      ${block.subtitle ? `<div class="surface-meta">${escapeHtml(block.subtitle)}</div>` : ''}
      ${block.body}
    </article>
  `).join('');
}

function renderFinding(originalFinding) {
  const finding = translateFinding(originalFinding);
  const severity = (finding.severity || 'info').toLowerCase();
  return `
    <article class="finding ${severity}">
      <div class="finding-topline">
        <span class="chip">${escapeHtml(translateSeverity(severity))}</span>
        <span class="chip">${escapeHtml(t('confidence'))}: ${escapeHtml(translateConfidence(finding.confidence))}</span>
        <span class="chip">${escapeHtml(translateKind(finding.kind))}</span>
        <span class="chip">${escapeHtml(finding.id)}</span>
      </div>
      <h3>${escapeHtml(finding.title)}</h3>
      <p>${escapeHtml(finding.description)}</p>
      <dl>
        <dt>${escapeHtml(t('location'))}</dt>
        <dd>${escapeHtml(finding.location)}</dd>
        <dt>${escapeHtml(t('evidence'))}</dt>
        <dd><pre>${escapeHtml(finding.evidence)}</pre></dd>
        <dt>${escapeHtml(t('recommendation'))}</dt>
        <dd>${escapeHtml(finding.recommendation)}</dd>
        <dt>${escapeHtml(t('precisionNote'))}</dt>
        <dd>${escapeHtml(finding.precision_note)}</dd>
      </dl>
    </article>
  `;
}

function draw(data) {
  targetText.innerHTML = `
    ${escapeHtml(t('targetPrefix'))}: <b>${escapeHtml(data.final_url || data.url || 'demo')}</b>
    · HTTP ${escapeHtml(data.status || '200')}
    · ${escapeHtml(data.version || 'v1.8')}
  `;
  renderSummary(data);
  renderSurfaceMap(data);
  const items = data.findings || [];
  findings.innerHTML = items.length
    ? items.map(renderFinding).join('')
    : `<div class="card"><h3>${escapeHtml(t('noFindings'))}</h3><p>${escapeHtml(t('noFindingsText'))}</p></div>`;
}

function demoReport() {
  return {
    version: '1.8.5-community',
    final_url: 'https://demo.local',
    status: 200,
    count: 5,
    summary: {
      risk_score: 2.8,
      posture: 'review',
      precision_mode: 'low-noise passive analysis',
      severity_counts: { high: 0, medium: 2, low: 1, info: 2 },
    },
    surface_map: {
      routes: ['/login', '/profile', '/search?q=phone', '/basket'],
      api_routes: ['/api/profile', '/rest/products/search?q=phone'],
      parameters: ['q', 'page', 'id'],
      scripts: ['/main.js', '/runtime.js'],
      pages_crawled: 3,
      forms: [
        { path: '/search', method: 'GET', field_count: 2, fields: [{ name: 'q' }, { name: 'page' }] },
        { path: '/login', method: 'POST', field_count: 2, fields: [{ name: 'email' }, { name: 'password' }] },
      ],
    },
    findings: [
      {
        id: 'HF-LITE-001', severity: 'medium', confidence: 'high', kind: 'Review',
        title: 'Browser hardening headers missing',
        description: 'One or more defensive browser headers were not observed.',
        location: 'HTTP response headers',
        evidence: 'Missing: content-security-policy, referrer-policy, permissions-policy',
        recommendation: 'Add conservative headers and tune them per application behavior.',
        precision_note: 'Confirmed from response headers; severity is conservative.',
      },
      {
        id: 'HF-LITE-032', severity: 'low', confidence: 'medium', kind: 'Review',
        title: 'API-like routes referenced by the client',
        description: 'The client response or same-origin scripts reference API-looking paths.',
        location: 'HTML/client bundle route extraction',
        evidence: '/api/profile\n/rest/products/search?q=phone\n/oauth/authorize',
        recommendation: 'Manually verify whether each endpoint is in scope and authenticated as expected.',
        precision_note: 'Route discovery is passive and does not claim vulnerability.',
      },
      {
        id: 'HF-LITE-034', severity: 'info', confidence: 'medium', kind: 'Informational',
        title: 'Query and form parameters discovered',
        description: 'Visible URLs and forms expose parameter names.',
        location: 'Passive parameter extraction',
        evidence: 'q | page | id | email | password',
        recommendation: 'Parameter discovery alone is not a vulnerability.',
        precision_note: 'Parameter names are extracted without sending payloads.',
      },
      {
        id: 'HF-LITE-005', severity: 'low', confidence: 'high', kind: 'Review',
        title: 'Wildcard CORS policy observed',
        description: 'Wildcard CORS was observed without credentials.',
        location: 'HTTP response headers',
        evidence: 'Access-Control-Allow-Origin: *; Access-Control-Allow-Credentials: absent',
        recommendation: 'Avoid wildcard CORS on sensitive resources.',
        precision_note: 'Not inflated to high without credentials or sensitive context.',
      },
      {
        id: 'HF-LITE-027', severity: 'info', confidence: 'high', kind: 'Informational',
        title: '/robots.txt is publicly reachable',
        description: 'Standard discovery file is accessible.',
        location: '/robots.txt',
        evidence: 'User-agent: *',
        recommendation: 'Review only if it exposes internal paths.',
        precision_note: 'Informational only.',
      },
    ],
  };
}

async function run() {
  applyI18n();
  if (demo) {
    draw(demoReport());
    return;
  }

  if (!target) {
    targetText.textContent = 'No target provided.';
    findings.innerHTML = `<div class="card"><p>${escapeHtml(t('noFindingsText'))}</p></div>`;
    surfaceMapEl.innerHTML = `<div class="empty">${escapeHtml(t('emptySurface'))}</div>`;
    return;
  }

  targetText.textContent = `Scanning ${target} ...`;
  try {
    const response = await fetch('/api/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: target, lang: getLang() }),
    });
    const data = await response.json();
    if (!data.ok) {
      findings.innerHTML = `<div class="card"><h3>Error</h3><p>${escapeHtml(data.error)}</p></div>`;
      surfaceMapEl.innerHTML = `<div class="empty">${escapeHtml(t('emptySurface'))}</div>`;
      return;
    }
    draw(data);
  } catch (error) {
    findings.innerHTML = `<div class="card"><h3>Error</h3><p>${escapeHtml(error.message)}</p></div>`;
    surfaceMapEl.innerHTML = `<div class="empty">${escapeHtml(t('emptySurface'))}</div>`;
  }
}

document.addEventListener('DOMContentLoaded', run);
