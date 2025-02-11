"""Wrapping rendering tests for ``po2md`` CLI."""

import glob
import math
import os

import pytest

from mdpo.po2md import pofile_to_markdown


EXAMPLES_DIR = os.path.join('test', 'test_po2md', 'wrapwidth-examples')
EXAMPLES = sorted(
    os.path.basename(fp) for fp in glob.glob(EXAMPLES_DIR + os.sep + '*.md')
    if not fp.endswith('.expect.md')
)


@pytest.mark.parametrize('wrapwidth', (10, 40, 80, math.inf, 0))
@pytest.mark.parametrize('filename', EXAMPLES)
def test_wrapwidth(filename, wrapwidth):
    filepath_in = os.path.join(EXAMPLES_DIR, filename)
    basename = 'inf' if not wrapwidth else wrapwidth
    filepath_out = f'{filepath_in}.{basename}.expect.md'
    po_filepath = os.path.join(
        os.path.dirname(filepath_in),
        os.path.splitext(os.path.basename(filepath_in))[0] + '.po',
    )

    output = pofile_to_markdown(filepath_in, po_filepath, wrapwidth=wrapwidth)

    with open(filepath_out) as f:
        expected_output = f.read()
    assert output == expected_output
