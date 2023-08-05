#!/usr/bin/env python3

# 3rd parties
import pytest

# klon
from klon import build_etree, make_all_urls_absolute, tostring


@pytest.mark.parametrize(
    'base_url, etree, expected',
    [
        (
            # relative URLs are made absolute
            'http://example.com/',
            build_etree('div', ['a', {'href': 'relative/link'}]),
            build_etree('div', ['a', {'href': 'http://example.com/relative/link'}]),
        ),
        (
            # absolute URLs are untouched
            'http://example.com/',
            build_etree('div', ['a', {'href': 'http://absolute/link'}]),
            build_etree('div', ['a', {'href': 'http://absolute/link'}]),
        ),
        (
            # an https:// URL doesn't override an http:// URL
            'https://example.com/',
            build_etree('div', ['a', {'href': 'http://absolute/link'}]),
            build_etree('div', ['a', {'href': 'http://absolute/link'}]),
        ),
        (
            # an #anchor link gets merged too
            'http://example.com/',
            build_etree('div', ['a', {'href': '#anchor'}]),
            build_etree('div', ['a', {'href': 'http://example.com/#anchor'}]),
        ),
        (
            # not just ahrefs are updated -- see full list in klon/html.py
            'http://example.com/',
            build_etree('div', ['img', {'src': 'image.jpg'}]),
            build_etree('div', ['img', {'src': 'http://example.com/image.jpg'}]),
        ),
        (
            # the root element is updated too
            'http://example.com/',
            build_etree('a', {'href': 'relative/link'}),
            build_etree('a', {'href': 'http://example.com/relative/link'}),
        ),
        (
            # if the URL attribute is missing we don't complain
            'http://example.com/',
            build_etree('div', ['a', {'name': 'rover'}]),
            build_etree('div', ['a', {'name': 'rover'}]),
        ),
        (
            # empty links are replaced by the full base URL, as a browser does
            'http://example.com/',
            build_etree('div', ['a', {'href': ''}]),
            build_etree('div', ['a', {'href': 'http://example.com/'}]),
        ),
    ]
)
def test_make_all_urls_absolute(base_url, etree, expected):
    make_all_urls_absolute(base_url, etree)
    assert tostring(etree) == tostring(expected)
