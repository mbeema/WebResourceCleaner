from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import argparse
import logging
import urllib.parse
import re
from webdriver_manager.chrome import ChromeDriverManager

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global sets for tracking JS usage
declared_js_functions = set()
used_js_functions = set()
visited = set()

# Global dictionary to track the source of each JS function
js_function_sources = {}

# URLs to exclude
exclude_urls = set()

def analyze_page(driver, url):
    global declared_js_functions, used_js_functions, js_function_sources
    logging.info(f"Analyzing {url}")

    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Analyze inline and external JS
    for script in soup.find_all('script'):
        if script.string:
            functions = re.findall(r'function (\w+)\(', script.string)
            declared_js_functions.update(functions)

            # Store the source URL for each function
            for js_function in functions:
                js_function_sources[js_function] = url

            called_functions = re.findall(r'(\w+)\(', script.string)
            used_js_functions.update(called_functions)

def crawl(driver, url, base_url):
    global visited
    if url in visited or not url.startswith(base_url) or url in exclude_urls:
        return

    visited.add(url)
    logging.info(f"Crawling: {url}")

    analyze_page(driver, url)

    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find and visit all internal links on the page
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            full_url = urllib.parse.urljoin(base_url, href)
            if full_url.startswith(base_url):
                crawl(driver, full_url, base_url)

def generate_report():
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('report_template.html')

    truly_unused_css_classes = declared_css_classes - used_css_classes
    truly_unused_js_functions = declared_js_functions - used_js_functions

    report_html = template.render(
        unused_css_classes=truly_unused_css_classes,
        css_class_sources=css_class_sources,
        unused_js_functions=truly_unused_js_functions,
        js_function_sources=js_function_sources
    )

    with open('report.html', 'w') as f:
        f.write(report_html)

    logging.info("HTML Report generated.")
    

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crawl a website to find unused JS.')
    parser.add_argument('--url', required=True, help='The URL of the website to crawl.')
    parser.add_argument('--exclude', nargs='*', default=[], help='List of URLs to exclude from crawling.')
    args = parser.parse_args()

    # Initialize ChromeDriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path='/home/oracle/drivers/chromedriver', options=chrome_options)  # Replace with your actual path
    #driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    # URLs to exclude
    exclude_urls = set(args.exclude)

    crawl(driver, args.url, args.url)
    driver.quit()

    generate_report()
