from bs4 import BeautifulSoup
from html.parser import HTMLParser


raw_html = """<td class='bau' colspan='12'> hey </td>"""
soup = BeautifulSoup(raw_html,'html.parser')
column = soup.td
print(column['colspan'])