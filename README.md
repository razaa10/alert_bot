# 🛒 Amul Product Stock Alert Bot

A Python script that monitors an Amul product page and sends an **instant Telegram notification** the moment it comes back in stock. Built specifically for the Amul High Protein Plain Lassi, but easily adaptable to any product on [shop.amul.com](https://shop.amul.com).

---

## 🧠 How It Works

1. Opens a headless Chrome browser (invisible, runs in background)
2. Loads the Amul homepage and enters your pincode so the site knows your location
3. Every 8 seconds, reloads the product page and **intercepts the backend API call** the website makes to check stock
4. Reads the `available` and `inventory_quantity` fields from the API response
5. The moment stock is detected → sends a Telegram message to your phone instantly

---

## 📦 Requirements

- Python 3.8+
- Google Chrome installed

Install dependencies:

```bash
pip install playwright requests
playwright install chromium
```

---

## ⚙️ Configuration

Open `burrah.py` and update the following fields at the top of the script:

```python
PRODUCT_ALIAS = "amul-high-protein-plain-lassi-200-ml-or-pack-of-30"  # 👈 change this for a different product
CHECK_INTERVAL = 8       # seconds between each stock check
BOT_TOKEN = "YOUR_BOT_TOKEN"   # from @BotFather on Telegram
CHAT_ID = "YOUR_CHAT_ID"       # from @userinfobot on Telegram
PINCODE = "411027"       # your delivery pincode
```

### 🔄 To monitor a different product
Copy the product URL from Amul's website, for example:
```
https://shop.amul.com/en/product/amul-high-protein-buttermilk-200-ml-or-pack-of-30
```
And set `PRODUCT_ALIAS` to the last part of the URL:
```python
PRODUCT_ALIAS = "amul-high-protein-buttermilk-200-ml-or-pack-of-30"
```

---

## 📱 Telegram Setup

1. Open Telegram → search **@BotFather** → type `/newbot` → follow steps → copy the **Bot Token**
2. Search **@userinfobot** → press Start → copy your **Chat ID**
3. Search your new bot → press **Start** (important, otherwise messages won't deliver)

---

## ▶️ Running the Script

```bash
python3 burrah.py
```

### To prevent your laptop from sleeping while the script runs (Mac):
```bash
caffeinate -dis python3 burrah.py
```

### To run in the background (terminal can close, but laptop must stay awake):
```bash
nohup python3 burrah.py > burrah.log 2>&1 &
```
- Check logs: `cat burrah.log`
- Stop the script: `pkill -f burrah.py`

---

## ☁️ Running 24/7 (Laptop Off)

To monitor even when your laptop is off, deploy to a cloud platform:

- **Railway** → [railway.app](https://railway.app) — recommended, free tier available
- **Google Colab** → quickest option, no setup needed

---

## 📋 Example Output

```
🚀 Monitoring product (API interception mode)...
📍 Pincode 411027 entered via UI
❌ Out of stock
❌ Out of stock
🔥 PRODUCT AVAILABLE!
Telegram response: {"ok":true,...}
```

---

## ⚠️ Notes

- Keep your **Bot Token private** — do not share it publicly
- Cookies/session expire occasionally — if script stops detecting stock, restart it
- Setting `CHECK_INTERVAL` below 5 seconds may get your IP flagged by the site
