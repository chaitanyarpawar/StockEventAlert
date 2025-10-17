# #
# # from selenium import webdriver
# # from selenium.webdriver.chrome.service import Service
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.chrome.options import Options
# # from webdriver_manager.chrome import ChromeDriverManager
# # import pandas as pd
# # import time
# # import os
# # import requests
# # import re
# #
# # def get_nse_price_and_index(symbol):
# #     """Fetch current price and index membership from NSE."""
# #     try:
# #         headers = {"User-Agent": "Mozilla/5.0"}
# #         session = requests.Session()
# #         session.get("https://www.nseindia.com", headers=headers)
# #
# #         # Fetch live quote
# #         quote_url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
# #         res = session.get(quote_url, headers=headers, timeout=5)
# #         if res.status_code != 200:
# #             return None, None
# #
# #         data = res.json()
# #         price = data.get("priceInfo", {}).get("lastPrice", "")
# #
# #         # Identify Nifty50 / BankNifty membership
# #         index_list = []
# #         for idx_name in ["NIFTY 50", "NIFTY BANK"]:
# #             index_url = f"https://www.nseindia.com/api/equity-stockIndices?index={idx_name.replace(' ', '%20')}"
# #             idx_res = session.get(index_url, headers=headers)
# #             if idx_res.status_code == 200:
# #                 idx_data = idx_res.json()
# #                 stocks = [s["symbol"] for s in idx_data.get("data", [])]
# #                 if symbol in stocks:
# #                     index_list.append(idx_name)
# #
# #         index = ", ".join(index_list) if index_list else "Other"
# #         return price, index
# #     except Exception:
# #         return None, None
# #
# # def classify_event(purpose):
# #     """Classify Purpose into Event Type and extract Ratio/Dividend."""
# #     event_type, ratio, dividend = "", "", ""
# #     purpose_lower = str(purpose).lower()
# #
# #     if "right" in purpose_lower:
# #         event_type = "Right"
# #     elif "split" in purpose_lower:
# #         event_type = "Split"
# #         match = re.search(r'from\s*rs\.?(\d+)[/-]*\s*to\s*rs\.?(\d+)', purpose_lower)
# #         if match:
# #             ratio = f"{match.group(1)}:{match.group(2)}"
# #     elif "spin off" in purpose_lower or "demerger" in purpose_lower:
# #         event_type = "Demerger"
# #     elif "bonus" in purpose_lower:
# #         event_type = "Bonus"
# #         match = re.search(r'(\d+[:/]\d+)', purpose)
# #         if match:
# #             ratio = match.group(1).replace("/", ":")
# #     elif "interim dividend" in purpose_lower or "final dividend" in purpose_lower or "dividend" in purpose_lower:
# #         event_type = "Dividend"
# #         match = re.search(r'rs\.?\s*[-:]?\s*(\d+\.?\d*)', purpose_lower)
# #         if match:
# #             dividend = match.group(1)
# #
# #     return event_type, ratio, dividend
# #
# # def download_bse_csv():
# #     """Download Corporate Actions CSV from BSE."""
# #     url = "https://www.bseindia.com/corporates/corporates_act.html"
# #     options = Options()
# #     options.add_argument("--no-sandbox")
# #     options.add_argument("--disable-dev-shm-usage")
# #
# #     print("🌐 Launching Chrome to get BSE Corporate Actions file...")
# #     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# #     driver.get(url)
# #     time.sleep(5)
# #
# #     # Click Download button
# #     print("📥 Downloading CSV...")
# #     driver.find_element(By.XPATH, '//*[@id="lnkDownload"]').click()
# #     time.sleep(7)
# #     driver.quit()
# #
# #     # Locate downloaded CSV
# #     download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
# #     latest_file = max([os.path.join(download_dir, f) for f in os.listdir(download_dir)], key=os.path.getctime)
# #     print(f"📂 Downloaded file: {latest_file}")
# #
# #     # Move file to script folder
# #     new_path = os.path.join(os.getcwd(), "corporate-events.csv")
# #     os.replace(latest_file, new_path)
# #     print(f"✅ File moved to: {new_path}")
# #     return new_path
# #
# # def process_bse_csv(csv_file):
# #     """Clean, classify and enrich CSV file."""
# #     df = pd.read_csv(csv_file)
# #
# #     # Rename columns
# #     df.rename(columns={
# #         "Company Name": "Stock Name",
# #         "Ex Date": "Ex-Date"
# #     }, inplace=True)
# #
# #     # Add missing columns
# #     required_cols = ["Event Type", "Ratio", "Dividend", "Last Price", "Index"]
# #     for col in required_cols:
# #         if col not in df.columns:
# #             df[col] = ""
# #
# #     # Classify event types
# #     print("🔍 Classifying corporate events...")
# #     for i, row in df.iterrows():
# #         purpose = str(row["Purpose"])
# #         event_type, ratio, dividend = classify_event(purpose)
# #         df.at[i, "Event Type"] = event_type
# #         df.at[i, "Ratio"] = ratio
# #         df.at[i, "Dividend"] = dividend
# #
# #     # Fetch NSE price & index
# #     print("💰 Fetching Last Price and Index from NSE...")
# #     for i, row in df.iterrows():
# #         stock = str(row["Stock Name"]).split()[0].upper().replace("&", "AND")
# #         price, index = get_nse_price_and_index(stock)
# #         if price:
# #             df.at[i, "Last Price"] = price
# #             df.at[i, "Index"] = index
# #         print(f"{stock}: ₹{price} | {index}")
# #         time.sleep(1)
# #
# #     # Save output
# #     output_file = "corporate-events.csv"
# #     df.to_csv(output_file, index=False, encoding="utf-8-sig")
# #     print(f"✅ Updated file saved as: {output_file}")
# #
# # def main():
# #     csv_path = download_bse_csv()
# #     process_bse_csv(csv_path)
# #
# # if __name__ == "__main__":
# #     main()
#
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import pandas as pd
# import time
# import os
# import requests
# import re
#
# # ----------------------------------------
# # 🏦 Fetch live NSE price and index details
# # ----------------------------------------
# def get_nse_price_and_index(symbol):
#     """Fetch current price and index membership from NSE."""
#     try:
#         headers = {"User-Agent": "Mozilla/5.0"}
#         session = requests.Session()
#         session.get("https://www.nseindia.com", headers=headers)
#
#         # Fetch live quote
#         quote_url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
#         res = session.get(quote_url, headers=headers, timeout=5)
#         if res.status_code != 200:
#             return None, None
#
#         data = res.json()
#         price = data.get("priceInfo", {}).get("lastPrice", "")
#
#         # Identify Nifty50 / BankNifty membership
#         index_list = []
#         for idx_name in ["NIFTY 50", "NIFTY BANK"]:
#             index_url = f"https://www.nseindia.com/api/equity-stockIndices?index={idx_name.replace(' ', '%20')}"
#             idx_res = session.get(index_url, headers=headers)
#             if idx_res.status_code == 200:
#                 idx_data = idx_res.json()
#                 stocks = [s["symbol"] for s in idx_data.get("data", [])]
#                 if symbol in stocks:
#                     index_list.append(idx_name)
#
#         index = ", ".join(index_list) if index_list else "Other"
#         return price, index
#     except Exception:
#         return None, None
#
#
# # ----------------------------------------
# # 🧩 Classify purpose into Event Type + Ratio + Dividend
# # ----------------------------------------
# def classify_event(purpose):
#     """Classify Purpose into Event Type and extract Ratio/Dividend."""
#     event_type, ratio, dividend = "", "", ""
#     purpose_lower = str(purpose).lower()
#
#     if "right" in purpose_lower:
#         event_type = "Right"
#
#     elif "split" in purpose_lower:
#         event_type = "Split"
#         match = re.search(r'from\s*rs\.?(\d+)[/-]*\s*to\s*rs\.?(\d+)', purpose_lower)
#         if match:
#             ratio = f"{match.group(1)}:{match.group(2)}"
#
#     elif "spin off" in purpose_lower or "demerger" in purpose_lower:
#         event_type = "Demerger"
#
#     elif "bonus" in purpose_lower:
#         event_type = "Bonus"
#         match = re.search(r'(\d+[:/]\d+)', purpose)
#         if match:
#             ratio = match.group(1).replace("/", ":")
#
#     elif "interim dividend" in purpose_lower or "final dividend" in purpose_lower or "dividend" in purpose_lower:
#         event_type = "Dividend"
#         match = re.search(r'rs\.?\s*[-:]?\s*(\d+\.?\d*)', purpose_lower)
#         if match:
#             dividend = match.group(1)
#
#     return event_type, ratio, dividend
#
#
# # ----------------------------------------
# # 📥 Download Corporate Actions CSV from BSE
# # ----------------------------------------
# def download_bse_csv():
#     """Download Corporate Actions CSV from BSE."""
#     url = "https://www.bseindia.com/corporates/corporates_act.html"
#     options = Options()
#     options.add_argument("--headless=new")  # uncomment for server/GitHub
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--window-size=1920,1080")
#
#     print("🌐 Launching Chrome to get BSE Corporate Actions file...")
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     driver.get(url)
#     wait = WebDriverWait(driver, 20)
#
#     try:
#         # Remove popups blocking the click
#         driver.execute_script("""
#             document.querySelectorAll('#divPopUp, .bx-close, .close, #popup, .advertisement').forEach(e => e.remove());
#         """)
#
#         print("📥 Waiting for Download button...")
#         download_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="lnkDownload"]')))
#         driver.execute_script("arguments[0].scrollIntoView(true);", download_btn)
#         time.sleep(1)
#         driver.execute_script("arguments[0].click();", download_btn)
#         print("✅ Download button clicked.")
#         time.sleep(7)  # Wait for file to download
#
#     except Exception as e:
#         print(f"⚠️ Error clicking Download button: {e}")
#     finally:
#         driver.quit()
#
#     # Locate downloaded CSV in Downloads folder
#     download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
#     latest_file = max([os.path.join(download_dir, f) for f in os.listdir(download_dir)], key=os.path.getctime)
#     print(f"📂 Downloaded file: {latest_file}")
#
#     # Move file to script folder with proper name
#     new_path = os.path.join(os.getcwd(), "corporate-events.csv")
#     os.replace(latest_file, new_path)
#     print(f"✅ File moved to: {new_path}")
#     return new_path
#
#
# # ----------------------------------------
# # 🧹 Process & enrich CSV data
# # ----------------------------------------
# def process_bse_csv(csv_file):
#     """Clean, classify and enrich CSV file."""
#     df = pd.read_csv(csv_file)
#
#     # Rename columns
#     df.rename(columns={
#         "Company Name": "Stock Name",
#         "Ex Date": "Ex-Date"
#     }, inplace=True)
#
#     # Add missing columns
#     required_cols = ["Event Type", "Ratio", "Dividend", "Last Price", "Index"]
#     for col in required_cols:
#         if col not in df.columns:
#             df[col] = ""
#
#     # Classify event types
#     print("🔍 Classifying corporate events...")
#     for i, row in df.iterrows():
#         purpose = str(row["Purpose"])
#         event_type, ratio, dividend = classify_event(purpose)
#         df.at[i, "Event Type"] = event_type
#         df.at[i, "Ratio"] = ratio
#         df.at[i, "Dividend"] = dividend
#
#     # Fetch NSE price & index
#     print("💰 Fetching Last Price and Index from NSE...")
#     for i, row in df.iterrows():
#         stock = str(row["Stock Name"]).split()[0].upper().replace("&", "AND")
#         price, index = get_nse_price_and_index(stock)
#         if price:
#             df.at[i, "Last Price"] = price
#             df.at[i, "Index"] = index
#         print(f"{stock}: ₹{price} | {index}")
#         time.sleep(1)
#
#     # Save output
#     output_file = "corporate-events.csv"
#     df.to_csv(output_file, index=False, encoding="utf-8-sig")
#     print(f"✅ Updated file saved as: {output_file}")
#
#
# # ----------------------------------------
# # 🚀 Main Function
# # ----------------------------------------
# def main():
#     csv_path = download_bse_csv()
#     process_bse_csv(csv_path)
#
#
# if __name__ == "__main__":
#     main()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os
import requests
import re

# ----------------------------------------
# 🏦 Fetch live NSE price and index details
# ----------------------------------------
def get_nse_price_and_index(symbol):
    """Fetch current price and index membership from NSE."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers)

        # Fetch live quote
        quote_url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        res = session.get(quote_url, headers=headers, timeout=5)
        if res.status_code != 200:
            return None, None

        data = res.json()
        price = data.get("priceInfo", {}).get("lastPrice", "")

        # Identify Nifty50 / BankNifty membership
        index_list = []
        for idx_name in ["NIFTY 50", "NIFTY BANK"]:
            index_url = f"https://www.nseindia.com/api/equity-stockIndices?index={idx_name.replace(' ', '%20')}"
            idx_res = session.get(index_url, headers=headers)
            if idx_res.status_code == 200:
                idx_data = idx_res.json()
                stocks = [s["symbol"] for s in idx_data.get("data", [])]
                if symbol in stocks:
                    index_list.append(idx_name)

        index = ", ".join(index_list) if index_list else "Other"
        return price, index
    except Exception:
        return None, None


# ----------------------------------------
# 🧩 Classify purpose into Event Type + Ratio + Dividend
# ----------------------------------------
def classify_event(purpose):
    """Classify Purpose into Event Type and extract Ratio/Dividend."""
    event_type, ratio, dividend = "", "", ""
    purpose_lower = str(purpose).lower()

    if "right" in purpose_lower:
        event_type = "Right"

    elif "split" in purpose_lower:
        event_type = "Split"
        match = re.search(r'from\s*rs\.?(\d+)[/-]*\s*to\s*rs\.?(\d+)', purpose_lower)
        if match:
            ratio = f"{match.group(1)}:{match.group(2)}"

    elif "spin off" in purpose_lower or "demerger" in purpose_lower:
        event_type = "Demerger"

    elif "bonus" in purpose_lower:
        event_type = "Bonus"
        match = re.search(r'(\d+[:/]\d+)', purpose)
        if match:
            ratio = match.group(1).replace("/", ":")

    elif "interim dividend" in purpose_lower or "final dividend" in purpose_lower or "dividend" in purpose_lower:
        event_type = "Dividend"
        match = re.search(r'rs\.?\s*[-:]?\s*(\d+\.?\d*)', purpose_lower)
        if match:
            dividend = match.group(1)
    else:
        event_type = "Other"
    return event_type, ratio, dividend


# ----------------------------------------
# 📥 Download Corporate Actions CSV from BSE (to same folder)
# ----------------------------------------
def download_bse_csv():
    """Download Corporate Actions CSV from BSE and save in same folder."""
    url = "https://www.bseindia.com/corporates/corporates_act.html"

    # Configure Chrome to download in current directory
    current_dir = os.getcwd()
    download_prefs = {"download.default_directory": current_dir}

    options = Options()
    options.add_argument("--headless=new")  # for server/GitHub runs
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("prefs", download_prefs)

    print("🌐 Launching Chrome to get BSE Corporate Actions file...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    try:
        # Remove popups blocking the click
        driver.execute_script("""
            document.querySelectorAll('#divPopUp, .bx-close, .close, #popup, .advertisement').forEach(e => e.remove());
        """)

        print("📥 Waiting for Download button...")
        download_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="lnkDownload"]')))
        driver.execute_script("arguments[0].scrollIntoView(true);", download_btn)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", download_btn)
        print("✅ Download button clicked.")
        time.sleep(7)  # Wait for file to download

    except Exception as e:
        print(f"⚠ Error clicking Download button: {e}")
    finally:
        driver.quit()

    # Find latest downloaded CSV in current folder
    files = [f for f in os.listdir(current_dir) if f.endswith(".csv")]
    if not files:
        raise FileNotFoundError("❌ No CSV file downloaded in current directory.")

    latest_file = max([os.path.join(current_dir, f) for f in files], key=os.path.getctime)
    print(f"📂 Downloaded file: {latest_file}")

    # Rename the downloaded file to "corporate-events.csv"
    new_path = os.path.join(current_dir, "corporate-events.csv")
    os.replace(latest_file, new_path)
    print(f"✅ File saved as: {new_path}")
    return new_path


# ----------------------------------------
# 🧹 Process & enrich CSV data
# ----------------------------------------
def process_bse_csv(csv_file):
    """Clean, classify and enrich CSV file."""
    df = pd.read_csv(csv_file)

    # Rename columns
    df.rename(columns={
        "Company Name": "Stock Name",
        "Ex Date": "Ex-Date"
    }, inplace=True)

    # Add missing columns
    required_cols = ["Event Type", "Ratio", "Dividend", "Last Price", "Index"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    # Classify event types
    print("🔍 Classifying corporate events...")
    for i, row in df.iterrows():
        purpose = str(row["Purpose"])
        event_type, ratio, dividend = classify_event(purpose)
        df.at[i, "Event Type"] = event_type
        df.at[i, "Ratio"] = ratio
        df.at[i, "Dividend"] = dividend

    # Fetch NSE price & index
    print("💰 Fetching Last Price and Index from NSE...")
    for i, row in df.iterrows():
        stock = str(row["Stock Name"]).split()[0].upper().replace("&", "AND")
        price, index = get_nse_price_and_index(stock)
        if price:
            df.at[i, "Last Price"] = price
            df.at[i, "Index"] = index
        print(f"{stock}: ₹{price} | {index}")
        time.sleep(1)

    # Save output
    output_file = "corporate-events.csv"
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"✅ Updated file saved as: {output_file}")


# ----------------------------------------
# 🚀 Main Function
# ----------------------------------------
def main():
    csv_path = download_bse_csv()
    process_bse_csv(csv_path)


if __name__ == "__main__":
    main()


