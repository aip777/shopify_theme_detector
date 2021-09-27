import requests
import csv
import json
import re

def shopify_theme_detector(url, find_word):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
    try:
        r = requests.get(url, headers=headers, timeout=10).text   
        is_shopify = r.count(find_word)
        if is_shopify:
            try:
                finder = re.findall(r'Shopify.theme = .*;', r)
                theme = json.loads(finder[0].replace('Shopify.theme = ', '').replace(';','').strip())
                theme_obj = {
                    'count_number':is_shopify,
                    'name':theme['name'],
                    'theme_id':theme['id'],
                    'theme_store_id': theme['theme_store_id'],
                }
                return theme_obj
            except Exception as e:
                theme_obj = {
                    'count_number':is_shopify,
                    'name':"Not Found",
                    'theme_id':"Not Found",
                    'theme_store_id': "Not Found",
                }
                return theme_obj
        else:
            return False   
    except Exception as e:
        return False

# csv data convert to list

with open('data.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

result = []
for website in data:
    site = website[0]
    rs = shopify_theme_detector(site, 'shopify')
    if rs:
        if rs['count_number']:
            print("Yes its shopify website", site)
            rs['website']=site
            result.append(rs)
    else:
        print("Its not shopify website", site)

# List data convert to csv
csv_file = "Names.csv"
csv_columns = ['count_number','website','theme_store_id','name','theme_id']
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in result:
            writer.writerow(data)
except IOError:
    print("I/O error")