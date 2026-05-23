let current = null;

async function j(url, opts={}) {
  const r = await fetch(url, {headers:{'Content-Type':'application/json'}, ...opts});
  return await r.json();
}

async function loadProjects() {
  const data = await j('/api/projects');
  const el = document.getElementById('projects');
  el.innerHTML = '';
  for (const p of data.projects) {
    const b = document.createElement('span');
    b.className = 'project-btn';
    b.textContent = p.name;
    b.onclick = () => selectProject(p.name);
    el.appendChild(b);
  }
  if (!current && data.projects.length) selectProject(data.projects[0].name);
}

async function selectProject(name) {
  current = name;
  document.getElementById('project-title').textContent = name;
  await refresh();
}

async function act(action) {
  if (!current) return;
  const data = await j(`/api/project/${current}/${action}`, {method:'POST'});
  document.getElementById('status').textContent = JSON.stringify(data, null, 2);
  setTimeout(refresh, 400);
}

function drawChart(seriesMap) {
  const canvas = document.getElementById('chart');
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const names = Object.keys(seriesMap);
  if (!names.length) {
    ctx.fillStyle = '#99a3d0';
    ctx.fillText('No metrics yet', 20, 30);
    return;
  }
  const colors = ['#7c6cff','#3ddc97','#ff8a65','#ffd54f','#64b5f6','#f06292'];
  let points = names.flatMap(n => seriesMap[n]);
  let xs = points.map(p => Number(p.x ?? 0));
  let ys = points.map(p => Number(p.y ?? 0));
  let minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
  if (minX === maxX) maxX = minX + 1;
  if (minY === maxY) maxY = minY + 1;
  const pad = 40, w = canvas.width - pad*2, h = canvas.height - pad*2;
  ctx.strokeStyle = '#36436f'; ctx.strokeRect(pad,pad,w,h);
  names.forEach((name, idx) => {
    const pts = seriesMap[name];
    ctx.strokeStyle = colors[idx % colors.length];
    ctx.lineWidth = 2;
    ctx.beginPath();
    pts.forEach((p, i) => {
      const x = pad + ((Number(p.x ?? 0)-minX)/(maxX-minX))*w;
      const y = pad + h - ((Number(p.y ?? 0)-minY)/(maxY-minY))*h;
      if (i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
    });
    ctx.stroke();
    ctx.fillStyle = colors[idx % colors.length];
    ctx.fillText(name, pad + 10, 20 + idx*16);
  });
}

async function refresh() {
  if (!current) return;
  const [st, logs, metrics] = await Promise.all([
    j(`/api/project/${current}/status`),
    j(`/api/project/${current}/logs?lines=200`),
    j(`/api/project/${current}/metrics`),
  ]);
  document.getElementById('status').textContent = JSON.stringify(st, null, 2);
  document.getElementById('logs').textContent = logs.text || '';
  const summary = {
    eta_seconds: metrics.eta_seconds,
    stages: metrics.stages?.slice(-10) || [],
    checkpoints: metrics.checkpoints?.slice(-10) || [],
    progress: metrics.progress?.slice(-10) || [],
  };
  document.getElementById('events').textContent = JSON.stringify(summary, null, 2);
  drawChart(metrics.series || {});
}

loadProjects();
setInterval(refresh, 5000);
