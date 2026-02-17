import wikipediaapi
import os
import time

# --- CONFIGURATION ---
TARGET_TOTAL_PAGES = 500
OUTPUT_FOLDER = "wiki_data"
LANGUAGE = "en"

# Categories to scrape (without the "Category:" prefix)
CATEGORIES = [
    "Banking",
    "Financial_instruments",
    "Monetary_policy",
    "Investment",
    "Stock_market",
    "Corporate_finance",
    "Insurance",
    "Accounting",
    "Taxation"
]

# --- SETUP ---
# Create output directory
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Initialize API with a proper user agent (Required by Wikipedia policy)
# Replace 'MyFinancialScraper' with your script name or email
wiki = wikipediaapi.Wikipedia(
    user_agent='MyFinancialScraper/1.0 (contact: your_email@example.com)',
    language=LANGUAGE
)

# Set to keep track of unique page titles (avoid duplicates)
collected_titles = set()


def save_page(page):
    """Saves the page text to a file."""
    # Clean title for filename
    filename = "".join(x for x in page.title if x.isalnum() or x in " _-").strip()
    filepath = os.path.join(OUTPUT_FOLDER, f"{filename}.txt")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Title: {page.title}\n")
        f.write(f"URL: {page.fullurl}\n")
        f.write("-" * 40 + "\n")
        f.write(page.text)

    print(f"✅ Saved: {page.title}")


def get_category_members(category_name):
    """
    Recursively fetches members of a category.
    Returns True if target count reached, False otherwise.
    """
    # Check if target reached
    if len(collected_titles) >= TARGET_TOTAL_PAGES:
        return True

    cat_page = wiki.page(f"Category:{category_name}")

    if not cat_page.exists():
        print(f"⚠️ Category '{category_name}' does not exist.")
        return False

    print(f"\n📂 Scanning Category: {category_name}...")

    # .categorymembers returns a dict of titles -> page objects
    members = cat_page.categorymembers

    for title, page in members.items():
        # Stop if we hit the limit
        if len(collected_titles) >= TARGET_TOTAL_PAGES:
            print("🎉 Target limit reached!")
            return True

        # Skip if already collected
        if title in collected_titles:
            continue

        # We only want articles (namespace 0), not sub-categories or talk pages
        if page.ns == wikipediaapi.Namespace.MAIN:
            save_page(page)
            collected_titles.add(title)
            # Sleep briefly to be polite to Wikipedia servers
            time.sleep(0.1)

        # Optional: Deep dive into subcategories (Depth 1)
        # Uncomment if you run out of pages in the top-level categories
        # elif page.ns == wikipediaapi.Namespace.CATEGORY:
        #     # Recursive call could go here, but be careful of infinite loops
        #     pass

    return False


# --- MAIN LOOP ---
print(f"🚀 Starting scrape for {TARGET_TOTAL_PAGES} pages...")
start_time = time.time()

for category in CATEGORIES:
    finished = get_category_members(category)
    if finished:
        break

end_time = time.time()
duration = round(end_time - start_time, 2)

print("\n" + "=" * 40)
print(f"🏁 Scrape Complete.")
print(f"Total Pages Saved: {len(collected_titles)}")
print(f"Time Taken: {duration} seconds")
print(f"Files stored in: {os.path.abspath(OUTPUT_FOLDER)}")