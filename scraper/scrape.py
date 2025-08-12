"""Scraper Service.

Uses Playwright to visit Udyam Registration site, take screenshots for Step 1 & Step 2,
and extract form fields into schema.json. This schema is later consumed by the backend/frontend.

Note: This avoids entering any sensitive information (Aadhaar, PAN) - only field metadata is captured.
"""

# TODO: add retry logic if site is temporarily unavailable
import asyncio, json, os, sys
from playwright.async_api import async_playwright

OUT_DIR = "/data"
URL = "https://udyamregistration.gov.in/UdyamRegistration.aspx"

async def extract_fields(page):
    fields = await page.evaluate("""() => {
        const nodes = Array.from(document.querySelectorAll('input, select, textarea'));
        return nodes.map(n => {
            const id = n.id || null;
            const name = n.name || null;
            const tag = n.tagName.toLowerCase();
            const type = n.type || null;
            const required = n.required || n.getAttribute('aria-required') === 'true' || false;
            const pattern = n.getAttribute('pattern') || null;
            const maxlength = n.maxLength && n.maxLength > 0 ? n.maxLength : null;
            const placeholder = n.getAttribute('placeholder') || null;
            let label = null;
            if(id){
                const lab = document.querySelector('label[for="' + id + '"]');
                if(lab) label = lab.innerText.trim();
            }
            if(!label){
                const p = n.closest('label');
                if(p) label = p.innerText.trim();
            }
            let options = null;
            if(tag === 'select'){
                options = Array.from(n.options).map(o => ({value: o.value, text: o.text}));
            }
            return {id, name, tag, type, label: label || placeholder, required, pattern, maxlength, options};
        }).filter(f => f.name || f.id);
    }""")
    return fields

async def run():
    os.makedirs(OUT_DIR, exist_ok=True)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        try:
            await page.goto(URL, timeout=60000, wait_until="networkidle")
            await page.screenshot(path=os.path.join(OUT_DIR,"step1.png"), full_page=True)
            # Extract form fields from current page
            fields = await extract_fields(page)
            # try to click Next
            selectors = ["button:has-text('Next')","button:has-text('NEXT')","a:has-text('Next')","input[type=button][value*='Next']"]
            for sel in selectors:
                try:
                    el = await page.query_selector(sel)
                    if el:
                        await el.click()
                        try:
                            await page.wait_for_load_state('networkidle', timeout=8000)
                        except:
                            await asyncio.sleep(2)
                        await page.screenshot(path=os.path.join(OUT_DIR,"step2.png"), full_page=True)
                        more = await extract_fields(page)
                        # merge fields
                        keys = { (f.get('name') or f.get('id')): f for f in fields }
                        for f in more:
                            k = f.get('name') or f.get('id')
                            if k and k not in keys:
                                keys[k] = f
                        fields = list(keys.values())
                        break
                except:
                    pass
            with open(os.path.join(OUT_DIR,"schema.json"), "w", encoding="utf-8") as f:
                json.dump(fields, f, indent=2)
            print("Wrote schema.json with", len(fields))
        except Exception as e:
            print("Scraper error:", e)
            with open(os.path.join(OUT_DIR,"schema.json"), "w", encoding="utf-8") as f:
                json.dump([], f)
        finally:
            await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
