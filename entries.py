from bs4 import BeautifulSoup
import requests

#data to scrape for each entry: title, number of the order, number of comments and points

def filter_gt5(entries):
    # filter all previous entries with more than five words in the title ordered by the number of comments first
    # using rank of the entry as tie-breaker
    # least to most number of comments

    # i could have sent the entire list of entries here and then filtered for the longer titles, but it was more efficient to separate them while generating the list of total entries
    num_comments = list(entries.keys())
    num_comments.sort()
    filtered = {i: entries[i] for i in num_comments}        
    return list(filtered.values())


def filter_ltet5(entries):
    # filter all previous entries with <= 5 words in the title ordered by points 
    # lowest to highest points
    # using rank of the entry as tie-breaker
    points = list(entries.keys())
    points.sort()
    filtered = {i: entries[i] for i in points}        
    return list(filtered.values())
  
def print_formatted(entries):
  # print the entries in a more legible format
  for e in entries:
    rank = e['rank']
    title = e['title']
    score = e['score']
    comm = e['comments']
    print(f'{rank}. {title}')
    print( f'    {score} points | {comm} comments')
    print()
  return 0
    
try: 
  url = 'https://news.ycombinator.com/'
  response = requests.get(url)
  # using Beautiful Soup to parse the html returned by the get request as an API that returns json data is still in the works according to the website
  soup1 = BeautifulSoup(response.text)

  #odd items have the titles and the even items have the rank 
  items = soup1.find_all('td', class_='title')

  scores = soup1.find_all('span', class_='score')

  spans = soup1.find_all('span', class_='subline')

  entries_total = []
  # both dictionaries to be able to sort by key in the filtering functions above
  entries_short_title = {}
  entries_long_title = {}
 
  # title index allows for indexing into the items list for only the odd tags
  title_index = 1

  # range 0 to 30 because we are scraping 30 entries
  for i in range(0, 30):
    entry = {}
    # the rank is the index + 1 because the find_all functions returns tags in the order they are encountered, which in this case is the order of the entries
    entry['rank'] = i + 1
  
    # used later to count the number of words in the title by splitting this string by spaces
    title_temp = items[title_index].text
    # [0:-1] to exclude the url at the end 
    title_words = title_temp.split()[0:-1]
    entry['title'] = ' '.join( title_words[0:-1])

    temp_s = scores[i].text
    entry['score'] = int(temp_s.split()[0])

    temp_c = spans[i].find_all('a')[3].text
    if 'comment' not in temp_c:
      entry['comments'] = 0
    # there is a 'discuss' link instead of comments when there are no comments
    else:
      comments = temp_c.split()[0]
      entry['comments'] = int(comments)
 
    if len(title_words) <= 5:
      # ordering by score so the dictionary is keyed by the score of each entry
      entries_short_title[entry['score']] = entry
    else:
      # ordering by number of comments so the dictionary is keyed by the number of comments for each entry
      entries_long_title[entry['comments']] = entry

    entries_total.append(entry)

    # += 2 to get to the next odd list item
    title_index += 2
except:
    print('An error has occurred.')
  

print_formatted(entries_total)

filter1 = input("Do you want to filter entries with long titles by number of comments? [y/n] \n")
if filter1 == 'y' or filter1 == 'Y':
  print_formatted( filter_gt5(entries_long_title) )

filter2 = input("Do you want to filter entries with short titles by number of points? [y/n] \n")
if filter2 == 'y' or filter2 == 'Y':
  print_formatted( filter_ltet5(entries_short_title))
