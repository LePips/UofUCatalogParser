class Campus:
    def __init__(self, title, baseURL, semesters):
        self.title = title
        self.baseURL = baseURL
        self.semesters = semesters

def calculateSemesterIDs(lowerBound = None):
    semesterYears = [id for id in range(988, 1225) if str(id)[-1] in ['4', '6', '8']]

    if lowerBound:
        semesterYears = [id for id in semesterYears if id >= lowerBound]

    semesterIDs = [str(id).zfill(4) for id in semesterYears]

    semesterMap = {}

    for year in semesterYears:
        stringID = str(year).zfill(4)
        adjustedYear = str(1900 + int(stringID[:3]))

        if stringID[3] == '4':
            semesterMap[f'Spring{ adjustedYear }'] = stringID
        elif stringID[3] == '6':
            semesterMap[f'Summer{ adjustedYear }'] = stringID
        elif stringID[3] == '8':
            semesterMap[f'Fall{ adjustedYear }'] = stringID

    return semesterMap

mainCampus = Campus('MainCampus',
                    'https://student.apps.utah.edu/uofu/stu/ClassSchedules/main',
                    calculateSemesterIDs())

asiaCampus = Campus('AsiaCampus',
                    'https://student.apps.utah.edu/uofu/stu/ClassSchedules/uac',
                    calculateSemesterIDs(1148))

uOnlineCampus = Campus('UOnline',
                        'https://student.apps.utah.edu/uofu/stu/ClassSchedules/online',
                        calculateSemesterIDs(1208))

allCampuses = [mainCampus, asiaCampus, uOnlineCampus]
