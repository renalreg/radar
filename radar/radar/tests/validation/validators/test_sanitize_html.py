import pytest

from radar.validation.validators import sanitize_html as _sanitize_html

sanitize_html = _sanitize_html()

SAFE_HTML = """
<p><a href="http://www.google.com/" target="_blank">Hello</a></p>

<p><strong>Strong</strong></p>

<p><em>Em</em></p>

<p>Hello<br>World</p>

<ul>
  <li>Foo</li>
  <li>Bar</li>
</ul>

<ol>
  <li>One</li>
  <li>Two</li>
</ol>
"""

UNSAFE_HTML = """
<div>A div!</div>

<script>alert('Uh oh!');</script>

<a href="javascript: alert('Uh oh!')">Trust in me</a>
"""

SANITIZED_UNSAFE_HTML = """
&lt;div&gt;A div!&lt;/div&gt;

&lt;script&gt;alert('Uh oh!');&lt;/script&gt;

<a>Trust in me</a>
"""


def test_safe_html():
    assert sanitize_html(SAFE_HTML) == SAFE_HTML


def test_unsafe_html():
    assert sanitize_html(UNSAFE_HTML) == SANITIZED_UNSAFE_HTML
