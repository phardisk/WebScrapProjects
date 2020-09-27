from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

url='https://www.filtrosmaster.com.co/index.php/pages/buscador-de-referencias'
driver = webdriver.Chrome('selenium/chromedriver.exe')
#driver = webdriver.Chrome()
driver.get (url)
df_car=[]
time.sleep(10)
radio=driver.find_elements_by_class_name('radio-inline')
radio[0].click()
marca=driver.find_elements_by_id('marca')
time.sleep(5)
marca[0].click()
time.sleep(10)
#value=marca[0].find_elements_by_class_name('value')
elem =driver.find_element_by_xpath("//select[@name='marca']")
options=elem.find_elements_by_tag_name('option')
for i in range(1,len(options)):
    options[i].click()
    time.sleep(5)
    print('The Brand is:', options[i].text)
    modelo =driver.find_element_by_xpath("//select[@name='modelo']")
    optionsModelo=modelo.find_elements_by_tag_name('option')
    for g in range (1,len(optionsModelo)):
       optionsModelo[g].click()
       time.sleep(5)
       print('The Model is:', optionsModelo[g].text)
       cylinder =driver.find_element_by_xpath("//select[@name='cilindraje']")
       optionsCylinder=cylinder.find_elements_by_tag_name('option')
       if len(optionsCylinder)==0:
           break
       if len(optionsCylinder)>2:
           for h in range(1,len(optionsCylinder)):
              optionsCylinder[h].click()
              time.sleep(10)
              print('The type of cylinder is:', optionsCylinder[h].text)
              caracteristik = driver.find_element_by_xpath("//ul[@class='list-group']")
              caracteristikText = caracteristik.text
              caracteristik = caracteristikText.split('\n')
              [caracteristik.remove(value) for value in caracteristik if value == 'Descargar PDF']
              lst_value = [value.split(':') for value in caracteristik]
              if lst_value==[['']]:
                  continue
              df_car.append(options[i].text)
              df_car.append(optionsModelo[g].text)
              df_car.append(optionsCylinder[h].text)
              lst_caract = []
              lst_verification = [1,3,4,5,7,9]
              lst_dispo = []
              lst_ref = ['completo','primario', 'secundario', 'externo', 'interno']
              for value in lst_value:
                  for x in value:
                      lst_caract.append(x)
              for v in range (0,len(lst_caract)):
                  if v in range(1,10,2):
                      lst_dispo.append(lst_caract[v])
                  else:
                      lst_dispo.append(lst_caract[v].split(' ')[-2])
              for b in range (0,len(lst_ref)):
                #try:
                  if lst_ref[b] in lst_dispo:
                      df_car.append(lst_dispo[lst_dispo.index(lst_ref[b]) + 1])
                  else:
                       df_car.append("N/A")
                 #except:
                       #continue
       else:
             optionsCylinder[1].click()
             time.sleep(5)
             print('The type of cylinder is:', optionsCylinder[1].text)
             caracteristik = driver.find_element_by_xpath("//ul[@class='list-group']")
             caracteristikText = caracteristik.text
             caracteristik = caracteristikText.split('\n')
             [caracteristik.remove(value) for value in caracteristik if value == 'Descargar PDF']
             lst_value = [value.split(':') for value in caracteristik]
             if lst_value == [['']]:
                 continue
             df_car.append(options[i].text)
             df_car.append(optionsModelo[g].text)
             df_car.append(optionsCylinder[1].text)
             lst_caract = []
             lst_dispo = []
             lst_verification=[]
             lst_ref = ['completo','primario', 'secundario', 'externo', 'interno']
             for value in lst_value:
                 for x in value:
                     lst_caract.append(x)
             if lst_caract == ['']:
                 break
             for v in range(0, len(lst_caract)):
                 if v in [1,3,5,7,9]:
                     lst_dispo.append(lst_caract[v])
                 else:
                     lst_dispo.append(lst_caract[v].split(' ')[-2])
             for b in range(0, len(lst_ref)):
                #try:
                    if lst_ref[b] in lst_dispo:
                     df_car.append(lst_dispo[lst_dispo.index(lst_ref[b])+1])
                    else:
                         df_car.append("N/A")
                 #except:
                    #continue
all=[]
for i in range(0,len(df_car),8):
       all.append(df_car[i:i+8])
 df = pd.DataFrame(all,columns =['Brand','Model','Cylinder','Full Filter','Primary Filter','Secondary Filter','External Filter','Internal Filter'])
 df.to_csv(r"C:\Users\Pecs\Desktop\Programming\PYprg\Scraper\selenium\result\Filter.csv", sep=';', encoding='utf-8')

