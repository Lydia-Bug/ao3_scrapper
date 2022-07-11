from pkg_resources import working_set
import requests
from bs4 import BeautifulSoup ##Dependency
import csv

url = "https://archiveofourown.org/tags/Our%20Flag%20Means%20Death%20(TV)/works"

NUM = 5
GET_BODY = False
CSV_FILE_NAME = "test.csv"

still_more_works = True

works_data = []
while len(works_data) < NUM and still_more_works:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    ## Sometimes the page request or something doesn't work first go
    content = None
    while content == None:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        content = soup.find(id="main")
    
    works = content.find_all("li", class_="work")
    ## Find the next page of works
    url = content.find(class_="next")
    if url != None:
        url = url.find("a")
        if url != None:
            url = "https://archiveofourown.org" + url["href"]
        else:
            still_more_works = False
    else:
        still_more_works = False
    ## How many works to analyze
    if NUM - len(works_data) > len(works):
        works_to_analyze = len(works)
    else:
        works_to_analyze = NUM - len(works_data)

    for i in range(works_to_analyze):
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

        ### Adds data
        ## ID
        works_data[-1]["id"] = works[i].get("id").split("_",1)[1]
        ## Data at the top
        heading = works[i].find(class_="heading").find_all("a")
        works_data[-1]["title"] = heading[0].text
        if(len(heading) > 1): ## Some works don't have an author, published by anonymous?
            works_data[-1]["author"] = heading[1].text
        if(len(heading) > 2):
            works_data[-1]["for"] = heading[2].text
        works_data[-1]["rating"] = works[i].find(class_="rating").text
        works_data[-1]["category"] = works[i].find(class_="category").text ## Puts multiple calegorys in same string
        works_data[-1]["iswip"] = works[i].find(class_="iswip").text
        works_data[-1]["last_updated"] = works[i].find(class_="datetime").text
        
        ## Tags
        fandoms = works[i].find(class_="fandoms").find_all("a")
        for j in range(len(fandoms)):
            works_data[-1]["fandoms"].append(fandoms[j].text)

        warnings = works[i].find_all("li", class_="warnings")
        for j in range(len(warnings)):
            works_data[-1]["warnings"].append(warnings[j].text)

        relationships = works[i].find_all("li", class_="relationships")
        for j in range(len(relationships)):
            works_data[-1]["relationships"].append(relationships[j].text)

        characters = works[i].find_all("li", class_="characters")
        for j in range(len(characters)):
            works_data[-1]["characters"].append(characters[j].text)

        freeform_tags = works[i].find_all("li", class_="freeforms")
        for j in range(len(freeform_tags)):
            works_data[-1]["freeform_tags"].append(freeform_tags[j].text)

        ## Summary
        summary = works[i].find(class_="summary")
        if summary != None:
            works_data[-1]["summary"] = works[i].find(class_="summary").text.strip()

        ## Data at the bottom
        works_data[-1]["language"] = works[i].find("dd", class_="language").text
        works_data[-1]["words"] = works[i].find("dd", class_="words").text
        works_data[-1]["chapters"] = " " + works[i].find("dd", class_="chapters").text ## Space is there so excel doesn't format as date
        collections = works[i].find("dd", class_="collections")
        if(collections != None):
            works_data[-1]["collections"] = collections.text
        comments = works[i].find("dd", class_="comments")
        if(comments != None):
            works_data[-1]["comments"] = comments.text
        kudos = works[i].find("dd", class_="kudos")
        if(kudos != None):
            works_data[-1]["kudos"] = kudos.text
        bookmarks = works[i].find("dd", class_="bookmarks")
        if(bookmarks != None):
            works_data[-1]["bookmarks"] = bookmarks.text

        if GET_BODY:
            body_url = "https://archiveofourown.org/works/" + works_data[-1]["id"]
            page = requests.get(body_url)
            soup = BeautifulSoup(page.content, "html.parser")
            content = soup.find(id="main")

            ## Sometimes the page request or something doesn't work first go
            while content == None:
                page = requests.get(body_url)
                soup = BeautifulSoup(page.content, "html.parser")
                content = soup.find(id="main")

            entire_works = content.find("li", class_="entire") ## If multiple chapters
            if entire_works != None:
                body_url = body_url  + "?view_full_work=true"
                page = requests.get(body_url)
                soup = BeautifulSoup(page.content, "html.parser")
                content = soup.find(id="main")

            works_data[-1]["body"] = content.find(id="chapters").text

            notes = content.find_all("div", class_="notes")
            for j in range(len(notes)):
                works_data[-1]["notes"].append(notes[j].text)

        print("works analyzed: %d" % len(works_data))


"""
for work in works_data:
    for key, value in work.items():
        print(key, ' : ', value)
    print("\n-----------------------------------------------------\n")
"""

with open(CSV_FILE_NAME, 'w', encoding="utf-8", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(list(works_data[0].keys()))
    for i in range(len(works_data)):
        writer.writerow(list(works_data[i].values()))


