__author__ = 'dmalik'

"""
This is just to update gorilla standard process
Uages
python google.py <GAID> <BUILD_NUMBER> <BUILD TIME>
"""

import sys
import os
import gspread as gs
import dotenv

DOTENV = '/var/lib/jenkins/.env'

dotenv.read_dotenv(DOTENV)

try:
    email = os.getenv('gl_email')
    password = os.getenv('gl_password')
except:
    print "Please update user & password"
    sys.exit()
else:
    xls = gs.login(email, password)

PRINARY_SHEET = '14eaBwd73nL6vYcGPXeXSW4M44jzR-eAuJHewVAgHbHE'

try:
    GAID = sys.argv[1]
    build_number = sys.argv[2]
    build_time = sys.argv[3]
except:
    build_number = None
    build_time = None

try:
    git_commit = os.getenv('GIT_COMMIT')
except:
    pass


class GorillaBusinessFlow(object):

    def __init__(self, gaid, sheet= 'Theme',
                 uuid=PRINARY_SHEET,
                 build_number=None,
                 build_time=None,
                 git_commit=None,
    ):
        self.uuid = uuid
        self.gaid = gaid
        self.gaid_sheet = sheet

        self.build_number = build_number
        self.build_time = build_time

        self.git_commit = git_commit

        self.ws_checklist = None
        self.ws_info = None
        self.ws_uat = None
        self.repo_name = None
        self.repo_url = None
        self.repo_source_url = None
        self.type_of_theme = None
        self.developer = None
        self.uat_tester = None
        self.code_reviewer = None
        self.theme_file_uuid = None
        self.theme_file_url = None
        self.demo_url = None
        self.build_tracker_uid = None
        self.set_theme_data()

        self.uat_cols = {
            '1': self.build_number,
            '2': self.developer,
            '3': self.uat_tester,
            '4': self.code_reviewer,
            '5': self.demo_url,
            '6': self.repo_url,
            '7': self.git_commit,
            '8': self.build_time
        }

        self.build_tracker_cols = {
            '1': self.gaid,
            '2': self.repo_name,
            '3': self.build_number,
            '4': self.theme_file_url,
            '5': self.demo_url,
            '6': self.build_time
        }

    def get_theme_sheet(self):
        s = xls.open_by_key(self.theme_file_uuid)
        return s

    def get_theme_checklist(self):
        s = self.get_theme_sheet()
        return s.worksheet(self.ws_checklist)

    def get_theme_information(self):
        s = self.get_theme_sheet()
        return s.worksheet(self.ws_info)

    def get_uat_ws(self):
        s = self.get_theme_sheet()
        return s.worksheet(self.ws_uat)

    def get_worksheet_obj(self):
        s = xls.open_by_key(self.uuid)
        return s.worksheet(self.gaid_sheet)

    def get_rownumber(self):
        worksheet = self.get_worksheet_obj()
        r = worksheet.find(self.gaid)
        return r.row

    def get_build_tracker_ws(self):
        s = xls.open_by_key(self.build_tracker_uid)
        return s


    def set_theme_data(self):
        ws = self.get_worksheet_obj()
        rownumber = self.get_rownumber()
        self.gaid, \
        self.ws_checklist, \
        self.ws_info, \
        self.ws_uat, \
        self.repo_name, \
        self.repo_url, \
        self.repo_source_url, \
        self.type_of_theme, \
        self.developer, \
        self.uat_tester, \
        self.code_reviewer, \
        self.theme_file_uuid, \
        self.theme_file_url, \
        self.demo_url, \
        self.build_tracker_uid = ws.row_values(rownumber)[0:15]
        return

    def next_free_row(self, w):
        r = len(w.col_values(1))
        return r + 1

    def update_uat(self):
        s = self.get_uat_ws()
        row = self.next_free_row(s)
        for col, value in self.uat_cols.items():
            s.update_cell(row, col, value)

    def update_build_tracker(self):
        ws = self.get_build_tracker_ws()
        s = ws.worksheets()[0]
        row = self.next_free_row(s)
        for col, value in self.build_tracker_cols.items():
            s.update_cell(row, col, value)



if __name__ == '__main__':
    g = GorillaBusinessFlow(sys.argv[1],
                            build_number=build_number,
                            build_time=build_time,
                            git_commit=git_commit,
    )
    g.update_uat()
    g.update_build_tracker()


