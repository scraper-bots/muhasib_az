#!/usr/bin/env python3
"""
Muhasib.az Accountant Information Scraper

This script scrapes accountant information from muhasib.az including:
- Personal details (name, age, gender, marital status)
- Contact information (phone, email, city)
- Professional information (education, experience, skills)
- Job preferences (category, position, minimum salary)
"""

import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import logging
from urllib.parse import urljoin
from typing import List, Dict, Optional
import random

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MuhasibScraper:
    def __init__(self):
        self.base_url = "https://www.muhasib.az"
        self.listings_url = f"{self.base_url}/cv_index.php"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse HTML content from URL"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
            
    def extract_accountant_ids(self, soup: BeautifulSoup) -> List[str]:
        """Extract accountant IDs from the listings page"""
        ids = []
        # Look for cv.php?id= links
        cv_links = soup.find_all('a', href=re.compile(r'cv\.php\?id=\d+'))
        
        for link in cv_links:
            href = link.get('href')
            id_match = re.search(r'id=(\d+)', href)
            if id_match:
                ids.append(id_match.group(1))
                
        return list(set(ids))  # Remove duplicates
        
    def scrape_listings_page(self) -> List[str]:
        """Scrape all accountant IDs from the listings page"""
        logger.info("Scraping listings page...")
        soup = self.get_page_content(self.listings_url)
        
        if not soup:
            logger.error("Failed to fetch listings page")
            return []
            
        accountant_ids = self.extract_accountant_ids(soup)
        logger.info(f"Found {len(accountant_ids)} unique accountant IDs")
        
        return accountant_ids
        
    def extract_text_by_label(self, soup: BeautifulSoup, label: str) -> str:
        """Extract text following a specific label"""
        # Look for bold text containing the label
        bold_elements = soup.find_all('b')
        for bold in bold_elements:
            if label in bold.get_text():
                # Get the parent element and extract text after the bold element
                parent = bold.parent
                if parent:
                    text = parent.get_text()
                    # Split by the label and take the part after it
                    if label in text:
                        after_label = text.split(label, 1)[1]
                        # Clean up the text - remove extra whitespace and newlines
                        return re.sub(r'\s+', ' ', after_label.strip())
        return ""
        
    def extract_section_content(self, soup: BeautifulSoup, section_header: str) -> str:
        """Extract content from a specific section"""
        # Find h2 headers
        headers = soup.find_all('h2')
        for header in headers:
            if section_header.lower() in header.get_text().lower():
                # Get the parent cell and extract all text
                cell = header.find_parent('td')
                if cell:
                    text = cell.get_text()
                    # Remove the header text from the beginning
                    text = re.sub(rf'^.*?{re.escape(section_header)}.*?\n', '', text, flags=re.IGNORECASE)
                    return re.sub(r'\s+', ' ', text.strip())
        return ""
        
    def scrape_accountant_details(self, accountant_id: str) -> Dict:
        """Scrape detailed information for a specific accountant"""
        url = f"{self.base_url}/cv.php?id={accountant_id}"
        logger.info(f"Scraping details for accountant ID: {accountant_id}")
        
        soup = self.get_page_content(url)
        if not soup:
            logger.error(f"Failed to fetch details for ID: {accountant_id}")
            return {}
            
        data = {'id': accountant_id, 'url': url}
        
        try:
            # Extract basic contact info from the top right section
            contact_cell = soup.find('td', {'align': 'right'})
            if contact_cell:
                contact_text = contact_cell.get_text()
                
                # Extract city
                city_match = re.search(r'Şəhər:\s*(.+)', contact_text)
                data['city'] = city_match.group(1).strip() if city_match else ""
                
                # Extract phone
                phone_match = re.search(r'Tel\.:\s*(.+)', contact_text)
                data['phone'] = phone_match.group(1).strip() if phone_match else ""
                
                # Extract email
                email_match = re.search(r'E-mail:\s*(.+)', contact_text)
                data['email'] = email_match.group(1).strip() if email_match else ""
            
            # Extract full name from h2 header
            name_header = soup.find('h2')
            if name_header:
                data['name'] = name_header.get_text().replace('—', '').strip()
            
            # Extract personal information
            data['age'] = self.extract_text_by_label(soup, 'Yaşı:').split()[0] if self.extract_text_by_label(soup, 'Yaşı:') else ""
            data['gender'] = self.extract_text_by_label(soup, 'Cinsi:').split()[0] if self.extract_text_by_label(soup, 'Cinsi:') else ""
            data['marital_status'] = self.extract_text_by_label(soup, 'Ailə vəziyyəti:').split()[0] if self.extract_text_by_label(soup, 'Ailə vəziyyəti:') else ""
            
            # Extract job-related information
            data['category'] = self.extract_text_by_label(soup, 'Kateqoriya:')
            data['position'] = self.extract_text_by_label(soup, 'Vəzifə:')
            data['min_salary'] = self.extract_text_by_label(soup, 'Minimum əmək haqqı')
            
            # Extract education information
            data['education'] = self.extract_section_content(soup, 'Təhsil')
            
            # Extract work experience
            data['experience'] = self.extract_section_content(soup, 'İş Təcrübəsi')
            
            # Extract skills
            data['skills'] = self.extract_section_content(soup, 'Bilik və bacarıqlar')
            
            logger.info(f"Successfully scraped data for {data.get('name', 'Unknown')} (ID: {accountant_id})")
            
        except Exception as e:
            logger.error(f"Error parsing details for ID {accountant_id}: {e}")
            
        return data
        
    def save_to_csv(self, data: List[Dict], filename: str = 'muhasib_accountants.csv'):
        """Save scraped data to CSV file"""
        if not data:
            logger.warning("No data to save")
            return
            
        fieldnames = ['id', 'url', 'name', 'city', 'phone', 'email', 'age', 'gender', 
                     'marital_status', 'category', 'position', 'min_salary', 
                     'education', 'experience', 'skills']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in data:
                # Ensure all fieldnames exist in the row
                filtered_row = {field: row.get(field, '') for field in fieldnames}
                writer.writerow(filtered_row)
                
        logger.info(f"Data saved to {filename}")
        
    def run_scraper(self, max_accounts: Optional[int] = None):
        """Main scraper function"""
        logger.info("Starting Muhasib.az scraper...")
        
        # Get all accountant IDs
        accountant_ids = self.scrape_listings_page()
        
        if not accountant_ids:
            logger.error("No accountant IDs found. Exiting.")
            return
            
        # Limit the number of accounts to scrape if specified
        if max_accounts:
            accountant_ids = accountant_ids[:max_accounts]
            logger.info(f"Limiting scrape to {max_accounts} accounts")
            
        # Scrape each accountant's details
        all_data = []
        for i, acc_id in enumerate(accountant_ids, 1):
            logger.info(f"Processing {i}/{len(accountant_ids)}: ID {acc_id}")
            
            data = self.scrape_accountant_details(acc_id)
            if data:
                all_data.append(data)
                
            # Add delay to be respectful to the server
            time.sleep(random.uniform(1, 3))
            
        # Save data to CSV
        self.save_to_csv(all_data)
        logger.info(f"Scraping completed. Total records: {len(all_data)}")

if __name__ == "__main__":
    scraper = MuhasibScraper()
    scraper.run_scraper(max_accounts=500)