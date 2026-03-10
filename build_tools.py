import re
import json

def extract_array(content, array_name):
    # Match the pattern `const arrayName = [` up to the matching closing bracket
    match = re.search(r"const\s+" + array_name + r"\s*=\s*(\[.*?\]);", content, re.DOTALL)
    if not match:
        return []

    array_str = match.group(1)

    # Clean up the string to be valid JSON if possible, or we can just parse it directly since it's JS.
    # Actually, a simpler approach is to extract the fields with regex since it's a consistent format.
    items = []

    # This regex looks for { key: "value", ... }
    item_matches = re.finditer(r"\{\s*emoji:\s*\"(.*?)\",\s*name:\s*\"(.*?)\",\s*slug:\s*\"(.*?)\",\s*desc:\s*\"(.*?)\"\s*\}", array_str)

    for item_match in item_matches:
        emoji = item_match.group(1)
        name = item_match.group(2)
        slug = item_match.group(3)
        desc = item_match.group(4)
        items.append({
            "emoji": emoji,
            "name": name,
            "slug": slug,
            "desc": desc
        })

    return items

def main():
    with open('src/pages/index.astro', 'r') as f:
        content = f.read()

    tools = extract_array(content, "tools")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>All Tools - ijustwantto.live</title>
  <meta name="description" content="A comprehensive list of all health, fitness, and DIY tools and calculators available on ijustwantto.live.">
  <link rel="canonical" href="https://ijustwantto.live/tools/">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap" rel="stylesheet">

  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-G86C7NJG3F"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-G86C7NJG3F');
  </script>

  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: 'Inter', -apple-system, sans-serif;
      background: #060a12;
      color: #c8d0de;
      line-height: 1.6;
    }}

    /* Hero */
    .hero {{
      text-align: center;
      padding: 100px 24px 70px;
      background: linear-gradient(180deg, #0a1a15 0%, #060a12 100%);
      position: relative;
    }}
    .hero::before {{
      content: '';
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at 50% 40%, rgba(45,184,154,0.08) 0%, transparent 60%);
    }}
    .hero-content {{ position: relative; z-index: 1; }}
    .hero .tagline {{
      color: #2DB89A;
      font-size: 0.85rem;
      font-weight: 700;
      letter-spacing: 3px;
      text-transform: uppercase;
      margin-bottom: 16px;
    }}
    .hero h1 {{
      font-size: 3rem;
      font-weight: 900;
      letter-spacing: -1.5px;
      margin-bottom: 20px;
      background: linear-gradient(135deg, #fff 0%, #2DB89A 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .search-container {{
      max-width: 500px;
      margin: 30px auto 0;
      position: relative;
    }}
    #search-input {{
      width: 100%;
      padding: 16px 20px 16px 48px;
      font-size: 1rem;
      background: #0c1410;
      border: 1px solid #1a2a24;
      border-radius: 30px;
      color: #fff;
      font-family: 'Inter', sans-serif;
      transition: all 0.2s ease;
    }}
    #search-input:focus {{
      outline: none;
      border-color: #2DB89A;
      box-shadow: 0 0 0 3px rgba(45, 184, 154, 0.2);
    }}
    #search-input::placeholder {{
      color: #5a6a80;
    }}
    .search-icon {{
      position: absolute;
      left: 18px;
      top: 50%;
      transform: translateY(-50%);
      color: #5a6a80;
    }}

    /* Sections */
    .section-container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 40px 24px 80px;
    }}
    .section-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 30px;
      border-bottom: 1px solid #1a2a24;
      padding-bottom: 15px;
    }}
    .section-title {{
      font-size: 1.8rem;
      font-weight: 800;
      color: #fff;
    }}
    #tools-count {{
      color: #5a6a80;
      font-size: 1rem;
      font-weight: 600;
      background: #111318;
      padding: 6px 14px;
      border-radius: 20px;
      border: 1px solid #1e2030;
    }}

    /* Tools Grid */
    #tools-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
    }}
    .tool-card {{
      background: #111318;
      border: 1px solid #1e2030;
      border-radius: 12px;
      padding: 20px;
      text-decoration: none;
      color: inherit;
      display: block;
      transition: all 0.2s ease;
    }}
    .tool-card:hover {{
      border-color: #2DB89A;
      transform: translateY(-2px);
    }}
    .tool-emoji {{
      font-size: 1.4rem;
      margin-bottom: 8px;
      display: block;
    }}
    .tool-name {{
      font-size: 0.95rem;
      font-weight: 700;
      color: #e0e8f0;
      margin-bottom: 6px;
    }}
    .tool-desc {{
      font-size: 0.8rem;
      color: #6a7a90;
      line-height: 1.4;
    }}

    .no-results {{
      grid-column: 1 / -1;
      text-align: center;
      padding: 60px 20px;
      background: #111318;
      border: 1px dashed #1e2030;
      border-radius: 12px;
      color: #5a6a80;
      display: none;
    }}

    /* Footer */
    .footer {{
      text-align: center;
      padding: 50px 24px;
      font-size: 0.85rem;
      color: #3a4a5a;
      border-top: 1px solid #151f2e;
      background: #040810;
    }}
    .footer a {{
      color: #2DB89A;
      text-decoration: none;
    }}
    .footer a:hover {{
      text-decoration: underline;
    }}

    /* Responsive */
    @media (max-width: 768px) {{
      .hero h1 {{ font-size: 2.2rem; }}
      .hero {{ padding: 80px 20px 50px; }}
      .section-container {{ padding: 20px 20px 60px; }}
      #tools-grid {{ grid-template-columns: 1fr; }}
      .section-header {{ flex-direction: column; align-items: flex-start; gap: 10px; }}
    }}
  </style>
</head>
<body>
  <script src="/nav.js"></script>

  <!-- Hero -->
  <div class="hero">
    <div class="hero-content">
      <div class="tagline">Explore All</div>
      <h1>Life Tools & Calculators</h1>

      <div class="search-container">
        <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" id="search-input" placeholder="Search by name or description...">
      </div>
    </div>
  </div>

  <div class="section-container">
    <div class="section-header">
      <h2 class="section-title">All Tools</h2>
      <span id="tools-count"></span>
    </div>

    <div id="tools-grid"></div>
    <div id="no-results" class="no-results">
      <div style="font-size: 2rem; margin-bottom: 10px;">🔍</div>
      <p>No tools found matching your search.</p>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    © <span id="year"></span> <a href="/">ijustwantto.live</a> · A <a href="https://gab.ae">GAB Ventures</a> property
  </div>

  <script>
    document.getElementById('year').textContent = new Date().getFullYear();

    const toolsData = {json.dumps(tools)};

    const toolsGrid = document.getElementById('tools-grid');
    const toolsCount = document.getElementById('tools-count');
    const searchInput = document.getElementById('search-input');
    const noResults = document.getElementById('no-results');

    function renderTools(tools) {{
      toolsGrid.innerHTML = '';

      if (tools.length === 0) {{
        noResults.style.display = 'block';
      }} else {{
        noResults.style.display = 'none';

        tools.forEach(tool => {{
          const a = document.createElement('a');
          a.className = 'tool-card';
          a.href = tool.slug;

          a.innerHTML = `
            <span class="tool-emoji">${{tool.emoji}}</span>
            <h3 class="tool-name">${{tool.name}}</h3>
            <p class="tool-desc">${{tool.desc}}</p>
          `;

          toolsGrid.appendChild(a);
        }});
      }}

      toolsCount.textContent = `${{tools.length}} tool${{tools.length === 1 ? '' : 's'}}`;
    }}

    // Initial render
    renderTools(toolsData);

    // Search functionality
    searchInput.addEventListener('input', (e) => {{
      const query = e.target.value.toLowerCase();

      const filteredTools = toolsData.filter(tool =>
        tool.name.toLowerCase().includes(query) ||
        tool.desc.toLowerCase().includes(query)
      );

      renderTools(filteredTools);
    }});
  </script>
</body>
</html>
"""

    with open('public/tools/index.html', 'w') as f:
        f.write(html_content)

if __name__ == '__main__':
    main()
