#To search specific job run:
# python beautifulshop.py -s "Python"


import threading
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
from time import sleep
from tqdm import tqdm
import argparse
chrome_options = Options()
chrome_options.add_argument("--lang=en")
#path to crome driver
PATH = './chromedriver'

driver = webdriver.Chrome(PATH,options=chrome_options)

#load the site in respective browser
driver.get("https://arbetsformedlingen.se/platsbanken/annonser?q=C%2B%2B")
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-s", "--search", type=str, default="C++",
	help="Search Job")
args = vars(ap.parse_args())


print(f"Searching {args['search']}")
sleep(4)
input_box = driver.find_element_by_id('search_input')
input_box.clear()
input_box.send_keys(args["search"])
input_box.send_keys(Keys.RETURN)



#soup = BeautifulSoup(driver.page_source, 'html.parser')
#Scripts = soup.find('html')
print("JavaScript of the page")
whole = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
#soup = BeautifulSoup(driver.page_source, 'html.parser', from_encoding="utf8")
with open("Script.txt", mode="w") as code:
    code.write(whole)

      #  print(javascript.text)
#print(driver.page_source)

count = 0
JOB_TITLE = []
JOB_LINK = []
COMPANY = []
DUE_DATE = []
PUBLISHED_DATE = []
sleep(5)
TOTAL_JOBS = int(driver.find_element_by_xpath("//div[@class='pb-header-row']//div[@class='number-of-jobs']//h2//span[@class='antal-lediga-jobb-siffra']").text)

print(f"Getting All The {TOTAL_JOBS} Information")
while(True):
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    CONTAINERS = soup.find_all('div', attrs = {'class':"card-container"})
    for CONTAINER in CONTAINERS:
        JOB_TITLE.append(CONTAINER.find('a').text)
        JOB_LINK.append('https://arbetsformedlingen.se'+str(CONTAINER.find('a')['href']))
        COMPANY.append(CONTAINER.find('strong',attrs = {'class':"pb-company-name"}).text)
        DUE_DATE.append(CONTAINER.find('span',attrs = {'class':'bold'}).text)
        PUBLISHED_DATE.append(CONTAINER.find('div',attrs={'class':"d-md-block"}).text)
        
        count+=1
   
      
    if count == TOTAL_JOBS:

        print(f"Total  {count} Jobs")
        break
    try:
        driver.execute_script("document.getElementsByClassName('i-angle-right pagination-icon next')[0].click()")
    except:
        pass  
    sleep(5)  


output = pd.DataFrame({'JOB_TITLE': JOB_TITLE,'JOB_HREF':JOB_LINK,'COMPANY':COMPANY,'DUE DATE':DUE_DATE,'PUBLISHED_DATE':PUBLISHED_DATE})
output.to_csv('JOB_LIST.csv', index=False)

driver.close()

#if you want detailed data too then uncomment this one
'''

title = []
company = []
role = []
location =[]
form_of_employment = []
salary = []
qualification = []
about = []
terms = []
employer = []
contact = []



redo_list = [] #to rerun for job with some error
def thread_function(link):
    
    try:
        driver = webdriver.Chrome(PATH,options=chrome_options)
        driver.get(link)
        sleep(5)

        SECTION = driver.find_element_by_xpath("//section[@class='col-md-12 col-lg-8 col-sm-12 col-12 left-content']")
        company.append(SECTION.find_element_by_id("pb-company-name").text)
        title.append(SECTION.find_element_by_xpath("//pb-section-job-quick-info//h1[@class='section-small break-title']").text)
        try:
            role.append(SECTION.find_element_by_id("pb-job-role").text)
        except:
            role.append("NOT MENTIONED")
        try:
            location.append(SECTION.find_element_by_id("pb-job-location").text)
        except:
            location.append("NOT MENTIONED")
        job_type = SECTION.find_element_by_xpath("//pb-section-job-quick-info//div[@class='section print-break-inside']")
    # SCOPE = job_type.find_element_by_xpath("//div[@class='ng-star-inserted']").text
        
        try:
            form_of_employment.append(job_type.find_element_by_xpath("//span[@class='upper-fist']").text)
        except:
            form_of_employment.append("NOT MENTIONED")
        
        try:
            qualification.append(SECTION.find_element_by_xpath("//div[@class = 'section ng-star-inserted']//pb-feature-job-qualifications//div[@class = 'qualifications-container ng-star-inserted']//div[@class = 'section print-break-inside']//div[@class='ng-star-inserted']").text)
        except:
            qualification.append("NOT MENTIONED")
        
        try:
            about.append(SECTION.find_element_by_xpath("//div[@class='section job-description']").text)
        except:
            about.append("NOT MENTIONED")
        
        try:
            terms.append(SECTION.find_element_by_xpath("//div[@class='double pre-wrap']").text)
        except:
            terms.append("NOT MENTIONED")
        
        
        try:         
            contact.append(SECTION.find_element_by_xpath("//a[@class = 'regular-link']").get_attribute('href'))
        except:
            contact.append("NOT MENTIONED")
    
        try:    
            employer.append(SECTION.find_element_by_xpath("//a[@class='break-word employer-link icon-before icon-link']").get_attribute("href"))

        except:        
            employer.append("NOT MENTIONED")

        try:    
            salary.append(SECTION.find_element_by_xpath("//div[@class='double ng-star-inserted']").text)
        except:        
            salary.append("NOT MENTIONED")    
        if len(redo_list)>0:
            redo_list.remove(link)
            print(f"After Getting Page We Need To Get {len(redo_list)} Pages Now ")

        driver.quit()
    except:
        if link in redo_list:
            pass
        else:
            redo_list.append(link)  
            print(f"After Getting Error We Have To Get {len(redo_list)} pages")
        driver.quit()  

for i in tqdm(range(0,len(JOB_LINK),4)):
    
    
    x1 = threading.Thread(target=thread_function, args=(JOB_LINK[i],))
    x1.start()
    if i+1 <= (len(JOB_LINK)-1):
        x2 = threading.Thread(target=thread_function, args=(JOB_LINK[i+1],)) 
        x2.start()
    if i+2 <= (len(JOB_LINK)-1):    
        x3 = threading.Thread(target=thread_function, args=(JOB_LINK[i+2],))
        x3.start()
    if i+3 <= (len(JOB_LINK)-1):    
        x4 = threading.Thread(target=thread_function, args=(JOB_LINK[i+3],))
        x4.start()
        
    x1.join()
    try:
        x2.join()
        x3.join()
        x4.join()
    except:
        pass    
i = 0
while(len(redo_list)>0):
    x1 = threading.Thread(target=thread_function, args=(JOB_LINK[i],))
    x1.start()
   
    if i+1 <= (len(redo_list)-1):
        x2 = threading.Thread(target=thread_function, args=(JOB_LINK[i+1],)) 
        x2.start()
    x1.join()
    x2.join()
    i+=1
    if i == len(redo_list):
        i = 0

    

   # document.getElementsByClassName("i-angle-right pagination-icon next")[0].click()
output = pd.DataFrame({'JOB_TITLE':title,'COMPANY':company,'ROLE':role,'LOCATION':location,'FORM_OF_EMPLOYMENT':form_of_employment,'SALARY':salary,'QUALIFICATION':qualification,'ABOUT':about,'TERMS':terms,'EMPLOYER':employer,'CONTACT_MAIL':contact})
output.to_csv('JOB_DETAILS.csv', index=False)

'''


# Create some Pandas dataframes from some data.
df1 = pd.read_csv('JOB_LIST.csv')

#if you want detailed data too then uncomment this one
#df2 = pd.read_csv("JOB_DETAILS.csv")

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('Full_JOb_DETAIL.xlsx', engine='xlsxwriter')

# Write each dataframe to a different worksheet.
df1.to_excel(writer, sheet_name='Sheet1')
#df2.to_excel(writer, sheet_name='Sheet2')
for column in df1:
    column_length = max(df1[column].astype(str).map(len).max(), len(column))
    if column_length >= 60:
        column_length = 50
    else:
        column_length = 30    
    col_idx = df1.columns.get_loc(column)
    writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_length)


#if you want detailed data too then uncomment this one
'''    
for column in df2:
    column_length = max(df2[column].astype(str).map(len).max(), len(column))
    if column_length >= 60:
        column_length = 50
    else:
        column_length = 30 
    col_idx = df2.columns.get_loc(column)
    writer.sheets['Sheet2'].set_column(col_idx, col_idx, column_length)    
'''
# Close the Pandas Excel writer and output the Excel file.
writer.save()


print("Your submission was successfully saved!")
