import os
import time
from datetime import datetime
from typing import List
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, Fore, Style

# Initialize colorama for colored console output
init()

class XMuteBot:
    def __init__(self):
        """Initialize the X (Twitter) mute bot with configuration and setup"""
        # Load environment variables
        load_dotenv()
        
        try:
            # Configure Chrome options
            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            
            # Initialize Chrome driver
            service = Service("chromedriver.exe")
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Set default wait time for elements (reduced from 20 to 10)
            self.wait = WebDriverWait(self.driver, 10)
            
            # Execute CDP commands to prevent detection
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                """
            })
            
        except Exception as e:
            print(f"{Fore.RED}Failed to initialize Chrome driver: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please make sure Chrome browser is installed and chromedriver.exe is in the same folder.{Style.RESET_ALL}")
            raise
        
        # Load credentials from environment variables
        self.username = os.getenv('X_USERNAME')
        self.password = os.getenv('X_PASSWORD')
        
        if not self.username or not self.password:
            raise ValueError("Username or password not found in .env file")
        
        # Initialize counters
        self.successful_mutes = 0
        self.failed_mutes = 0

    def load_words_from_file(self) -> List[str]:
        """
        Load words to be muted from wordlist.md file
        Returns:
            List[str]: List of words to be muted
        """
        try:
            with open('wordlist.md', 'r', encoding='utf-8') as file:
                # Filter lines starting with '-' and remove the dash
                return [line.replace('-', '').strip() 
                       for line in file.readlines() 
                       if line.strip().startswith('-')]
        except Exception as e:
            print(f"{Fore.RED}Error loading wordlist: {e}{Style.RESET_ALL}")
            return []

    def login(self) -> bool:
        """
        Log in to X (Twitter) using credentials from .env file
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            # Navigate to X login page
            self.driver.get('https://twitter.com/login')
            time.sleep(5)  # Increased wait time for initial load

            # Enter username
            username_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
            )
            username_input.send_keys(self.username)
            username_input.send_keys(Keys.RETURN)
            time.sleep(3)

            # Handle possible verification step
            try:
                verify_input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="ocfEnterTextTextInput"]')),
                    timeout=5
                )
                if verify_input:
                    print(f"{Fore.YELLOW}Please complete verification in the browser...{Style.RESET_ALL}")
                    input("Press Enter after completing verification...")
            except:
                pass  # No verification needed

            # Enter password
            password_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
            )
            password_input.send_keys(self.password)
            password_input.send_keys(Keys.RETURN)
            time.sleep(5)  # Increased wait time after login

            print(f"{Fore.GREEN}Successfully logged in to X{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}Login failed: {e}{Style.RESET_ALL}")
            return False

    def mute_word(self, word: str) -> bool:
        """
        Mute a specific word on X
        Args:
            word (str): Word to be muted
        Returns:
            bool: True if muting successful, False otherwise
        """
        try:
            # Navigate to mute words settings
            self.driver.get('https://twitter.com/settings/muted_keywords')
            time.sleep(2)  # Reduced from 5 to 2

            # Click the add button using multiple possible selectors
            try:
                # Try finding the button by aria-label
                add_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="Sessize alınan kelime veya cümle ekle"]'))
                )
                add_button.click()
                time.sleep(1)  # Reduced from 2 to 1
            except:
                try:
                    # Try finding the button by href
                    add_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/settings/add_muted_keyword"]'))
                    )
                    add_button.click()
                    time.sleep(1)
                except:
                    try:
                        # Try finding by SVG path
                        add_button = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//svg//*[contains(@d, 'M11 11V4h2v7h7v2h-7v7h-2v-7H4v-2h7z')]"))
                        )
                        add_button.click()
                        time.sleep(1)
                    except Exception as e:
                        print(f"{Fore.RED}Could not find add button: {e}{Style.RESET_ALL}")
                        return False

            # Enter the word
            try:
                word_input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="keyword"]'))
                )
                word_input.clear()
                word_input.send_keys(word)
                time.sleep(0.5)  # Reduced from 1 to 0.5
            except Exception as e:
                print(f"{Fore.RED}Could not enter word: {e}{Style.RESET_ALL}")
                return False

            # Set duration to "Forever"
            try:
                duration_dropdown = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Time options dropdown menu"]'))
                )
                duration_dropdown.click()
                time.sleep(0.5)
                forever_option = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Forever']"))
                )
                forever_option.click()
                time.sleep(0.5)
            except Exception as e:
                print(f"{Fore.YELLOW}Could not set duration to Forever, using default: {e}{Style.RESET_ALL}")

            # Save the muted word - try multiple selectors
            try:
                # Try finding by text content
                save_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Kaydet']"))
                )
                save_button.click()
            except:
                try:
                    # Try finding by class and text
                    save_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '.css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3'))
                    )
                    save_button.click()
                except:
                    try:
                        # Try finding by data-testid
                        save_button = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="settingsDetailSave"]'))
                        )
                        save_button.click()
                    except Exception as e:
                        print(f"{Fore.RED}Could not find save button: {e}{Style.RESET_ALL}")
                        return False

            time.sleep(1)  # Reduced from 3 to 1
            self.successful_mutes += 1
            print(f"{Fore.GREEN}Successfully muted: {word}{Style.RESET_ALL}")
            return True

        except Exception as e:
            self.failed_mutes += 1
            print(f"{Fore.RED}Failed to mute {word}: {e}{Style.RESET_ALL}")
            return False

    def run(self):
        """Main method to run the mute bot"""
        print(f"{Fore.CYAN}Starting X Mute Bot...{Style.RESET_ALL}")
        
        # Load words to mute
        words = self.load_words_from_file()
        if not words:
            print(f"{Fore.RED}No words found to mute. Check wordlist.md file.{Style.RESET_ALL}")
            return

        print(f"{Fore.CYAN}Loaded {len(words)} words to mute{Style.RESET_ALL}")

        # Login to X
        if not self.login():
            return

        # Process each word
        start_time = datetime.now()
        for i, word in enumerate(words, 1):
            print(f"\n{Fore.YELLOW}Processing word {i}/{len(words)}: {word}{Style.RESET_ALL}")
            self.mute_word(word)
            time.sleep(1)  # Reduced from 3 to 1

        # Print summary
        end_time = datetime.now()
        duration = end_time - start_time
        print(f"\n{Fore.CYAN}=== Mute Bot Summary ==={Style.RESET_ALL}")
        print(f"Total words processed: {len(words)}")
        print(f"Successfully muted: {self.successful_mutes}")
        print(f"Failed to mute: {self.failed_mutes}")
        print(f"Total duration: {duration}")

    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

if __name__ == "__main__":
    try:
        bot = XMuteBot()
        bot.run()
    except Exception as e:
        print(f"{Fore.RED}Bot failed to start: {e}{Style.RESET_ALL}")
    finally:
        if 'bot' in locals():
            bot.cleanup() 