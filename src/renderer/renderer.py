"""
This module utilizes the python webbrowser library to render html/css output from the constructor module.
"""
import webbrowser
import os

def write_html(html_file: str, html_content: str, pathroot: str = "mockups/") -> None:
    """
    Write HTML content to a file.

    Args:
        html_file: The path to the HTML file.
        html_content: The HTML content to write.
    """
    fpath = os.path.join(pathroot, html_file)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return fpath

def render_html(html_path: str) -> None:
    """
    Render file from the given path using the default web browser.
    Args:
        html_path: The path to the HTML file to render.
    Raises:
        FileNotFoundError: If the HTML file does not exist.
    """
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"HTML file does not exist: {html_path}")
    # Ensure the path is absolute
    html_path = os.path.abspath(html_path)
    # normalize to url
    url = 'file://' + html_path
    webbrowser.open(url, new=2)  # Open in a new tab, if possible