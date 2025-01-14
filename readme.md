# X Mute Words Bot

Automatically mute multiple words on X (Twitter) using Selenium automation.

## Features

- Bulk mute words from a list
- Automatic login to X account
- Customizable word list in markdown format
- Colorful console output
- Detailed error handling
- Progress tracking
- Summary report

## Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- ChromeDriver matching your Chrome version

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/x-mute-words.git
cd x-mute-words
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Download ChromeDriver:
   - Check your Chrome version at `chrome://version`
   - Download matching ChromeDriver from [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
   - Place `chromedriver.exe` in the project folder

4. Set up environment variables:
   - Edit `.env`file.
   - Update with your X credentials

## Usage

1. Edit `wordlist.md` to add words you want to mute:
```markdown
# Mute Words List

- word1
- word2
- word3
```

2. Run the bot:
```bash
python mute_bot.py
```

3. The bot will:
   - Log in to your X account
   - Navigate to mute settings
   - Add each word from your list
   - Show progress in the console
   - Provide a summary when finished

## Configuration

- Edit `wordlist.md` to modify the list of words to mute
- Each word should be on a new line and start with a dash (-)
- Update `.env` file with your X credentials

## Troubleshooting

1. **ChromeDriver Error**:
   - Make sure Chrome is installed
   - Download the correct ChromeDriver version
   - Place chromedriver.exe in the project folder

2. **Login Issues**:
   - Check your credentials in `.env`
   - Complete any verification if prompted
   - Make sure your account is not locked

3. **Rate Limiting**:
   - The bot includes delays to prevent rate limiting
   - If you encounter issues, try increasing delays in the code

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This bot is for educational purposes only. Use at your own risk. Make sure to comply with X's Terms of Service.
