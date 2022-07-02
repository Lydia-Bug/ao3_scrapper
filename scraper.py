import requests
from bs4 import BeautifulSoup

URL = "https://archiveofourown.org/works?commit=Sort+and+Filter&work_search%5Bsort_column%5D=kudos_count&include_work_search%5Barchive_warning_ids%5D%5B%5D=17&include_work_search%5Barchive_warning_ids%5D%5B%5D=18&work_search%5Bother_tag_names%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Bcrossover%5D=&work_search%5Bcomplete%5D=&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bquery%5D=&work_search%5Blanguage_id%5D=&tag_id=Our+Flag+Means+Death+%28TV%29"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

content = soup.find(id="main")

works = content.find_all("li", class_="work")

work_id = works[0].get("id").split("_",1)[1]
work_url = "https://archiveofourown.org/works/" + work_id

work_heading = works[0].find(class_="heading").find_all("a")
work_title = work_heading[0].text
work_author = work_heading[1].text

work_fandoms = works[0].find(class_="fandoms").find_all("a")
for i in range(len(work_fandoms)):
    work_fandoms[i] = work_fandoms[i].text

work_warnings = works[0].find_all("li", class_="warnings")
for i in range(len(work_warnings)):
    work_warnings[i] = work_warnings[i].text

print(work_id)
print(work_title)
print(work_author)
print(work_fandoms)
print(work_warnings)
#for fic in fics:
#    print(fic)

"""
results = soup.find(id="ResultsContainer")

job_elements = results.find_all("div", class_="card-content")

python_jobs = results.find_all("h2", string=lambda text: "python" in text.lower())

python_job_elements = [h2_element.parent.parent.parent for h2_element in python_jobs]

for job_element in python_job_elements:
    links = job_element.find_all("a")
    for link in links:
        link_url = link["href"]
        print(f"Apply here: {link_url}\n")
    #print(job_element.text.strip())
    #print()
#print(results.prettify())

for job_element in job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()
"""