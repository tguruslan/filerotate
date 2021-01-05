#!/usr/bin/env python

from collections import defaultdict
from datetime import *
import sys, os, re, json

# ==============================================================================

data=json.loads(os.popen('rclone lsjson google-drive:{}'.format(sys.argv[1])).read())

dates=defaultdict(lambda: defaultdict(dict))
curDate=date.today()

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def gdriveDelete(files):
    for file in files:
        result=os.popen('rclone delete google-drive:{}/{} --drive-use-trash=false'.format(sys.argv[1],file).replace('//','/'))
    return result
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


for file in data:
    if re.match(r'{}'.format(sys.argv[2]), file['Name']):
        fDate=datetime.strptime(file['ModTime'].split('T')[0], '%Y-%m-%d').date()
        if dates[fDate.year][fDate.month].get(fDate.day,0) == 0:
            dates[fDate.year][fDate.month][fDate.day]=[file['Name']]
        else:
            dates[fDate.year][fDate.month][fDate.day].append(file['Name'])

for a in sorted(dates):
	for b in sorted(dates[a]):
		if ((curDate.year * 12 + curDate.month) - (a * 12 + b)) >= 18:
			for c in sorted(dates[a][b]):
				if b == sorted(dates[a].keys())[-1]:
					if c == sorted(dates[a][b].keys())[-1]:
						print('{} {} {} {} last in year need\n'.format(a,b,c,dates[a][b][c]))
					else:
						print('{} {} {} {} rm +\n'.format(a,b,c,dates[a][b][c]))
						gdriveDelete(dates[a][b][c])
				else:
					print('{} {} {} {} rm +\n'.format(a,b,c,dates[a][b][c]))
					gdriveDelete(dates[a][b][c])
		else:
			for c in sorted(dates[a][b]):
				if (curDate - date(a,b,c)).days >= 31:
					if c == sorted(dates[a][b].keys())[-1]:
						print('{} {} {} {} last in month need\n'.format(a,b,c,dates[a][b][c]))
					else:
						print('{} {} {} {} rm +'.format(a,b,c,dates[a][b][c]))
						gdriveDelete(dates[a][b][c])
				else:
					if (curDate - date(a,b,c)).days >= 7:
						if date(a,b,c).weekday() == 6:
							print('{} {} {} {} last in week need\n'.format(a,b,c,dates[a][b][c]))
						else:
							print('{} {} {} {} rm +\n'.format(a,b,c,dates[a][b][c]))
							gdriveDelete(dates[a][b][c])
					else:
						print('{} {} {} {} last 7day need\n'.format(a,b,c,dates[a][b][c]))
