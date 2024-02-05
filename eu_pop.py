import requests
from bs4 import BeautifulSoup

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
    table = soup.find('table')
    if table:
        tbody = table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
            data_rows = {}
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 5:
                    country = cols[1].text.strip()
                    population = cols[4].text.strip()
                    population = ''.join(filter(str.isdigit, population))  # Remove non-numeric characters
                    if population:  # Ensure population is not empty
                        population = int(population)
                        data_rows[country] = {'country_population': population}
            return data_rows
    return None

# Main function
def main():
    url = 'https://en.wikipedia.org/wiki/List_of_European_Union_member_states_by_population'

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

    # Calculate total population
    total_population = sum(data['country_population'] for data in data_rows.values())

    # Calculate population percentage for each country and update the dictionary
    for country, data in data_rows.items():
        population = data['country_population']
        percentage = (population / total_population) * 100
        data_rows[country]['country_population_percentage'] = round(percentage, 1)

    # Print the countries dictionary
    for country, data in data_rows.items():
        print(f"{country}: {data}")

if __name__ == "__main__":
    main()
