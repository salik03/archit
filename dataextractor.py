from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


x=input("Enter: ")

role,comp,loc=[],[],[]
driver_path = "C:/chromedriver.exe"
chr_options = Options()
chr_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(driver_path, options=chr_options)

driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3389978895&keywords={}".format(x))

srchresu=driver.find_elements(By.CSS_SELECTOR,".two-pane-serp-page__results")    
for i in srchresu:
    lst=i.find_elements(By.CSS_SELECTOR,".base-search-card__info")
    for i in lst:
        role.append(i.find_element(By.CSS_SELECTOR,".base-search-card__title").text)
        comp.append(i.find_element(By.CSS_SELECTOR,".base-search-card__subtitle").text)
        loc.append(i.find_element(By.CSS_SELECTOR,".job-search-card__location").text)

for i in range(0,len(role)):
    print(role[i]+"----"+comp[i]+"----"+loc[i])