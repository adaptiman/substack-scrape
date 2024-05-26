"""Module providing a summary of substack articles."""

import substack_api as ss
from substack_api import newsletter, user

#print(ss.newsletter.list_all_categories())
#print(ss.newsletter.get_newsletters_in_category(4, start_page=0, end_page=2))
print(ss.newsletter.get_newsletter_post_metadata("wilderreport", start_offset=0, end_offset=1))