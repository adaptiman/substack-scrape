"""Module providing a summary of substack articles."""

import sys
import substack_api as ss
from substack_api import newsletter


# These are the fields of an article that we're interested in. 
# Other fields will be discarded.
GOOD_FIELDS = [
    'canonical_url',
    'description',
    'post_id',
    'title',
    'subtitle',
    'slug',
    'truncated_body_text',
]

# Categories that we want to pull newsletters from. Also a threshold of readership OoM.
CATEGORIES_AND_THRESHOLDS = [
    (4, 100000),      # technology
    (103, 100000),    # news
    (223, 100000),    # faith & spirituality
    (34, 100000)      # education
]


# Gets an article based on it's newsletters name and the article name
# filters the article to only keep the fields named in GOOD_FIELDS
def get_article_by_name(newsletter, title):
    article = ss.newsletter.get_post_contents(newsletter, title, html_only=False)

    filtered_article = {}

    for good_field in GOOD_FIELDS:
        filtered_article[good_field] = article.get(good_field)
    
    return filtered_article

# Gets all the newsletters in a category that have a readership order of magnitude at or above the threshold
def get_top_newsletters_in_category(category_id: int, readership_threshold: int):
    # Get all the newsletters on the first 2 pages of the category
    newsletters = ss.newsletter.get_newsletters_in_category(category_id, start_page=0, end_page=1)
    # Discard newsletters where the ranking OoM is None
    newsletters = [n for n in newsletters if n['rankingDetailFreeIncludedOrderOfMagnitude'] is not None]
    # Discard newsletters where the ranking OoM is less than the defined threshold
    newsletters = [n for n in newsletters if n['rankingDetailFreeIncludedOrderOfMagnitude'] >= readership_threshold]
    return newsletters


# Gets the top newsletters in a category, then gets the article with the most pins
# from the first page of each of those newsletters. Returns a list of articles.
def get_top_articles_in_category(category_id, readership_threshold):
    newsletters = get_top_newsletters_in_category(category_id, readership_threshold)
    articles = []

    for nl in newsletters:
        print(f'getting articles from newsletter {nl["name"]} in category {category_id}')
        found_articles = newsletter.get_newsletter_post_metadata(nl['subdomain'], start_offset = 0, end_offset = 1)
        found_articles.sort(key = lambda x: x['pins'], reverse = True)
        articles.append(found_articles[0])

    return articles
    
def main():
    print('starting')

    # Initialize a new object where the key is the category ID, and the value is
    # an array of the top articles. Starts out empty, we'll fill it in a second.
    articles = {cat_id: [] for cat_id, _ in CATEGORIES_AND_THRESHOLDS}

    # Get the top articles in each category
    for cat_id, threshold in CATEGORIES_AND_THRESHOLDS:
        articles[cat_id] = get_top_articles_in_category(cat_id, threshold)

    # This just prints the article titles
    # TODO: These articles should be cross checked against the actual top articles
    #       on substack, ie. make sure that these are actually the top articles. I'm
    #       not entirely convinced that sorting by pin count is the best way to sort.
    # TODO: Write the article content from this list to instapaper
    for cat_id, arts in articles.items():
        print(f"\n\nfound {len(arts)} articles in category {cat_id}")
        for art in arts:
            print(f"{art['title']}")

if __name__ == '__main__':
    main()
