from .settings import *

# In order to get a full page, you need to get:
# 1) a header,
# 2) a container, and
# 3) a footer.

# Unfortunately, the structure of pages are not made flexible.
# I know some of the code is quite hacky. So I duly noted in some variable names. 

def gen_header(blog_name=BLOG_NAME, blog_url=BLOG_URL, favicon=FAVICON, addtional_nav_links=ADDITIONAL_NAV_LINKS, css_file=CSSFILE, ext_js=EXTERNAL_JS, header_logo=HEADERLOGO, specific_page_title=None):
    """Note: If this page is 1) page for archive; 2) for a tag; 3) for a single note or page, (namely, anything but the home page) pass in `specific_page_title`.
    """
    scrolling_interaction = ''
    if not specific_page_title:
        page_title = blog_name
        nav_style_name = "headerIndexPage"
        scrolling_interaction = 'id="scrollingInteraction"'
        HACKY_container_style = "<style>div#container { margin-top: 320px }</style>"
        HACKY_scrolling_script = f"""<script type="text/javascript" src="/assets/{ext_js}"></script>"""
    else:
        page_title = f"{specific_page_title } — {blog_name}"
        nav_style_name = "headerSpecificPage"
        HACKY_container_style = "<style>div#container { margin-top: 90px }</style>"
        HACKY_scrolling_script = ""

    header_nav_links = """<a href="/">Home</a> • <a href="/archive/">Archive</a> • <a href="/tags/">Tags</a>"""

    for (name, href) in addtional_nav_links:
        header_nav_links += f""" • <a href="{href}">{name}</a>"""

    html = f"""<!DOCTYPE html><html>
    <head><title>{page_title}</title><link rel="stylesheet" href="/assets/{css_file}" />
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="alternate" type="application/atom+xml" href="/atom.xml" />
    <link rel="icon" type="image/png" href="/assets/{favicon}" />
    {HACKY_scrolling_script}
    {HACKY_container_style}
    </head>
    <body><div {scrolling_interaction} class="{nav_style_name}"><div id="headerAvatar"><a href="{blog_url}"><img src="/assets/{header_logo}" alt="Header logo." /></a></div><div id="headerBlogName"><a href="{blog_url}">{blog_name}</a></div><div id="headerNav">{header_nav_links}</div></div>"""
    return html

def gen_specific_page_container(body: str, date, tags: list, title: str):
    '''
    [ 'body', 'date', 'ext_url', 'filename', 'page', 'slug', 'summary', 'tags', 'title', 'year_quarter' ]
    '''
    # TODO Future: If we were to take care of internal links to local files, we should work on this function.
    # TODO How do we even unpack these keyword arguments?
    # TODO How does this method work? It's datetime.date()
    pub_date = date.isoformat()
    tag_links = ""
    for tag in tags:
        tag_links += f'<a href="/tags/{tag}/">{tag}</a>'

    html = f"""<div id="container"><article><h1>{title}</h1><div class="articleDateLine"><span class="articleDate">{pub_date}</span><span class="articleDatelineTags">{tag_links}</span></div><div id="body">{body}</div></article></div>"""

    return html

def gen_listing_container(prev_url, next_url, included_notes, listing_header=None):
    '''listing_header: If it's the home page or it's pagination, use default. Otherwise, pass in the listing header, something like:
    Notes tagged with `yosup`, page 2.
    '''
    if listing_header:
        listing_header_html = f"""<div id="listingHeader"><h2>{listing_header}</h2></div>"""
    else:
        listing_header_html = ""

    listed_notes_html = ""
    for note in included_notes:
        pub_date = note.date # convert to string

        note_tags_html = ""
        for tag in note.tags:
            note_tags_html += f'<a href="/tags/{tag}/">{tag}</a>'

        listed_notes_html += f"""
        <article>
                <h3><a href="/{note.ext_url}">{note.title}</a></h3>
                <div class="articleDateLine">
                    <span class="articleDate">{pub_date}</span>
                    <span class="articleDatelineTags">{note_tags_html}</span>
                </div>
                <div>{note.summary}</div>
            </article>
        """

    if prev_url or next_url:
        nav_links = ""
        if prev_url:
            nav_links += f"""<a class="newer" href={prev_url}>Newer notes</a>"""
        if next_url:
            nav_links += f"""<a class="older" href={next_url}>Older notes</a>"""
        
        pagination_html = f"""<div id="pagination">{nav_links}</div>"""
    else:
        pagination_html = ""

    html = f"""<div id="container">
    {listing_header_html}
    <div id="listing">{listed_notes_html}</div>
    {pagination_html}
    """

    return html

def gen_archive_list_container(archive_collection):
    """Takes in data_collections.archive_collection as input."""
    
    keys = list(archive_collection.keys())
    keys.sort(reverse=True)

    list_html = f"""<ul>"""
    for key in keys:
        count = len(archive_collection[key])
        y_q = f'Q{key[1]}, {key[0]}'
        url = f'/archive/{key[0]}q{key[1]}/'
        if count == 1:
            list_html += f"""<li><a href="{url}">{y_q}</a>, {count} note</li>"""
        else:
            list_html += f"""<li><a href="{url}">{y_q}</a>, {count} notes</li>"""
    list_html += "</ul>"

    html = f"""<div id="container"><div id="listingHeader"><h2>Archive</h2></div>
    <div id="listing">{list_html}</div>
    """

    return html

def gen_tags_list_container(tags_collection):

    key_count = [(key, len(tags_collection[key])) for key in tags_collection]
    key_count.sort(key=lambda item:item[1], reverse=True)

    list_html = f"""<ul>"""
    for item in key_count:
        url = f'/tags/{item[0]}/'
        if item[1] == 1:
            list_html += f"""<li><a href="{url}">{item[0]}</a>, {item[1]} note</li>"""
        else:
            list_html += f"""<li><a href="{url}">{item[0]}</a>, {item[1]} notes</li>"""
    list_html += "</ul>"

    html = f"""<div id="container"><div id="listingHeader"><h2>Tags</h2></div>
    <div id="listing">{list_html}</div>
    """

    return html

def gen_footer(footer_links=FOOTER_LINKS):

    entries_html = ""
    for entry in footer_links:
        entries_html += f"""<div class="footerBlock">
        <div class="footerTitleLink"><a href="{entry['href']}">{entry['name']}</a></div>
        <p>{entry['desc']}</p>
        </div>
        """

    html = f"""<div id="footer">{entries_html}</div></body></html>"""

    return html