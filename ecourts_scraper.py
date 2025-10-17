# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# from datetime import datetime
# import requests
# import time
# import json
# import re
# import os

# # === Setup browser ===
# driver = webdriver.Chrome()
# driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")
# time.sleep(2)

# # === Click on CNR tab ===
# driver.find_element(By.LINK_TEXT, "CNR Number").click()
# time.sleep(1)

# # === Enter CNR number ===
# cnr_number = "BRBU110025272016"
# cnr_input = driver.find_element(By.ID, "cino")
# cnr_input.send_keys(cnr_number)

# # === Wait for CAPTCHA ===
# input("🧠 Solve CAPTCHA in browser and press Enter here...")

# # === Submit form ===
# driver.find_element(By.ID, "searchbtn").click()
# time.sleep(3)

# # === Parse page content ===
# soup = BeautifulSoup(driver.page_source, 'html.parser')

# def extract(label_keywords):
#     for row in soup.find_all('tr'):
#         cells = row.find_all('td')
#         if len(cells) >= 2:
#             label = cells[0].get_text(strip=True)
#             value = cells[1].get_text(strip=True)
#             if any(keyword.lower() in label.lower() for keyword in label_keywords):
#                 return value
#     return None

# # === Extract FIR details ===
# fir_details = {}
# fir_table = soup.find('table', class_='order_table')
# if fir_table:
#     for row in fir_table.find_all('tr'):
#         cells = row.find_all('td')
#         if len(cells) >= 2:
#             key = cells[0].get_text(strip=True)
#             value = cells[1].get_text(strip=True)
#             fir_details[key.lower().replace(" ", "_")] = value

# # === Extract Acts and Sections ===
# acts = {}
# acts_table = soup.find('table', string=lambda s: s and "Under Act(s)" in s)
# if acts_table:
#     for row in acts_table.find_all('tr'):
#         cells = row.find_all('td')
#         if len(cells) >= 2:
#             act = cells[0].get_text(strip=True)
#             sections = cells[1].get_text(strip=True).split(',')
#             acts["act"] = act
#             acts["sections"] = [s.strip() for s in sections]

# # === Extract Parties ===
# def extract_party(role):
#     block = soup.find('td', string=lambda s: s and role in s)
#     if block:
#         parent = block.find_parent('tr')
#         cells = parent.find_all('td')
#         if len(cells) >= 2:
#             name = cells[1].get_text(strip=True)
#             advocate = None
#             if "Advocate-" in name:
#                 parts = name.split("Advocate-")
#                 name = parts[0].strip()
#                 advocate = parts[1].strip()
#             return {"name": name, "advocate": advocate}
#     return {}

# # === Extract Case History ===
# case_history = []
# history_table = soup.find('table', string=lambda s: s and "Case History" in s)
# if history_table:
#     for row in history_table.find_all('tr')[1:]:
#         cells = row.find_all('td')
#         if len(cells) >= 3:
#             case_history.append({
#                 "judge": cells[0].get_text(strip=True),
#                 "business_date": cells[1].get_text(strip=True),
#                 "hearing_date": cells[2].get_text(strip=True),
#                 "purpose": cells[3].get_text(strip=True) if len(cells) > 3 else None
#             })

# # === Extract Final Orders and Download PDFs ===
# final_orders = []
# os.makedirs("downloads", exist_ok=True)

# order_table = soup.find('table', class_='order_table')
# if order_table:
#     for row in order_table.find_all('tr')[1:]:
#         cells = row.find_all('td')
#         if len(cells) >= 3:
#             order_number = cells[0].get_text(strip=True)
#             order_date = cells[1].get_text(strip=True)
#             order_title = cells[2].get_text(strip=True)
#             pdf_tag = row.find('a', onclick=True)
#             pdf_url = None
#             if pdf_tag:
#                 onclick_text = pdf_tag['onclick']
#                 match = re.search(r"filename=(.*?)&", onclick_text)
#                 if match:
#                     filename = match.group(1).replace("&amp;", "&")
#                     pdf_url = f"https://services.ecourts.gov.in/ecourtindia_v6/home/display_pdf?filename={filename}"
#                     try:
#                         pdf_data = requests.get(pdf_url).content
#                         pdf_filename = f"downloads/{cnr_number}_order_{order_number}.pdf"
#                         with open(pdf_filename, "wb") as f:
#                             f.write(pdf_data)
#                         print(f"📄 Downloaded: {pdf_filename}")
#                     except Exception as e:
#                         print(f"❌ Failed to download PDF for order {order_number}: {e}")
#             final_orders.append({
#                 "order_number": order_number,
#                 "order_date": order_date,
#                 "order_title": order_title,
#                 "pdf_url": pdf_url
#             })

# # === Build final case info ===
# case_info = {
#     "cnr": cnr_number,
#     "case_type": extract(["Case Type"]),
#     "filing": {
#         "number": extract(["Filing Number"]),
#         "date": extract(["Filing Date"])
#     },
#     "registration": {
#         "number": extract(["Registration Number"]),
#         "date": extract(["Registration Date"])
#     },
#     "decision_date": extract(["Decision Date"]),
#     "first_hearing_date": extract(["First Hearing Date"]),
#     "case_status": extract(["Case Status"]),
#     "disposal_nature": extract(["Nature of Disposal"]),
#     "court_number_and_judge": extract(["Court Number and Judge"]),
#     "petitioner": extract_party("Petitioner"),
#     "respondent": extract_party("Respondent"),
#     "acts": acts,
#     "fir_details": fir_details,
#     "case_history": case_history,
#     "final_orders": final_orders,
#     "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# }

# # === Save as JSON ===
# with open("full_case_details.json", "w") as f:
#     json.dump(case_info, f, indent=2)
# print("📝 Saved full case details to full_case_details.json")

# # === Show on console ===
# print("\n🔍 Case Info:")
# print(json.dumps(case_info, indent=2))

# driver.quit()


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fpdf import FPDF
import time
import json
import os

# === Setup Chrome with PDF download preferences ===
download_dir = os.path.abspath("downloads")
os.makedirs(download_dir, exist_ok=True)

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "plugins.always_open_pdf_externally": True,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
})

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")
time.sleep(2)

# === Click on CNR tab ===
driver.find_element(By.LINK_TEXT, "CNR Number").click()
time.sleep(1)

# === Enter CNR number ===
#cnr_number = "BRBU110025272017"
cnr_number = input("Please enter CNR : ")
driver.find_element(By.ID, "cino").send_keys(cnr_number)

# === Wait for CAPTCHA ===
input("🧠 Solve CAPTCHA in browser and press Enter here...")

# === Submit form ===
driver.find_element(By.ID, "searchbtn").click()
time.sleep(3)

# === Parse page content ===
soup = BeautifulSoup(driver.page_source, 'html.parser')

# === Extract all tables ===
tables = soup.find_all('table')
all_tables = []

for table in tables:
    rows = []
    for row in table.find_all('tr'):
        cells = row.find_all(['td', 'th'])
        row_data = [cell.get_text(strip=True) for cell in cells]
        if row_data:
            rows.append(row_data)
    if rows:
        all_tables.append(rows)

# === Save as JSON ===
json_data = {
    "cnr": cnr_number,
    "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    "tables": all_tables
}

with open("case_tables.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)
print("📝 Saved all tables to case_tables.json")
print("\n🔍 Full JSON Output:")
print(json.dumps(json_data, indent=2, ensure_ascii=False))

# === Save as PDF ===
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=11)

pdf.cell(200, 10, txt=f"Case Tables for CNR: {cnr_number}", ln=True, align='C')
pdf.ln(5)

for idx, table in enumerate(all_tables, start=1):
    pdf.set_font("Arial", style='B', size=11)
    pdf.cell(200, 10, txt=f"Table {idx}", ln=True)
    pdf.set_font("Arial", size=10)
    for row in table:
        line = " | ".join(row)
        pdf.multi_cell(0, 8, line)
    pdf.ln(5)

pdf.output("case_tables.pdf")
print("📄 Saved all tables to case_tables.pdf")

driver.quit()
