"""Module providing a summary of substack articles."""

import substack_api as ss
from substack_api import newsletter

GOOD_FIELDS = [
    'canonical_url',
    'description',
    'post_id',
    'title',
    'subtitle',
    'slug',
    'truncated_body_text',
]

CATEGORIES_AND_THRESHOLDS = [
    (4, 100000),      # technology
    (103, 100000),    # news
    (223, 100000),     # faith & spirituality
    (34, 100000)       # education
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
    newsletters = ss.newsletter.get_newsletters_in_category(category_id, start_page=0, end_page=2)
    newsletters = [n for n in newsletters if n['rankingDetailFreeIncludedOrderOfMagnitude'] is not None]
    newsletters = [n for n in newsletters if n['rankingDetailFreeIncludedOrderOfMagnitude'] >= readership_threshold]
    return newsletters

# For each category, get the top newsletters for that category and print them
for category, threshold in CATEGORIES_AND_THRESHOLDS:
    print(f'{category}:')
    newsletters = get_top_newsletters_in_category(category, threshold)
    [print(n['name']) for n in newsletters]
    print('\n')

# print(ss.newsletter.list_all_categories())
#print(ss.newsletter.get_newsletter_post_metadata("wilderreport", start_offset=0, end_offset=1))
# article = ss.newsletter.get_post_contents("wilderreport", "the-prairies-frozen-angel", html_only=False)
