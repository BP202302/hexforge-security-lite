async function scan(){
  const url=document.getElementById('target').value;
  const lang=document.getElementById('lang').value;
  const activity=document.getElementById('activity');
  const results=document.getElementById('results');
  activity.textContent=lang==='es'?'Iniciando análisis HexForge Security Lite...':'Starting HexForge Security Lite scan...';
  results.innerHTML='<p>'+(lang==='es'?'Analizando...':'Analyzing...')+'</p>';
  document.getElementById('count').textContent='0';
  try{
    const r=await fetch('/api/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url,lang})});
    const data=await r.json();
    if(!data.ok){results.innerHTML='<div class="finding"><h4>Error</h4><p>'+escapeHtml(data.error||'Error')+'</p></div>';return}
    document.getElementById('count').textContent=data.count;
    activity.innerHTML=(lang==='es'?'Objetivo: ':'Target: ')+escapeHtml(data.final_url)+'<br>'+(lang==='es'?'Estado HTTP: ':'HTTP status: ')+escapeHtml(String(data.status))+'<br>'+(lang==='es'?'Versión: ':'Version: ')+escapeHtml(data.version)+'<br>'+(lang==='es'?'Hallazgos: ':'Findings: ')+data.count+'<br>'+(lang==='es'?'Límite: ':'Limit: ')+escapeHtml(String(data.limit))+' URLs/session';
    results.innerHTML=data.findings.map(f=>renderFinding(f,lang)).join('')||'<p>'+(lang==='es'?'Sin hallazgos.':'No findings.')+'</p>'
  }catch(e){results.innerHTML='<div class="finding"><h4>Error</h4><p>'+escapeHtml(e.message)+'</p></div>'}
}
function renderFinding(f,lang){
  const info=(f.kind||'').toLowerCase().includes('inform')?' info':'';
  const locLabel=lang==='es'?'Ubicación':'Location';
  const recLabel=lang==='es'?'Recomendación':'Recommendation';
  return `<div class="finding${info}"><div class="chips"><span>${escapeHtml(f.kind||'Medio')}</span><span>${escapeHtml(f.confidence||'medium')}</span><span>${escapeHtml(f.id)}</span></div><h4>${escapeHtml(f.title)}</h4><p>${escapeHtml(f.description)}</p><p><b>${locLabel}:</b> ${escapeHtml(f.location)}</p><div class="evidence">${escapeHtml(f.evidence||'')}</div><p><b>${recLabel}:</b> ${escapeHtml(f.recommendation||'')}</p></div>`
}
function escapeHtml(s){return String(s).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]))}
