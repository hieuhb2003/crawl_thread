import json
import argparse
from typing import Dict, List
from random import randint
from datetime import datetime
import jmespath
from parsel import Selector
from nested_lookup import nested_lookup
from playwright.sync_api import sync_playwright
import pickle
from find_view import get_text_from_span_containing
from scroll_simulator import scoll_and_get_list

def load_existing_data(file_path):
    """Load existing data from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return [] 
    except json.JSONDecodeError:
        return []  
    
existing_data = load_existing_data('data.json')
print(f"Loaded {len(existing_data)} existing threads.")

def parse_timestamp(timestamp) -> str:
    readable_date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S').split(" ")
    day = readable_date[0]
    time = readable_date[1]
    return day,time


def parse_thread(data: Dict) -> Dict:
    """Parse Twitter tweet JSON dataset for the most important fields"""
    result = jmespath.search(
        """{
        text: post.caption.text,
        published_on: post.taken_at,
        username: post.user.username,
        reply_count: post.text_post_app_info.direct_reply_count,
        like_count: post.like_count,
        repost_count: post.text_post_app_info.repost_count
        share_count: post.text_post_app_info.reshare_count
    }""",
        data,
    )
    if result["reply_count"] and type(result["reply_count"]) != int:
        result["reply_count"] = int(result["reply_count"].split(" ")[0])
    if result["like_count"] and type(result["like_count"]) != int:
        result["like_count"] = int(result["like_count"].split(" ")[0])
    if result["repost_count"] and type(result["repost_count"]) != int:
        result["repost_count"] = int(result["repost_count"].split(" ")[0])
    # readable_date = datetime.utcfromtimestamp(result['published_on']).strftime('%Y-%m-%d %H:%M:%S')
    day,hour = parse_timestamp(result['published_on'])
    result['day'] = day
    result['hour'] = hour
    del result['published_on']
    result['view'] = None
    return result

def scrape_threads(urls: List[str]) -> List[dict]:
    """Scrape multiple Threads posts from given URLs"""
    results = []
    
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})

        cookies = pickle.load(open("my_cookie.pkl", "rb"))
        context.add_cookies(cookies)

        page = context.new_page()

        for url in urls:
            try:
                page.goto(url)
                page.wait_for_timeout(randint(5000, 10000))

                selector = Selector(text=page.content())
                full_html = selector.get()
                view = get_text_from_span_containing(full_html)

                hidden_datasets = selector.css('script[type="application/json"][data-sjs]::text').getall()

                thread_data = None
                for hidden_dataset in hidden_datasets:
                    if '"ScheduledServerJS"' not in hidden_dataset or "thread_items" not in hidden_dataset:
                        continue
                    
                    data = json.loads(hidden_dataset)
                    thread_items = nested_lookup("thread_items", data)
                    
                    if not thread_items:
                        continue
                    
                    threads = [parse_thread(t) for thread in thread_items for t in thread]
                    threads[0]['view'] = view
                    
                    thread_data = {
                        "thread": threads[0],
                        "replies": threads[1:],
                    }
                    break  # Tìm thấy dữ liệu, thoát khỏi vòng lặp hidden_datasets
                
                if thread_data:
                    results.append(thread_data)
                    existing_data.append(thread_data)
                else:
                    print(f"No thread data found for URL: {url}")

            except Exception as e:
                print(f"Error scraping {url}: {str(e)}")

        browser.close()

    return results


parser = argparse.ArgumentParser()
parser.add_argument('-n','--number', type=str, help='Số vòng reaload trang', required=True)

args = parser.parse_args()
urls = scoll_and_get_list(int(args.number))

scraped_data = scrape_threads(urls)

# existing_data.extend(scraped_data)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=4)
print(f"After scraping, there are {len(existing_data)} threads in total.")
print(f"Scraped {len(scraped_data)} threads successfully.")

# script :
# python scrape.py -a 2