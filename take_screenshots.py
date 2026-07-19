import os
import django
import asyncio
from playwright.async_api import async_playwright

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from onlinecourse.models import Choice

def get_correct_choices():
    return list(Choice.objects.filter(is_correct=True).values_list('id', flat=True))

async def main(correct_choice_ids):
    print(f"Correct choice IDs in DB: {correct_choice_ids}")

    async with async_playwright() as p:
        # Launch headless browser
        browser = await p.chromium.launch(headless=True)
        # Create browser context with a large screen size to fit sections
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()

        # --- Task 3: Admin Site Screenshot ---
        print("Navigating to admin login...")
        await page.goto("http://localhost:8000/admin/")
        await page.fill("input[name='username']", "admin")
        await page.fill("input[name='password']", "adminpass")
        await page.click("input[type='submit']")
        await page.wait_for_load_state("networkidle")
        
        print("Capturing admin site screenshot...")
        # Save to both paths
        screenshot_path_1 = "03-admin-site.png"
        screenshot_path_2 = "../03-admin-site.png"
        await page.screenshot(path=screenshot_path_1)
        await page.screenshot(path=screenshot_path_2)
        print(f"Saved admin screenshot to {screenshot_path_1} and {screenshot_path_2}")

        # --- Task 7: Mock Exam and Results ---
        print("Navigating to course index...")
        await page.goto("http://localhost:8000/onlinecourse/")
        await page.wait_for_load_state("networkidle")

        # Enroll / Enter Course
        print("Clicking Enroll / Enter...")
        # Find the submit button of the first course
        await page.click("input[value='Enroll '], input[value='Enter ']")
        await page.wait_for_load_state("networkidle")

        # Click "Take Exam" button
        print("Clicking Take Exam...")
        await page.click("text=Take Exam")
        # Wait a moment for collapse animation
        await page.wait_for_timeout(1000)

        # Check correct choice checkboxes
        print("Selecting correct choices...")
        for cid in correct_choice_ids:
            selector = f"input[id='{cid}']"
            await page.check(selector)
            print(f"Checked checkbox for choice ID {cid}")

        # Submit Exam
        print("Submitting exam...")
        await page.click("#questionform input[type='submit']")
        await page.wait_for_load_state("networkidle")

        # Capture results page
        print("Capturing exam results screenshot...")
        screenshot_path_result_1 = "07-final.png"
        screenshot_path_result_2 = "../07-final.png"
        await page.screenshot(path=screenshot_path_result_1, full_page=True)
        await page.screenshot(path=screenshot_path_result_2, full_page=True)
        print(f"Saved final results screenshot to {screenshot_path_result_1} and {screenshot_path_result_2}")

        await browser.close()

if __name__ == "__main__":
    cids = get_correct_choices()
    asyncio.run(main(cids))
