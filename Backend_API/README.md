# This is a project I made at a university course. It was built over a period of 10 weeks. The reason I cannot show the original commits is because they were made to a private organisation repository. 

## Team CloudChaos

Team Members: Anish Saraogi, Braveen Murugathas, Patrick Hoang, Sammriddh Gupta

### Idea:

Streamline the Stock Comparison Process

### Data Source

The Yahoo Finance API, via the yfinance python module

### Services

#### 1. Collection API

Collect data from yfinance, converts it to the ADAGE format and stores it in the S3 bucket

#### 2. Retrieval API

Public API where users can request for stock data, and specify the level of preprocessing they want

#### 3. Preprocessing-1 API

Adds percentage daily return column

#### 4. Preprocessing-2 API

Adds average daily price, price range, and moving averages for 7, 14 and 30 days

#### 5. Preprocessing-Final API

Adds all columns added by preprocessing 1 and 2

### Linting Setup and Rules:

We use Flake8 for linting
We use Black as a formatter.

To install black, use the command `pip install black` (preferably use a virtual environment)
To format, can use `black <filename>` or just `black .` to format all files 
