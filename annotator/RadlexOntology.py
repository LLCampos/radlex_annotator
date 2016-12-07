from lxml import etree


class RadlexOntology(object):

    def __init__(self):
        ontology_file_path = 'annotator/radlex.owl'

        with open(ontology_file_path) as f:
            self.ontology_tree = etree.parse(f).getroot()

        self.default_namespace = self.ontology_tree.nsmap[None]

    def get_entity_elements(self):
        """Return all elements that represent an ontology entity."""
        return filter(
            lambda element: element.find('{*}Preferred_name') is not None,
            self.ontology_tree
        )

    @classmethod
    def get_pref_and_synonyms(cls, class_elem):
        """Return a dict with two values:

        preferred - list of one element, corresponding to the preferred name of
        the class
        synonyms - list of elements corresponding to the synonyms of the
        class"""

        preferred_name_elem = class_elem.findall('{*}Preferred_name')
        synonyms_elems = class_elem.findall('{*}Synonym')

        return {'preferred': preferred_name_elem,
                'synonym': synonyms_elems}
