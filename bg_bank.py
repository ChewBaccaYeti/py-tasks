import requests
from bs4 import BeautifulSoup
import csv

# Function to fetch the webpage content
def fetch_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None

# Function to extract data rows from the table
def extract_data_rows(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='table')
    if table:
        tbody = table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')[:-1]  # Exclude the last row
            data_rows = []
            for row in rows:
                cols = row.find_all('td')
                # Get the 8th td tag and extract the span value
                span_value = cols[7].find('span').text.strip() if len(cols) > 7 else ''
                data_row = [col.text.strip() for col in cols[:-1]]  # Exclude the last td tag
                data_row.append(span_value)
                data_rows.append(data_row)
            return data_rows
    return None

# Function to sort data rows by 'обем продадени'
def sort_data_rows(data_rows):
    sorted_rows = sorted(data_rows, key=lambda x: float(x[3].replace(',', '')) if x[3] else 0, reverse=True)
    return sorted_rows

# Function to save sorted data to CSV file
def save_to_csv(data_rows, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Банка', 'Купува', 'Продава', 'Обем продадени'])
        for row in data_rows:
            writer.writerow(row)

# Function to compare current data with the one saved in the CSV file
def compare_with_csv(data_rows, filename):
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            saved_rows = [row for row in reader]
        return saved_rows != data_rows
    except FileNotFoundError:
        return True

# Main function
def main():
    url = 'https://bnb.bg/Statistics/StInterbankForexMarket/index.htm'
    csv_filename = 'interbank_forex_market.csv'

    # Fetch webpage content
    webpage_content = fetch_webpage(url)
    if not webpage_content:
        print("Failed to fetch webpage content.")
        return

    # Extract data rows from the table
    data_rows = extract_data_rows(webpage_content)
    if not data_rows:
        print("Failed to extract data rows from the table.")
        return

    # Sort data rows by 'обем продадени'
    sorted_data_rows = sort_data_rows(data_rows)

    # Compare with the CSV file
    if compare_with_csv(sorted_data_rows, csv_filename):
        # Save sorted data to CSV file
        save_to_csv(sorted_data_rows, csv_filename)
        print("Data saved to CSV file.")
    else:
        print("No changes detected. CSV file not updated.")

if __name__ == "__main__":
    main()
