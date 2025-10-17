import os
import time
import shutil
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BSE_URL = "https://www.bseindia.com/corporates/ann.html"
OUTPUT_FILE = "corporate-events.csv"


def setup_driver(download_dir):
    """Set up Chrome driver for headless mode."""
    chrome_options = Options()
    prefs = {"download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=chrome_options)


def download_bse_csv():
    """Download the corporate action CSV from BSE site."""
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    print("🌐 Launching Chrome to get BSE Corporate Actions file...")
    driver = setup_driver(download_dir)
    driver.set_page_load_timeout(180)
    driver.get(BSE_URL)

    wait = WebDriverWait(driver, 30)
    print("📥 Waiting for Download button...")

    download_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="lnkDownload"]'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", download_btn)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", download_btn)
    print("✅ Download button clicked.")
    time.sleep(7)  # Wait for file to download

    # Locate the latest file
    files = [os.path.join(download_dir, f) for f in os.listdir(download_dir)]
    if not files:
        print("❌ No file found in download folder.")
        driver.quit()
        return None

    latest_file = max(files, key=os.path.getctime)
    print(f"📂 Downloaded file: {latest_file}")

    # Move to main folder
    new_path = os.path.join(os.getcwd(), OUTPUT_FILE)
    shutil.move(latest_file, new_path)
    driver.quit()
    print(f"✅ File moved to: {new_path}")
    return new_path


def process_bse_csv(csv_file):
    """Clean, rename and enrich CSV file."""
    df = pd.read_csv(csv_file)
    print("🧹 Cleaning and renaming columns...")

    # Rename columns
    df.rename(
        columns={"Company Name": "Stock Name", "Ex Date": "Ex-date"},
        inplace=True,
    )

    # Add missing columns
    for col in ["Last Price", "Index"]:
        if col not in df.columns:
            df[col] = ""

    # Save final file
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"💾 Saved final CSV as {OUTPUT_FILE}")


def main():
    print("🚀 Starting BSE Data Downloader...")
    csv_path = download_bse_csv()
    if csv_path:
        process_bse_csv(csv_path)
    else:
        print("⚠️ Failed to download CSV.")


if __name__ == "__main__":
    main()
