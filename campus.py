class Campus:
    def __init__(self, title, baseURL, semesters):
        self.title = title
        self.baseURL = baseURL
        self.semesters = semesters

# TODO: fill in all past semesters

mainCampus = Campus('MainCampus',
                    'https://student.apps.utah.edu/uofu/stu/ClassSchedules/main',
                    {
                        'Spring2022': '1224',
                        'Fall2021': '1218',
                        'Summer2021': '1216',
                        'Spring2021': '1214'
                    })

asiaCampus = Campus('AsiaCampus',
                    'https://student.apps.utah.edu/uofu/stu/ClassSchedules/uac',
                    {
                        'Spring2022': '1224'
                    })

uOnlineCampus = Campus('UOnline',
                        'https://student.apps.utah.edu/uofu/stu/ClassSchedules/online',
                        {
                            'Spring2022': '1224'
                        })

allCampuses = [mainCampus, asiaCampus, uOnlineCampus]
