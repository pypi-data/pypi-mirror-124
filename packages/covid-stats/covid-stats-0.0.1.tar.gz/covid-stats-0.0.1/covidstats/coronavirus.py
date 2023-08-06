from bs4 import BeautifulSoup
import requests

page = requests.get('https://www.worldometers.info/coronavirus/')

soup = BeautifulSoup(page.content, "html.parser")

class Coronavirus:
    def get_stats(self, country=None):
        """
        Get the Coronavirus statistics for the world/all countries/a specific country.
        Leave the parameters empty to get the global statistics, enter the country name to get the stats for that country, or enter 'all' to get the stats for all countries.
        """
        table = soup.find('tbody')
        if country != None:
            if country.lower() == 'all':
                table_data = []
                for row in table.findAll('tr'):
                    row_data = []
                    for cell in row.findAll('td'):
                        row_data.append(cell.text)
                    if(len(row_data) > 0):
                        
                        data_item = {"Country": row_data[1],
                                        "TotalCases": row_data[2],
                                        "NewCases": row_data[3],
                                        "TotalDeaths": row_data[4],
                                        "NewDeaths": row_data[5],
                                        "TotalRecovered": row_data[6],
                                        "ActiveCases": row_data[7],
                                        "CriticalCases": row_data[8],
                            }
                        table_data.append(data_item)
                return table_data
            else:
                table_data = []
                for row in table.findAll('tr'):
                    row_data = []
                    for cell in row.findAll('td'):
                        row_data.append(cell.text)
                    if(len(row_data) > 0):
                        
                        data_item = {"Country": row_data[1],
                                        "TotalCases": row_data[2],
                                        "NewCases": row_data[3],
                                        "TotalDeaths": row_data[4],
                                        "NewDeaths": row_data[5],
                                        "TotalRecovered": row_data[6],
                                        "ActiveCases": row_data[7],
                                        "CriticalCases": row_data[8],
                            }
                        if row_data[1].lower() == country.lower():
                            table_data.append(data_item)

                return table_data


        else:
            elements = soup.find_all("div", class_="maincounter-number")

            data = {}
            data.update({'cases': elements[0].text.strip(), 'deaths': elements[1].text.strip(), 'recovered': elements[2].text.strip()})
            return data