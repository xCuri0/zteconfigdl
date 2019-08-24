#!/usr/bin/python3
import re
import sys
import html
import requests

def main(ip, user, password, outfile):
    url = "http://" + ip + "/"
    session = requests.Session()

    Frm_Logintoken = re.findall(r"getObj\(\"Frm_Logintoken\"\)\.value = \"(.*?)\"\;", str(session.get(url, timeout=1).content), re.MULTILINE)[0]
    data = f"frashnum=&action=login&Frm_Logintoken={Frm_Logintoken}&Username={user}&Password={password}"
    session.post(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    if 'SID' not in session.cookies:
        print('Failed to login')
    
    manager_dev_config_t = str(session.get(url + "getpage.gch?pid=1002&nextpage=manager_dev_config_t.gch").content)

    UPLOAD_SESSION_TOKEN = re.findall(r"name=\"UPLOAD_SESSION_TOKEN\" value=\"(.*?)\"", manager_dev_config_t, re.MULTILINE)[0]
    fDownload = html.unescape(re.findall(r"name=\"fDownload\" method=\"POST\" action=\"(.*?)\"", manager_dev_config_t, re.MULTILINE)[0])

    headers = {
        'Content-Type': f'multipart/form-data; boundary=---------------------------{UPLOAD_SESSION_TOKEN}',
    }
    data = f'-----------------------------{UPLOAD_SESSION_TOKEN}\r\nContent-Disposition: form-data; name=\"config\"\r\n\r\n\r\n-----------------------------{UPLOAD_SESSION_TOKEN}--\r\n'

    configfile = session.post(f'{url}{fDownload}', data=data, headers=headers).content

    with open(outfile, 'wb') as s:
        print(f'Writing config file to {outfile}')
        s.write(configfile)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
