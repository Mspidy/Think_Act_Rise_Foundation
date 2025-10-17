# 🏛️ eCourts Case Scraper

This project automates the extraction of case details from the Indian eCourts portal using a valid CNR number. It retrieves all available tables from the case page and saves the data in both **JSON** and **PDF** formats for easy access and documentation.

---

## 🚀 Features

- ✅ Automates browser interaction using Selenium
- ✅ Supports manual CAPTCHA verification
- ✅ Extracts all tables from the case detail page
- ✅ Saves structured data in `.json` format
- ✅ Generates a readable `.pdf` summary of all tables
- ✅ Stores output locally for archiving or sharing

---

## 🧰 Technologies Used

- **Python 3**
- **Selenium** — for browser automation
- **BeautifulSoup** — for HTML parsing
- **FPDF** — for PDF generation
- **Chrome WebDriver**

---

## 📦 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ecourts-scraper.git
   cd ecourts-scraper
2. Create and activate a virtual environment:


python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

3. Install dependencies:

bash
pip install -r requirements.txt


4.Run the scraper:

bash
python ecourts_scraper.py
