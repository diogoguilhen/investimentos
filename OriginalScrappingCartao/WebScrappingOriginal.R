#install.packages(c("XML","rvest","xml2","read_html"), dep=T)
#install.packages("tidyverse",dep=T)
library("XML")
library("rvest")
library(rvest)
library(tidyverse)

getwd()

setwd("C:/Users/sguil/OneDrive/investimentos2/OriginalScrappingCartao")

getwd()


page <- read_html('Banco Original.html') 
 
tabela <- html_nodes(page,".timeline-default .ng-scope" ) %>% 
  map_df(~{
    data_frame(
      Data =  html_nodes(.x,".date-timeline") %>% html_text(trim=T),
      Estabelecimento =  html_nodes(.x,".colun01 .ng-binding") %>% html_text(trim=T),
      Valor =  html_nodes(.x,".timeline-info .colun04 .ng-binding") %>% html_text(trim=T),
      Origem =  (html_nodes(.x,".timeline-info .colun03 .ng-binding") %>% html_text(trim=T))
    )
  }) 
 
 tabela
 
write.csv(tabela, file="original2.csv",col.names = T, sep="|")


