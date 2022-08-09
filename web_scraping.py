from bs4 import BeautifulSoup
import requests
import csv

nihLinkList = ['https://ods.od.nih.gov/factsheets/VitaminA-HealthProfessional/',
'https://ods.od.nih.gov/factsheets/VitaminB6-HealthProfessional/',
'https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/',
'https://ods.od.nih.gov/factsheets/Manganese-HealthProfessional/',
'https://ods.od.nih.gov/factsheets/Omega3FattyAcids-HealthProfessional/',
'https://ods.od.nih.gov/factsheets/Potassium-HealthProfessional/',
'https://ods.od.nih.gov/factsheets/Riboflavin-HealthProfessional/',
'https://ods.od.nih.gov/factsheets/Thiamin-HealthProfessional/',
'https://ods.od.nih.gov/factsheets/Selenium-HealthProfessional/']
length = 40
finalList = []

for x in nihLinkList:
    page = requests.get(x)
    doc = BeautifulSoup(page.text, "html.parser")
    rda = doc.find_all('td') 
    for y in range(length):
        output = rda[y].text 
        finalList.append(output)
        
sublists = [finalList[x:x+5] for x in range(0, len(finalList), 5)]
with open('out.csv', 'w', newline="\n") as file:
    wr = csv.writer(file)
    wr.writerows(sublists)
