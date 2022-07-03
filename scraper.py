import requests
from bs4 import BeautifulSoup
import json
import csv
import pprint

url = "https://archiveofourown.org/tags/Our%20Flag%20Means%20Death%20(TV)/works"

NUM = 100
GET_BODY = False
CSV_FILE_NAME = "scrapper.csv"

still_more_works = True

works = []
while len(works) < NUM and still_more_works:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    content = soup.find(id="main")
    works_on_page = content.find_all("li", class_="work")
    works.extend(works_on_page)
    url = content.find(class_="next")
    if url != None:
        url = url.find("a")
        if url != None:
            url = "https://archiveofourown.org" + url["href"]
        else:
            still_more_works = False
    else:
        still_more_works = False

    print("works got: %d" % len(works))

works_data = []
for work in range(NUM):
    works_data.append({
        "id": "",
        "title": "",
        "author": "",
        "for": "",
        "rating": "",
        "category": "",
        "iswip": "",
        "last_updated": "",
        "fandoms": [],
        "warnings": [],
        "relationships": [],
        "characters": [],
        "freeform_tags": [],
        "summary": "",
        "language": "",
        "words": "",
        "chapters": "",
        "collections": "",
        "comments": "",
        "kudos": "",
        "bookmarks": "",
        "body": "",
        "notes": []
    })


for i in range(len(works_data)):
    ## ID
    works_data[i]["id"] = works[i].get("id").split("_",1)[1]
    ## Data at the top
    heading = works[i].find(class_="heading").find_all("a")
    works_data[i]["title"] = heading[0].text
    if(len(heading) > 1): ## Some works don't have an author, published by anonymous?
        works_data[i]["author"] = heading[1].text
    if(len(heading) > 2):
        works_data[i]["for"] = heading[2].text
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

    relationships = works[i].find_all("li", class_="relationships")
    for j in range(len(relationships)):
        works_data[i]["relationships"].append(relationships[j].text)

    characters = works[i].find_all("li", class_="characters")
    for j in range(len(characters)):
        works_data[i]["characters"].append(characters[j].text)

    freeform_tags = works[i].find_all("li", class_="freeforms")
    for j in range(len(freeform_tags)):
        works_data[i]["freeform_tags"].append(freeform_tags[j].text)

    ## Summary
    summary = works[i].find(class_="summary")
    if summary != None:
        works_data[i]["summary"] = works[i].find(class_="summary").text.strip()

    ## Data at the bottom
    works_data[i]["language"] = works[i].find("dd", class_="language").text
    works_data[i]["words"] = works[i].find("dd", class_="words").text
    works_data[i]["chapters"] = works[i].find("dd", class_="chapters").text
    collections = works[i].find("dd", class_="collections")
    if(collections != None):
        works_data[i]["collections"] = collections.text
    comments = works[i].find("dd", class_="comments")
    if(comments != None):
        works_data[i]["comments"] = comments.text
    kudos = works[i].find("dd", class_="kudos")
    if(kudos != None):
        works_data[i]["kudos"] = kudos.text
    bookmarks = works[i].find("dd", class_="bookmarks")
    if(bookmarks != None):
        works_data[i]["bookmarks"] = bookmarks.text

    if GET_BODY:
        url = "https://archiveofourown.org/works/" + works_data[i]["id"]
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        content = soup.find(id="main")

        if content == None:
            print(works_data[i]["title"] + " none")

        entire_works = content.find("li", class_="entire") ## If multiple chapters
        if entire_works != None:
            url = url  + "?view_full_work=true"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            content = soup.find(id="main")

        works_data[i]["body"] = content.find(id="chapters").text

        notes = content.find_all("div", class_="notes")
        for j in range(len(notes)):
            works_data[i]["notes"].append(notes[j].text)

    print("works analyzed: %d" % i)


for work in works_data:
    for key, value in work.items():
        print(key, ' : ', value)
    print("\n-----------------------------------------------------\n")


with open(CSV_FILE_NAME, 'w', encoding="utf-8", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(list(works_data[0].keys()))
    for i in range(len(works_data)):
        writer.writerow(list(works_data[i].values()))

