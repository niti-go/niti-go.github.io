#!/usr/bin/env python3
"""
Build blog posts from markdown files to static HTML.
Run this script whenever you add/update a blog post.
"""

import os
import re
from pathlib import Path

# Simple markdown to HTML converter
def markdown_to_html(text):
    """Convert basic markdown to HTML"""
    # Code blocks
    text = re.sub(r'```(\w+)?\n([\s\S]*?)\n```', r'<pre><code class="language-\1">\2</code></pre>', text)

    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

    # Italic
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)

    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)

    # Headings
    text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)

    # Blockquotes
    text = re.sub(r'^> (.*?)$', r'<blockquote>\1</blockquote>', text, flags=re.MULTILINE)

    # Unordered lists
    text = re.sub(r'^- (.*?)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*?</li>\n)+', lambda m: '<ul>\n' + m.group(0) + '</ul>\n', text)

    # Ordered lists
    text = re.sub(r'^\d+\. (.*?)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*?</li>\n)+', lambda m: '<ol>\n' + m.group(0) + '</ol>\n', text)

    # Paragraphs
    text = re.sub(r'\n\n+', '</p>\n<p>', text)
    text = '<p>' + text + '</p>'

    return text

def parse_frontmatter(content):
    """Extract metadata from frontmatter"""
    match = re.match(r'^---\n([\s\S]*?)\n---\n([\s\S]*)$', content)

    metadata = {}
    body = content

    if match:
        frontmatter = match.group(1)
        body = match.group(2)

        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip().lower()] = value.strip().strip('"\'')

    return metadata, body

def build_blog_posts():
    """Generate HTML files for each markdown blog post"""
    blog_dir = Path('blog-posts')

    if not blog_dir.exists():
        print("❌ blog-posts directory not found")
        return

    markdown_files = list(blog_dir.glob('*.md'))

    if not markdown_files:
        print("⚠️  No markdown files found in blog-posts/")
        return

    print(f"📝 Building {len(markdown_files)} blog post(s)...\n")

    for md_file in markdown_files:
        with open(md_file, 'r') as f:
            content = f.read()

        metadata, body = parse_frontmatter(content)

        title = metadata.get('title', 'Untitled')
        date = metadata.get('date', 'No date')
        image = metadata.get('image', '')

        # Generate HTML filename from markdown filename
        html_filename = md_file.stem + '.html'

        # Convert markdown to HTML
        body_html = markdown_to_html(body)

        # Build the HTML page
        html_content = f'''<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - Niti Goyal</title>
  <link rel="stylesheet" href="styles.css">
  <style>
    .blog-post {{
      max-width: 800px;
      margin: 0 auto;
      padding: 3rem 2rem;
    }}

    .blog-post-header {{
      margin-bottom: 3rem;
    }}

    .back-link {{
      display: inline-block;
      margin-bottom: 2rem;
      color: #1a5bcd;
      text-decoration: none;
      font-weight: 500;
      transition: color 0.3s ease;
    }}

    .back-link:hover {{
      color: #0d3a7a;
    }}

    .blog-post-title {{
      font-size: 2.5rem;
      font-weight: 700;
      margin-bottom: 1rem;
      color: #000;
    }}

    .blog-post-meta {{
      color: #999;
      font-size: 0.95rem;
      margin-bottom: 2rem;
    }}

    .blog-post-image {{
      width: 100%;
      height: 400px;
      object-fit: cover;
      border-radius: 1rem;
      margin-bottom: 3rem;
    }}

    .blog-post-content {{
      color: #333;
      line-height: 1.8;
      font-size: 1.05rem;
    }}

    .blog-post-content h1,
    .blog-post-content h2,
    .blog-post-content h3 {{
      margin-top: 2rem;
      margin-bottom: 1rem;
      color: #000;
      font-weight: 700;
    }}

    .blog-post-content h1 {{
      font-size: 2rem;
    }}

    .blog-post-content h2 {{
      font-size: 1.8rem;
    }}

    .blog-post-content h3 {{
      font-size: 1.4rem;
    }}

    .blog-post-content p {{
      margin-bottom: 1.5rem;
    }}

    .blog-post-content ul,
    .blog-post-content ol {{
      margin-bottom: 1.5rem;
      margin-left: 2rem;
    }}

    .blog-post-content li {{
      margin-bottom: 0.5rem;
    }}

    .blog-post-content code {{
      background: #f5f5f5;
      padding: 0.2rem 0.5rem;
      border-radius: 0.25rem;
      font-family: 'Courier New', monospace;
      font-size: 0.9rem;
    }}

    .blog-post-content pre {{
      background: #2d2d2d;
      padding: 1.5rem;
      border-radius: 0.5rem;
      overflow-x: auto;
      margin-bottom: 1.5rem;
    }}

    .blog-post-content pre code {{
      background: none;
      color: #f8f8f2;
      padding: 0;
    }}

    .blog-post-content blockquote {{
      border-left: 4px solid #1a5bcd;
      padding-left: 1.5rem;
      margin-left: 0;
      margin-bottom: 1.5rem;
      color: #666;
      font-style: italic;
    }}

    .blog-post-content a {{
      color: #1a5bcd;
      text-decoration: underline;
    }}

    .blog-post-content a:hover {{
      color: #0d3a7a;
    }}

    @media (max-width: 640px) {{
      .blog-post {{
        padding: 2rem 1rem;
      }}

      .blog-post-title {{
        font-size: 1.75rem;
      }}

      .blog-post-image {{
        height: 250px;
        margin-bottom: 2rem;
      }}

      .blog-post-content {{
        font-size: 1rem;
      }}

      .blog-post-content h2 {{
        font-size: 1.4rem;
      }}
    }}
  </style>
</head>

<body>
  <nav class="navbar">
    <div class="nav-brand"><a href="index.html" style="color: #1a5bcd; text-decoration: none;">NG</a></div>
    <ul class="nav-links">
      <li><a href="index.html#about">About</a></li>
      <li><a href="index.html#experience">Experience</a></li>
      <li><a href="index.html#projects">Projects</a></li>
      <li><a href="index.html#blog">Blog</a></li>
      <li><a href="index.html#hobbies">Hobbies</a></li>
      <li><a href="index.html#contact">Contact</a></li>
    </ul>
  </nav>

  <div class="blog-post">
    <a href="index.html#blog" class="back-link">← Back to Blog</a>

    <div class="blog-post-header">
      <h1 class="blog-post-title">{title}</h1>
      <div class="blog-post-meta">{date}</div>
      {f'<img src="{image}" alt="{title}" class="blog-post-image">' if image else ''}
    </div>

    <div class="blog-post-content">
      {body_html}
    </div>
  </div>
</body>

</html>'''

        # Write the HTML file
        with open(html_filename, 'w') as f:
            f.write(html_content)

        print(f"✅ Generated: {html_filename}")
        print(f"   Title: {title}")
        print(f"   Date: {date}\n")

if __name__ == '__main__':
    build_blog_posts()
    print("✨ Blog build complete!")
