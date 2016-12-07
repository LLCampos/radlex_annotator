# radlex_annotator
A local [NCBO Annotator] (http://bioportal.bioontology.org/annotator) replacement to annotate [RadLex](http://www.radlex.org/) terms. 

You can check how to use the annotator by reading the [test code](https://github.com/LLCampos/radlex_annotator/blob/master/tests/annotator_test.py).

From the tests I've done, it replicates the behaviour of NCBO Annotator with a sweet extra that annotates some terms that BioPortal annotator doesn't annotate. For example, this system annotates “benign” in “•Benign” (note the little black point) but NCBO's doesn’t. 

Having said this, this system is way slower than NCBO's one, even though it is local. 

If speed is something important to your project but you don't want to depend on a third-party's service, you can ask for the [NCBO Virtual Appliance](https://www.bioontology.org/wiki/index.php/Category:NCBO_Virtual_Appliance#Getting_Started), which includes the NCBO Annotator ([NBO Annotator GitHub repository](https://github.com/ncbo/ncbo_annotator)).

I wrote one "sanity-check test" to be sure nothing is broken when some code is changed. To run it, do:

```bash run_tests.sh```
