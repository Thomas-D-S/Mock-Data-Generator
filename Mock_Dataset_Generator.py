# A function that writes X number of mock data rows to a csv file in the local directory
# The CDEs included in the mock data is a Party ID, Account ID, First Name, Surname, Initials, Email, Telephone Number, Title, Birth Date, Gender Code, National Insurance Number, Sort Code, 
# Post Code, Inbound Post Code, Outbound Post Code, Relationship Type, Tax Code, Deceased Date and Death Notification Date.
# This function is reliant on three external files, make sure these are saved in the same directory as this file. The files are Last_Names.txt, First_Names.csv, UK_Area_Codes.txt

import random
import pandas as pd
import numpy as np
import string 
import random


def clean_date(dates):
    return ['0' + i[0:i.find('/')+1] + '0' + i[i.rfind('/')-1:] if len(i[0:i.find('/')]) == 1 and len(i[i.find('/')+1:i.rfind('/')]) == 1 else '0' + i 
    if len(i[0:i.find('/')]) == 1 else i[0:i.find('/')+1] + '0' + i[i.rfind('/')-1:] if len(i[i.find('/')+1:i.rfind('/')]) == 1  else i for i in dates]

def gen_data(rows):

    df = pd.DataFrame()

    #Party ID + Account ID
    print('pty_id')

    pty_ids, act_ids = [], []
    for i in [pty_ids, act_ids]:
        while len(i) != rows:
            curr_id = random.randint(10000000, 1000000000)
            if curr_id not in i:
                i.append(curr_id)
    df = df.assign(pty_id = pty_ids, act_id = act_ids)


    #Title
    print('title')

    poss_titles, title_weights = ['Mr', 'Mrs', 'Miss', 'Ms', 'Dr'], [49.5, 18, 16, 16 , 0.5]
    titles = [random.choices(poss_titles, title_weights)[0] for i in range(rows)]
    df = df.assign(psl_pty_tl = titles)


    #First Names
    print('first names')

    df_first_names = pd.read_csv('First_Names.csv')
    gender_order = [True if i == 'Mr' else False if i in ['Mrs', 'Miss', 'Ms'] else random.randint(0,1) for i in df['psl_pty_tl']]
    first_names = [
        df_first_names['Boy Names'][random.randint(0,len(df_first_names)-1)] if i 
        else df_first_names['Girl Names'][random.randint(0,len(df_first_names)-1)] 
        for i in gender_order]
    df = df.assign(frs_nm = first_names)


    #Surnames
    print('surnames')

    f = open('Last_Names.txt', 'r')
    list_contents= f.readlines()
    idxs = [random.randint(0, len(list_contents)-1) for i in range(rows)] 
    last_names = [list_contents[i][0:list_contents[i].find('\n')] for i in idxs if i != '\n']
    df = df.assign(sn = last_names)


    #Initials
    print('initials')

    df = df.assign(Initials = [i[0] for i in df['sn']])


    #Birth Date
    print('brth_date')

    birthdates = ['%s/%s/%s' %(random.randint(1,31), random.randint(1,12), random.randint(1940,2000)) for i in range(rows)]
    birthdates = ['0' + i[0:i.find('/')+1] + '0' + i[i.rfind('/')-1:] if len(i[0:i.find('/')]) == 1 and len(i[i.find('/')+1:i.rfind('/')]) == 1 else '0' + i 
    if len(i[0:i.find('/')]) == 1 else i[0:i.find('/')+1] + '0' + i[i.rfind('/')-1:] if len(i[i.find('/')+1:i.rfind('/')]) == 1  else i for i in birthdates] 
    df = df.assign(brt_date = birthdates)


    #Gender Code
    print('gnd')

    df = df.assign(Gender = ['U' if not random.randint(0,11) else 'M' if i else 'F' for i in gender_order])


    #Email
    print ('email')

    email_domains = [
    '@gmail.com', '@hotmail.com', '@outlook.com', '@yahoo.com', '@mail.com', '@aol.com', 
    '@gmail.co.uk', '@yahoo.co.uk', '@hotmail.co.uk', '@msn.com', '@zoho.com']
    emails = []

    for i in range(rows):
        curr_email, first_chosen = '', False
        if random.randint(0,1):
            curr_email += first_names[i] if random.randint(0,2) else first_names[i][0]
            first_chosen = True
        else:
            curr_email += last_names[i] 
        if random.randint(0,3):
            curr_email += '.'
        if first_chosen:
            curr_email += last_names[i]
        else:
            curr_email += first_names[i] if random.randint(0,2) else first_names[i][0]
        if random.randint(0,1):
            curr_email += str(random.randint(10, 999))
        curr_email += random.choice(email_domains)
        curr_email.replace(' ', '_')
        emails.append(curr_email)
    df = df.assign(email = emails)

    #Telephone Number
    print('tel')

    number_type, f = [random.randint(0,1) for i in range(rows)], open('UK_Area_Codes.txt', 'r')
    phone_area_codes = [i[0:i.find('\n')] for i in f.readlines() if i != '\n']
    phone_numbers = []
    for i in number_type:
        if i:
            phone_number = '+447' if random.randint(0,1) else '07'
        else:
            phone_number = random.choice(phone_area_codes)
        while len(phone_number) != 11:
            phone_number += str(random.randint(0,9))
        phone_numbers.append(phone_number) if '+' not in phone_number else phone_numbers.append(phone_number+str(random.randint(10,99)))
    df = df.assign(tel_no = phone_numbers)


    #National Insurance Number
    print('nino')

    ninos, illegal_prefixes = [], ['D', 'F', 'I', 'Q', 'U', 'V', 'BG', 'GB', 'KN', 'NT', 'TN', 'ZZ']
    while len(ninos) != rows:
        curr_nino = '{}{}{}'.format(''.join(random.sample(string.ascii_uppercase,2)), random.randint(100000,999999), random.choice(string.ascii_uppercase))
        nino_check = set(tuple([i for n, i in enumerate(curr_nino[0:2])] + [curr_nino[0:2]]))
        if not nino_check.intersection(illegal_prefixes):
            if curr_nino not in ninos:
                ninos.append(curr_nino)
    df = df.assign(nino = ninos)
    

    #Sort Code
    print('sort code')

    sort_codes = []
    while len(sort_codes) != rows:
        sort_code = '{}-{}-{}'.format(*[random.randint(10,99) for i in range(3)])
        if sort_code not in sort_codes:
            sort_codes.append(sort_code)
    df = df.assign(srt_cd = sort_codes)

    #Post Code
    print('post code')

    postcodes, postcode_formats  = [], {'outcodes':['LN', 'LNN', 'LLNN', 'LLNL', 'LNL'], 'incodes':['NL', 'NLL']}
    for i in range(rows):
        curr_format = '{} {}'.format(random.choice(postcode_formats['outcodes']), random.choice(postcode_formats['incodes']))
        curr_postcode = ''.join([random.choice(string.ascii_uppercase) if i == 'L' else random.choice(string.digits) if i == 'N' else i for i in curr_format])
        while '0' in curr_postcode[0:curr_postcode.find(' ')]:
            if curr_postcode[0:curr_postcode.find(' ')][-2:] in [str(i) for i in range(10,90, 10)]:
                break
            curr_postcode = ''.join([random.choice(string.ascii_uppercase) if i == 'L' else random.choice(string.digits) if i == 'N' else i for i in curr_format])
        postcodes.append(curr_postcode)
    postcodes
    df = df.assign(Postcodes = postcodes)

    #Post Code Incodes + Post Code Outcodes
    print('incode, outcode')

    postcode_outcodes = [i[0:i.find(' ')] for i in postcodes]
    postcode_incodes = [i[i.find(' ')+1:] for i in postcodes]  
    df = df.assign(ibd_post_cd = postcode_incodes, otb_post_codes = postcode_outcodes)

    #Relationship Type
    print('rel type')

    
    relationship_types = [random.choices(['Married', 'Living Together', 'Civil Partnership', 'Single'],[1,1,1,3])[0] for i in range(rows)]
    df = df.assign(rel_type = relationship_types)

    #Tax Code
    print('tax code')

    valid_tc, valid_tc_weights = ['1275L', '1275P', '1275V', '1275Y', '384T','K384', 'BR', 'OT', 'DO', 'NT'], [20, 6, 6, 6, 5, 5, 3, 3, 2, 4 ]
    tax_codes = [random.choices(valid_tc, valid_tc_weights)[0] if random.randint(0,3) else np.NaN for i in range(rows)]
    df = df.assign(tax_cd = tax_codes)

    #Deceased Date + Death Notificaiton Date
    print('deceased_dates')

    death_idxs, deceased_dates, death_notification = [random.randint(0,9) for i in range(rows)], [], []
    for n, i in enumerate(death_idxs):
        if i:
            curr_deceased_date, curr_death_noti = 'Null', 'Null'
        else:
            curr_deceased_date = '%s/%s/%s'%(
                random.randint(1,31), 
                random.randint(1,12), 
                random.randint(int(df.iloc[n]['brt_date'][-4:])+19,2020))
            curr_death_noti = '%s/%s/%s'%(
                random.randint(1,31), 
                random.randint(1,12), 
                random.randint(int(curr_deceased_date[-4:])+1,int(curr_deceased_date[-4:])+2))         
        deceased_dates.append(curr_deceased_date)
        death_notification.append(curr_death_noti)
    deceased_dates, death_notification = clean_date(deceased_dates), clean_date(death_notification)
    deceased_dates, death_notification = [i if i != 'Null' else np.NaN for i in deceased_dates], [i if i != 'Null' else np.NaN for i in death_notification]

    df = df.assign(dcd_dt = deceased_dates, dth_ntf_dt = death_notification)

    return df


datas = gen_data(100000)

datas

datas.to_csv('mock_data_100.csv', index=False)
