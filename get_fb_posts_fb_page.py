#!/usr/bin/python
import json
import datetime
import csv
import time
import sys
import argparse # Using argparse to parse cli arguments
#import subprocess
import os

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

# app_id = "493304454337930"
# app_secret = "cac0d9826e6ff8533b67c7bccbf9e1ea" #Hangbo Zhao's app_secret
# access_token = app_id + "|" + app_secret
# access_token = "EAACEdEose0cBADsgsQgFZBui4T2SJjXWkLc3d7OwTa6XCivGWwtmfLSVDAOq1TC5uLVkdwafxauMtKVUJYxi80mH7oCID5nX0oE09WmurK4BASAjfxf1Wa4rUNuya4bBpZBFuGrjWKLTSXStRnHRT6vzDXpSuMAFz8dA7DDeojE0Vq3CnyRnJOOOsPIx0ZD"
# print "access_token : " +  access_token

# input date formatted as YYYY-MM-DD
date_now = datetime.datetime.now().strftime ("%Y-%m-%d")
time_delta = 7
date_7_days_ago = (datetime.datetime.now() - datetime.timedelta(days= time_delta)).strftime ("%Y-%m-%d")
since_date_default = date_7_days_ago  #"2017-07-8"
until_date_default = date_now #"2017-07-15"

# Set a parser object
parser = argparse.ArgumentParser()
### Mandatory Parameters
parser.add_argument("--page_id", type=str, help="facebook page_id")
parser.add_argument("--access_token", type=str, help="facebook api access_token")
parser.add_argument("--file_name", type=str, help="csv file_name")
### Optional Parameters
parser.add_argument("--since_date",type=str, default= since_date_default,
                    help="since_date to scrape (format YYYY-MM-DD , default today-7days)")
parser.add_argument("--until_date",type=str, default= until_date_default,
                    help="util_date to scrape (format YYYY-MM-DD , default today)")

args = parser.parse_args()
page_id      =  args.page_id
access_token =  args.access_token
since_date   =  args.since_date
until_date   =  args.until_date
file_name    =  args.file_name

def request_until_succeed(url):
    req = Request(url)
    success = False
    try_failed_count = 0
    while success is False and try_failed_count < 5:
        try:
            response = urlopen(req)
            if response.getcode() == 200:
                print("Succeed for URL {}: {}".format(url, datetime.datetime.now()))
                success = True
                try_failed_count = 0
        except Exception as e:
            try_failed_count = try_failed_count + 1
            print(e)
            time.sleep(5)

            print("Error for URL {}: {}".format(url, datetime.datetime.now()))
            print("Retrying.")

    return response.read()


# Needed to write tricky unicode correctly to csv
def unicode_decode(text):
    try:
        return text.encode('utf-8').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8')


def getFacebookPageFeedUrl(base_url):

    # Construct the URL string; see http://stackoverflow.com/a/37239851 for
    # Reactions parameters
    fields = "&fields=message,link,created_time,type,name,id," + \
        "comments.limit(0).summary(true),shares,reactions" + \
        ".limit(0).summary(true)"

    return base_url + fields


def getReactionsForStatuses(base_url):
    reaction_types = ['like', 'love', 'wow', 'haha', 'sad', 'angry']
    reactions_dict = {}   # dict of {status_id: tuple<6>}

    for reaction_type in reaction_types:
        fields = "&fields=reactions.type({}).limit(0).summary(total_count)".format(
            reaction_type.upper())

        url = base_url + fields

        data = json.loads(request_until_succeed(url))['data']

        data_processed = set()  # set() removes rare duplicates in statuses
        for status in data:
            id = status['id']
            count = status['reactions']['summary']['total_count']
            data_processed.add((id, count))

        for id, count in data_processed:
            if id in reactions_dict:
                reactions_dict[id] = reactions_dict[id] + (count,)
            else:
                reactions_dict[id] = (count,)

    return reactions_dict


def processFacebookPageFeedStatus(status):

    # The status is now a Python dictionary, so for top-level items,
    # we can simply call the key.

    # Additionally, some items may not always exist,
    # so must check for existence first

    status_id = status['id']
    status_type = status['type']

    status_message = '' if 'message' not in status else \
        unicode_decode(status['message'])
    link_name = '' if 'name' not in status else \
        unicode_decode(status['name'])
    status_link = '' if 'link' not in status else \
        unicode_decode(status['link'])

    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.

    status_published = datetime.datetime.strptime(
        status['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + \
        datetime.timedelta(hours=-5)  # EST
    status_published = status_published.strftime(
        '%Y-%m-%d %H:%M:%S')  # best time format for spreadsheet programs

    # Nested items require chaining dictionary keys.

    num_reactions = 0 if 'reactions' not in status else \
        status['reactions']['summary']['total_count']
    num_comments = 0 if 'comments' not in status else \
        status['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in status else status['shares']['count']

    return (status_id, status_message, link_name, status_type, status_link,
            status_published, num_reactions, num_comments, num_shares)


def scrapeFacebookPageFeedStatus(page_id, access_token, since_date, until_date, file_name):
	if not os.path.exists('csv'):
		os.makedirs('csv')

	with open('csv/{}_facebook_statuses.csv'.format(file_name), 'w') as file:
		w = csv.writer(file)
		w.writerow(["status_id", "status_message", "link_name", "status_type",
					"status_link", "status_published", "num_reactions",
					"num_comments", "num_shares", "num_likes", "num_loves",
					"num_wows", "num_hahas", "num_sads", "num_angrys",
					"num_special"])

        has_next_page = True
        num_processed = 0
        scrape_starttime = datetime.datetime.now()
        after = ''
        base = "https://graph.facebook.com/v2.9"
        node = "/{}/posts".format(page_id)
        parameters = "/?limit={}&access_token={}".format(100, access_token)
        since = "&since={}".format(since_date) if since_date \
            is not '' else ''
        until = "&until={}".format(until_date) if until_date \
            is not '' else ''

        print("Scraping {} Facebook Page: {}\n".format(page_id, scrape_starttime))

        while has_next_page:
            after = '' if after is '' else "&after={}".format(after)
            base_url = base + node + parameters + after + since + until
            print 'base_url is : ' + base_url

            url = getFacebookPageFeedUrl(base_url)
            statuses = json.loads(request_until_succeed(url))
            reactions = getReactionsForStatuses(base_url)

            for status in statuses['data']:

                # Ensure it is a status with the expected metadata
                if 'reactions' in status:
                    status_data = processFacebookPageFeedStatus(status)
                    reactions_data = reactions[status_data[0]]

                    # calculate thankful/pride through algebra
                    num_special = status_data[6] - sum(reactions_data)
                    w.writerow(status_data + reactions_data + (num_special,))

                num_processed += 1
                if num_processed % 100 == 0:
                    print("{} Statuses Processed: {}".format
                          (num_processed, datetime.datetime.now()))

            # if there is no next page, we're done.
            if 'paging' in statuses:
                after = statuses['paging']['cursors']['after']
            else:
                has_next_page = False

        print("\nDone!\n{} Statuses Processed in {}".format(
              num_processed, datetime.datetime.now() - scrape_starttime))

if __name__ == '__main__':
	print "page_id = " +  page_id
	print "access_token = " + access_token
	print "since_date = " + since_date + " until_date = " + until_date
	print "file_name = " + file_name
	scrapeFacebookPageFeedStatus(page_id, access_token, since_date, until_date, file_name)

#if __name__ == '__main__':
#  if len(sys.argv) <= 1:
#    print("Usage: -page_id <facebook page id>")
#    sys.exit(-1)
#
#  if sys.argv[1] == '-page_id':
#      page_id = sys.argv[2]
#      scrapeFacebookPageFeedStatus(page_id, access_token, since_date, until_date)
#      sys.exit(-1)
#
#  else:
#      print("Usage:python get_fb_posts_fb_page.py -page_id <facebook page id> ")
#      sys.exit(-1)
