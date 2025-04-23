The **Ecosystem Health Index (EHI)** is a methodology developed by the Tech Ecosystem Institute to assess the maturity and effectiveness of technology ecosystems. It evaluates a company across five core pillars, each representing a critical dimension of ecosystem development.

## Five Pillars of EHI

### 1. Partner Ecosystem
Evaluates the strength, breadth, and activation of strategic alliances, integrations, and co-marketing efforts.
- Quantity and quality of active partners
- Public partner listings and integrations
- Co-marketing or co-selling initiatives
- Presence in major marketplaces (e.g., Salesforce, AWS)

### 2. Developer Ecosystem
Measures how effectively a company supports and engages developers.
- API/SDK availability and documentation
- Developer portal maturity
- GitHub activity and stars
- Presence at developer events / hackathons

### 3. Customer Ecosystem
Assesses engagement, retention, and customer community vitality.
- Customer case studies and testimonials
- Referenceable customers
- Online user forums, Slack groups, or community spaces
- Public review ratings (e.g., G2, Capterra)

### 4. Employee Ecosystem
Evaluates workforce growth, satisfaction, and engagement.
- Glassdoor ratings and reviews
- LinkedIn headcount growth
- Employee engagement initiatives
- Hiring momentum and open roles

### 5. Community Ecosystem
Assesses the company’s presence and impact in the broader tech and industry community.
- Open source contributions
- Speaking appearances and thought leadership
- Participation in standards groups or consortiums
- Content and engagement on social platforms

## 📂 Repo Structure
- `ehi/` – Core scoring logic and config
- `scripts/` – Run EHI reports
- `data/` – Input CSVs (e.g., company data)
- `results/` – Output files
- `notebooks/` – Exploratory analysis
- `docs/` – Methodology explanation
- `tests/` – Unit tests

## 🧪 Quickstart
```bash
pip install -r requirements.txt
python scripts/run_ehi_report.py --input data/example_companies.csv
