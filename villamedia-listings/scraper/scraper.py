# Set up playwright
from playwright.sync_api import sync_playwright
import random

# Set up a browser and a page
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    print("Browser and page set up")
    page.goto("https://www.villamedia.nl/vacatures")
    page.wait_for_load_state("networkidle")

    # Get the number of pages
    pagination_text = page.query_selector_all(".page-navigation small")
    print(pagination_text)
    pagination_text = pagination_text[0].inner_text()
    print(pagination_text)
    pagination_text = pagination_text.split(" ")
    page_amount = pagination_text[3]

    listings = []

    print(f"Found {page_amount} pages")

    # Loop through all pages
    for page_number in range(1, int(page_amount) + 1):
        # Get all items with the class "vacature"
        items = page.query_selector_all("li.vacature")
        for item in items:
            # Get the a tag 
            a_tag = item.query_selector("a")
            # Get the link
            link = a_tag.get_attribute("href")
            # Add the link to the listings array
            listings.append(link)

        # Sleep for 1s
        page.wait_for_timeout(500)

        # Go to the next page by clicking the a tag with inner text "Volgende"
        if page_number != int(page_amount) - 1:
            page.click("a:has-text('Volgende')")
        print(f"Scraped page {page_number}")


    print(f"Found {len(listings)} listings")
    print(listings)

    # Loop through all listings
    for listing in listings:
        # Check if url contains villamedia.nl, other websites we can not scrape
        if "villamedia.nl" not in listing:
            continue

        print(f"Now scraping {listing}")
        page.goto(listing)
        page.wait_for_load_state("networkidle")

        # Get the title
        title = page.query_selector("h1").inner_text()
        print(title)

        # Make title safe for file name
        title = title.replace(" ", "-")
        title = title.replace("/", "-")
        title = title.lower()

        # Get the description
        listing_text = ""
        description = page.query_selector("div.text:last-child")

        # Select all p tags
        p_tags = description.query_selector_all("p")
        print(p_tags)

        # Loop through all p tags
        for p_tag in p_tags:
            # Get the inner text
            text = p_tag.inner_text()
            print(text)
            # Add the inner text to the listing_text variable
            listing_text += text + "\n"

        # Generate a random number to prevent overwriting
        random_number = random.randint(0, 100000)

        if(len(listing_text) > 0):
            # Write the description to a .txt file in the data folder
            with open(f"../data/{title}-{random_number}.txt", "w") as file:
                file.write(listing_text)
        else: 
            print("No description found")





