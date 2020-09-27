from bs4 import  BeautifulSoup
import requests
import pandas as pd
import os
import datetime
franchise=[]
for page in range(1,2):
     base='https://www.entrepreneur.com'
     url='https://www.entrepreneur.com/franchise500/2019/'+str(page)
     soup = BeautifulSoup(requests.get(url).text,'html.parser')
     files = soup.find_all('a',class_='franchise-list-item ga-click')
     for file in files:
        suffix=file['href']
        urlink=base+suffix
        soupe = BeautifulSoup(requests.get(urlink).text, 'html.parser')
        id=soupe.find_all('div',class_='sticky-info-top')
        company_name=id[0].getText().strip()
        bio=soupe.find_all('div',class_='content-right')[0].find_all('span')[1].getText()
        finrequire=soupe.find_all('div', class_='collapsible-parent')
        ongoingFees=finrequire[2]
        initialFranchiseFeeLow=ongoingFees.find_all('p')[0].getText().split('-')[0].strip()
        initialFranchiseFeeHigh = ongoingFees.find_all('p')[0].getText().split('-')[1]
        initialInvestment_Low=finrequire[1].find_all('p')[0].getText().split('-')[0]
        initialInvestment_High = finrequire[1].find_all('p')[0].getText().split('-')[1]
        if len(ongoingFees.find_all('p')[1].getText().split('-')[0].strip()) == 1:
            ongoingRoyaltyLow=ongoingFees.find_all('p')[1].getText().split('-')[0].strip()
            ongoingRoyaltyHigh =ongoingRoyaltyLow
        else:
            ongoingRoyaltyHigh = ongoingFees.find_all('p')[1].getText().split('-')[0].strip()
        if len(ongoingFees.find_all('p')[2].getText().split('-'))==1:
          adRoyaltyFeeLow=ongoingFees.find_all('p')[2].getText().split('-')[0]
          adRoyaltyFeeHigh=adRoyaltyFeeLow
        else:
         adRoyaltyFeeHigh = ongoingFees.find_all('p')[2].getText().split('-')[1]

        if len(finrequire[1].find_all('p')[1].getText())==1:
          liquidCashRequireLow=finrequire[1].find_all('p')[1].getText()
          liquidCashRequireHigh=liquidCashRequireLow
        else:
            liquidCashRequireHigh = finrequire[1].find_all('p')[1].getText()[1]
        percentunitgrow_1year=soupe.find_all('span',class_="green-text")[2].getText()[1:]
        percentunitgrow_3year = soupe.find_all('span', class_="green-text")[3].getText()[1:]
        franchise.append(company_name)
        franchise.append(bio)
        franchise.append(initialInvestment_Low)
        franchise.append(initialInvestment_High)
        franchise.append(initialFranchiseFeeLow)
        franchise.append(initialFranchiseFeeHigh)
        franchise.append(liquidCashRequireLow)
        franchise.append(liquidCashRequireHigh)
        franchise.append(ongoingRoyaltyLow)
        franchise.append(ongoingRoyaltyHigh)
        franchise.append(adRoyaltyFeeLow)
        franchise.append(adRoyaltyFeeHigh)
        franchise.append(percentunitgrow_1year)
        franchise.append(percentunitgrow_3year)

result=[]
for i in range(0,len(franchise),13):
           result.append(franchise[i:i+13])
df=pd.DataFrame(result,columns=['Company','Bio','Initial Investment (Low)','Initial Investment (High)',
                                        'Initial Franchise Fee (Low)','Initial Franchise Fee (High)','Liquid Cash Requirement (Low)',
                                        'Liquid Cash Requirement (High)','Ongoing Royalty Fee (Low)','Ongoing Royalty Fee (High)',
                                        '1 Year Percent Unit Growth','3 Year Percent Unit Growth'])

df.to_excel(encoding='utf-8')