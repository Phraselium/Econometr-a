// Vivienda en España: evidencia. Utilidades comunes (gráficos con Observable Plot, mapas con Leaflet, tablas).
// Sin peticiones a terceros: las librerías están en vendor/ y los mapas no usan teselas externas.
"use strict";
const V = {};
V.fmt = (x, d = 1) => (x === null || x === undefined || Number.isNaN(x)) ? "—" :
  Number(x).toLocaleString("es-ES", { minimumFractionDigits: d, maximumFractionDigits: d });
V.json = async (url) => { const r = await fetch(url); if (!r.ok) throw new Error(url); return r.json(); };
V.el = (tag, attrs = {}, hijos = []) => {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) { if (k === "text") e.textContent = v; else e.setAttribute(k, v); }
  for (const h of [].concat(hijos)) if (h) e.append(h);
  return e;
};
V.capa = (c) => V.el("span", { class: `capa ${c}`, title: `Capa ${c}`, text: c });
V.meta = (m) => V.el("p", { class: "meta" }, [V.capa(m.capa || "C4"), ` Fuente: ${m.fuente}. Dato: ${m.fecha_dato || m.fecha || ""}. Unidad: ${m.unidad || ""}.`]);
V.csv = (filas, cols) => [cols.join(",")].concat(filas.map(f => cols.map(c => {
  const v = f[c]; const s = v === null || v === undefined ? "" : String(v);
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; }).join(","))).join("\n");
V.descarga = (texto, nombre) => {
  const b = V.el("button", { type: "button", text: `Descargar ${nombre}` });
  b.addEventListener("click", () => { const a = V.el("a", { href: URL.createObjectURL(new Blob([texto], { type: "text/csv" })), download: nombre }); a.click(); });
  return b;
};
V.tabla = (filas, cols, etiquetas = cols, decimales = {}) => {
  const t = V.el("table");
  t.append(V.el("thead", {}, V.el("tr", {}, etiquetas.map((e, i) => V.el("th", { scope: "col", class: typeof filas[0]?.[cols[i]] === "number" ? "num" : "", text: e })))));
  const tb = V.el("tbody");
  for (const f of filas) tb.append(V.el("tr", {}, cols.map(c => V.el("td", { class: typeof f[c] === "number" ? "num" : "",
    text: typeof f[c] === "number" ? V.fmt(f[c], decimales[c] ?? 2) : (f[c] ?? "—") }))));
  t.append(tb);
  return V.el("div", { class: "tabla-desplazable" }, t);
};
V.fecha = (p) => {
  let m;
  if ((m = /^(\d{4})T([1-4])$/.exec(p))) return new Date(Date.UTC(+m[1], (+m[2] - 1) * 3, 1));
  if ((m = /^(\d{4})-(\d{2})/.exec(p))) return new Date(Date.UTC(+m[1], +m[2] - 1, 1));
  if ((m = /^(\d{4})S([12])$/.exec(p))) return new Date(Date.UTC(+m[1], m[2] === "1" ? 0 : 6, 1));
  if ((m = /^(\d{4})$/.exec(p))) return new Date(Date.UTC(+m[1], 0, 1));
  return null;
};
V.lineas = (filas, { y = "valor", z = "nombre", titulo = "", unidad = "", ancho = 760 } = {}) => {
  filas = filas.map(d => ({ ...d, fecha: V.fecha(d.periodo) })).filter(d => d.fecha);
  const x = "fecha";
  const fig = Plot.plot({
    width: ancho, height: 380, marginLeft: 60, style: { fontSize: "12px" },
    x: { label: null, type: "utc" },
    y: { label: unidad, grid: true, tickFormat: (d) => Number(d).toLocaleString("es-ES") },
    color: { legend: true, scheme: "observable10" },
    marks: [Plot.ruleY([0], { stroke: "#bbb" }), Plot.lineY(filas, { x, y, z, stroke: z, strokeWidth: 1.8 }),
            Plot.dot(filas, { x, y, fill: z, r: 2, tip: true, title: d => `${d[z]} · ${d.periodo}: ${V.fmt(d[y], 2)} ${unidad}` })]
  });
  fig.setAttribute("role", "img");
  fig.setAttribute("aria-label", `${titulo}. Gráfico de líneas; los datos están en la tabla desplegable de debajo.`);
  return fig;
};
// Mapa coroplético accesible: GeoJSON + escala cividis + leyenda + tabla equivalente
V.mapa = (div, geo, prop, { etiqueta = "", decimales = 1, divergente = false } = {}) => {
  div.innerHTML = "";
  const m = L.map(div, { zoomControl: true, attributionControl: false, preferCanvas: true });
  const vals = geo.features.map(f => f.properties[prop]).filter(v => v !== null && v !== undefined && !Number.isNaN(v)).sort((a, b) => a - b);
  const q = (p) => vals.length ? vals[Math.min(vals.length - 1, Math.floor(p * (vals.length - 1)))] : 0;
  let lo = q(0.02), hi = q(0.98);
  if (divergente) { const a = Math.max(Math.abs(lo), Math.abs(hi)); lo = -a; hi = a; }
  const interp = divergente ? d3.interpolatePuOr : d3.interpolateCividis;
  const color = (v) => (v === null || v === undefined || Number.isNaN(v)) ? "#e6e6e6" : interp(Math.max(0, Math.min(1, (v - lo) / ((hi - lo) || 1))));
  const capa = L.geoJSON(geo, {
    style: f => ({ fillColor: color(f.properties[prop]), weight: 0.4, color: "#ffffff", fillOpacity: 0.92 }),
    onEachFeature: (f, l) => l.bindTooltip(`${f.properties.nombre}: ${V.fmt(f.properties[prop], decimales)} ${etiqueta}`, { sticky: true })
  }).addTo(m);
  m.fitBounds(capa.getBounds());
  const ley = L.control({ position: "bottomright" });
  ley.onAdd = () => {
    const d = V.el("div", { class: "leyenda" });
    const c = V.el("canvas", { class: "barra", width: 192, height: 10, "aria-hidden": "true" });
    const ctx = c.getContext("2d");
    for (let i = 0; i < 192; i++) { ctx.fillStyle = interp(i / 191); ctx.fillRect(i, 0, 1, 10); }
    d.append(V.el("div", { text: etiqueta }), c, V.el("div", { text: `${V.fmt(lo, decimales)} … ${V.fmt(hi, decimales)} (percentiles 2-98)` }),
             V.el("div", { text: "gris: sin dato" }));
    return d;
  };
  ley.addTo(m);
  return m;
};
window.V = V;
