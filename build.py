import os
import shutil
from datetime import datetime
from datetime import date
from code.utils import *
from code.data_collections import *
from code.template import *
from operator import attrgetter

working_dir = os.getcwd()
SOURCE_PATH = os.path.join(working_dir, SOURCE_DIR)
SOURCE_ASSETS_PATH = os.path.join(working_dir, SOURCE_ASSETS_DIR)
TARGET_PATH = os.path.join(working_dir, TARGET_DIR)
TARGET_ASSETS_PATH = os.path.join(working_dir, TARGET_DIR, 'assets')

def write_html_file(ext_url, html):
    print('writing file: ', ext_url)
    output_pathname = os.path.join(TARGET_PATH, ext_url, 'index.html')
    
    os.makedirs(os.path.dirname(output_pathname), exist_ok=True)
    with open(output_pathname, "w") as f:
        f.write(html)

if __name__ == "__main__":
    
    asset_files = os.listdir(SOURCE_ASSETS_PATH)
    for asset_file in asset_files:
        print('copying: ', asset_file)
        source_pathname = os.path.join(SOURCE_ASSETS_PATH, asset_file)
        target_pathname = os.path.join(TARGET_ASSETS_PATH, asset_file)
        os.makedirs(os.path.dirname(target_pathname), exist_ok=True)
        shutil.copyfile(source_pathname, target_pathname)

    # Prepare data collections.
    filenames = os.listdir(SOURCE_PATH)

    for filename in filenames:
        if filename.endswith('.md'):
            entry = parse_entry(os.path.join(SOURCE_PATH, filename), filename)
            if entry['page']:
                pages.append(Page(entry))
            else:
                notes.append(Note(entry))

    for note in notes:
        quarter_collection[note.year_quarter].append(note)

        if note.tags:
            for tag in note.tags:
                tags_collection[tag].append(note)

    for tag in tags_collection:
        tag_listings.append(TagList(tag, tags_collection[tag]))
    
    for year_quarter in quarter_collection:
        # print('build line 51', year_quarter)
        quarter_listings.append(
            QuarterList(year_quarter, 
            quarter_collection[year_quarter])
        )

    blog_home = BlogHome(notes)
    
    # To output HTML files:
    # - In each Class, add a method to output ✅
    #       a) HTML string; and
    #       b) ext_url variable
    # - In this script:
    #      ✅ c) write a function that writes `index.html` to the non-existant /2021q3/test/ folder
    # Use for loops to 
    # ✅ 1. iterate through [archive_listings]
    # ✅ 1.1. At this step, output the paginations of archive_listings
    # ✅ 2. iterate through [tag_listings]
    # ✅ 2.1. output the pagination of each item in [tag_listings]
    # ✅ 3. iterate through single pages in [pages]
    # ✅ 4. iterate through single notes in [notes]
    # ✅ 5. generate BlogHome pagination
    # ✅ 6. generate a page for list of archive
    # ✅ 7. generate a page for list of tags

    # Specific steps.
    # 1. 
    # Reminder: quarter_listings contains a bunch of QuarterList objects. Which are iterated through using this quarter_list variable.
    for quarter_list in quarter_listings:
        for quarter_list_pagination in quarter_list.pagination:
            ext_url, html = quarter_list_pagination.output_html()
            write_html_file(ext_url, html)

    # 2.
    for tag_list in tag_listings:
        for tag_list_pagination in tag_list.pagination:
            ext_url, html = tag_list_pagination.output_html()
            write_html_file(ext_url, html)

    # 3.
    for page in pages:
        ext_url, html = page.output_html()
        write_html_file(ext_url, html)

    # 4. DONE! Can you imagine this actually worked!
    for note in notes:
        ext_url, html = note.output_html()
        write_html_file(ext_url, html)

    # 5. generate BlogHome pagination
    # use blog_home
    
    for blog_home_p in blog_home.pagination:
        ext_url, html = blog_home_p.output_html()
        write_html_file(ext_url, html)
    
    blog_home.gen_feed(os.path.join(TARGET_PATH, 'atom.xml'))

    # 6. generate a page for list of archive
    quarter_list_html = gen_header(specific_page_title="Archive")
    quarter_list_html += gen_archive_list_container(quarter_collection)
    quarter_list_html += gen_footer()
    write_html_file('archive/', quarter_list_html)

    # 7. generate a page for list of tags
    tags_list_html = gen_header(specific_page_title="Tags")
    tags_list_html += gen_tags_list_container(tags_collection)
    tags_list_html += gen_footer()
    write_html_file('tags/', tags_list_html)

# Map assets
