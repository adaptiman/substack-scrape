"""Module providing a summary of substack articles."""

# Key fields from the Substack article JSON:
#     canonical_url
#     description
#     post_id
#     title
#     subtitle
#     slug
#     truncated_body_text


import substack_api as ss
from substack_api import newsletter

from flask import Flask
app = Flask(__name__)

#print(ss.newsletter.list_all_categories())
#print(ss.newsletter.get_newsletters_in_category(4, start_page=0, end_page=2))
#print(ss.newsletter.get_newsletter_post_metadata("wilderreport", start_offset=0, end_offset=1))
print(ss.newsletter.get_post_contents("wilderreport", "the-prairies-frozen-angel", html_only=False))

@app.route("/")
def home():
    return newsletter.get_post_contents("wilderreport", "the-prairies-frozen-angel", html_only=False)