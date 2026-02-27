from playwright.sync_api import sync_playwright


def run(playwright):
  browser = playwright.chromium.launch(headless=False)
  page = browser.new_page()

  page.goto("https://www.youtube.com/", wait_until="domcontentloaded")
  page.wait_for_timeout(5000)

  
  page.goto("https://www.youtube.com/feed/subscriptions", wait_until="domcontentloaded")
  page.wait_for_timeout(5000)



  if "signin" in page.url.lower():
    print("You are not signed in. Please sign in to view subscriptions.")
  else:
    titles = page.locator("#video-title").all_inner_texts()
    titles = [title.strip() for title in titles if title.strip()]
    print("Recent subscription videos:")
    for title in titles[:10]:
      print(f"- {title}")
  browser.close()
with sync_playwright() as playwright:
  run(playwright)

