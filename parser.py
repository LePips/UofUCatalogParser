import re

from bs4 import BeautifulSoup

from urllib import request
from urllib.parse import quote

class CourseParser:

    def __init__(self, catalogNum):
        self.baseURL = f'https://student.apps.utah.edu/uofu/stu/ClassSchedules/main/{catalogNum}/'
        self.catalogNum = catalogNum
        self.subjects = []
        self.subjectCourses = {}

    def start(self):
        homePage = self.getHomePage()
        self.parseHomePage(homePage)

        for subject in self.subjects[:1]:
            subjectAbbr = subject.split(' - ')[0]
            subjectCoursesHTML = self.getSubjectCoursesPage(subjectAbbr)
            self.parseSubjectCoursesPage(subject, subjectCoursesHTML)

    def getHomePage(self):
        homeURL = self.baseURL + 'index.html'

        homePageFile = request.urlopen(homeURL)
        homePageHTML = homePageFile.read().decode('utf8')
        homePageFile.close()

        return homePageHTML

    def parseHomePage(self, pageHTML):
        pageSoup = BeautifulSoup(pageHTML, 'html.parser')

        for subject in pageSoup.select('a[href*="class_list.html?subject"]'):
            self.subjects.append(subject.string)

    def getSubjectCoursesPage(self, subjectAbbr):
        subjectURL = self.baseURL + f'class_list.html?subject={quote(subjectAbbr)}'

        subjectPageFile = request.urlopen(subjectURL)
        subjectPageHTML = subjectPageFile.read().decode('utf8')
        subjectPageFile.close()

        return subjectPageHTML

    def parseSubjectCoursesPage(self, subject, pageHTML):
        pageSoup = BeautifulSoup(pageHTML, 'html.parser')

        classInfoCards = pageSoup.select('div[class*="class-info card"]')

        parsed = []

        for card in classInfoCards:
            courseCatalogNo = None
            courseTitle = None
            courseSection = None
            classNum = None
            instructor = None
            component = None
            type = None
            units = None
            requisites = None
            waitlist = None
            description = None
            dayTimes = None
            location = None

            body = card.select('div[class*="card-body"]')[0]

            ### Header
            header = body.findChildren('h3')[0]

            headerSpans = header.findChildren('span')
            headerLinks = header.findChildren('a')

            courseCatalogNo = headerLinks[0].string
            courseSection = headerSpans[0].string

            if len(headerSpans) > 1:
                courseTitle = headerSpans[1].string
            else:
                courseTitle = headerLinks[1].string

            ### Details
            details = body.findChildren('ul')[0]

            classNumP = details.findAll(text=lambda t: "Class Number" in t)[0].parent
            classNum = classNumP.contents[1]['id']

            footer = card.select('div[class*="card-footer"]')[0]

            footerTables = footer.findChildren('tr')

            if len(footerTables) > 1:
                try:
                    mainTable = footerTables[1]
                    items = mainTable.findChildren('th')

                    time = items[0].select('span[data-time]')[0].string
                    try:
                        location = items[1].select('a')[0].string
                    except:
                        location = "TBA"
                except:
                    ()

            itemDict = {
            'catalogNumber': courseCatalogNo,
            'section': courseSection,
            'title': courseTitle
            }

            parsed.append(itemDict)

        self.subjectCourses[subject] = parsed


if __name__ == '__main__':
    subjectParser = CourseParser('1224')
    subjectParser.start()

    import ipdb; ipdb.set_trace()

    # html_doc = open("raw_subjects.html", "r")
    #
    # soup = BeautifulSoup(html_doc, 'html.parser')
    #
    # # Get all subjects
    # # for part in soup.select('a[href*="class_list.html?subject"]'):
    # #     print(part.string)
    #
    # cs_courses = open("cs_courses.html", "r")
    #
    # cs_soup = BeautifulSoup(cs_courses, 'html.parser')
    #
    # for part in cs_soup.select('div[class*="class-info card"]'):
    #     header = part.findChildren("h3")[0]
    #
    #     courseNumber = header.findChildren("a")[0].string
    #     spans =  header.findChildren("span")
    #
    #     courseSection = spans[0].string
    #
    #     if len(spans) < 2:
    #         import ipdb; ipdb.set_trace()
    #
    #     courseTitle = spans[1].string
    #     print(f'{courseNumber} - {courseSection} {courseTitle}')
