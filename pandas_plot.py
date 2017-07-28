#!/usr/bin/python
import pandas
from datetime import datetime
import matplotlib.dates as mdates
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
#coding:utf-8
#plt.rcParams['font.sans-serif']=['SimHei']
#plt.rcParams['axes.unicode_minus']=False

colnames = [
'status_id',
'status_message',
'link_name',
'status_type',
'status_link',
'status_published',
'num_reactions',
'num_comments',
'num_shares',
'num_likes',
'num_loves',
'num_wows',
'num_hahas',
'num_sads',
'num_angrys',
'num_special']


def str2dt(status_published_str):
	status_published = []
	for string_date in status_published_str:
		a_datetime = datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S")
		status_published += [a_datetime]
	return status_published

def readCsvFile(file_path):
	csv_data = pandas.read_csv(file_path, names=colnames)
	status_published_str = csv_data.status_published.tolist()
	num_comments = csv_data.num_comments.tolist()
	num_shares = csv_data.num_shares.tolist()
	num_likes = csv_data.num_likes.tolist()
	status_published_str.pop(0)
	num_comments.pop(0)
	num_shares.pop(0)
	num_likes.pop(0)
	status_published = str2dt(status_published_str)
	print status_published
	print num_shares
	print num_likes
	status_published = mdates.date2num(status_published)
	return status_published,num_comments  ,num_shares,num_likes

def plotCurve(fig, status_published,num_comments, num_shares, num_likes):
	fmt = mdates.DateFormatter('%Y-%m-%d')
	ax = fig.add_subplot(311)
	ax.xaxis.set_major_formatter(fmt)
	ax.set_title('number of comments')
	ax.plot(status_published , num_comments)
	ax = fig.add_subplot(312)
	ax.xaxis.set_major_formatter(fmt)
	ax.set_title('number of shares')
	ax.plot(status_published , num_shares)
	ax = fig.add_subplot(313)
	ax.xaxis.set_major_formatter(fmt)
	ax.set_title('number of likes')
	ax.plot(status_published , num_likes)
	plt.gcf().autofmt_xdate()# beautify the x-labels
	plt.tight_layout(pad=1, h_pad=0.5, w_pad=1)
	fig.subplots_adjust(hspace=.5) #spcaing between subplots
	plt.show()

csv_dir = "csv"
all_file_names = [f for f in listdir(csv_dir) if isfile(join(csv_dir, f))]

for full_file_name in all_file_names:
	file_name = full_file_name.split('_facebook_statuses.')[0]
	print file_name
	file_path = csv_dir + '/' + full_file_name
	(status_published, num_comments, num_shares, num_likes) = readCsvFile(file_path)
	if len(status_published) > 0 and  len(num_comments) > 0 and  len(num_shares) > 0 and  len(num_likes) > 0:
		#date_start = status_published[0]
		#date_end   = status_published[len(status_published)-1]
		#print str(date_start) +"  " + str(date_end)
		#date_start = datetime.fromtimestamp(date_start )
		#date_end   = datetime.fromtimestamp(date_end )
		fig = plt.figure(figsize=(8, 8)) # size of the figure
		fig_title = file_name
		fig.canvas.set_window_title(fig_title)
		plotCurve(fig, status_published,num_comments, num_shares, num_likes)
