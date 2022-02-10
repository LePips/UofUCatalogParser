import json
import os
import re

from bs4 import BeautifulSoup
from campus import allCampuses
from urllib import request
from urllib.parse import quote

# TODO: better print outs

class SemesterParser:

    def __init__(self, campus, catalogName, catalogNum):
        self.baseURL = f'{campus.baseURL}/{catalogNum}/'
        self.campus = campus
        self.catalogName = catalogName
        self.catalogNum = catalogNum
        self.subjects = {}
        self.subjectCourses = {}

    def parseSemester(self):

        print(f'\nBeginning to parse semester: { self.catalogName }\nCampus: { self.campus.title }')

        homePage = self.getHomePage()
        self.parseHomePage(homePage)

        for subject in list(self.subjects.keys()):
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

        self.title = pageSoup.findChildren('span')[2].string[3:]

        for subject in pageSoup.select('a[href*="class_list.html?subject"]'):
            subjectToken = subject.string.split(' - ')
            subjectAbbr = subjectToken[0].replace(' ', '-')
            subjectTitle = subjectToken[1]
            self.subjects[subjectAbbr] = subjectTitle

        print("-- parsed home page")

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

            # TODO: other details from footer via some regex, as not all items
            #       are always present

            itemDict = {
            'catalogTitle': courseCatalogNo,
            'section': courseSection,
            'courseTitle': courseTitle
            }

            parsed.append(itemDict)

        self.subjectCourses[subject] = parsed

        print(f'-- parsed subject: { subject }')

    def writeFiles(self):
        self.writeMainFile()

        for subjectAbbr in self.subjectCourses:
            self.writeSubjectCoursesFile(subjectAbbr)

    def writeMainFile(self):
        semesterSubjects = f'{ self.campus.title }/{ self.catalogName }/subjects.json'

        os.makedirs(os.path.dirname(semesterSubjects), exist_ok = True)

        with open(semesterSubjects, "w") as subjectsFile:
            subjectsRAW = f'{{"semester": { json.dumps(self.catalogName) }, "id": { json.dumps(self.catalogNum) }, "subjects": { json.dumps(self.subjects) }}}'
            subjectJSON = json.loads(f'{ subjectsRAW }')
            subjectsFile.write(json.dumps(subjectJSON, indent = 4))

    def writeSubjectCoursesFile(self, subjectAbbr):
        subjectCourses = f'{ self.campus.title }/{ self.catalogName }/{ subjectAbbr }.json'

        with open(subjectCourses, "w") as subjectCoursesFile:
            coursesRAW = f'{{"courses": { json.dumps(self.subjectCourses[subjectAbbr]) }}}'
            coursesJSON = json.loads(coursesRAW)
            subjectCoursesFile.write(json.dumps(coursesJSON, indent = 4))

if __name__ == '__main__':

    # TODO: arguments for not parsing files that already exist, or override

    for campus in allCampuses:
        for semester in campus.semesters:
            subjectParser = SemesterParser(campus, semester,  campus.semesters[semester])
            subjectParser.parseSemester()
            subjectParser.writeFiles()
