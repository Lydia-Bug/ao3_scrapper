import requests
from bs4 import BeautifulSoup
import json
import csv
import pprint

URL = "https://archiveofourown.org/works?commit=Sort+and+Filter&work_search%5Bsort_column%5D=kudos_count&work_search%5Bother_tag_names%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Bcrossover%5D=&work_search%5Bcomplete%5D=&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bquery%5D=&work_search%5Blanguage_id%5D=&tag_id=Our+Flag+Means+Death+%28TV%29"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

content = soup.find(id="main")

works = content.find_all("li", class_="work")

works_data = []
for work in range(len(works)):
    works_data.append({
        "id": "",
        "title": "",
        "author": "",
        "rating": "",
        "category": "",
        "iswip": "",
        "last_updated": "",
        "fandoms": [],
        "warnings": [],
        "realationships": [],
        "characters": [],
        "freeform_tags": [],
        "summary": "",
        "language": "",
        "words": "",
        "chapters": "",
        "collections": "",
        "comments": "",
        "kudos": "",
        "bookmarks": ""
    })

for i in range(len(works)):
    ## ID
    works_data[i]["id"] = works[i].get("id").split("_",1)[1]
    ## Data at the top
    heading = works[i].find(class_="heading").find_all("a")
    works_data[i]["title"] = heading[0].text
    works_data[i]["author"] = heading[1].text
    works_data[i]["rating"] = works[i].find(class_="rating").text
    works_data[i]["category"] = works[i].find(class_="category").text ## Puts multiple calegorys in same string
    works_data[i]["iswip"] = works[i].find(class_="iswip").text
    works_data[i]["last_updated"] = works[i].find(class_="datetime").text
    
    ## Tags
    fandoms = works[i].find(class_="fandoms").find_all("a")
    for j in range(len(fandoms)):
        works_data[i]["fandoms"].append(fandoms[j].text)

    warnings = works[i].find_all("li", class_="warnings")
    for j in range(len(warnings)):
        works_data[i]["warnings"].append(warnings[j].text)

    realationships = works[i].find_all("li", class_="relationships")
    for j in range(len(realationships)):
        works_data[i]["realationships"].append(realationships[j].text)

    characters = works[i].find_all("li", class_="characters")
    for j in range(len(characters)):
        works_data[i]["characters"].append(characters[j].text)

    freeform_tags = works[i].find_all("li", class_="freeforms")
    for j in range(len(freeform_tags)):
        works_data[i]["freeform_tags"].append(freeform_tags[j].text)

    ## Summary
    works_data[i]["summary"] = works[i].find(class_="summary").text.strip()

    ## Data at the bottom
    works_data[i]["language"] = works[i].find("dd", class_="language").text
    works_data[i]["words"] = works[i].find("dd", class_="words").text
    works_data[i]["chapters"] = works[i].find("dd", class_="chapters").text
    collections = works[i].find("dd", class_="collections")
    if(collections != None): ## Not all works have collections
        works_data[i]["collections"] = works[i].find("dd", class_="collections").text
    works_data[i]["comments"] = works[i].find("dd", class_="comments").text
    works_data[i]["kudos"] = works[i].find("dd", class_="kudos").text
    works_data[i]["bookmarks"] = works[i].find("dd", class_="bookmarks").text
    


for key, value in works_data[0].items():
    print(key, ' : ', value)

