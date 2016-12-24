from lxml import etree
import os
import annotator


class RadlexOntology(object):

    def __init__(self, subset=False):

        if not subset:
            onto_file_name = 'radlex.owl'
        elif subset == 'anatomical_entity':
            onto_file_name = 'radlex_subset_anatomical_entity.owl'
        else:
            raise Exception('That subset is not supported.')

        annotator_package_path = os.path.dirname(annotator.__file__)
        ontology_file_path = os.path.join(annotator_package_path,
                                          onto_file_name)

        with open(ontology_file_path) as f:
            self.ontology_tree = etree.parse(f).getroot()

        self.namespaces = self.ontology_tree.nsmap
        self.namespaces['radlex'] = self.namespaces[None]
        del self.namespaces[None]

    def get_entity_elements(self):
        """Return all elements that represent an ontology entity."""
        return filter(
            lambda element:
                element.find('{*}Preferred_name') is not None or
                element.find('{*}Synonym') is not None,
            self.ontology_tree
        )

    def get_pref_and_synonyms(self, class_elem):
        """Return a dict with two values:

        preferred - list of one string, corresponding to the preferred name of
        the class
        synonyms - list of strings corresponding to the synonyms of the
        class"""

        preferred_name_elem = class_elem.findall('{*}Preferred_name')

        # If it does not have a Preferred_name elem, the preferred name will be
        # the ID of the class.
        if not preferred_name_elem:
            id_key = '{' + self.namespaces['rdf'] + '}ID'
            preferred_name = class_elem.get(id_key)
        else:
            preferred_name = map(lambda elem: elem.text, preferred_name_elem)

        synonyms_elems = class_elem.findall('{*}Synonym')
        synonyms = map(lambda elem: elem.text, synonyms_elems)

        return {'preferred': preferred_name,
                'synonym': synonyms}

    def get_direct_children(self, rid):
        """Returns a list of all direct child nodes of the node with the RID
        given in the argument."""
        query = '//rdfs:subClassOf[@rdf:resource="#{}"]/..'.format(rid)
        return self.ontology_tree.xpath(query, namespaces=self.namespaces)

    def get_children(self, rid):
        """Returns a list of all child nodes of the node with the RID
        given in the argument."""
        children = []
        direct_children = self.get_direct_children(rid)
        children += direct_children
        direct_children_rids = map(
            lambda node: node.get('{{{}}}ID'.format(self.namespaces['rdf'])),
            direct_children
        )

        for child_rid in direct_children_rids:
            children += self.get_children(child_rid)

        return children
