import requests

import base64, pickle, json, pprint, datetime, yaml, requests, urllib, urllib2, time

try:
    from urllib.request import Request, urlopen, HTTPError  # Python 3
except:
    from urllib2 import Request, urlopen, HTTPError  # Python 2

'''
Set : 
DUT = 1 for CAWS QA with user  amitpatel741234567890gmailcom
DUT = 2 for CAWS QA with user  amitpatel
DUT = 3 fopr CAWS PATCH QA with user  patellabs
DUT = 5 for BETA patch system

'''

Dut = 4
# FIXME - [Tsune] uncommented invalid URL token refered below (my guess) URL_SUBMIT_TOKEN.txt is not at directory
target_url = open("/Users/design/GitHub/CAWS_API_2.2_V1/URL_SUBMIT_TOKEN.txt", 'a+')

if Dut == 1:
    # cawsqa -- user/password
    username = "amitpatel741234567890gmailcom"
    password = "D7A37396AB0C40CBA489D88316D727F3"
    url = "http://apiqa.qa.colo1.nsslabs.com"

if Dut == 2:
    # cawsqa -- user/password
    username = "amitpatel"
    password = "BB8FA646126D4C8991C6088E1E60E684"
    url = "http://apiqa.qa.colo1.nsslabs.com"

if Dut == 3:
    # caws qa patch
    username = "patellabs"
    password = "240DA1A652B44014993D59986156DE47"
    url = "http://apiqa-patch.qa.colo1.nsslabs.com"
    # url = "http://10.144.192.71:8081/Scan/URL/"
    # url = "http://10.144.192.71:8081"

if Dut == 4:
    # caws qa patch
    username = "patellabs"
    password = "2992A2D48ED942A2A3596D762A4415BC"
    url = "http://data.nsslabs.com/"

if Dut == 5:
    # caws Beta
    username = "patellabs"
    password = "2992A2D48ED942A2A3596D762A4415BC"
    # url = "http://10.144.192.60:82"
    # url = "https://apibeta.nsslabs.com"
    url = "https://apibeta.nsslabs.com"
    # url = "http://apibeta.nsslabs.com/Scan/url/"


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


def submit_invalid_url(base_api_url="", username="", password="", action="", extention="", full_url="", url_combo="",
                       url_list_file=""):
    # print datetime.date.today() - datetime.timedelta(days=i)
    base64string = base64.b64encode('%s:%s' % (username, password))
    if action == "":
        base_api_url = base_api_url + '/Scan/url/'
    if extention != "":
        urls_to_submit1 = 'http://amit-patel.com/test/test' + extention + '/'
        final_urls_to_submit = 'url' + ':' + urls_to_submit1
        # print "final_urls_to_submit is : ", final_urls_to_submit
        urls_to_submit1 = urllib.quote_plus(urls_to_submit1)
        # data = urllib.urlencode('url' + urls_to_submit1)
        data = 'url=' + urls_to_submit1

    if full_url != "":
        urls_to_submit1 = urllib.quote_plus(full_url)
        # data = urllib.urlencode('url' + urls_to_submit1)
        data = 'url=' + urls_to_submit1

    if url_combo != "":
        data = urllib.urlencode(url_combo) + '&browserPackage=1&template=1'
        # data_1 =  urllib.urlencode('browserPackage=1', 'applicationPackage=1')
        # print "new url is combo:  ", base_api_url, "urls_to_submit is :" ,  data

    if url_list_file != "":
        testsite_array = []
        line_num = 0
        with open(url_list_file, "r") as ins:
            for line in ins:
                #                array.append(line)
                # ===================================================================
                # if line_num <= 460:
                #     line_num = line_num + 1
                #     continue
                # ===================================================================
                line_num = line_num + 1
                line = line.replace(" ", "")
                line = line.rstrip('\n')
                line = line.rstrip('\r')
                line = line.lstrip()
                if "http" not in line:
                    line = "http://" + line
                testsite_array.append(line)
                # values1 = (('url' , 'http://empowernetworkpackage.com/test2/test.php/'),
                # ('url', 'http://www.akilaindia.com/'),
        testsite_array_len = len(testsite_array)
        url_blocks_arrays = split(testsite_array, 20)
        total_blocks = len(url_blocks_arrays)

        for k in range(len(url_blocks_arrays)):
            if k > 14:
                continue;
            target_url = open("/Users/apatel/Documents/workspace/URL_SUBMIT_TOKEN.txt", 'a+')
            values1 = ""
            for i in url_blocks_arrays[k]:
                # print i
                values1 = values1 + 'url=' + urllib.quote_plus(i) + '&'
            data = values1 + '&browserPackage=2&template=1'
            print "new url is url file:  ", base_api_url, "urls_to_submit is :", data
            pre_submit_time = datetime.datetime.now()
            capture_list = sub_api_call(base_api_url=base_api_url, data=data, base64string=base64string)
            post_submit_time = datetime.datetime.now()
            print "time taken for submit call is :", (post_submit_time - pre_submit_time)
            if type(capture_list) is dict:
                token_list = capture_list['Token']
                print "total tokens returned are : ", len(token_list)
                tmp_cnt = 1;
                for token in token_list:
                    capture_token_string = str(k) + "-" + str(tmp_cnt) + " ; " + str(post_submit_time) + " ; " + \
                                           url_blocks_arrays[k][tmp_cnt - 1] + " ; " + token
                    # capture_token_string = str(now)  + " ; "   + token
                    print capture_token_string
                    target_url.write(capture_token_string)
                    target_url.write("\n")
                    tmp_cnt = tmp_cnt + 1
            target_url.close()
            time.sleep(300)

        return (capture_list)


def sub_api_call(base_api_url="", data="", base64string=""):
    base_api_url = base_api_url
    data = data
    base64string = base64string

    q = Request(base_api_url, data)
    q.add_header("Authorization", "Basic %s" % base64string)
    q.add_header('Accept-encoding', 'gzip, deflate')
    q.add_header('Connection', "keep-alive")
    q.add_header('context', 'ssl._create_unverified_context()')
    q.add_header('Accept',
                 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')  # q.add_header('User-agent', 'Mozilla/5.0')
    q.add_header('User-Agent',
                 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')

    try:
        a = urllib2.urlopen(q).read()
        # cookie = a.getheader('Set-Cookie')
    except urllib2.HTTPError, e:
        error_message = e.read()
        print  error_message
        return error_message
        data = {}
    data = json.loads(a)
    data = byteify(data)
    # print "printing status for the token :" , token
    pprint.pprint(data)
    return (data)


def get_file_submit_status(url, username, password, token):
    # print datetime.date.today() - datetime.timedelta(days=i)
    base64string = base64.b64encode('%s:%s' % (username, password))
    new_url = url + '/Scan/Status/url/' + token
    print "new url is : ", new_url
    q = Request(new_url)
    # q = Request(url+'/files/32CC69ECEDE54C689D5BCF755A48144C')
    # q = Request('http://apiqa.qa.colo1.nsslabs.com/Captures/List')
    # q = Request('http://apiqa-patch.qa.colo1.nsslabs.com/statistics/global?startDate=2016-11-01&endDate=2016-1201')
    q.add_header("Authorization", "Basic %s" % base64string)
    q.add_header('Accept-encoding', 'gzip, deflate')
    q.add_header('Connection', "keep-alive")
    q.add_header('context', 'ssl._create_unverified_context()')
    # q.add_unredirected_header('User-Agent', 'Custom User-Agent')
    q.add_header('Accept',
                 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')  # q.add_header('User-agent', 'Mozilla/5.0')
    q.add_header('User-Agent',
                 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    # q.add_headers = ('User-Agent', 'Mozilla/5.0')

    # a = {}
    # a = requests.get('http://apiqa.qa.colo1.nsslabs.com/Captures/List', auth=('amitpatel741234567890gmailcom', 'D7A37396AB0C40CBA489D88316D727F3'))
    try:
        a = urllib2.urlopen(q).read()
        # cookie = a.getheader('Set-Cookie')
    except urllib2.HTTPError, e:
        error_message = e.read()
        print  error_message
        return error_message

    data = {}
    data = json.loads(a)
    data = byteify(data)
    print "printing status for the token :", token
    pprint.pprint(data)
    return (a)


def check_capture_list_type(capture_list):
    capture_list = capture_list
    if type(capture_list) is dict:
        # data  = {}
        # data = json.loads(capture_list)
        # data = byteify(data)
        # #data = yaml.safe_load(json.loads(a))
        # pprint.pprint(data)
        data = capture_list
        token_list = data['Token']
        for token in token_list:
            # print line , "Token is : " , token
            # token_submit_status = get_file_submit_status( url, username, password, token)
            now = datetime.datetime.now()
            # capture_token_string = str(line_num) + ";" + str(now)  + " ; "  + line + " ; " + token
            capture_token_string = str(now) + " ; " + token
            print capture_token_string
            target_url.write(capture_token_string)
            target_url.write("\n")
    elif type(capture_list) is list:
        print "Returned as list :", capture_list

    elif type(capture_list) is str:
        print "Returned as string really :", capture_list
        print capture_list.split(":")
        print capture_list.split(':', 1)
        print capture_list.split(':', 2)
    else:
        print "Return is a unknown :", capture_list, ":"


values1 = (('url', 'http://empowernetworkpackage.com/test2/test.php/'),
           ('url', 'http://www.akilaindia.com/'),
           ('url', 'http://www.sandesh.com/'),
           ("url", 'http://www.timeofindia.com/'),
           ("url", 'http://www.divyabhaskar.com/'))

values2 = (('url', 'http://amit-patel-test1.com/test1.apk/'),
           ('url', 'http://amit-patel-test2.com/test2.bat/'),
           ('url', 'http://amit-patel-test3.com/test3.bin/'),
           ("url", 'http://amit-patel-test4.com/test4.cab/'),
           ("url", 'http://amit-patel-test5.com/test5.cmd/'))

invalid_url_ext_list = [".apk", ".bat", ".bin", ".cab", ".cmd", ".css", ".dat", ".dll", ".doc", ".enc", ".exe", ".flv",
                        ".gif",
                        ".gzip", ".ico", ".inf", ".jpeg", ".js", ".mp3", ".msi", ".nub", ".pdf", ".pif", ".png", ".rar",
                        ".scr", ".txt", ".vbs", ".wix", ".wmv", ".xls", ".zip", ".jpg"]

# capture_list = submit_invalid_url( url=url, username=username, password=password, url_combo=values1)
# FIXME: topsites.txt file does not exist
capture_list = submit_invalid_url(base_api_url=url, username=username, password=password,
                                  url_list_file="/Users/design/GitHub/CAWS_API_2.2_V1/topsites.txt")
# check_capture_list_type(capture_list)


target_url.close()
print "program is done"
''' 
print "now will wait for 300 secs."
time.sleep(300)

with open("/Users/apatel/Documents/workspace/target_url.txt", "r") as ins:
#with open("/Users/apatel/Documents/workspace/topsites.txt", "r") as ins: 

    array = []
    line_num=0
    for line in ins:
#                array.append(line)
        if line_num <= 460:
            line_num = line_num + 1
            continue
        line_num = line_num + 1
        line=line.replace(" ", "")
        line=line.rstrip('\n')
        line=line.rstrip('\r')
        line=line.lstrip()
        if "http" not in line:
            line="http://" + line
        print "line is:",line,":"    
        capture_list = submit_invalid_url( base_api_url=url, username=username, password=password, full_url = line)
        now = datetime.datetime.now()
        #capture_list = submit_invalid_url( url=url, username=username, password=password, full_url = "http://103.1.249.74:30003/index.php?OSVer=%d")
        #capture_list = submit_url( url, username, password, values1)
        #print "capture_list in row form is : ", capture_list  
        if type(capture_list) is dict:
                #data  = {}
                #data = json.loads(capture_list)
                #data = byteify(data)
                # #data = yaml.safe_load(json.loads(a))
                #pprint.pprint(data)
                data = capture_list
                token_list = data['Token']
                for token in token_list:
                    #print line , "Token is : " , token 
                    #token_submit_status = get_file_submit_status( url, username, password, token)
                    capture_token_string = str(line_num) + ";" + str(now)  + " ; "  + line + " ; " + token
                    print capture_token_string 
                    target_url.write(capture_token_string)
                    target_url.write("\n")
        elif type(capture_list) is list:
            print "Returned as list :" , capture_list
            
        elif type(capture_list) is str:
            print "Returned as string really :" , capture_list
            print capture_list.split(":" )
            print capture_list.split(':', 1 ) 
            print capture_list.split(':', 2 )  
        else:
            print "Return is a unknown :", capture_list,":"
   



if isinstance(capture_list, dict):
    print "Returned dictionary :" 
    data  = {}
    data = json.loads(capture_list)
    # #data = byteify(data)
    # #data = yaml.safe_load(json.loads(a))
    pprint.pprint(data)
        
if isinstance(capture_list, str): 
    print "Returned string :", capture_list
    
if isinstance( capture_list, list):
    print "Returned as list :" , capture_list  
    




invalid_url_ext_list = [".apk", ".bat", ".bin", ".cab", ".cmd", ".css", ".dat", ".dll", ".doc", ".enc", ".exe", ".flv", ".gif",
".gzip", ".ico", ".inf", ".jpeg", ".js", ".mp3", ".msi", ".nub", ".pdf", ".pif", ".png", ".rar",
".scr", ".txt", ".vbs", ".wix", ".wmv", ".xls", ".zip", ".jpg"]


for invalid_url_ext in invalid_url_ext_list:
#payload = "url=http%3A%2F%2Fabcd.com&url=http%3A%2F%2Fxyz."+"apk"
#payload = "url=http%3A%2F%2Fabcd"+".com"
    payload = "url=http%3A%2F%2Fabcd"+invalid_url_ext
    headers = {
        'authorization': "Basic cGF0ZWxsYWJzOjI5OTJBMkQ0OEVEOTQyQTJBMzU5NkQ3NjJBNDQxNUJD",
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
        #'postman-token': "326ebc98-0eae-8709-deb5-adcec4ea9914"
        }
    
    response = requests.request("POST", url, data=payload, headers=headers)
    print "Response for the submit URL http://apibeta.nsslabs.com/Scan/url/ request which returns tokens."
    print(response.text)

'''
