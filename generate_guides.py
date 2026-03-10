import re
import json

def extract_array(content, array_name):
    # Match the entire array declaration const array_name = [ ... ];
    # Using non-greedy match to grab just the array
    pattern = r"const\s+" + array_name + r"\s*=\s*\[(.*?)\];"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return []

    array_content = match.group(1)
    # Parse individual objects. This is a bit tricky with regex, let's just find all { ... }
    items = []
    # Find all { ... } blocks
    object_matches = re.findall(r"\{[^{}]+\}", array_content)

    for obj_str in object_matches:
        item = {}
        # Extract fields
        emoji_match = re.search(r'emoji:\s*["\']([^"\']+)["\']', obj_str)
        name_match = re.search(r'name:\s*["\']([^"\']+)["\']', obj_str)
        slug_match = re.search(r'slug:\s*["\']([^"\']+)["\']', obj_str)
        desc_match = re.search(r'desc:\s*["\']([^"\']+)["\']', obj_str)

        if name_match and slug_match:
            item['emoji'] = emoji_match.group(1) if emoji_match else ""
            item['name'] = name_match.group(1)
            item['slug'] = slug_match.group(1)
            item['desc'] = desc_match.group(1) if desc_match else ""
            items.append(item)

    return items

def generate_html(all_guides):
    # HTML template based on the requirement

    cards_html = ""
    for guide in all_guides:
        emoji = guide.get("emoji", "")
        name = guide.get("name", "")
        desc = guide.get("desc", "")
        slug = guide.get("slug", "")

        cards_html += f"""
        <a class="guide-card" href="{slug}">
          <span class="guide-emoji">{emoji}</span>
          <h3 class="guide-name">{name}</h3>
          <p class="guide-desc">{desc}</p>
        </a>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-G86C7NJG3F"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-G86C7NJG3F');</script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>All Guides & Tools - ijustwantto.live</title>
  <meta name="description" content="A complete collection of all guides, calculators, and tools available on ijustwantto.live.">
  <link rel="canonical" href="https://ijustwantto.live/guides/">

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');

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
      padding: 100px 24px 50px;
      background: linear-gradient(180deg, #0a1a15 0%, #060a12 100%);
      position: relative;
    }}
    .hero::before {{
      content: '';
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at 50% 40%, rgba(45,184,154,0.08) 0%, transparent 60%);
    }}
    .hero-content {{ position: relative; z-index: 1; max-width: 800px; margin: 0 auto; }}
    .hero h1 {{
      font-size: 3rem;
      font-weight: 900;
      letter-spacing: -1.5px;
      margin-bottom: 20px;
      background: linear-gradient(135deg, #fff 0%, #2DB89A 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    /* Search Box */
    .search-container {{
      margin: 30px auto;
      max-width: 500px;
      position: relative;
    }}
    .search-input {{
      width: 100%;
      padding: 16px 20px 16px 50px;
      border-radius: 30px;
      border: 1px solid #1e2030;
      background: #111318;
      color: #fff;
      font-size: 1.05rem;
      font-family: 'Inter', sans-serif;
      outline: none;
      transition: border-color 0.2s;
    }}
    .search-input:focus {{
      border-color: #2DB89A;
    }}
    .search-icon {{
      position: absolute;
      left: 20px;
      top: 50%;
      transform: translateY(-50%);
      color: #5a6a80;
    }}

    .counter {{
      color: #5a6a80;
      font-size: 0.95rem;
      font-weight: 500;
      margin-bottom: 40px;
    }}

    /* Guides Grid */
    .section-container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 24px 80px;
    }}
    .guides-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 20px;
    }}
    .guide-card {{
      background: #111318;
      border: 1px solid #1e2030;
      border-radius: 12px;
      padding: 24px 20px;
      text-decoration: none;
      color: inherit;
      display: block;
      transition: all 0.2s ease;
    }}
    .guide-card:hover {{
      border-color: #2DB89A;
      transform: translateY(-2px);
    }}
    .guide-emoji {{
      font-size: 1.5rem;
      margin-bottom: 10px;
      display: block;
    }}
    .guide-name {{
      font-size: 1rem;
      font-weight: 700;
      color: #e0e8f0;
      margin-bottom: 6px;
    }}
    .guide-desc {{
      font-size: 0.85rem;
      color: #6a7a90;
      line-height: 1.4;
    }}

    /* No Results */
    .no-results {{
      text-align: center;
      padding: 40px;
      color: #5a6a80;
      font-size: 1.1rem;
      display: none;
      grid-column: 1 / -1;
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
      .hero {{ padding: 70px 20px 40px; }}
      .guides-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <script src="/nav.js"></script>

  <div class="hero">
    <div class="hero-content">
      <h1>Guides & Tools</h1>

      <div class="search-container">
        <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input type="text" id="searchInput" class="search-input" placeholder="Search guides, tools, and calculators...">
      </div>

      <div class="counter" id="counter">{len(all_guides)} guides</div>
    </div>
  </div>

  <div class="section-container">
    <div class="guides-grid" id="guidesGrid">
      {cards_html}
      <div class="no-results" id="noResults">No guides found matching your search.</div>
    </div>
  </div>

  <div class="footer">
    © 2026 <a href="/">ijustwantto.live</a> · A <a href="https://gab.ae">GAB Ventures</a> property
  </div>

  <script>
    document.addEventListener('DOMContentLoaded', function() {{
      const searchInput = document.getElementById('searchInput');
      const guidesGrid = document.getElementById('guidesGrid');
      const cards = guidesGrid.querySelectorAll('.guide-card');
      const counter = document.getElementById('counter');
      const noResults = document.getElementById('noResults');

      searchInput.addEventListener('input', function() {{
        const searchTerm = this.value.toLowerCase().trim();
        let visibleCount = 0;

        cards.forEach(card => {{
          const name = card.querySelector('.guide-name').textContent.toLowerCase();
          const desc = card.querySelector('.guide-desc').textContent.toLowerCase();

          if (name.includes(searchTerm) || desc.includes(searchTerm)) {{
            card.style.display = 'block';
            visibleCount++;
          }} else {{
            card.style.display = 'none';
          }}
        }});

        // Update counter
        counter.textContent = visibleCount === 1 ? '1 guide' : visibleCount + ' guides';

        // Show/hide no results message
        if (visibleCount === 0) {{
          noResults.style.display = 'block';
        }} else {{
          noResults.style.display = 'none';
        }}
      }});
    }});
  </script>
</body>
</html>
"""
    return html

def main():
    with open("src/pages/index.astro", "r") as f:
        content = f.read()

    tools = extract_array(content, "tools")
    guides = extract_array(content, "guides")
    lists = extract_array(content, "lists")

    # "listing ALL guides from the index.astro arrays" -> I'll combine them all as requested
    all_items = tools + guides + lists

    html = generate_html(all_items)

    import os
    os.makedirs("public/guides", exist_ok=True)
    with open("public/guides/index.html", "w") as f:
        f.write(html)

    print(f"Generated public/guides/index.html with {len(all_items)} items.")

if __name__ == "__main__":
    main()
