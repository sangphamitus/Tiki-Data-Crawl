from os import write
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
index=7
pages=10
file_name="data.csv"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options,executable_path=ChromeDriverManager().install())
def load_url_selenium_tiki(url,index):
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # driver = webdriver.Chrome(options=options,executable_path=ChromeDriverManager().install())
    


    print("Loading url=", url)
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
    list_review = []
    # just craw 10 page
    x=0
    try:
        Total = driver.find_element_by_css_selector("div.review-rating__total")
    
        Num= int(Total.text.split(' ')[0])
    except:
        Num=100
    while Num-len(list_review)>0:
        try:

        #     #Get the review details here
            WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"div.customer-reviews")))
        except :
            print('Not has comment!')
            break
        # Get product review
        
        product_reviews = driver.find_elements_by_class_name("review-comment")
        #Haveproduct=product_reviews[0].find_element_by_css_selector("[class='review-comment__content']")
        for product in product_reviews: 
            review = product.find_element_by_css_selector("[class='review-comment__content']").text
            vote = product.find_element_by_css_selector("[class='review-comment__title']").text
            if (vote!= "" or review.strip()):
                x=x+1
                #print(f"{x} - {vote} \n")
               # list_review.append(review)
            if (review != "" or review.strip()):
                file =open(file_name,'a',encoding="utf-8")
                print(f"{review} \n")
                file.write(f"{review} \n")
                file.close()
                file =open("place.txt",'w',encoding="utf-8")
                file.write(str(index))
                file.close()
                list_review.append(review)
            
        #Check for button next-pagination-item have disable attribute then jump from loop else click on the next button
        try:
            #driver.find_element_by_xpath("//li[@class='btn next']/a").click()
            button_next=WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[class = 'btn next']")))
            driver.execute_script("arguments[0].click();", button_next)
            print("next page")
            time.sleep(2)
          
        except Exception as e:
            print('Load several page!')
            break
    # driver.close()   
    

def readpage(url,pagesize):
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # driver = webdriver.Chrome(options=options,executable_path=ChromeDriverManager().install())
    
    print("Loading url=", url)
    driver.get(url)
    list_Page = []
    # just craw 10 page
    x=pagesize-1
    err=0
    while x<pages:
        try:
            
        #     #Get the review details here
            WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"[data-view-id='product_list_container']")))
        except :
            print('Not has comment!')
            break
        # Get product review
        
        product_reviews = driver.find_elements_by_class_name("product-item")
      
        #Haveproduct=product_reviews[0].find_element_by_css_selector("[class='review-comment__content']")
        for product in product_reviews: 
            try:
                review = product.get_attribute('href')
            
                if (review != "" or review.strip()):
            
                    print(f"{review} \n")
                    list_Page.append(review)
            except:
                err=err+1
        #Check for button next-pagination-item have disable attribute then jump from loop else click on the next button
        try:
            #driver.find_element_by_xpath("//li[@class='btn next']/a").click()
            button_next=WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-view-id='product_list_pagination_item']")))
            driver.execute_script("arguments[0].click();", button_next)
            driver.get(url+"?page="+str(x+1))
            print(f"next page {x}")
            time.sleep(2)
            x +=1
        except Exception as e:
            print('Load several page!')
            break
    # driver.close()
    return list_Page



#load_url_selenium_tiki("https://tiki.vn/ban-phim-co-khong-day-rk61-brown-switch-chinh-hang-p21313534.html")
out=readpage("https://tiki.vn/ban-phim-van-phong/c1830",index)
file=open("place.txt",'r')

tempindex=index
for i in out[index:]:
    load_url_selenium_tiki(i,tempindex)
    tempindex=tempindex+1
 
driver.close()