import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
import matplotlib.pyplot as plt
import pandas as pd
from pandas.errors import EmptyDataError 
import streamlit as st
import numpy as np

st.image("CMAbg.png")
st.markdown("<h1 style='font-family: Montserrat Semi-Bold; text-align: center; color: white;'>CAREER MARKET ANALYZER</h1>", unsafe_allow_html=True)
st.markdown("<style> footer {visibility: hidden;}</style>", unsafe_allow_html=True) 
scrape=st.slider("Select How Much Data you want to Scrape", 20,1000)



try:
    if st.button("Press to Scrape Data"):

        driver = webdriver.Chrome()
        jobs={"roles":[],
            "companies":[],
            "locations":[],
            "experience":[],
            "skills":[]}
        for i in range(scrape//4):
            driver.get("https://www.naukri.com/jobs-in-india-{}".format(i))
            time.sleep(3)
            lst=driver.find_elements(By.CSS_SELECTOR, '.jobTuple.bgWhite.br4.mb-8')
            for job in lst:
                try:
                    driver.implicitly_wait(3)
                    role=job.find_element(By.CSS_SELECTOR,"a.title.fw500.ellipsis").text
                    company=job.find_element(By.CSS_SELECTOR, "a.subTitle.ellipsis.fleft").text
                    location=job.find_element(By.CSS_SELECTOR, ".fleft.grey-text.br2.placeHolderLi.location").text
                    exp=job.find_element(By.CSS_SELECTOR, ".fleft.grey-text.br2.placeHolderLi.experience").text
                    skills=job.find_element(By.CSS_SELECTOR, ".tags.has-description").text
                    jobs["roles"].append(role)
                    jobs["companies"].append(company)
    #                 jobs["locations"].append(location)
                    jobs["experience"].append(exp)
    #                 jobs["skills"].append(skills)

                    month,day=[],[]
                    month.append(skills.lower())
                    day.append(location.lower())

                    for i in month:
                        x=(i.split('\n'))
                        jobs["skills"].append(x)
                        
                    for j in day:
                        y=(j.split(','))
                        jobs["locations"].append(y)

                except NoSuchElementException:
                    pass
                    break
                except NameError:
                    pass
                except NoSuchWindowException:
                    pass

        DS_jobs_df=pd.DataFrame(jobs)
        DS_jobs_df.to_csv("final.csv")
        st.write("Scraping Done")
        



    data=pd.read_csv("final.csv")


    loc=data["locations"]
    comp=data["skills"]
    nameor=data["roles"]
    nameoc=data["companies"]




    resloc,res2loc,userloc,uloc,cloc=[],[],[],[],[]
    res,res2,user,uskill,cskill,newx=[],[],[],[],[],[]
    fin,finloc,chos=[],[],[]


    for i in comp:
        res2.append(i.strip('][').split(', '))
    for i in res2:
        for j in range(len(i)):
            i[j]=i[j].replace("'", "")
        x=set(i)
        cskill.append(x)
    for i in cskill:
        for j in i:
            chos.append(j)




    for i in loc:
        resloc.append(i.strip('][').split(', '))
    for j in resloc:
        for k in range(len(j)):
            j[k]=j[k].replace("'", "").lstrip()
            cloc.append(j[k])



    ls,us=[],[]
    for i in range(len(cskill)):
        ls.append(list(cskill[i])+resloc[i])


    for i in ls:
        for j in i:
            us.append(j)

    usl=st.multiselect("Select Your Skills",set(chos))
    lit=st.multiselect("Select Your Locations",set(cloc))

    finalist=usl+lit


    
    for i in ls:
        datch=len(set(i).intersection(set(finalist)))
        e = round(datch/len(i),2)
        newx.append(e)
        finloc.append((str(round(float(e),2)*100)+'%'))
    # a=[]
    # for i in finloc:
    #     if i!='0.0%':
    #         a.append(i)
    b={"Company":nameoc,"Position":nameor,"Probability":finloc}

    if st.button("Compute Probability"):
        probab2=pd.DataFrame(b)
        st.dataframe(probab2)
        explode_value=(0.08,0.08,0.08,0.08,0.08,0.08,0.08,0.08,0.08,0.08,)
        y = np.array(newx[:10])
        # plt.legend(labels=nameor[:10], loc="upper left",bbox_to_anchor=(1,1) )
        plt.pie(y, labels=nameor[:10], explode=explode_value,
        wedgeprops = {"edgecolor" : "#010f20",
                      'linewidth': 1, 
                      'antialiased': True}, shadow=False)


        st.pyplot(plt)

except EmptyDataError:
    st.error("Please Scrape Data")
except ValueError:
    st.error("Please Choose an Option")
except NoSuchWindowException:
    st.error("Data Scraping Evicted, Please Refresh")