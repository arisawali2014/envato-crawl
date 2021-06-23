import asyncio
from pyppeteer import launch
import os
import json
import requests
import time
from pyppeteer.browser import Browser
from pyppeteer.page import Page
import threading
from decouple import config


async def main():
    browser = await launch({'headless': False})
    page = await browser.newPage()
    # if os.path.exists("./cookies/login.json") != True:
    await login(page)
    # else:
    #     parsedCookies = json.load(open("./cookies/login.json",'r'))
    #     for cook in parsedCookies:
    #         await page.setCookie(cook)
    #     print("[LOGIN WITH COOKIES]")
    #     await page.goto("https://elements.envato.com/sign-in")
    await crawling(page, browser)


async def crawling(page: Page, browser: Browser):
    params = {
        'type': 'web-templates'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'sec-ch-ua': 'Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    s = requests.session()
    s.headers = headers
    r = s.get("https://elements.envato.com/api/v1/items.json", params=params)
    rj = json.loads(r.text)
    totPage = rj['data']['attributes']['totalPages']
    print(totPage)
    for i in range(1, 2):
        params = {
            'type': 'web-templates',
            'page': i,
            'languageCode': 'en'
        }
        r = s.get("https://elements.envato.com/api/v1/items.json", params=params)
        items = r.json()['data']['attributes']['items']
        for item in items:
            url = f"https://elements.envato.com/{item['slug']}-{item['id']}"
            print(f"[ENVATO OPEN PAGE] - {item['title']}")
            newPage = await browser.newPage()
            await newPage.goto(url)
            cdp = await page.target.createCDPSession()
            # Set download path
            await cdp.send('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': "./downloads/"})
            time.sleep(1)
            await newPage.waitForSelector("button[data-test-selector='download-button']")
            await newPage.click("button[data-test-selector='download-button']")
            try:
                await newPage.click("button[data-test-selector='download-button']")
            except:
                pass
            try:
                await newPage.waitForSelector("button[data-test-selector='download-without-license']")
                await newPage.click("button[data-test-selector='download-without-license']")
            except:
                await newPage.waitForSelector("button[data-test-selector='download-button']")
                await newPage.click("button[data-test-selector='download-button']")

                await newPage.waitForSelector("button[data-test-selector='download-without-license']")
                await newPage.click("button[data-test-selector='download-without-license']")
            print(
                f"[ENVATO DOWNLOAD {item['id']}] - Clicking download without license")

            async def waitClose(page: Page):
                time.sleep(3)
                await page.close()
                print('page closed')
                time.sleep(1)
            th = threading.Thread(target=asyncio.run,
                                  args=(waitClose(newPage),))
            th.daemon = True
            th.start()
    print("All envato has been success downloaded")
    print("Do not close, please wait until finish downloading")


async def login(page: Page):
    await page.goto('https://elements.envato.com/sign-in')
    await page.waitForSelector("input[name='username']")
    await page.click("input[name='username']")
    # print(os.environ.get('ENVATO_USERNAME'))
    await page.type("input[name='username']", config('ENVATO_USERNAME'))
    await page.type("input[name='password']", config('ENVATO_PASSWORD'))
    await page.click("button[data-test-selector='sign-in-submit']")
    cookiesObj = await page.cookies()
    with open("./cookies/login.json", 'w+') as f:
        json.dump(cookiesObj, f, indent=2)
    print("[LOGIN WITH USERNAME] Cookies Saved")


# asyncio.get_event_loop().run_until_complete(main())
loop = asyncio.get_event_loop()
asyncio.ensure_future(main())
loop.run_forever()

# params = {
#         'type':'web-templates'
#     }
# headers= {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
#     'sec-ch-ua':'Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
#     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
# }
# r = requests.get("https://elements.envato.com/api/v1/items.json",params=params,headers=headers)
# print(r.text)
# rj = print(r.text)#json.loads(r.text)
# totPage = rj['data']['attributes']['totalPages']
# print(totPage)
