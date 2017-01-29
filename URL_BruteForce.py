import requests,os,sys,time
from lxml import html

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    data = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            if content == -1 : continue
            outlinks,forms = get_all_links(content)
            print page
            print "*************************************"
            for i in outlinks:
                print i
            print "*************************************"
            for form in forms:
                print "method:",form.method,"\t\tform:",form.action
                data["method"] = form.method
                data["action"] = form.action
                data["parameters"] = []
                for input in form.inputs:
                    print "type:" , input.type , "\t\tname:" , input.name
                    if input.type.lower() == "submit":
                        data["submit"] = input.name
                    data["parameters"] += [input.name]
                print "*************************************"
                test(data)
                data = {}
            union(tocrawl, outlinks)
            crawled.append(page)

def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def get_page(url):
    try:
        result = requests.get(url)
        tree = html.fromstring(result.text)
        return tree
    except:
        return -1

def get_all_links(page):
    tmp = []
    links = page.xpath("//link/@href")
    forms = page.xpath("//form")
    links = sorted(set(links))
    for link in links:
        if link.find(domain) == -1:
            tmp.append(link)
    for link in tmp:
        links.remove(link)
    return links,forms

def brute(url):
    dict = open("dict.txt","r")
    lines = dict.readlines()
    for line in lines:
        word = line.strip("\n")
        link = url + "/" + word
        res = requests.get(link)
        print "\t", res.status_code, "\t\t", link

def test(data):
    tmp = {}
    if data["method"] == "POST":
        for i in data["parameters"]:
            tmp[i] = "<script>alert(1)</script>"
    tmp[data["submit"]] = data["submit"]
    print tmp
    res = requests.post("https://www.codecademy.com"+data["action"],data=tmp)
    print res.text
url = sys.argv[1]
domain = sys.argv[2]
crawl_web(url)
#brute("https://www.instagram.com")
