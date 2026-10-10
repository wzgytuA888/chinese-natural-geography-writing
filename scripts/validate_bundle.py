"""Validate skill links, corpus integrity and numeric ledger behavior.

Run with Python 3.10+; only stdlib is needed. This does not grade prose quality.
"""
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ledger',ROOT/'scripts/build_evidence_ledger.py')
ledger=importlib.util.module_from_spec(spec)
spec.loader.exec_module(ledger)


class BundleTests(unittest.TestCase):
    def fixture(self):
        return json.loads((ROOT/'evals/ledger-input.json').read_text(encoding='utf-8'))

    def test_endpoint_arithmetic(self):
        facts=ledger.build_ledger(self.fixture())['facts']
        self.assertEqual(facts[0]['absolute_change'],12)
        self.assertEqual(facts[0]['relative_percent_change'],10)
        self.assertEqual(facts[1]['percentage_point_change'],5)
        self.assertEqual(facts[1]['relative_percent_change'],25)

    def test_index_is_not_percentage(self):
        row=ledger.build_ledger(self.fixture())['facts'][2]
        self.assertEqual(row['absolute_change'],.05)
        self.assertIsNone(row['percentage_point_change'])

    def test_zero_baseline(self):
        row=ledger.build_ledger(self.fixture())['facts'][3]
        self.assertEqual(row['absolute_change'],5)
        self.assertIsNone(row['relative_percent_change'])

    def test_negative_baseline(self):
        data=self.fixture();data['series'][0]['observations'][0]['value']=-2
        self.assertIsNone(ledger.build_ledger(data)['facts'][0]['relative_percent_change'])

    def test_nonmonotone_series(self):
        data=self.fixture();data['series'][0]['observations']=[{'time':2000,'value':8},{'time':2010,'value':7.2},{'time':2020,'value':8.4}]
        row=ledger.build_ledger(data)['facts'][0]
        self.assertEqual(row['absolute_change'],.4)
        self.assertEqual(row['relative_percent_change'],5)
        self.assertEqual(row['observed_sequence_shape'],'non_monotone_or_contains_plateaus')

    def test_two_points_do_not_claim_continuous_trend(self):
        self.assertEqual(ledger.build_ledger(self.fixture())['facts'][0]['observed_sequence_shape'],'two_endpoints_only')

    def test_scenario_keeps_source_kind(self):
        data=self.fixture();data['series'][0]['kind']='scenario_estimate'
        row=ledger.build_ledger(data)['facts'][0]
        self.assertEqual(row['kind'],'scenario_estimate')
        self.assertTrue(any('conditional' in text for text in row['limitations']))

    def test_duplicate_id_rejected(self):
        data=self.fixture();data['series'][1]['id']=data['series'][0]['id']
        with self.assertRaises(ValueError): ledger.build_ledger(data)

    def test_duplicate_or_unsorted_times_rejected(self):
        for time in (2000,1990):
            data=self.fixture();data['series'][0]['observations'][1]['time']=time
            with self.assertRaises(ValueError): ledger.build_ledger(data)

    def test_missing_or_nonfinite_values_rejected(self):
        for value in (None,True,'NaN','Infinity','not-a-number'):
            data=self.fixture();data['series'][0]['observations'][0]['value']=value
            with self.assertRaises(ValueError): ledger.build_ledger(data)

    def test_required_context(self):
        data=self.fixture();del data['series'][0]['source']
        with self.assertRaises(ValueError): ledger.build_ledger(data)

    def test_percentage_scale(self):
        data=self.fixture();data['series'][1]['observations'][0]['value']=150
        with self.assertRaises(ValueError): ledger.build_ledger(data)

    def test_markdown_local_links(self):
        broken=[]
        for p in ROOT.rglob('*.md'):
            if '.git' in p.parts: continue
            for dest in re.findall(r'\]\(([^)\s]+)\)',p.read_text(encoding='utf-8')):
                if re.match(r'^(?:https?://|mailto:|#)',dest): continue
                target=(p.parent/dest.split('#')[0]).resolve()
                if not target.exists(): broken.append(f'{p.relative_to(ROOT)} -> {dest}')
        self.assertEqual(broken,[])

    def test_all_chapters_routed(self):
        index=(ROOT/'references/chapter-index.md').read_text(encoding='utf-8')
        chapters=list((ROOT/'chapters').glob('*.md'))
        self.assertEqual(len(chapters),52)
        self.assertTrue(all(p.name in index for p in chapters))

    def test_corpus_coverage(self):
        papers=json.loads((ROOT/'knowledge/corpus-bibliography.json').read_text(encoding='utf-8'))
        stats=json.loads((ROOT/'knowledge/corpus-statistics.json').read_text(encoding='utf-8'))
        self.assertEqual(len(papers),100)
        self.assertEqual(len({p['paper_id'] for p in papers}),100)
        self.assertEqual(len({p['sha256'] for p in papers}),100)
        self.assertEqual(sum(p['pdf_pages'] for p in papers),1485)
        self.assertEqual(sum(p['han_body_chars'] for p in papers),stats['overall']['han_chars'])
        self.assertFalse(any(p['extraction_warning'] for p in papers))

    def test_no_raw_corpus_or_machine_paths(self):
        prohibited=[]
        for p in ROOT.rglob('*'):
            if not p.is_file() or '.git' in p.parts: continue
            if p.suffix.lower() in ('.pdf','.zip','.png','.jpg','.jpeg','.docx'):
                prohibited.append(str(p.relative_to(ROOT)))
            if p.suffix.lower() in ('.md','.json','.py','.yaml'):
                text=p.read_text(encoding='utf-8')
                if re.search(r'[CG]:[\\/]Users[\\/]|G:[\\/]D01_water|gh[oprs]_[A-Za-z0-9]{30,}',text):
                    prohibited.append(str(p.relative_to(ROOT)))
        self.assertEqual(prohibited,[])


if __name__=='__main__':
    unittest.main(verbosity=2)
