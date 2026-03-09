import re

with open('src/pages/index.astro', 'r') as f:
    content = f.read()

# Replace empty studies array
new_studies = """// Studies
const studies = [
  {
    title: "Average Electricity Cost by State 2026",
    subtitle: "50 items analyzed",
    slug: "/electricity-costs",
    stat: "16¢",
    statLabel: "National Average",
    desc: "A comprehensive breakdown of residential electricity rates across all 50 US states with nulls properly handled.",
    tag: "ORIGINAL RESEARCH"
  }
];"""

content = re.sub(r'// Studies \(none for this domain\)\nconst studies = \[[\s\S]*?\];', new_studies, content)

with open('src/pages/index.astro', 'w') as f:
    f.write(content)
