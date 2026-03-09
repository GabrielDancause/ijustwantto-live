const fs = require('fs');
const filepath = 'src/pages/index.astro';
let content = fs.readFileSync(filepath, 'utf8');

if (!content.includes('studies.map(')) {
  const insertIndex = content.indexOf('<!-- Guides Section -->');
  if (insertIndex !== -1) {
    const studiesHTML = `
  <!-- Studies Section -->
  {studies.length > 0 && (
    <div class="section-container">
      <div class="section-header">
        <span class="section-tag">🔬 ORIGINAL RESEARCH</span>
        <h2 class="section-title">Studies & Reports</h2>
        <p class="section-sub">Data-driven analysis and insights.</p>
      </div>
      <div class="studies-grid" style="display: grid; grid-template-columns: 1fr; gap: 20px; margin-bottom: 40px;">
        {studies.map(study => (
          <a class="study-card" href={study.slug} style="background: #0c1410; border: 1px solid #1a2a24; border-radius: 14px; padding: 32px; text-decoration: none; color: inherit; display: flex; flex-direction: column; gap: 16px; transition: all 0.2s ease;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
              <div>
                <span style="color: #2DB89A; font-size: 0.75rem; font-weight: 800; letter-spacing: 1px;">{study.tag}</span>
                <h3 style="font-size: 1.5rem; font-weight: 800; color: #fff; margin-top: 8px;">{study.title}</h3>
                <p style="color: #6a7a90; font-size: 0.95rem; margin-top: 4px;">{study.subtitle}</p>
              </div>
              <div style="text-align: right; background: rgba(45,184,154,0.1); padding: 12px 20px; border-radius: 8px;">
                <div style="color: #fff; font-size: 1.8rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; line-height: 1;">{study.stat}</div>
                <div style="color: #2DB89A; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-top: 4px;">{study.statLabel}</div>
              </div>
            </div>
            <p style="color: #e0e8f0; font-size: 1.05rem; line-height: 1.6; padding-top: 16px; border-top: 1px solid #1a2a24;">{study.desc}</p>
          </a>
        ))}
      </div>
    </div>
  )}

`;
    content = content.slice(0, insertIndex) + studiesHTML + content.slice(insertIndex);
    fs.writeFileSync(filepath, content, 'utf8');
    console.log('Homepage studies HTML injected');
  }
}
