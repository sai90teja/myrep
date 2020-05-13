from flask import Flask, render_template, request, url_for, redirect
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

usr = ''
pwd = ''


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global usr
        usr = request.form['username']
        global pwd
        pwd = request.form['password']

        return redirect(url_for('request_attendance'))
    return render_template('helo.html')


def request_attendance():
    all_content = ""
    global usr, pwd
    with requests.Session() as req:
        headers = \
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
            }
        res = req.get('http://vlearn.veltech.edu.in/login/index.php', headers=headers)

        login_data = {
            'username': usr,
            'password': pwd
        }
        res1 = req.post('http://vlearn.veltech.edu.in/login/index.php', headers=headers, data=login_data)

        soup1 = BeautifulSoup(res1.content, 'html.parser')
        tag1 = soup1.find_all("a", class_='')
        subject_ids = []
        attendance_ids = []
        for i in tag1:
            a = str(i['href'])
            link = 'http://vlearn.veltech.edu.in/course/view.php?id='
            if link in a:
                b = a.replace(link, '')
                if b not in subject_ids:
                    subject_ids.append(b)

        for j in subject_ids:
            link = 'http://vlearn.veltech.edu.in/course/view.php?id='
            link = link + j

            res2 = req.get(link, headers=headers)
            # print(res2.content)

            soup1 = BeautifulSoup(res2.content, 'html.parser')
            tag1 = soup1.find_all("a", class_='')
            for i in tag1:
                a = str(i['href'])
                link = 'http://vlearn.veltech.edu.in/mod/attendance/view.php?id='
                if link in a:
                    b = a.replace(link, '')
                    if b not in attendance_ids:
                        attendance_ids.append(b)

                        link1 = 'http://vlearn.veltech.edu.in/mod/attendance/view.php?id='
                        link1 = link1 + b + '&view=5'

                        a1 = link1 + b + '&view=1'
                        a2 = link1 + b + '&view=2'
                        a3 = link1 + b + '&view=3'
                        a4 = link1 + b + '&view=4'

                        res3 = req.get(link1, headers=headers)

                        soup_a = BeautifulSoup(res3.content, 'html.parser')
                        tg2 = soup_a.find('h1')
                        tg1 = soup_a.find_all("tbody")
                        tg1 = str(tg1)
                        tg1 = tg1.replace('<tbody>', '<table class="table table-bordered">')
                        tg1 = tg1.replace('</tbody>', '<table>')
                        tg1 = tg1.replace('[', '')
                        tg1 = tg1.replace(']', '')
                        tg1 = tg1.replace(',', '')
                        rem_html1 = """<td class="cell c0" style="text-align:left;"></td>
                        <td class="cell c1" style="text-align:center;"></td>
                        <td class="cell c2" style="text-align:right;"></td>"""
                        rem_html2 = """<td class="cell c3 lastcol" style="text-align:right;"><nobr><span class="attcurbtn">All</span><span class="attbtn"><a href="{3}">All past</a></span><span class="attbtn"><a href="{2}">Months</a></span><span class="attbtn"><a href="{1}">Weeks</a></span><span class="attbtn"><a href="{0}">Days</a></span></nobr></td>
                        </tr>""".format(a1, a2, a3, a4)
                        tg1 = str(tg2) + str(tg1)
                        tg1 = tg1.strip()
                        tg1 = tg1.replace(rem_html1, '')
                        tg1 = tg1.replace(rem_html2, '')
                        all_content = all_content + tg1
    return render_template('content.html', all_content=all_content)


app.add_url_rule('/attendance', 'request_attendance', request_attendance)

if __name__ == '__main__':
    app.run(debug=True)
