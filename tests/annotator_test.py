import unittest
from annotator import Annotator


class AnnotatorTests(unittest.TestCase):

    def test_sanity_check(self):
        """A sanity check test just to be sure that nothing is broken when
        making some change to the code."""

        with open('tests/report.txt') as f:
            text = f.read()

        annot = Annotator.RadlexAnnotator()
        annotations = annot.annotate(text)

        self.assertEqual(75, len(annotations))
