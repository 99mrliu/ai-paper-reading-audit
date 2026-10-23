import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'skill/scripts'
sys.path.insert(0,str(SCRIPTS))
import verify_claims as v

TEXT='The prospective test achieved a correlation of 0.862 on 17 countries. The retrospective test achieved 0.990. A value of 9.7% is reported.'


class EvidenceInvariants(unittest.TestCase):
    def setUp(self):
        self.pages=[{'page':1,'flat':TEXT},{'page':2,'flat':'In 2017, a different measurement was performed.'}]
        self.doc={'claims':[{'id':'C1','class':'FACT','statement':'Prospective test score','value':'0.862','page':1,
                             'quote':'The prospective test achieved a correlation of 0.862 on 17 countries.'}]}
    def result(self,doc=None): return v.verify(doc or self.doc,self.pages,{'scope':'provided_document'})
    def test_valid_evidence(self): self.assertEqual(self.result()['summary']['failures'],0)
    def test_wrong_page_is_failure(self):
        self.doc['claims'][0]['page']=2
        self.assertGreater(self.result()['summary']['failures'],0)
    def test_nearby_other_experiment_number_not_support(self):
        self.doc['claims'][0]['value']='0.990'
        self.assertGreater(self.result()['summary']['failures'],0)
    def test_integer_does_not_match_year(self):
        self.doc['claims'][0].update(value='17',page=2,quote=self.pages[1]['flat'])
        self.assertGreater(self.result()['summary']['failures'],0)
    def test_percentage_not_unitless(self):
        self.doc['claims'][0].update(value='9.7',quote='A value of 9.7% is reported.')
        self.assertGreater(self.result()['summary']['failures'],0)
    def test_equivalent_decimal_spelling(self):
        self.doc['claims'][0].update(value='0.9900',quote='The retrospective test achieved 0.990.')
        self.assertEqual(self.result()['summary']['failures'],0)
    def test_unknown_really_executes_search(self):
        self.doc['claims'].append({'id':'U1','class':'UNKNOWN','statement':'Country-specific calibration unresolved',
                                  'absence_probe':['countries','China'],'search_scope':'supplied PDF',
                                  'reasoning':'A list does not establish country-specific calibration'})
        res=self.result()['claims'][1]
        self.assertEqual(res['status'],'WARN')
        self.assertTrue(res['search_results'][0]['hits'])
        self.assertFalse(res['search_results'][1]['hits'])
    def test_unknown_without_search_fails(self):
        self.doc['claims'][0]={'id':'U1','class':'UNKNOWN','statement':'Missing information'}
        self.assertGreater(self.result()['summary']['failures'],0)
    def test_duplicate_ids_fail(self):
        self.doc['claims'].append(copy.deepcopy(self.doc['claims'][0]))
        with self.assertRaises(ValueError):self.result()
    def test_invalid_class_fails(self):
        self.doc['claims'][0]['class']='CERTIFIED'
        self.assertGreater(self.result()['summary']['failures'],0)
    def test_unsupported_transfer_reference_fails(self):
        self.doc['transfer']=[{'step':'input','verdict':'可直接用','because':['DOES_NOT_EXIST']}]
        self.assertGreater(self.result()['summary']['failures'],0)
    def test_overall_contradiction_fails(self):
        self.doc['transfer']=[{'step':'input','verdict':'信息不足','because':['C1']}]
        self.doc['verdict_overall']='可直接用'
        self.assertGreater(self.result()['summary']['failures'],0)
    def test_unanchored_arithmetic_fails(self):
        self.doc['derivations']=[{'id':'D1','expr':'2/3*100','expected':66.67,'source_claims':['C1']}]
        self.assertGreater(self.result()['summary']['failures'],0)
    def test_bounded_arithmetic(self):
        self.assertAlmostEqual(v.safe_eval('959/9846*100'),9.739996,places=5)
        with self.assertRaises(ValueError):v.safe_eval('10**100000000')
        with self.assertRaises(ValueError):v.safe_eval('__import__("os")')
    def test_empty_claims_fails(self):
        with self.assertRaises(ValueError):self.result({'claims':[]})
    def test_render_rejects_modified_claims(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=Path(tmp);idx=r/'index';idx.mkdir()
            (idx/'pages.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in self.pages))
            meta={'status':'ok','scope':'provided_document','source':'synthetic.pdf','sha256':'synthetic-source',
                  'pages_sha256':v.digest(idx/'pages.jsonl'),'pages':2}
            (idx/'index.json').write_text(json.dumps(meta))
            claims=r/'claims.json';claims.write_text(json.dumps(self.doc))
            verification=r/'verification.json'
            cmd=[sys.executable,str(SCRIPTS/'verify_claims.py'),'--claims',str(claims),'--index',str(idx),'--out',str(verification)]
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,0)
            self.doc['claims'][0]['statement']='Changed after verification'
            claims.write_text(json.dumps(self.doc))
            cmd=[sys.executable,str(SCRIPTS/'render_report.py'),'--claims',str(claims),'--verification',str(verification),
                 '--index',str(idx),'--out',str(r/'report.md')]
            self.assertNotEqual(subprocess.run(cmd,capture_output=True).returncode,0)
            self.assertFalse((r/'report.md').exists())
    def test_missing_pdf_has_structured_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            idx=Path(tmp)/'index'
            cmd=[sys.executable,str(SCRIPTS/'build_index.py'),str(Path(tmp)/'missing.pdf'),'--out',str(idx)]
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,2)
            self.assertEqual(json.loads((idx/'index.json').read_text())['status'],'invalid_input')


if __name__=='__main__':unittest.main(verbosity=2)
