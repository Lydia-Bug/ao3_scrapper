from pkg_resources import working_set
import requests
from bs4 import BeautifulSoup ##Dependency
import csv
import pandas as pd  ##Dependency
import math
import datetime

URL = "https://archiveofourown.org/works?commit=Sort+and+Filter&work_search%5Bsort_column%5D=revised_at&include_work_search%5Brating_ids%5D%5B%5D=10&work_search%5Bother_tag_names%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Bcrossover%5D=&work_search%5Bcomplete%5D=&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bquery%5D=&work_search%5Blanguage_id%5D=&tag_id=Our+Flag+Means+Death+%28TV%29"

num = "all"
GET_BODY = False ## This will mess up the formatting of the excel sheet, but the actual file is still fine
GET_FIRST = True##Get first 100, or 100 distributed throughout works
CSV_FILE_NAME = "test2.csv"

def get_page_content(url):
    ## Sometimes the page request or something doesn't work first go
    content = None
    while content == None:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        content = soup.find(id="main")
    return content
## Gets url with page number puts it in an array with page number at index 1, so it can easily be changed
def get_page_number_url(content):
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
    ## Create array with first half of array and page number and second half of array
    url = url.split('page=')
    page = url[1][0]
    url[0] = url[0] + "page="
    url[1] = url[1][1:]
    url.insert(1, int(page)-1)

    return url

def get_every_th_page(content):
    if GET_FIRST:
        return 1
    heading = content.find("h2", class_="heading").text.split()
    total_num_works = heading[heading.index("of") + 1]
    return int(int(total_num_works)/num)
## Checks that there is another page
def get_still_more_works(content):
    next_url = content.find(class_="next")
    if next_url == None:
        return False
    else:
        next_url = next_url.find("a")
        if next_url == None:
            return False
        else:
            return True

def convert_to_datetime(date):
    date = date.split()
    if(date[1] == "Jan"):
        month = 1
    elif(date[1] == "Feb"):
        month = 2
    elif(date[1] == "Mar"):
        month = 3
    elif(date[1] == "Apr"):
        month = 4
    elif(date[1] == "May"):
        month = 5
    elif(date[1] == "Jun"):
        month = 6
    elif(date[1] == "Jul"):
        month = 7
    elif(date[1] == "Aug"):
        month = 8
    elif(date[1] == "Sep"):
        month = 9
    elif(date[1] == "Oct"):
        month = 10
    elif(date[1] == "Nov"):
        month = 11
    elif(date[1] == "Dec"):
        month = 12
    return datetime.datetime(int(date[2]), month, int(date[0]))

def write_csv_file(works_data):
    with open(CSV_FILE_NAME, 'w', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(list(works_data[0].keys()))
        for i in range(len(works_data)):
            writer.writerow(list(works_data[i].values()))

## Initialize variables
content = get_page_content(URL)
url_arr = get_page_number_url(content)
still_more_works = True 
every_th_page = get_every_th_page(content)
if(num == "all"):
    heading = content.find("h2", class_="heading").text.split()
    num = int(heading[heading.index("of") + 1])
if(url_arr != None):
    url = url_arr[0] + str(url_arr[1]) + url_arr[2]
else:
    url = URL
works_data = []
## Analyze works
while len(works_data) < num and still_more_works:
    content = get_page_content(url) ##Get contents
    works = content.find_all("li", class_="work") ##Get array of works
    still_more_works = get_still_more_works(content) ##Find if there aren't anymore works
    if(url_arr != None): ##Create url of next page
        url_arr[1] = url_arr[1] + every_th_page
        url = url_arr[0] + str(url_arr[1]) + url_arr[2]
    ## How many works to analyze
    if num - len(works_data) > len(works):
        works_to_analyze = len(works)
    else:
        works_to_analyze = num - len(works_data)

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
        ## Adds data
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
        date = works[i].find(class_="datetime").text
        works_data[-1]["last_updated"] = convert_to_datetime(date)
                
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

        ##Get rid of commas in values
        for i in range(5):
            key = list(works_data[-1].keys())[i+15]
            if("," in str(works_data[-1][key])):
                works_data[-1][key] = works_data[-1][key].replace(",", "")

        if GET_BODY:
            body_url = "https://archiveofourown.org/works/" + works_data[-1]["id"]
            
            content = get_page_content(body_url)

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

write_csv_file(works_data)
