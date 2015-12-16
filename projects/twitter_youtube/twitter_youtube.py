
# Runs through some tweets, expands short URLs, and if they point to youtube it tries to find out
# what category the video was posted to.
#
# To run the file:
#    python twitter_youtube.py
#
# It expects to find a file called 'tweets.csv' in the same directory.
# That file should be comma-separated and have the links to be followed in the first column.
# See the example tweets.csv file
#
# What we're looking for is a short section of html that lists the video categorym e,g,:
#    <h4 class="title">
#      Category
#    </h4>
#    <ul class="content watch-info-tag-list">
#        <li><a href="/channel/UC-9-kyTW8ZkZNDHQJ6FgpwQ" class="yt-uix-sessionlink g-hovercard      spf-link " data-ytid="UC-9-kyTW8ZkZNDHQJ6FgpwQ" data-sessionlink="ei=1rRhVvePNeX7iAbbhbfYBQ" >Music</a></li>
#    </ul>
#

from bs4 import BeautifulSoup
from urllib import urlopen

def get_category(url):
    """Assumes that the url points to youtube. Follows it and tries to find the categoty. Returns
    the category on None if it can't find one"""

    print("Following url", url,)

    page = urlopen(url)

    html = page.read() # Read the html and save it as a string

    soup = BeautifulSoup(html, 'html.parser')

    # print(soup.prettify())
    # FInd the category by: finding the header with 'Category', moving up one to the parent tag,
    # then finding the first li tag which has the link and actual category
    # (parent.li.a.contents[0]). See the html snipped at the top to see why this works.

    for h in soup.find_all('h4'):
        for content in h.contents:
            if "Category" in content:
                category = h.parent.li.a.contents[0].strip()
                # This is the h4 tag that we're after.
                print("\tI found the category:",category)
                return category

    print("\tI can't find a category, maybe not a youtube page?")
    return None




# ************ MAIN PROGRAM STARTS HERE *************

successes = 0 # Count the number of successful categories retrieved
total = 0 # Count the total number of urls checked

output = "" # PRepare a long list of results that will be written out to a file

# Read a csv file with tweets in it

with open('tweets.csv', 'r') as inf:

    for line in inf: # Iterate over every line in the file
        total += 1

        cols = line.strip().split(',') # Split the line into separate columns
        url = cols[0].strip() # The url is in the first column

        cat = get_category(url) # Call the get_category function to get the category

        if cat == None: # I didn't find a category
            output += ( line.strip() + "," + "-" + "\n" ) # Write out '-' to show that no category was found

        else: # I did find a category
            successes += 1
            output += ( line.strip() + "," + cat + "\n") 

print ("Finished! I found {} / {} pages that had a category".format(successes, total) )

# Write out the results to a file called 'output.csv'

with open('output.csv', 'w') as outf:
    outf.write(output)


