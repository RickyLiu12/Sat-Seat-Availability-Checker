import psutil, time
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from discord import SyncWebhook
from selenium.webdriver.common.keys import Keys


boolUC = True # Keep this false, otherwise it will break the code atm
boolHeadless = True # True if you want browser windows to show up
boolBlockImages = True # True if you want images to load (disabled because I have bad connection atm)
intSleepTime = 1800 # Sleep time between refreshing browser incase no results were found
webhook = "https://discord.com/api/webhooks/1262553570570539060/i6k1sBy_MLNTp99_MqszFY4zvekyS-l1oX2WPfNz9DSa3EkMjiCqR88LGDt2d0V3pwc8"


def killAllChrome():
    try:
        for proc in psutil.process_iter():
            if proc.name() == 'chrome.exe':
                proc.kill()
    except:
        pass

def main():
    zipCode = input("Please Enter a ZIP Code: ")
    while(True):
        killAllChrome()
        driver = Driver(uc=boolUC, disable_gpu=True, headless2=boolHeadless, block_images=boolBlockImages)
        driver.get(f'https://satsuite.collegeboard.org/sat/test-center-search')
        time.sleep(10)
        
        select_element = driver.find_element(By.TAG_NAME, 'select')
        select = Select(select_element)

        options = [option.text for option in select.options]
        print("Available Dates:")
        for idx, option in enumerate(options):
            print(f"{idx + 1}. {option}")
        choice = int(input("Enter a Date: ")) - 1
        while(choice > 0 and choice <= len(options)):
            int(input("Enter a Date: ")) - 1
        select.select_by_visible_text(options[choice])
        
        try:
            body = driver.find_element(By.CSS_SELECTOR, 'body')
            body.click()
            body.send_keys(Keys.ESCAPE)
        except:
            pass
        
        input_element = driver.find_element(By.ID, 'apricot_input_5')
        input_element.send_keys(zipCode)
        
        try:
            body = driver.find_element(By.CSS_SELECTOR, 'body')
            body.click()
            body.send_keys(Keys.ESCAPE)
        except:
            pass
        
        button = driver.find_element(By.CSS_SELECTOR, "button.cb-btn-yellow")
        button.click()
        
        time.sleep(5)
        search_results = driver.find_elements(By.CSS_SELECTOR, 'div.sat-tc-card')
        items = []
        for result in search_results:
            try:
                location_name = result.find_element(By.CSS_SELECTOR, 'h2.cb-card-title').text
            except:
                location_name = None
            try:
                seatAvailable = result.find_element(By.CSS_SELECTOR, 'span.seat-availability').text
            except:
                seatAvailable = None
            
            try:
                testCode = result.find_element(By.CSS_SELECTOR, 'span.test-center-code').text
            except:
                testCode = None
            if location_name and seatAvailable and testCode:
                if(seatAvailable == "Seat Is Available"):
                    items.append([location_name, seatAvailable, testCode])
        if(len(items) > 0):
            print("Following Results were found: ")
            bumped = ""
            for idx, option in enumerate(items):
                print(f"{idx + 1}. {option[0]} - {option[2]}")
                bumped += f"{idx + 1}. {option[0]} - {option[2]}\n"
            bumped = f"{bumped}\n<t:{int(time.time())}:R>"
            webhook = SyncWebhook.from_url(webhook)
            webhook.send(bumped)
            break
        else:
            print(f"No Results were found, Sleeping for {int(intSleepTime/60)} minutes and trying again!")
            time.sleep(intSleepTime)

        killAllChrome()
    exit()

if __name__ == '__main__':
  main()
