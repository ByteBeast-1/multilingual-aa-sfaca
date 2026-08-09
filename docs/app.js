/**
 * app.js — SFA-CA Frontend Logic
 * Handles API calls, chart rendering, file uploads
 */

// ── Config ────────────────────────────────────────────────────────────────────
// Replace with your HuggingFace Spaces URL after deployment
const API_BASE = "https://creatures-darwin-writing-clinic.trycloudflare.com";

// ── Class color palette ───────────────────────────────────────────────────────
const CLASS_COLORS = {
  "human":                  { bar: "#34d399", radar: "rgba(52,211,153,0.7)"  },
  "gpt-3.5-turbo-0125":     { bar: "#f59e0b", radar: "rgba(245,158,11,0.7)"  },
  "Mistral-7B-Instruct-v0.2":{ bar: "#8b5cf6", radar: "rgba(139,92,246,0.7)" },
  "Llama-2-70b-chat-hf":    { bar: "#ec4899", radar: "rgba(236,72,153,0.7)"  },
  "vicuna-13b":             { bar: "#06b6d4", radar: "rgba(6,182,212,0.7)"   },
  "v5-Eagle-7B-HF":         { bar: "#f97316", radar: "rgba(249,115,22,0.7)"  },
  "opt-iml-max-30b":        { bar: "#64748b", radar: "rgba(100,116,139,0.7)" },
  "aya-101":                { bar: "#a855f7", radar: "rgba(168,85,247,0.7)"  },
  "Gemini-2.5-Flash":       { bar: "#3b82f6", radar: "rgba(59,130,246,0.7)"  },
  "Claude-Haiku-4.5":       { bar: "#10b981", radar: "rgba(16,185,129,0.7)"  },
};

const DEFAULT_COLOR = { bar: "#475569", radar: "rgba(71,85,105,0.7)" };

// ── DOM refs ──────────────────────────────────────────────────────────────────
const textInput    = document.getElementById("text-input");
const charCount    = document.getElementById("char-count");
const btnAnalyze   = document.getElementById("btn-analyze");
const btnClear     = document.getElementById("btn-clear");
const uploadZone   = document.getElementById("upload-zone");
const fileInput    = document.getElementById("file-input");
const statusBadge  = document.getElementById("status-badge");
const idleState    = document.getElementById("idle-state");
const loadingState = document.getElementById("loading-state");
const resultsState = document.getElementById("results-state");

// ── Health check ──────────────────────────────────────────────────────────────
async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(5000) });
    if (res.ok) {
      statusBadge.textContent = "● Online";
      statusBadge.style.color = "#34d399";
    } else { setOffline(); }
  } catch { setOffline(); }
}

function setOffline() {
  statusBadge.textContent = "● Offline";
  statusBadge.style.color = "#f87171";
}

// ── Char count ────────────────────────────────────────────────────────────────
textInput.addEventListener("input", () => {
  const n = textInput.value.length;
  charCount.textContent = `${n.toLocaleString()} chars`;
});

// ── Example buttons ───────────────────────────────────────────────────────────
document.querySelectorAll(".example-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    textInput.value = btn.dataset.text;
    textInput.dispatchEvent(new Event("input"));
    textInput.focus();
  });
});

// ── Clear ─────────────────────────────────────────────────────────────────────
btnClear.addEventListener("click", () => {
  textInput.value = "";
  charCount.textContent = "0 chars";
  showIdle();
});

// ── File Upload ───────────────────────────────────────────────────────────────
uploadZone.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", () => readFile(fileInput.files[0]));
uploadZone.addEventListener("dragover", e => { e.preventDefault(); uploadZone.classList.add("drag-over"); });
uploadZone.addEventListener("dragleave", () => uploadZone.classList.remove("drag-over"));
uploadZone.addEventListener("drop", e => {
  e.preventDefault();
  uploadZone.classList.remove("drag-over");
  const f = e.dataTransfer.files[0];
  if (f) readFile(f);
});

function readFile(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    textInput.value = e.target.result;
    textInput.dispatchEvent(new Event("input"));
  };
  reader.readAsText(file);
}

// ── State helpers ─────────────────────────────────────────────────────────────
function showIdle()    { idleState.classList.remove("hidden"); loadingState.classList.add("hidden"); resultsState.classList.add("hidden"); }
function showLoading() { idleState.classList.add("hidden");    loadingState.classList.remove("hidden"); resultsState.classList.add("hidden"); }
function showResults() { idleState.classList.add("hidden");    loadingState.classList.add("hidden"); resultsState.classList.remove("hidden"); }

// ── Analyze ───────────────────────────────────────────────────────────────────
btnAnalyze.addEventListener("click", analyze);
textInput.addEventListener("keydown", e => { if (e.ctrlKey && e.key === "Enter") analyze(); });

async function analyze() {
  const text = textInput.value.trim();
  if (!text || text.length < 10) {
    alert("Please enter at least 10 characters of text.");
    return;
  }

  btnAnalyze.disabled = true;
  showLoading();

  try {
    const res = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Server error ${res.status}`);
    }

    const data = await res.json();
    renderResults(data);
    showResults();

  } catch (err) {
    console.error(err);
    alert(`Analysis failed: ${err.message}\n\nMake sure the backend is online.`);
    showIdle();
  } finally {
    btnAnalyze.disabled = false;
  }
}

// ── Render results ────────────────────────────────────────────────────────────
function renderResults(data) {
  // Verdict banner
  const isAI = data.verdict === "AI-Generated";
  document.getElementById("verdict-icon").textContent = isAI ? "🤖" : "🧑";
  const label = document.getElementById("verdict-label");
  label.textContent = data.verdict;
  label.className = "verdict-label " + (isAI ? "ai" : "human");
  document.getElementById("verdict-detail").textContent =
    isAI ? `Primary: ${data.top_generator} (${pct(data.top_generator_confidence)})` : "Likely Authentic Human Text";

  // Confidence ring
  const pctVal = Math.round(data.confidence * 100);
  const circumference = 2 * Math.PI * 34; // r=34
  const offset = circumference * (1 - data.confidence);
  const arc = document.getElementById("confidence-arc");
  arc.style.strokeDashoffset = circumference; // start at 0
  requestAnimationFrame(() => requestAnimationFrame(() => {
    arc.style.transition = "stroke-dashoffset 1s cubic-bezier(0.4,0,0.2,1)";
    arc.style.strokeDashoffset = offset;
  }));
  document.getElementById("conf-pct").textContent = pctVal + "%";

  // Cluster badge
  document.getElementById("cluster-badge").textContent =
    capitalize(data.script_cluster) + " Script";
  document.getElementById("ai-prob-pill").textContent =
    pct(data.ai_probability) + " AI";

  // Bar chart
  renderBarChart(data.probabilities);

  // Radar chart
  renderRadar(data.probabilities);
}

// ── Bar Chart ─────────────────────────────────────────────────────────────────
function renderBarChart(probs) {
  const container = document.getElementById("bar-chart");
  container.innerHTML = "";

  // Sort descending
  const sorted = Object.entries(probs).sort((a, b) => b[1] - a[1]);

  sorted.forEach(([label, prob], i) => {
    const color = (CLASS_COLORS[label] || DEFAULT_COLOR).bar;
    const row = document.createElement("div");
    row.className = "bar-row";
    row.style.animationDelay = `${i * 50}ms`;

    const pctWidth = Math.round(prob * 100);
    row.innerHTML = `
      <div class="bar-label" title="${label}">${label}</div>
      <div class="bar-track">
        <div class="bar-fill" style="width:0%; background:${color};" data-target="${pctWidth}"></div>
      </div>
      <div class="bar-pct">${pct(prob)}</div>
    `;
    container.appendChild(row);
  });

  // Animate bars after DOM insertion
  requestAnimationFrame(() => requestAnimationFrame(() => {
    container.querySelectorAll(".bar-fill").forEach(el => {
      el.style.width = el.dataset.target + "%";
    });
  }));
}

// ── Radar Chart ───────────────────────────────────────────────────────────────
function renderRadar(probs) {
  const canvas = document.getElementById("radar-canvas");
  const ctx = canvas.getContext("2d");
  const W = canvas.width, H = canvas.height;
  const cx = W / 2, cy = H / 2;
  const R = Math.min(W, H) / 2 - 36;

  ctx.clearRect(0, 0, W, H);

  const labels = Object.keys(probs);
  const values = labels.map(l => probs[l]);
  const N = labels.length;

  const angle = (i) => (i / N) * 2 * Math.PI - Math.PI / 2;
  const point = (i, r) => ({
    x: cx + r * Math.cos(angle(i)),
    y: cy + r * Math.sin(angle(i)),
  });

  // Grid rings
  [0.25, 0.5, 0.75, 1].forEach(scale => {
    ctx.beginPath();
    for (let i = 0; i < N; i++) {
      const p = point(i, R * scale);
      i === 0 ? ctx.moveTo(p.x, p.y) : ctx.lineTo(p.x, p.y);
    }
    ctx.closePath();
    ctx.strokeStyle = "rgba(255,255,255,0.07)";
    ctx.lineWidth = 1;
    ctx.stroke();
  });

  // Spokes
  for (let i = 0; i < N; i++) {
    const p = point(i, R);
    ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(p.x, p.y);
    ctx.strokeStyle = "rgba(255,255,255,0.08)"; ctx.lineWidth = 1; ctx.stroke();
  }

  // Data polygon
  ctx.beginPath();
  values.forEach((v, i) => {
    const p = point(i, R * v);
    i === 0 ? ctx.moveTo(p.x, p.y) : ctx.lineTo(p.x, p.y);
  });
  ctx.closePath();
  ctx.fillStyle = "rgba(124,58,237,0.18)";
  ctx.fill();
  ctx.strokeStyle = "#7c3aed";
  ctx.lineWidth = 2;
  ctx.stroke();

  // Data points
  values.forEach((v, i) => {
    const color = (CLASS_COLORS[labels[i]] || DEFAULT_COLOR).bar;
    const p = point(i, R * v);
    ctx.beginPath();
    ctx.arc(p.x, p.y, 4, 0, 2 * Math.PI);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.strokeStyle = "white"; ctx.lineWidth = 1; ctx.stroke();
  });

  // Labels
  ctx.font = "600 10px Inter, sans-serif";
  ctx.textAlign = "center";
  labels.forEach((label, i) => {
    const p = point(i, R + 20);
    const shortLabel = label.length > 14 ? label.slice(0, 13) + "…" : label;
    const color = (CLASS_COLORS[label] || DEFAULT_COLOR).bar;
    ctx.fillStyle = color;
    ctx.fillText(shortLabel, p.x, p.y);
  });
}

// ── Utils ─────────────────────────────────────────────────────────────────────
function pct(v)       { return (v * 100).toFixed(1) + "%"; }
function capitalize(s){ return s.charAt(0).toUpperCase() + s.slice(1); }

// ── Init ──────────────────────────────────────────────────────────────────────
checkHealth();
setInterval(checkHealth, 30_000);
