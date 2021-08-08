from zoneinfo import ZoneInfo
from datetime import datetime, date, timedelta
from .settings import *
from .template import *
import markdown2 as md
from feedgen.feed import FeedGenerator

def parse_frontmatter(frontmatter):
    lines = frontmatter.split('\n')
    parsed = dict()
    for line in lines:
        if not line:
            break
        key, value = line.split("=")
        if key == 'tags':
            parsed[key] = [i.strip() for i in value.split(',')]
        elif key == 'summary':
            parsed[key] = f"<p>{value}</p>"
        elif key == 'page':
            if value == 'True':
                parsed[key] = True
            else:
                parsed[key] = False
        else:
            parsed[key] = value.strip()
    if 'page' not in parsed.keys():
        parsed['page'] = False

    return parsed

def gen_ext_url(date, slug, page):
    quarter = int((date.month-0.01)//3+1)
    if not page:
        ext_url = f'{date.year}/q{quarter}/{slug}/'
    else:
        ext_url = f'pages/{slug}/'
    return ext_url

def gen_year_quarter(date):
    quarter = int((date.month-0.01)//3+1)
    year = date.year
    return (year, quarter)

def parse_entry(full_path_name, filename):

    with open(full_path_name) as fin:
        frontmatter, body = fin.read().split('///')
        entry = parse_frontmatter(frontmatter)
        entry['filename'] = filename
        body = md.markdown(body, extras=["footnotes", "fenced-code-blocks"])
        entry['body'] = body
        created = datetime.strptime(filename.split()[0], '%y%m%d')
        entry['date'] = created.date()
        entry['ext_url'] = gen_ext_url(entry['date'], entry['slug'], entry['page'])

        # In parse_frontmatter, I made sure there will be a 'page' key in metadata indicating if this file is a page.`
        if entry['page']==False:
            entry['year_quarter'] = gen_year_quarter(entry['date'])
            if 'summary' not in entry.keys():
                separate_graphs = [graf for graf in body.split('\n') if graf != '' and graf.startswith('<p>')]

                # Argh... I wish I were better at RegEx.
                graphs_to_show = separate_graphs[0:SHOW_PARAGRAPHS]
                if len(separate_graphs) > SHOW_PARAGRAPHS:
                    graphs_to_show[-1] = graphs_to_show[-1].replace('</p>', ' [...]</p>')

                entry['summary'] = ''.join(
                    graphs_to_show
                )

    return entry

# [ 'body', 'date', 'ext_url', 'filename', 'page', 'slug', 'summary', 'tags', 'title', 'year_quarter' ]
class Note:

    def __init__(self, entry):
        self.__dict__.update(entry)

    def entry_lead(self):
        return { "title": self.title, "tags": self.tags, 'date': self.date, 'ext_url': self.ext_url, 'summary': self.summary }
    
    def __repr__(self):
        return f"{self.filename}"

    def output_html(self):
        specific_page_title = f"{self.title}"
        html = ""
        html += gen_header(specific_page_title=specific_page_title)
        html += gen_specific_page_container(self.body, self.date, self.tags, self.title)
        html += gen_footer()

        return (self.ext_url, html)


# Stupid naming of property. It should be `isPage`.
# [ 'body', 'date', 'ext_url', 'filename', 'page', 'slug', 'title' ]
class Page:
    
    def __init__(self, entry):
        self.__dict__.update(entry)

    def output_html(self):
        specific_page_title = f"{self.title}"
        html = ""
        html += gen_header(specific_page_title=specific_page_title)
        # Pages do not have tags. 
        html += gen_specific_page_container(self.body, self.date, [], self.title)
        html += gen_footer()

        return (self.ext_url, html)

# TagList:
# A list of posts marked with a certain tag.
# There's a TagList object for each tag.
# And following pages if there are any.
# Sub-class Page to contain information needed for
# rendering a single page.
class TagList:

    class TagListPage:

        def __init__(self, tag_name, page_num, included_notes, is_last):
            if page_num == 1:
                self.ext_url = f"tags/{tag_name}/"
                self.header = f'Notes tagged with “{tag_name}”'
            else:
                self.ext_url = f"tags/{tag_name}/{page_num}/"
                self.header = f'Notes tagged with “{tag_name}”: page {page_num}'

            self.prev_url = None
            self.next_url = None
            if page_num == 2:
                self.prev_url = f"/tags/{tag_name}/"
            elif page_num > 2:
                self.prev_url = f"/tags/{tag_name}/{page_num-1}/"
            
            if not is_last:
                self.next_url = f"/tags/{tag_name}/{page_num+1}/"

            self.included_notes = included_notes
        
        def __repr__(self):
            text_rep = f"""§ext_url: {self.ext_url}\nprev_url: {self.prev_url}\nnext_url: {self.next_url}\nnotes: {str(self.included_notes)}§"""
            return text_rep

        def output_html(self):
            specific_page_title = f"{self.header}"
            html = ""
            html += gen_header(specific_page_title=specific_page_title)
            # Pages do not have tags. 
            html += gen_listing_container(
                self.prev_url, self.next_url, self.included_notes, self.header
            )
            html += gen_footer()

            return (self.ext_url, html)

    def __init__(self, tag_name, tagged_notes):
        self.tag_name = tag_name
        self.pagination = []
        self.notes = sorted(tagged_notes, key=lambda k: k.date, reverse=True)
        self._paginate()
    
    # TODO
    # Representation of it needs to be fixed/improved.
    def _paginate(self):

        total_pages = int(len(self.notes) / POSTS_PER_PAGE) + 1

        all_pages = []
        page_num = 1
        notes_on_this_page = []

        for note in self.notes:
            notes_on_this_page.append(note)
            if len(notes_on_this_page) == POSTS_PER_PAGE:
                all_pages.append( (page_num, notes_on_this_page) )
                page_num += 1
                notes_on_this_page = []
        else:
            if len(notes_on_this_page) > 0:
                all_pages.append( (page_num, notes_on_this_page) )
        
        for page in all_pages:
            if page[0] == total_pages:
                last = True
            else:
                last = False
            self.pagination.append(
                self.TagListPage( self.tag_name, page[0], page[1], last)
            )

# QuarterList:
# A list of notes published in a quarter.
# Other aspects similar to the above.

class QuarterList:

    class QuarterListPage:

        def __init__(self, tag_name, page_num, included_notes, is_last):
            year = tag_name[0]
            quarter = tag_name[1]
            if page_num == 1:
                self.ext_url = f"archive/{year}q{quarter}/"
                self.header = f'Notes published in Q{quarter}, {year}'
            else:
                self.ext_url = f"archive/{year}q{quarter}/{page_num}/"
                self.header = f'Notes published in Q{quarter}, {year}: page {page_num}'

            self.prev_url = None
            self.next_url = None
            if page_num == 2:
                self.prev_url = f"/archive/{year}q{quarter}/"
            elif page_num > 2:
                self.prev_url = f"/archive/{year}q{quarter}/{page_num-1}/"
            
            if not is_last:
                self.next_url = f"/archive/{year}q{quarter}/{page_num+1}/"

            self.included_notes = included_notes
        
        def __repr__(self):
            base = f"§ext_url: {self.ext_url}\nprev_url: {self.prev_url}\nnext_url: {self.next_url}\nnotes: {str(self.included_notes)}§"
            return base
        
        def output_html(self):
            specific_page_title = f"{self.header}"
            html = ""
            html += gen_header(specific_page_title=specific_page_title)
            # Pages do not have tags. 
            html += gen_listing_container(
                self.prev_url, self.next_url, self.included_notes, self.header
            )
            html += gen_footer()

            return (self.ext_url, html)
    
    def __init__(self, tag_name, tagged_notes):
        self.tag_name = tag_name
        self.pagination = []
        self.notes = sorted(tagged_notes, key=lambda k: k.date, reverse=True)
        self._paginate()
    
    # TODO
    # Representation of it needs to be fixed/improved.
    def _paginate(self):

        total_pages = int(len(self.notes) / POSTS_PER_PAGE) + 1

        all_pages = []
        page_num = 1
        notes_on_this_page = []

        for note in self.notes:
            notes_on_this_page.append(note)
            if len(notes_on_this_page) == POSTS_PER_PAGE:
                all_pages.append( (page_num, notes_on_this_page) )
                page_num += 1
                notes_on_this_page = []
        else:
            if len(notes_on_this_page) > 0:
                all_pages.append( (page_num, notes_on_this_page) )
        
        for page in all_pages:
            if page[0] == total_pages:
                last = True
            else:
                last = False
            self.pagination.append(
                self.QuarterListPage( self.tag_name, page[0], page[1], last)
            )


class BlogHome:

    class BlogHomeListPage:

        def __init__(self, page_num, included_notes, is_last):
            
            if page_num == 1:
                self.ext_url = f""
            else:
                self.ext_url = f"index/{page_num}/"
            
            self.prev_url = None
            self.next_url = None

            if page_num == 2:
                self.prev_url = f"/"
            elif page_num > 2:
                self.prev_url = f"/index/{page_num-1}/"
            
            if not is_last:
                self.next_url = f"/index/{page_num+1}/"

            self.included_notes = included_notes

        def __repr__(self):
            base = f"§ext_url: {self.ext_url}\nprev_url: {self.prev_url}\nnext_url: {self.next_url}\nnotes: {str(self.included_notes)}§"
            return base
        
        def output_html(self):
            html = ""
            html += gen_header()
            # Pages do not have tags. 
            html += gen_listing_container(self.prev_url, self.next_url, self.included_notes)
            html += gen_footer()

            return (self.ext_url, html)

    def __init__(self, published_notes):
        self.pagination = []
        self.notes = sorted(published_notes, key=lambda k: k.date, reverse=True)
        self._paginate()

    def _paginate(self):

        total_pages = int(len(self.notes) / POSTS_PER_PAGE) + 1

        all_pages = []
        page_num = 1
        notes_on_this_page = []

        for note in self.notes:
            notes_on_this_page.append(note)
            if len(notes_on_this_page) == POSTS_PER_PAGE:
                all_pages.append( (page_num, notes_on_this_page) )
                page_num += 1
                notes_on_this_page = []
        else:
            if len(notes_on_this_page) > 0:
                all_pages.append( (page_num, notes_on_this_page) )
        
        for page in all_pages:
            if page[0] == 1:
                self._rss = page[1]
            if page[0] == total_pages:
                last = True
            else:
                last = False
            self.pagination.append(
                self.BlogHomeListPage( page[0], page[1], last)
            )

    def gen_feed(self, ext_url):
        # TODO Values in this file should be made tweakable.
        fg = FeedGenerator()
        fg.id(BLOG_URL)
        fg.title(BLOG_NAME)
        fg.author( {'name':'Tonghe Wang','email':'meow'} )
        fg.link( href=BLOG_URL, rel='alternate' )
        fg.logo(f'{BLOG_URL}assets/{HEADERLOGO}')
        fg.icon(f'{BLOG_URL}assets/{FAVICON}')
        fg.language('en')
        for item in self._rss:
            item = item.entry_lead()
            fe = fg.add_entry()
            fe.id('tonghe_xyz_'+item['ext_url'])
            fe.title(item['title'])
            fe.link(href='https://tonghe.xyz/'+item['ext_url'])
            
            # pub_datetime=datetime(*item['date'].timetuple()[:-4], tzinfo=timezone(timedelta(seconds=3600)))
            pub_datetime=datetime(*item['date'].timetuple()[:-4], tzinfo=ZoneInfo('Europe/Stockholm'))
            # fe.published(datetime(y, m, d))
            fe.published(pub_datetime)
            fe.summary(item['summary'])

        fg.atom_file(ext_url)
