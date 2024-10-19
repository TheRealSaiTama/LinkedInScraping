# LinkedIn Job Scraper 🔍

A robust Python script for scraping job listings from LinkedIn with built-in rate limiting, error handling, and logging capabilities.

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🌟 Features

- Search LinkedIn job listings based on job title and location
- Smart rate limiting with exponential backoff
- Rotating User-Agent headers for improved reliability
- Comprehensive error handling and logging
- JSON output format for easy integration
- Session management for optimal performance

## 📋 Prerequisites

Before running this script, make sure you have Python 3.6 or higher installed and the following packages:

```bash
pip install requests beautifulsoup4
```

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/TheRealSaiTama/LinkedInScraping.git
cd LinkedInScraping
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the script:
```bash
python fetchjobtest.py
```

4. Follow the prompts to enter:
   - Job title to search for
   - Location to search in

## 💻 Usage Example

```python
from linkedinscraper import get_job_listings
import requests

with requests.Session() as session:
    jobs = get_job_listings("Software Engineer", "San Francisco", session)
    print(jobs)
```

## 📝 Output Format

The script returns JSON-formatted data containing job listings with the following information:

```json
[
    {
        "title": "Software Engineer",
        "location": "San Francisco, CA",
        "apply_link": "https://www.linkedin.com/jobs/view/..."
    },
    ...
]
```

## 🔧 Configuration

The script includes several configurable parameters:

- `USER_AGENTS`: List of user agent strings for rotation
- `retries`: Number of retry attempts (default: 5)
- `logging`: Configured to write to 'scraping_log.txt'

## 📊 Logging

The script maintains detailed logs in `scraping_log.txt` with the following information:
- Timestamp of each operation
- Warning messages for rate limiting
- Error messages for failed requests
- Information about parsing issues

## ⚠️ Rate Limiting

The script implements smart rate limiting with exponential backoff:
- Respects LinkedIn's rate limits
- Implements automatic retries with increasing delays
- Random jitter added to prevent thundering herd problem

## 🛡️ Best Practices

1. Use responsibly and respect LinkedIn's terms of service
2. Implement reasonable delays between requests
3. Handle rate limiting appropriately
4. Monitor your logs for any issues

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

Your Name - [@stillhatetrigo](https://www.instagram.com/stillhatetrigo/)
Project Link: [https://github.com/TheRealSaiTama/LinkedInScraping.git](https://github.com/TheRealSaiTama/LinkedInScraping.git)

## 🙏 Acknowledgments

- Beautiful Soup documentation
- LinkedIn's public job search interface
- Python Requests library
