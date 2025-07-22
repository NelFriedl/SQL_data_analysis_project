# Project no. 3: Election results scraper
## Description
This Python script is designed to scrape official results from the 2017 elections to the Chamber of Deputies of the Parliament of the Czech Republic. Data is publicly available on this website: https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ.
The script allows users to extract election data for a specific location/district and save it into a structured CSV file.

## Installation
1. The script is available for free download:

2. Set a virtual environment (venv) - highly recommended:
    - create venv:      python -m venv your_venv_name
    - activate venv:    .\your_venv_name\Scripts\Activate.ps1 (Windows PowerShell)
                        .\your_venv_name\Scripts\activate     (Windows Command Prompt)
                        source venv/bin/activate              (Linux, macOS)
    Once activated, the (your_venv_name) will show in terminal prompt.

3. Install required libraries
    Except built-in libraries, the script uses external libraries listed in requirements.txt. These libraires can be installed using following command: pip install -r requirements.txt
    
## Input and output

To run the script, two arguments must be provided by user: python main.py <LOCATION_NAME> <OUTPUT_FILENAME.csv>
1. location_name 
    The exact name of the district or municipality as it appears on the volby.cz website.
    Use Czech diacritics. If the location name contains spaces, enclose it in quotation marks 
    (e.g., "Nový Jičín").

2. output_filename.csv
    The desired name for the generated CSV file.
    Must include the .csv extension. Avoid using prohibited characters, such as  <, >, :, ", /, \, |, ?, *. The script will raise an ArgumentTypeError, if invalid chars are detected. In case of existing filename(s) in the same path, an appropriate number will be added to CSV filename (e.g., "novy_jicin_2.csv").

CSV file output structure:

    code            = unique city identifier
    city            = city name
    reg_voters      = total number of registered voters
    num_envelopes   = number of envelopes issued
    num_valid_votes = number of valid votes
    individual political parties (aphabetically ordered and separated in columns) and number of votes received
    
## Successful executions
simple location:     python main.py Praha praha.csv                -> Data successfully saved to praha.csv.
location with space: python main.py "Nový Jičín" "novy_jicin.csv"  -> Data successfully saved to novy_jicin.csv.

## Common errors
Missing quotation marks:
    python main.py Nový Jičín novy_jicin.csv      -> usage: main.py [-h] location output_file
                                                     main.py: error: unrecognized arguments: novy_jicin.csv
    Revise: Enclose multi-word location names in quotation marks (e.g., "Nový Jičín").

Incorrect location name:
    python main.py "Novy Jicin" "novy_jicin.csv"  -> Could not find the URL for location 'Novy Jicin'.

    Revise: Ensure the location name exactly matches the spelling and diacritics used on the volby.cz website.

Prohibited characters in output filename:
    python main.py "Nový Jičín" "novy_jicin?.csv" -> usage: main.py [-h] location output_file
                                                    main.py: error: argument output_file: Filename 'novy_jicin?.csv' contains prohibited characters.
                                                    Prohibited characters include: < > : " / \ | ? * and control characters.
    Revise: Remove prohibited characters from the filename. 
            Stick to letters, numbers, hyphens, underscores, and periods.

## Author
Nela Friedlová
nela.friedl@gmail.com