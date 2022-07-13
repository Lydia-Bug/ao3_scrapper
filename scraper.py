from pkg_resources import working_set
import requests
from bs4 import BeautifulSoup ##Dependency
import csv

URL = "https://archiveofourown.org/tags/Our%20Flag%20Means%20Death%20(TV)/works?commit=Sort+and+Filter&page=2&work_search%5Bcomplete%5D=&work_search%5Bcrossover%5D=&work_search%5Bdate_from%5D=2022-07-01&work_search%5Bdate_to%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Blanguage_id%5D=&work_search%5Bother_tag_names%5D=&work_search%5Bquery%5D=&work_search%5Bsort_column%5D=kudos_count&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D="

NUM = 40
GET_BODY = False
GET_FIRST = True ##Get first 100, or 100 distributed throughout works
CSV_FILE_NAME = "test2.csv"

def find_url_with_page_number():
    ### To find the url with 'page=_' in it, to more easily get to the next page or 10th next page
    ## Sometimes the page request or something doesn't work first go
    content = None
    while content == None:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        content = soup.find(id="main")
    ## The link when you click next contains 'page=_
    url = content.find(class_="next")
    if url != None:
        url = url.find("a")
        if url != None:
            url = "https://archiveofourown.org" + url["href"]
        else:
            return None
    else:
        return None
    print(url)
    print()
    ## Create array with first half of array and page number and second half of array
    url = url.split('page=')
    page = url[1][0]
    url[0] = url[0] + "page="
    url[1] = url[1][1:]
    url.insert(1, int(page)-1)

    print(url[0] + str(url[1]) + url[2])
    return url

url_arr = find_url_with_page_number()

still_more_works = True
url = url_arr[0] + str(url_arr[1]) + url_arr[2]
works_data = []
while len(works_data) < NUM and still_more_works:
    ## Sometimes the page request or something doesn't work first go
    content = None
    while content == None:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        content = soup.find(id="main")
    
    ## Find all individual works
    works = content.find_all("li", class_="work")

    ## Check there is another page, and create url
    url = content.find(class_="next")
    if url != None:
        url = url.find("a")
        if url != None:
            url_arr[1] = url_arr[1] + 1
            url = url_arr[0] + str(url_arr[1]) + url_arr[2]
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
            "completed_chapters": "",
            "total_chapters": "", ## Can be ? char
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
            ## Chapters
        chapters = works[i].find("dd", class_="chapters").text.split("/")
        works_data[-1]["completed_chapters"] = chapters[0]
        works_data[-1]["total_chapters"] = chapters[1]

        collections = works[i].find("dd", class_="collections")
        if(collections != None):
            works_data[-1]["collections"] = collections.text
        else:
            works_data[-1]["collections"] = 0
        comments = works[i].find("dd", class_="comments")
        if(comments != None):
            works_data[-1]["comments"] = comments.text
        else:
            works_data[-1]["comments"] = 0
        kudos = works[i].find("dd", class_="kudos")
        if(kudos != None):
            works_data[-1]["kudos"] = kudos.text
        else: 
            works_data[-1]["kudos"] = 0
        bookmarks = works[i].find("dd", class_="bookmarks")
        if(bookmarks != None):
            works_data[-1]["bookmarks"] = bookmarks.text
        else:
            works_data[-1]["bookmarks"] = 0

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
