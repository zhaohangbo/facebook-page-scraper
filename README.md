# Usage

## Case 1：Scrape All Default Pages

Run 
```
python scrape_fb_pages.py --page_id all --access_token "your_access_token"
```

## Case 2：Scrape One Specific Page

Run 
```
python scrape_fb_pages.py --page_id 123123 --access_token "your_access_token"
```

## How To Get "access_token"

```
1. Goto https://developers.facebook.com/tools-and-support/
2. Click "Graph API Explorer"
3. A tempory_token Is Created For You, Copy It
```

## How To Get "page_id"

```
1. Goto the Facebook Page You Want to Scrape
2. Right Click and Select "View Page Source"
3. In the HTML Souce Code, Find page_id="123123xxx"
```

## Parameters
| Parameter | Description |
| --- | --- |
| `--page_id ` | __"all"__ means scraping all default pages, __OR__ a specific facebook page_id like __"12321xxxxx"__|
| `--access_token ` | temporary access_token for facebook developer|
| `--since_date` | date start scraping, __"date 7 days ago by default"__, format YYYY-MM-DD|
| `--until_date` | date end scraping, __"date today by default"__, format YYYY-MM-DD|

## Help Guide
Run 
```
python scrape_fb_pages.py -h
```

## Default Pages
```
1. open file "scrape_fb_pages.py"
2. all deafult page_id are stored in the list variable called "page_ids"
3. all mappings of page_id and page_name are stored in the dict variable called "page_id_name"
```

## Plot
Run
```
python pandas_plot.py
```

## Contribution
You are more then welcome!
Please open a PR or issues here.
