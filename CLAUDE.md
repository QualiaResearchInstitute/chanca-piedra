# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a research project analyzing the effectiveness and side effects of Chanca Piedra (and other supplements) for kidney stones using web-scraped review data from multiple platforms (WebMD, Amazon, Reddit). The project combines web scraping, AI-powered text classification, and statistical analysis.

## Key Commands

### Testing
- `npx playwright test` - Run all Playwright tests
- `npx playwright test --ui` - Run tests in UI mode for debugging
- `npx playwright test tests/amazon-reviews.spec.ts` - Run specific test file
- `npx playwright show-report` - View test results

### Python Scripts
- `python claude-classification.py` - Classify reviews using Claude AI (requires ANTHROPIC_API_KEY)
- `python webmd-scraper-chanca-piedra.py` - Scrape Chanca Piedra reviews from WebMD
- `python webmd-scraper-all-supplements.py` - Scrape reviews for multiple supplements
- `python webmd-supplement-index-scraper.py` - Get supplement URLs from WebMD
- `python webmd-ratings-scraper.py` - Get ratings data for supplements
- `python webmd-analysis.py` - Perform statistical analysis on WebMD data
- `python find_amazon_duplicates.py` - Find duplicate Amazon reviews

### Jupyter Notebooks
- Analysis notebooks are in root directory (*.ipynb files)
- Main analysis: `chanca-piedra-analysis.ipynb`
- Statistical analysis: `chanca-piedra-stats-paper.ipynb`

## Project Architecture

### Data Pipeline
1. **Web Scraping**: Playwright tests (`tests/`) scrape reviews from Amazon, Reddit, WebMD
2. **Data Storage**: Raw data stored in `csv-files/` directory
3. **Classification**: `claude-classification.py` uses Claude API to classify reviews for effectiveness/side effects
4. **Analysis**: Jupyter notebooks perform statistical analysis and generate visualizations
5. **Output**: HTML reports and visualizations stored in `docs/` directory

### Key Components

#### Web Scrapers
- **Amazon**: `tests/amazon-reviews.spec.ts` - Scrapes product reviews with star ratings
- **Reddit**: `tests/reddit-scraper.spec.ts` - Scrapes r/KidneyStones subreddit posts/comments
- **WebMD**: Python scrapers (`webmd-*.py`) - Extract review data from supplement pages

#### Classification System
- **Prompts**: `classification_prompt_effectiveness.md` and `classification_prompt_high_quality.md` contain classification criteria
- **Classifier**: `claude-classification.py` processes reviews in batches using Claude API
- **Output**: Classified results saved as `classified_results_{platform}.csv`

#### Data Structure
- **Raw Data**: Platform-specific CSV files in `csv-files/`
- **Processed Data**: Effect estimates, raw counts, and summary tables
- **Visualizations**: Forest plots, bar charts, and tables in `docs/`

### Authentication
- Playwright tests use stored authentication (`tests/amazonAuth.json`, `tests/redditAuth.json`)
- Claude classification requires `ANTHROPIC_API_KEY` environment variable
- Auth setup: `tests/save-auth.spec.ts`

### Configuration
- **Playwright**: `playwright.config.ts` - 60s timeout, HTML reporter, Chrome only
- **Products**: Product configurations defined in test files with URLs, names, and review counts
- **Search Terms**: Reddit scraper uses configurable keyword searches

### Data Processing Notes
- Reviews are classified for both effectiveness (helped with kidney stones) and quality (detailed, credible reviews)
- Statistical analysis includes odds ratios, confidence intervals, and forest plots
- Duplicate detection and removal for Amazon reviews
- Platform-specific data processing due to different HTML structures