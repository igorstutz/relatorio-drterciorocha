"""Gera index.html (relatório estático para o GitHub Pages) a partir da página do painel.

Uso: python gerar.py painel.html
O painel lê o GA4 ao vivo; aqui os mesmos gráficos leem a foto dos dados em dados.js.
"""
import re
import sys
from pathlib import Path

AQUI = Path(__file__).parent
fonte = Path(sys.argv[1]).read_text(encoding='utf-8')

corpo = fonte.replace('<meta name="dash-one-writer">\n', '', 1)

# Textos que falavam de "hoje" no painel ao vivo: aqui o período é fechado.
trocas = [
    ('<p class="lr-eyebrow">Google Analytics 4 · site novo no ar desde 19 de outubro de 2026</p>',
     '<p class="lr-eyebrow">Google Analytics 4 · 19 a 29 de outubro de 2026</p>'),
    ('<p class="lr-note">As linhas mostram cada dia completo desde o lançamento; o dia de hoje fica de fora até terminar.</p>',
     '<p class="lr-note">As linhas mostram cada dia, de 19 a 29 de outubro.</p>'),
    ('<p class="lr-note">Cada ponto é um lead. A linha tracejada vai até hoje, que ainda está em andamento.</p>',
     '<p class="lr-note">Cada ponto é um lead. Toque num dia para ver os números.</p>'),
    ('Sessões em cada hora do dia, no fuso da propriedade do GA4. Quanto mais longa e escura a barra, mais visitas.',
     'Sessões em cada hora do dia, no horário de Brasília. Quanto mais longa e escura a barra, mais visitas.'),
]
for a, b in trocas:
    assert corpo.count(a) == 1, a[:70]
    corpo = corpo.replace(a, b)

# No celular o dedo "sai" do gráfico assim que solta a tela: a dica fica aberta até o próximo toque.
corpo = corpo.replace(".on('pointerleave', () => {", ".on('pointerleave', (ev) => { if (ev.pointerType === 'touch') return;")
corpo = corpo.replace("addEventListener('pointerleave', () => {", "addEventListener('pointerleave', (ev) => { if (ev.pointerType === 'touch') return;")

# Ids das seções para o menu.
assert 'id="publico"' in corpo and 'id="ajustes"' in corpo

TOKENS = """
  /* Identidade do site: marinho, azul, osso, dourado e jade. */
  :root {
    color-scheme: light;
    --color-bg: #faf7f1;
    --color-panel: #ffffff;
    --color-fg: #0c1a36;
    --color-fg-muted: #59657c;
    --color-border-line: #e9e1d2;
    --color-ok: #2f7c68;
    --color-warn: #a5843e;
    --color-bad: #b3261e;
    --cds-chart-categorical-1: #244c9a;
    --cds-chart-categorical-2: #c4a056;
    --cds-chart-categorical-3: #2f7c68;
    --cds-chart-categorical-4: #5d8fe0;
    --cds-chart-categorical-5: #a5843e;
    --cds-chart-categorical-6: #4d9a86;
    --cds-chart-categorical-7: #132650;
    --cds-chart-categorical-8: #d9bd78;
    --cds-chart-muted: #a7afc0;
    --cds-chart-grid: #eee8dc;
    --cds-chart-axis: #d3c9b6;
    --cds-chart-reference: #8a93a6;
    --cds-surface-popover: #ffffff;
    --cds-border: #e3d9c7;
    --cds-shadow-popover: 0 10px 28px rgba(10, 23, 51, 0.14);
    --cds-text-secondary: #59657c;
    --cds-gap-xs: 4px; --cds-gap-sm: 8px; --cds-gap-md: 12px; --cds-gap-lg: 16px; --cds-gap-xl: 24px;
    --cds-pad-xs: 4px; --cds-pad-sm: 8px; --cds-pad-md: 12px; --cds-pad-lg: 20px; --cds-pad-xl: 32px;
    --cds-radius: 12px;
    --cds-font-size-caption: 13px; --cds-font-size-body: 15.5px; --cds-font-size-heading: 17px; --cds-font-size-title: 30px;
    --cds-font-weight-medium: 500;
    --cds-dur-slow: 700ms;
    --cds-ease-out: cubic-bezier(0.2, 0.7, 0.2, 1);
    --font-anthropic-sans: "Geist", ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    --font-anthropic-serif: "Instrument Serif", Georgia, "Times New Roman", serif;
    --nav-bg: rgba(250, 247, 241, 0.88);
  }
  @media (prefers-color-scheme: dark) {
    :root {
      color-scheme: dark;
      --color-bg: #0a1733;
      --color-panel: #0d1d3f;
      --color-fg: #f1ebe0;
      --color-fg-muted: #a3aec4;
      --color-border-line: #1e3263;
      --color-ok: #6fbca6;
      --color-warn: #e8d3a0;
      --color-bad: #f08a80;
      --cds-chart-categorical-1: #6f9ce6;
      --cds-chart-categorical-2: #d9bd78;
      --cds-chart-categorical-3: #4d9a86;
      --cds-chart-categorical-4: #9dbcf2;
      --cds-chart-categorical-5: #c4a056;
      --cds-chart-categorical-6: #6fbca6;
      --cds-chart-categorical-7: #3567c4;
      --cds-chart-categorical-8: #f2e4c4;
      --cds-chart-muted: #4f5f86;
      --cds-chart-grid: #182a52;
      --cds-chart-axis: #2a4072;
      --cds-chart-reference: #7d89a6;
      --cds-surface-popover: #132650;
      --cds-border: #243d73;
      --cds-shadow-popover: 0 10px 28px rgba(0, 0, 0, 0.45);
      --cds-text-secondary: #a3aec4;
      --nav-bg: rgba(10, 23, 51, 0.86);
    }
  }
"""

EXTRA = """
<style>
  [hidden] { display: none !important; }
  html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
  @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
  body {
    margin: 0; background: var(--color-bg); color: var(--color-fg);
    font-family: var(--font-anthropic-sans); font-size: var(--cds-font-size-body); line-height: 1.5;
    -webkit-font-smoothing: antialiased;
  }
  .rel-wrap {
    max-width: 72rem; margin-inline: auto;
    padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
    padding-block: 0 calc(var(--cds-pad-xl) + env(safe-area-inset-bottom, 0px));
  }
  .rel-nav {
    position: sticky; top: 0; z-index: 20; backdrop-filter: saturate(1.4) blur(12px); -webkit-backdrop-filter: saturate(1.4) blur(12px);
    background: var(--nav-bg); border-bottom: 1px solid var(--color-border-line);
    padding-top: env(safe-area-inset-top, 0px);
  }
  .rel-nav-in {
    max-width: 72rem; margin-inline: auto; display: flex; align-items: center; gap: var(--cds-gap-lg);
    padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); min-height: 52px;
  }
  .rel-marca { font-family: var(--font-anthropic-serif); font-size: 19px; white-space: nowrap; color: var(--color-fg); text-decoration: none; }
  .rel-marca span { color: var(--cds-chart-categorical-2); }
  .rel-links { display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; margin-left: auto; padding-block: 8px; mask-image: linear-gradient(90deg, transparent 0, #000 12px, #000 calc(100% - 16px), transparent 100%); padding-inline: 12px; }
  .rel-links::-webkit-scrollbar { display: none; }
  .rel-links a {
    flex: none; font-size: 13px; color: var(--color-fg-muted); text-decoration: none; padding: 6px 12px; border-radius: 999px;
    border: 1px solid var(--color-border-line); background: var(--color-panel); min-height: 32px; box-sizing: border-box; display: inline-flex; align-items: center;
  }
  .rel-links a:hover, .rel-links a:focus-visible { color: var(--color-fg); border-color: var(--cds-chart-categorical-1); outline: none; }
  .lr { padding-block: var(--cds-pad-lg) 0; }
  .lr section, .lr header { scroll-margin-top: 72px; }
  .lr code { font-size: 0.9em; }

  /* Abertura no marinho do site, nos dois temas. */
  .lr-hero {
    --color-fg: #f1ebe0; --color-fg-muted: #b3bdd1; --color-border-line: rgba(241, 235, 224, 0.16);
    --cds-chart-grid: rgba(241, 235, 224, 0.12);
    --cds-chart-categorical-1: #6f9ce6; --cds-chart-categorical-2: #d9bd78;
    --lr-a: #e8d3a0;
    color: var(--color-fg); border: 0;
    background:
      radial-gradient(90% 120% at 100% 0%, rgba(93, 143, 224, 0.32) 0%, transparent 55%),
      radial-gradient(70% 110% at 0% 100%, rgba(196, 160, 86, 0.22) 0%, transparent 60%),
      linear-gradient(160deg, #132650 0%, #0a1733 70%);
    box-shadow: 0 18px 40px rgba(10, 23, 51, 0.18);
  }
  .lr-hero h1 { color: #ffffff; }
  .lr-hero .lr-sw--a { background: var(--cds-chart-categorical-1); }
  .lr-hero .lr-sw--b { background: var(--cds-chart-categorical-2); }
  .lr-hero .lr-ring-legend .lr-conv { border-top-color: rgba(241, 235, 224, 0.16); }

  .lr-tip { max-width: min(18rem, calc(100vw - 48px)); white-space: normal; }
  a { color: var(--cds-chart-categorical-1); }

  .rel-rodape { margin-top: var(--cds-gap-xl); padding-top: var(--cds-pad-lg); border-top: 1px solid var(--color-border-line); font-size: 12.5px; color: var(--color-fg-muted); display: grid; gap: 4px; }

  /* Celular */
  @container lr (max-width: 40rem) {
    .lr { gap: var(--cds-gap-xl); }
    .lr-hero { padding: 22px 18px; gap: var(--cds-gap-lg); border-radius: 18px; }
    .lr h1 { font-size: 34px; }
    .lr h2 { font-size: 26px; }
    .lr-ring { max-width: 9.5rem; }
    .lr-hero-ring { grid-template-columns: auto 1fr; align-items: center; justify-items: stretch; }
    .lr-kpis { grid-template-columns: 1fr 1fr; gap: 10px; }
    .lr-kpi { padding: 12px 14px 8px; }
    .lr-kpi:last-child { grid-column: 1 / -1; }
    .lr-kpi-value { font-size: 27px; }
    .lr-card { padding: 16px; }
    .lr-new { padding: 18px; }
    .lr-new-stats dd { font-size: 26px; }
    .lr-funnel-steps b { font-size: 22px; }
    .lr-funnel-steps span { font-size: 11.5px; }
    .lr-todo li { padding: 16px; }
  }
  @media (hover: none) { .lr-src-row, .lr-page, .lr-city { -webkit-tap-highlight-color: transparent; } }
</style>
"""

NAV = """<nav class="rel-nav" aria-label="Seções do relatório">
  <div class="rel-nav-in">
    <a class="rel-marca" href="#topo">Dr. Tércio Rocha <span>·</span> site</a>
    <div class="rel-links">
      <a href="#numeros">Números</a>
      <a href="#dia-a-dia">Dia a dia</a>
      <a href="#conversao">Conversão</a>
      <a href="#origens">Origens</a>
      <a href="#paginas">Páginas</a>
      <a href="#publico">Público</a>
      <a href="#ajustes">Ajustes</a>
    </div>
  </div>
</nav>
"""

RODAPE = """<footer class="rel-rodape">
  <span>Fonte: Google Analytics 4 da propriedade Dr Tércio Rocha. Período de 19 a 29 de outubro de 2026, extraído em 30 de outubro de 2026.</span>
  <span>Os totais contam todo o tráfego; mapa e cidades mostram só acessos do Brasil.</span>
</footer>
"""

SHIM = """<script>
  /* Os mesmos gráficos do painel ao vivo, lendo a foto dos dados em dados.js. */
  window.dash = (() => {
    const bruto = window.DADOS || {};
    const calculos = new Map();
    const cache = new Map();
    const desenhos = [];
    const data = (id) => {
      if (Object.prototype.hasOwnProperty.call(bruto, id)) return {status: 'ok', data: bruto[id]};
      const c = calculos.get(id);
      if (!c) return {status: 'missing', data: []};
      if (!cache.has(id)) {
        try { cache.set(id, c.fn(...c.inputs.map((i) => data(i).data))); } catch (e) { console.error(id, e); cache.set(id, null); }
      }
      const v = cache.get(id);
      return v == null ? {status: 'error', data: []} : {status: 'ok', data: v};
    };
    const run = () => desenhos.forEach(([nome, fn]) => {
      document.querySelectorAll(`[data-draw="${nome}"]`).forEach((el) => {
        try { fn(el); } catch (e) { console.error(nome, e); }
      });
    });
    return {data, run, calc: (id, def) => calculos.set(id, def), draw: (nome, fn) => desenhos.push([nome, fn]), colors: []};
  })();
</script>
"""

FINAL = """<script>
  dash.run();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => dash.run());
  let largura = window.innerWidth;
  let espera;
  window.addEventListener('resize', () => {
    if (window.innerWidth === largura) return;
    largura = window.innerWidth;
    clearTimeout(espera);
    espera = setTimeout(() => dash.run(), 150);
  });
  const fechar = () => document.querySelectorAll('.lr-tip').forEach((t) => { t.hidden = true; });
  document.addEventListener('pointerdown', (ev) => { if (!ev.target.closest('svg, .lr-tile')) fechar(); });
  window.addEventListener('scroll', fechar, {passive: true});
</script>
"""

# O estilo do painel fica no corpo; o rodapé entra no fim do .lr.
corpo = corpo.replace('<style>\n', '<style>\n' + TOKENS, 1)
fim_lr = corpo.index('<script>')
conteudo, scripts = corpo[:fim_lr], corpo[fim_lr:]
conteudo = conteudo.rstrip()
assert conteudo.endswith('</div>')
conteudo = conteudo[: -len('</div>')] + RODAPE + '</div>\n'

html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0a1733">
<title>Relatório do site · Dr. Tércio Rocha</title>
<meta name="description" content="Google Analytics 4 do site novo do Dr. Tércio Rocha, de 19 a 29 de outubro de 2026.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Instrument+Serif&display=swap">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230a1733'/%3E%3Cpath d='M8 22l5-6 4 3 7-9' fill='none' stroke='%23d9bd78' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">
</head>
<body>
{NAV}<main class="rel-wrap">
{conteudo}{EXTRA}</main>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script src="dados.js"></script>
{SHIM}{scripts.strip()}
{FINAL}</body>
</html>
"""

(AQUI / 'index.html').write_text(html, encoding='utf-8')
print('index.html', len(html.encode('utf-8')), 'bytes')
