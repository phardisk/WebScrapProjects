library(rvest)
library(stringr)
library(dplyr)
library(httr)
library(nortest)
library(multcomp)
library(tidygeocoder)



get_gas_price<-function(ville)
{
  ## pages à lire 
  step=c(0,25,50,75,100,125,150)
  
  ## toutes les références des pages du site sont mises dans une liste
  all_site=list()
  for (i in 1:length(step))
  {
    
    all_site[[i]]<- paste0("https://www.gasbuddy.com/home?search=",ville,"&fuel=1&maxAge=0&cursor=",step[i]) %>% 
      html_session()%>%
      follow_link(paste("More",ville,"Gas Prices"))
  }
  
  ## les prix de chaque observation sont extraits
  price_all=list()
  
  for (i in 1:length(step))
  {
    
    price_all[[i]]<-content(all_site[[i]]$response)%>%
      
      html_nodes(xpath='//*[@class="text__left___1iOw3 GenericStationListItem__price___3GpKP"]')%>%
      html_text()
    
  }
  
  price<-unlist(price_all)
  
  # les  bannières de chaque observation sont extraites
  brand_all=list()
  
  for (i in 1:length(step))
  {
    
    brand_all[[i]]<-content(all_site[[i]]$response)%>%
      
      html_nodes(xpath='//*[@class="header__header3___1b1oq header__header___1zII0 header__evergreen___2DD39 header__snug___lRSNK GenericStationListItem__stationNameHeader___3qxdy"]')%>%
      html_text()
    
  }
  
  
  brand<-unlist(brand_all)
  
  # les adresses de chaque observation sont extraites
  address_all=list()
  
  for (i in 1:length(step))
  {
    
    address_all[[i]]<-content(all_site[[i]]$response)%>%
      html_nodes(xpath='//*[@class="GenericStationListItem__address___1VFQ3"]')%>%
      as.character() %>%
      strsplit('<br>')
    
  }
  
  address<-unlist(address_all)
  seq_street<-seq(from= 1,to =length(address),by=2)
  seq_prov<-seq(from= 2,to =length(address),by=2)
  
  province<-""
  street<-""
  city<-""
  for(sek in seq_street)
  {
    
    street[which(seq_street==sek)]<-strsplit(address[sek],'>')[[1]][2]
    
  }
  
  for(sek in seq_prov)
  {
    city[which(seq_prov==sek)]<-strsplit(strsplit(address[sek],'<')[[1]][1],",")[[1]][1]
    province[which(seq_prov==sek)]<-strsplit(strsplit(address[sek],'<')[[1]][1],",")[[1]][2]
    
  }
  
  # banniere, prix, adresse sont regroupés dans un dataframe
  df<-data.frame(brand,price,street,city,province)
  
  colnames(df)<-c("Brand","Price","Adresse","Ville",'Province')
  df<-subset(df,Price!="---")
  df$Price<-as.character(df$Price)
  df$Price<-gsub('¢',"",df$Price)
  df$Price<-as.numeric(df$Price)
  # identification des bannières et adresses uniques
  df_unik<-unique(df[c(1,3)])
  df_unik$Price<-0
  df_unik$Ville<-"test"
  df_unik$Province<-"test"
  # Constitution d'Une seule observation par station service
  for(i in 1:dim(df_unik)[1])
  {
    for(g in 1:dim(df)[1] )
    {
      if(df_unik[i,1]==df[g,1] && df_unik[i,2]==df[g,3] )
      {
        df_unik[i,3]<-df[g,2]
        df_unik[i,4]<-as.character(df[g,4])
        df_unik[i,5]<-as.character(df[g,5])
      }
    }
  }
  # homogéneisation de la colonne ville
  df_unik$Ville<-ville
  # On enlève l'espace après le nom des bannières
  df_unik$Brand <-sub("[[:space:]]+$", "", df_unik$Brand)
  # On enlève l'espace avant le nom des provinces
  df_unik$Province<- sub("^[[:space:]]", "", df_unik$Province)
  # la fonction retourne un dataframe
  return (df_unik)
}