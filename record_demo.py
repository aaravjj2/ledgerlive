import asyncio
from playwright.async_api import async_playwright

async def record_demo():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=800,
            args=["--window-size=1440,900"]
        )
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            record_video_dir="./demo_video/",
            record_video_size={"width": 1440, "height": 900}
        )
        page = await context.new_page()

        BASE = "https://web-omega-silk-71.vercel.app"

        # Scene 1: Dashboard
        print("Scene 1: Dashboard")
        await page.goto(BASE, wait_until="networkidle")
        await asyncio.sleep(8)

        # Scene 2: Exceptions page
        print("Scene 2: Exceptions")
        try:
            await page.goto(f"{BASE}/exceptions", wait_until="networkidle")
        except:
            await page.goto(BASE, wait_until="networkidle")
        await asyncio.sleep(6)

        # Scene 3: Agent Console
        print("Scene 3: Agent Console")
        for route in ["/agent-console", "/airia", "/race-control", "/"]:
            try:
                await page.goto(f"{BASE}{route}", wait_until="networkidle", timeout=10000)
                await asyncio.sleep(2)
                # Check page actually loaded meaningful content
                content = await page.content()
                if len(content) > 1000:
                    break
            except:
                continue

        await asyncio.sleep(2)

        # Try to find and use the input
        input_el = None
        for selector in ["textarea", "input[type='text']", "[placeholder*='essage']", "[placeholder*='ask']", "[contenteditable='true']"]:
            try:
                input_el = await page.wait_for_selector(selector, timeout=3000)
                if input_el:
                    break
            except:
                continue

        if input_el:
            await input_el.click()
            await asyncio.sleep(1)
            await input_el.type(
                "What exceptions are open and which can be auto-resolved to close the books this month?",
                delay=45
            )
            await asyncio.sleep(2)
            await page.keyboard.press("Enter")
            print("Waiting for agent response (15s)...")
            await asyncio.sleep(15)
        else:
            print("No input found - continuing")
            await asyncio.sleep(8)

        # Scene 4: Readiness Dashboard
        print("Scene 4: Readiness")
        for route in ["/readiness", "/readiness-dashboard", "/dashboard", "/"]:
            try:
                await page.goto(f"{BASE}{route}", wait_until="networkidle", timeout=8000)
                await asyncio.sleep(5)
                break
            except:
                continue

        # Scene 5: Final dashboard
        print("Scene 5: Final shot")
        await page.goto(BASE, wait_until="networkidle")
        await asyncio.sleep(4)

        await context.close()
        await browser.close()
        print("Done. Video in ./demo_video/")

asyncio.run(record_demo())
