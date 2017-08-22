#!/usr/bin/python
import sys
import subprocess
import argparse # Using argparse to parse cli arguments
import datetime

app_id = "493304454337930"
app_secret = "cac0d9826e6ff8533b67c7bccbf9e1ea" #Hangbo Zhao's app_secret

# access_token = app_id + "|" + app_secret
# each token is valid only for  2 hours
# access_token = "xxx"
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
### Optional Parameters
parser.add_argument("--since_date",type=str, default= since_date_default,
                    help="since_date to scrape (format YYYY-MM-DD , default today-7days)")
parser.add_argument("--until_date",type=str, default= until_date_default,
                    help="util_date to scrape (format YYYY-MM-DD , default today)")

args = parser.parse_args()
page_id      = args.page_id
access_token = args.access_token
since_date   = args.since_date
until_date   = args.until_date

page_ids = [
        #SportPesa
        "1405760996324754", # SportPesa Care(@SportPesaKenya) fans 260K
        "1867805660116956", # SportPesa (@SportPesaOfficial) fans 260K
        "902712263200628", # SportPesa Tanzania(@SportPesaTZ) fans 6k
        "1566015680331387", # SportPesa News(@SportPesanews) fans 200K
        "174615826306470", # SportPesa JackPot&Mega JackPot(@sportpesajackpotmega) fans 7K
        #Betin
        "165050220570368", # Betin fans 600
        "1279345088752660", # Betin Uganda fans 1300
        #BetWay
        "118919844934195", # Betway (@Betway) fans 150K
        "1364893833626548", # BetWay SafeGames (@BetWayOfficialSafeGames) fans 60K
        #BetPawa
        "1604218366574621", #BetPawa Kenya fans 28K
        "1866779623582263", #BetPawa Uganda fans 4K
        #Elitebet
        "367023026816184", #Elitebet KE fans 67K
        "193386711162910", #EliteBet Uganda fans 8K
        #Betika
        "582575691926792", #Betika kenya fans 300
        #Mcheza
        "246794449031956", #Mcheza fans 2800
        #Betyetu
        "546815985451460", # Betyetu (@Betyetu) fans 65K
        #goal.com
        "25427813597", # goal.com global fans 16.6M
        #all football
        "1195121897229652" # all football global fans 2.3M
]

page_id_name = {
        #SportPesa
        "1405760996324754" : "SportPesa_Care",
        "1867805660116956" : "SportPesa",
        "902712263200628" : "SportPesa_TZ",
        "1566015680331387" : "SportPesa_News",
        "174615826306470" : "SportPesa_JackPot_MegaJackPot",
        #BetWay
        "118919844934195" : "Betway",
        "1364893833626548" : "BetWay_SafeGames",
		#Betin
		"165050220570368" :"Betin",
		"1279345088752660" : "Betin_Uganda",
		#BetWay
		"118919844934195" : "Betway",
		"1364893833626548" : "BetWay_SafeGames",
		#BetPawa
		"1604218366574621" : "BetPawa_Kenya",
		"1866779623582263" : "BetPawa_Uganda",
		#Elitebet
		"367023026816184"  : "Elitebet_KE",
		"193386711162910"  : "EliteBet_Uganda",
		#Betika
		"582575691926792" : "Betika_kenya",
		#Mcheza
		"246794449031956" : "Mcheza",
        #Betyetu
		"546815985451460" : "BetYetu"
        #goal.com
		"25427813597" : "Goal_Com"
        #all football
		"1195121897229652" : "All_Football"
}

def scrape_all():
    for p_id in page_ids:
		print "p_id is : " + p_id
		cmd = "python get_fb_posts_fb_page.py --page_id " + p_id + " --access_token " + access_token + " --since_date " + since_date + " --until_date " + until_date + " --file_name " + page_id_name[p_id] + " "
		print "cmd is : " + cmd
		subprocess.call(cmd, shell=True)
        #time.sleep(60)
    sys.exit(-1)

def scrape_one():
	cmd = "python get_fb_posts_fb_page.py --page_id " + page_id + " --access_token " + access_token + " --since_date " + since_date + " --until_date " + until_date + " --file_name page_" + page_id + " "
	print "cmd is : " + cmd
	subprocess.call(cmd, shell=True)
	sys.exit(-1)

def main():
	if page_id == "all":
		print "scraping all"
		scrape_all()
	else:
		print "scraping your target page"
		scrape_one()

if __name__ == "__main__":
  main()
