'''
Author : Bhishan Bhandari
bbhishan@gmail.com

The following script uses python2 and following default libraries
csv 	to read and write to csv format.

sys 	to exit the program when no csv files are found.

glob 	to search for csv files in the current directory.

smtplib to send email.

email 	to create email message as well as encode attachments.

os 	to delete the old csv file.
'''

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import csv 
import sys
import glob
import time
import datetime
import os

def send_mail(original_file, final_file):

    '''
	params: string original file name, string final file name

	Takes the file name of original csv file and output csv file name as input parameters. Generates timestamp 
	Create email template containing informations original file name, final file name, timestamp along with
 the attachment of the final csv file. The sender email must be gmail account.
    '''
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts-0).strftime('%Y-%m-%d %H:%M:%S')

    fromaddr = "from@gmail.com"		#replace with your gmail email.
    toaddr = "to@gmail.com"		#email to whom message is to be sent.
 
    msg = MIMEMultipart()
 
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Feed Conversion Report"
 
    body = "Hi, \n Original File Name : " + original_file + "\n Final File Name : " + final_file + "\n Date of Run : " + st + "\n Thanks." 
 
    msg.attach(MIMEText(body, 'plain'))
 
    filename = final_file
    attachment = open(final_file, "rb")
 
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
    msg.attach(part)
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "frompassword")	#password of from address at line 43.
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def main():

    '''
	Searches the current working directory for files with extension .csv
        For all the csv files found which is not named cdk-dh-feed.csv, modifies the csv file and
	saves as cdk-dh-feed.csv . Sends
    '''
    files = glob.glob("*.csv")
    if len(files) < 1: 
        sys.exit(1)

    for each_file in files:
        if each_file != 'cdk-dh-feed.csv':
            ID = ''
            ID2 = ''
            Item_title = ''
            Final_URL = ''
            Image_URL = ''
            Item_subtitle = ''
            Item_description = ''
            Item_category = ''
            Price = ''
            Sale_price = ''
            Contextual_keywords = ''
            Item_address = ''
            Tracking_template = ''

            
    
            try:
                csvwriter = csv.writer(file('cdk-dh-feed.csv', 'wb'))
                csvwriter.writerow(['ID', 'ID2', 'Item title', 'Final URL', 'Image URL', 'Item subtitle', 'Item description', 'Item category', 'Price', 'Sale price', 'Contextual keywords', 'Item address', 'Tracking template'])
                with open(each_file,'rt') as csvfile1:
                    reader = csv.reader(csvfile1)
                    headers = next(reader, None) 

                    for r in reader:
                        ID = str(r[0])
                        ID2 = str(r[1])
                        Item_title = str(r[2]) + " " + str(r[3]) + " " + str(r[4]) + " " + str(r[5])
                        Final_URL = str(r[-1])
                        Image_URL = str(r[6])
                        Price = str(r[7]) + " USD"
                        csvwriter.writerow([ID, ID2, Item_title, Final_URL, Image_URL, Item_subtitle, Item_description, Item_category, Price, Sale_price, Contextual_keywords, Item_address, Tracking_template])
                send_mail(each_file, 'cdk-dh-feed.csv') 
                os.remove(each_file)   
            except:
                print "Modification of csv file unsuccessful."
    
    


if __name__ == '__main__':
    main()
