from RadlexOntology import RadlexOntology
import re
from stopwords import STOPWORDS


class RadlexAnnotator(object):

    def __init__(self):

        self.ontology = RadlexOntology()

    def annotate(self, text, stopwords=STOPWORDS, min_length=3):
        """

        stopwords - words that are ignored
        min_length - the minimum a word has to have to be annotated
        """

        ontology_classes = self.ontology.get_entity_elements()

        annotations_result = []

        for ontology_class in ontology_classes:

            name_elems = RadlexOntology.get_pref_and_synonyms(ontology_class)

            annotations = []

            # type of name is 'preferred' or 'synonym'
            for type_of_name in name_elems.keys():

                for name_elem in name_elems[type_of_name]:

                    name_text = name_elem.text.upper()

                    if len(name_text) < min_length or name_text in stopwords:
                        continue

                    escaped_name_text = re.escape(name_text)

                    name_regex = r'\b' + escaped_name_text + r'\b'

                    for match in re.finditer(name_regex, text.upper()):
                        span = match.span()
                        annotation = {}

                        if type_of_name == 'preferred':
                            annotation['matchType'] = 'PREF'
                        elif type_of_name == 'synonym':
                            annotation['matchType'] = 'SYN'

                        annotation['from'] = span[0] + 1
                        annotation['to'] = span[1]
                        annotation['text'] = match.group(0)

                        annotations.append(annotation)

            if annotations:
                annotations_class = {}

                annotated_class = {}
                annotated_class['label'] = ontology_class.find('{*}label').text
                annotated_class['prefName'] = name_elems['preferred'][0].text
                annotated_class['synonym'] = map(
                    lambda synonym: synonym.text,
                    name_elems['synonym']
                )

                definition = ontology_class.find('{*}Definition')
                if definition is not None:
                    annotated_class['definition'] = definition.text
                else:
                    annotated_class['definition'] = []

                annotations_class['annotatedClass'] = annotated_class
                annotations_class['annotations'] = annotations

                annotations_result.append(annotations_class)

        return annotations_result
