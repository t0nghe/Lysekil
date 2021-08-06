BLOG_NAME = "NAME OF YOUR BLOG"
BLOG_URL = "https://url.to.your.blog/"

FAVICON = "favicon.ico"
CSSFILE = "template.css"
HEADERLOGO = "logo.png"
EXTERNAL_JS = "script.js"

SOURCE_DIR = '_source'
SOURCE_ASSETS_DIR = '_assets'
TARGET_DIR = '_target'

# This number determines how many posts are shown per page.
# This also controls how many entries are publsihed in the Atom feed.
POSTS_PER_PAGE = 10

# If a summary is not given in the header, this many paragraphs
# from the top of an entry are shown in an index/listing and in the Atom feed.
SHOW_PARAGRAPHS = 2

# These are by default
# ("Home", "/"),
# ("Archive", "/archive/"),
# ("Tags", "/tags")
ADDITIONAL_NAV_LINKS = [
    ("About", "/pages/about/"),
    ("Feed", "/atom.xml")
]

# Why don't we randomly sprinkle three from the list to the footer?
FOOTER_LINKS = [
    {
        "name": "Check Out My Friend's Blog",
        "href": "http://mycoolfriend.blog/",
        "desc": "There's a lot of cool stuff on their site!"
    }
]