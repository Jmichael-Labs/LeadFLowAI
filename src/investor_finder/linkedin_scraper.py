#!/usr/bin/env python3
"""
🤖 LeadFlow AI - LinkedIn Investor Scraper
Professional LinkedIn scraping for real estate investors
"""

import time
import csv
import random
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

class LinkedInInvestorScraper:
    def __init__(self):
        """Initialize the LinkedIn scraper with professional settings"""
        self.ua = UserAgent()
        self.chrome_options = Options()
        
        # Professional Chrome options for scraping
        self.chrome_options.add_argument(f"--user-agent={self.ua.random}")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Target search terms for real estate investors
        self.search_terms = [
            "real estate investor",
            "property investor", 
            "fix and flip",
            "rental property investor",
            "cash buyer real estate",
            "real estate wholesaler",
            "property developer",
            "real estate entrepreneur",
            "multifamily investor",
            "commercial real estate investor"
        ]
        
        # Target cities for investor search
        self.target_cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
            "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte",
            "San Francisco", "Indianapolis", "Seattle", "Denver", "Boston",
            "Miami", "Atlanta", "Orlando", "Tampa", "Las Vegas"
        ]
        
    def setup_driver(self):
        """Initialize Chrome driver with anti-detection measures"""
        try:
            service = ChromeDriverManager().install()
            self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 15)
            return True
        except Exception as e:
            print(f"❌ Driver setup error: {e}")
            return False
        
    def search_investors(self, search_term, city, max_results=50):
        """Search for real estate investors in specific city"""
        investors = []
        
        try:
            # Construct LinkedIn people search URL
            search_query = f"{search_term} {city}"
            encoded_query = search_query.replace(' ', '%20')
            linkedin_url = f"https://www.linkedin.com/search/results/people/?keywords={encoded_query}&origin=CLUSTER_EXPANSION"
            
            print(f"🔍 Searching: {search_query}")
            self.driver.get(linkedin_url)
            
            # Random delay to appear human-like
            time.sleep(random.uniform(4, 7))
            
            # Scroll to load more results
            for scroll in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(3, 5))
                
            # Extract investor profiles
            profile_containers = self.driver.find_elements(By.CSS_SELECTOR, ".reusable-search__result-container")
            
            for container in profile_containers[:max_results]:
                try:
                    investor_data = self._extract_profile_data(container, search_term, city)
                    if investor_data:
                        investors.append(investor_data)
                        print(f"✅ Found: {investor_data['name']} - {investor_data['title']}")
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"❌ Search error for {search_term} in {city}: {e}")
            
        return investors
    
    def _extract_profile_data(self, container, search_term, city):
        """Extract investor data from profile container"""
        try:
            # Extract name
            name_element = container.find_element(By.CSS_SELECTOR, ".entity-result__title-text a span[aria-hidden='true']")
            name = name_element.text.strip()
            
            # Extract title/description  
            title_element = container.find_element(By.CSS_SELECTOR, ".entity-result__primary-subtitle")
            title = title_element.text.strip()
            
            # Extract location
            try:
                location_element = container.find_element(By.CSS_SELECTOR, ".entity-result__secondary-subtitle")
                location = location_element.text.strip()
            except:
                location = city
            
            # Extract profile URL
            try:
                profile_link = container.find_element(By.CSS_SELECTOR, ".entity-result__title-text a")
                profile_url = profile_link.get_attribute("href")
            except:
                profile_url = ""
            
            # Calculate investor quality score (AI-like scoring)
            quality_score = self._calculate_quality_score(title, location, search_term)
            
            if name and title and len(name) > 2:
                return {
                    'name': name,
                    'title': title,
                    'location': location,
                    'profile_url': profile_url,
                    'search_term': search_term,
                    'target_city': city,
                    'quality_score': quality_score,
                    'scraped_at': datetime.now().isoformat(),
                    'lead_type': 'LinkedIn Investor'
                }
                
        except Exception as e:
            pass
            
        return None
    
    def _calculate_quality_score(self, title, location, search_term):
        """AI-powered quality scoring for investor leads"""
        score = 50  # Base score
        
        # Title scoring
        high_value_keywords = ['investor', 'developer', 'capital', 'properties', 'real estate', 'cash buyer']
        for keyword in high_value_keywords:
            if keyword.lower() in title.lower():
                score += 10
                
        # Location relevance
        if any(city.lower() in location.lower() for city in ['new york', 'los angeles', 'chicago', 'miami']):
            score += 15
            
        # Search term relevance
        if search_term.lower().replace(' ', '') in title.lower().replace(' ', ''):
            score += 20
            
        return min(score, 100)  # Cap at 100
    
    def save_investors_to_csv(self, investors, filename=None):
        """Save investor data to CSV file"""
        if not investors:
            print("❌ No investors found to save")
            return None
            
        if not filename:
            timestamp = int(time.time())
            filename = f"leadflow_investors_{timestamp}.csv"
            
        output_dir = os.path.join(os.getcwd(), 'data')
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'name', 'title', 'location', 'profile_url', 'search_term', 
                'target_city', 'quality_score', 'lead_type', 'scraped_at'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(investors)
            
        print(f"💾 Saved {len(investors)} investors to {filepath}")
        return filepath
    
    def run_investor_hunt(self, target_cities=5, investors_per_city=30):
        """Main function to hunt for investors across multiple cities"""
        if not self.setup_driver():
            return []
            
        all_investors = []
        
        try:
            print("🚀 LeadFlow AI - LinkedIn Investor Hunt Started")
            print("=" * 60)
            
            # Manual login prompt
            print("🔐 MANUAL LOGIN REQUIRED:")
            print("1. Browser will open LinkedIn")
            print("2. Login manually")  
            print("3. Press Enter here when logged in")
            
            self.driver.get("https://www.linkedin.com/login")
            input("Press Enter after you've logged in to LinkedIn...")
            
            # Select random cities for hunting
            selected_cities = random.sample(self.target_cities, min(target_cities, len(self.target_cities)))
            
            for city in selected_cities:
                print(f"\n🎯 Hunting in: {city}")
                city_investors = []
                
                # Use top search terms for each city
                for search_term in self.search_terms[:3]:
                    investors = self.search_investors(search_term, city, investors_per_city // 3)
                    city_investors.extend(investors)
                    
                    # Respectful delay between searches
                    time.sleep(random.uniform(15, 25))
                    
                all_investors.extend(city_investors)
                print(f"✅ {city}: Found {len(city_investors)} investors")
                
            # Save results
            csv_file = self.save_investors_to_csv(all_investors)
            
            # Generate summary report
            self._generate_summary_report(all_investors)
            
        except Exception as e:
            print(f"❌ Hunt error: {e}")
        finally:
            self.driver.quit()
            
        return all_investors
    
    def _generate_summary_report(self, investors):
        """Generate AI-powered summary report"""
        if not investors:
            return
            
        high_quality = [inv for inv in investors if inv['quality_score'] >= 80]
        medium_quality = [inv for inv in investors if 60 <= inv['quality_score'] < 80]
        
        report = f"""
🤖 LeadFlow AI - Investor Hunt Summary Report
{'='*60}

📊 RESULTS OVERVIEW:
- Total Investors Found: {len(investors)}
- High Quality Leads (80+ score): {len(high_quality)}
- Medium Quality Leads (60-79 score): {len(medium_quality)}
- Average Quality Score: {sum(inv['quality_score'] for inv in investors) / len(investors):.1f}

💰 REVENUE POTENTIAL:
- High Quality Leads: ${len(high_quality) * 250:,} (@$250 each)
- Medium Quality Leads: ${len(medium_quality) * 150:,} (@$150 each)
- Total Market Value: ${len(high_quality) * 250 + len(medium_quality) * 150:,}

🎯 TOP 5 HIGHEST QUALITY LEADS:
"""
        
        sorted_investors = sorted(investors, key=lambda x: x['quality_score'], reverse=True)
        for i, inv in enumerate(sorted_investors[:5], 1):
            report += f"\n{i}. {inv['name']} (Score: {inv['quality_score']})"
            report += f"   {inv['title']} - {inv['location']}"
            
        report += f"\n\n📈 Generated by LeadFlow AI - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Save report
        report_file = os.path.join('data', 'investor_hunt_report.txt')
        with open(report_file, 'w') as f:
            f.write(report)
            
        print(report)
        print(f"📋 Report saved to: {report_file}")

if __name__ == "__main__":
    scraper = LinkedInInvestorScraper()
    investors = scraper.run_investor_hunt(target_cities=3, investors_per_city=25)
    print(f"\n🎯 Hunt Complete: {len(investors)} investors ready for outreach!")