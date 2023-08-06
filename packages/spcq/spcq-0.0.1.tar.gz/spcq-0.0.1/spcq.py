def check_complaint(complaint_number):
    import sys
    from bs4 import BeautifulSoup
    import requests
    from pprint import pprint
    #complaint_number=97939
    url='http://igpcms.sindhpolice.gov.pk/Complaint_Detail_For_Complainant.aspx?Complaint_Id={}'.format(complaint_number)

    res = requests.get(url)
    parsed = BeautifulSoup(res.text, 'html.parser')
    complaint = {
            'id':0,
            'cnic':'-',
            'date':'-',
            'time':'-',
            'name':'-',
        }

    print('\nSINDH POLICE COMPLAINT')
    print('----------------------')

    try:
        complaint['id'] = parsed.find('span', {'id': 'Label_Track'}).text
        complaint['date'] = parsed.find('span', {'id': 'Label_Date'}).text
        complaint['time'] = parsed.find('span', {'id': 'LabelTime'}).text
        complaint['cnic'] = parsed.find('span', {'id': 'LabelCNIC'}).text
        complaint['cname'] = parsed.find('span', {'id': 'Label_Complainent_Name'}).text
        complaint['fname'] = parsed.find('span', {'id': 'Label_Father_Namne'}).text
        complaint['deadline'] = parsed.find('span', {'id': 'LabelResponseDate'}).text
        complaint['status'] = parsed.find('div', {'class': 'middle_text'}).text
        complaint['comments'] = parsed.find('span', {'class': 'title'})
    except:
        print('ERROR: ', 'Failed to acquire complaint.')

    print('ID: ', complaint['id'])
    print('DATE: ', complaint['date'])
    print('TIME: ', complaint['time'])
    print('CNIC: ', complaint['cnic'])
    print('COMPLAINANT: ', complaint['cname'])
    print('FATHER: ', complaint['fname'])
    print('DEADLINE: ', complaint['deadline'])
    print('STATUS: ', complaint['status'].strip())
    if complaint['comments']:
        print('COMMENTS: ')
        c = complaint['comments']
        while True:
            c = c.nextSibling
            if c:
                pprint(c.text)
            else:
                break


if __name__ == '__main__':

    complaint_number=sys.argv[1]
    check_complaint(complaint_number)
