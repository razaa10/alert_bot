import asyncio
import requests
from playwright.async_api import async_playwright

# ===== CONFIG =====
PRODUCT_ALIAS = "amul-high-protein-plain-lassi-200-ml-or-pack-of-30"
CHECK_INTERVAL = 8

BOT_TOKEN = "8184251876:AAG_8o1bLwSX8edpg2mBG_B2urK494zyzNU"
CHAT_ID = "1468438384"

PINCODE = "411027"  # Your pincode
# ==================

BASE_URL = "https://shop.amul.com"
PRODUCT_URL = f"{BASE_URL}/en/product/{PRODUCT_ALIAS}"


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    print("Telegram response:", response.text)


async def set_location_via_ui(page, pincode):
    """Type pincode into Amul's location input field like a real user"""
    try:
        await page.goto(BASE_URL, timeout=60000)
        await page.wait_for_timeout(3000)

        pincode_input = page.locator("input[placeholder*='pincode'], input[placeholder*='Pincode'], input[placeholder*='city'], input[name*='pincode'], input[name*='zip']")

        if await pincode_input.count() > 0:
            await pincode_input.first.fill(pincode)
            await page.wait_for_timeout(1000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(2000)
            print(f"📍 Pincode {pincode} entered via UI")
        else:
            await page.evaluate(f"""
                localStorage.setItem('userPincode', '{pincode}');
                localStorage.setItem('pincode', '{pincode}');
            """)
            print(f"📍 Pincode {pincode} set in localStorage")

    except Exception as e:
        print("Location UI error:", e)


async def monitor():
    print("🚀 Monitoring product (API interception mode)...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # no browser window
        context = await browser.new_context()
        page = await context.new_page()

        # Set location once at startup
        await set_location_via_ui(page, PINCODE)

        while True:
            try:
                async with page.expect_response(
                    lambda r: "ms.products" in r.url and r.status == 200,
                    timeout=15000
                ) as response_info:
                    await page.goto(PRODUCT_URL, timeout=60000)

                response = await response_info.value
                data = await response.json()

                if not data.get("data"):
                    print("⚠️ No product data — re-setting location...")
                    await set_location_via_ui(page, PINCODE)
                    await asyncio.sleep(CHECK_INTERVAL)
                    continue

                product = data["data"][0]
                available = product.get("available", 0)
                quantity = product.get("inventory_quantity", 0)

                print(f"Available: {available}, Quantity: {quantity}")

                if available == 1 and quantity > 0:
                    print("🔥 PRODUCT AVAILABLE!")
                    send_telegram(
                        f"🚨 Amul Lassi is AVAILABLE!\nStock: {quantity}\n{PRODUCT_URL}"
                    )
                    break
                else:
                    print("❌ Out of stock")

            except Exception as e:
                print("Error:", e)

            await asyncio.sleep(CHECK_INTERVAL)

        await browser.close()


asyncio.run(monitor())