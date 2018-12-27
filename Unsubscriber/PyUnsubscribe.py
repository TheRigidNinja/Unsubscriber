import imaplib, email, os

user = 'brian.shisanya2000@gmail.com'
password = '*********'
imap_url = 'imap.gmail.com'

#Where you want your attachments to be saved (ensure this directory exists) 
attachment_dir = 'your_attachment_dir'
# sets up the auth
def auth(user,password,imap_url):
    con = imaplib.IMAP4_SSL(imap_url)
    con.login(user,password)
    return con
# extracts the body from the email
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None,True)


def search(key,value,con):
    result, data  = con.search(None,key,'"{}"'.format(value))
    return data
#extracts emails from byte array


def get_emails(result_bytes):
    msgs = []
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)
    return msgs

con = auth(user,password,imap_url)
con.select('[Gmail]/Spam')
status, data  = con.search(None, 'ALL')


for num in reversed(data[0].split()):
	print(con.fetch(num, '(RFC822)')," ------------------------------ ")


