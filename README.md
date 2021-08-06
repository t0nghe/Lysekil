# DirtyHakBlogGenerator

This is a static-file blog generator written in Python (3.9.5). 

## Dependencies

These packages are used in this program. Respectively, 
* [python-markdown2](https://github.com/trentm/python-markdown2) is used to convert markdown to HTML;
* [Pygments](https://github.com/pygments/pygments) is used to highlight code syntax; and 
* [python-feedgen](https://feedgen.kiesow.be/) is used to generate 

You need to use Python 3.9+ because FeedGen requires timezone information to indicate time of publication. And `zoneinfo` package available from Python 3.9 allows you to specify timezones using a string, such as “Europe/Stockholm”.

## Usage

### Creating a Blog Post

1. Create a markdown file under `_source` folder. The folder structure under this directory is flat. 
2. The markdown file should be name something like this:
   1. `210101 filename.md` in which `210101` will be interpreted as the date of creation of this blog post in `yymmdd` format. This string is equivalent to January 1, 2021.
   2. `filename` part is for human reading and is not parsed by the generator.
3. The markdown file should have a format like this, with front matter and content separated by `///`. 

```
title=Title of the Post
tags=tag1, tag2, tag3
slug=sample_post
summary=This Is A Summary.
///
Paragraph 1 of your blog post.

Paragraph 2 of your blog post.

Paragraph 3 of your blog post.
```

**Fields in the header**

* `title` is the title of this blog post. It will be shown in either <h3> or <h1> on the webpage. 
* `tags` are the tags of this blog post. You may choose not to tag your post. Multiple tags are separated by a comma.
* `slug` is part of the URL by which this blog post is visited from the web.
  * When published, the URL of this post will be: `<yourblog.com>/2021/q1/sample_post`
  * Namely, your domain name; year; quarter; slug.
* `summary` is the summary of this blog post. It will be displayed on the index page, archive pages, tag listing pages, as well as the generated ATOM feed.

Check out `_source/210101 filename.md` and 

### Creating a page

This is a sample “about me” page. It also needs to bear a six-digit date stamp in it's filename. 

`title` functions similarly to that of a blog post.

Notably, the `page` property specifies this markdown file is a page and not a blog post. The difference between the two is that `pages` are not shown among blogs on the home page or other chornically ordered lists. 

The `slug` determines the URL of the published page. This page will be available at `<yourblog.com>/pages/about`.

Pages are not 

```
title=About Me
page=True
slug=about
///
My name is So-And-So. I live in Somewhere-Town. I do some stuff at work. I do some other stuff off work.
```

### Settings

Check out `code/settings.py`. Hopefully it's self-explanatory. 

### Generating Site

Run `python build.py`. 

The generated site will be created under `_target` directory by default. 

Move all the generated stuff to GitHub Pages. And it's done. 

## Editing the Template

The default color palette of this blog is inspired by [Bear](https://bear.app/). 

The page structure is quite straightforward. You can edit the `template.scss` under `_assets` folder to change the color palette and styling of the page. 

Changing the structure of the pages is a bit more cumbersome. You can start by reading`template.py`, which contains a bunch of functions that generate HTML partials. These functions are invoked by the `output_html` method in classes in `utils.py`.

## Known Issues

1. Pagination error: When the number of blog posts to be shown is divisible by `POSTS_PER_PAGE`, one more “next page” link will be created.  

## Demo

My own blog at [tonghe.xyz](https://tonghe.xyz/) is a demo for this blog generator. 