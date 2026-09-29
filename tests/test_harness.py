import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import wiki

class HarnessTests(unittest.TestCase):
    def test_original_passages_are_exact(self):
        for e in wiki.catalog():
            lines=(wiki.ROOT/e['path']).read_text().splitlines(keepends=True)
            for c in wiki.chunks(e):
                self.assertEqual(c['text'], ''.join(lines[c['line_start']-1:c['line_end']]))

    def test_fixed_retrieval_expectations(self):
        wiki.rebuild()
        for c in json.loads((wiki.ROOT/'evals/cases.json').read_text())[:3]:
            self.assertTrue(any(p['path']==c['expected_source'] and c['expected_quote'] in p['text'] for p in wiki.retrieve(c['question'])))

    def test_retrieval_excludes_generated_material(self):
        wiki.rebuild()
        canary='UNSEARCHABLE_TANGERINE_CANARY_87342'
        with tempfile.TemporaryDirectory(dir=wiki.ROOT/'.state') as d:
            Path(d,'chat.txt').write_text(canary)
            self.assertEqual(wiki.retrieve(canary), [])
        for p in wiki.retrieve('alignment'):
            self.assertTrue(p['path'].startswith('vault/raw/'))

    def test_search_does_not_call_model(self):
        with patch.object(wiki,'generate',side_effect=AssertionError('Model called')):
            self.assertTrue(wiki.retrieve('alignment'))

    def test_missing_and_forged_citations_fail_closed(self):
        passage={'id':'P123','text':'Training lasts 3,000 steps.'}
        for supports in [[],[{'source_id':'P999','quote':'Training lasts 3,000 steps.'}],[{'source_id':'P123','quote':'Training lasts 9,000 steps.'}]]:
            answer, refs, errors=wiki.assess_claims({'insufficient_evidence':False,'claims':[{'text':'Claim','supports':supports}]},[passage])
            self.assertIn('Insufficient evidence',answer); self.assertTrue(errors)

    def test_valid_citation_and_honest_abstention(self):
        p={'id':'P123','text':'Training lasts 3,000 steps.'}
        answer, refs, errors=wiki.assess_claims({'insufficient_evidence':False,'claims':[{'text':'Training lasts 3,000 steps.','supports':[{'source_id':'P123','quote':p['text']}]}]},[p])
        self.assertFalse(errors); self.assertIn('[P123]',answer)
        self.assertIn('Insufficient evidence',wiki.assess_claims({'insufficient_evidence':True,'claims':[]},[p])[0])

    def test_repair_retains_failure_and_is_bounded(self):
        # Unit-only doubles test control flow; actual model evidence is separate.
        wiki.rebuild()
        p=wiki.retrieve('alignment')[0]
        quote=next(line for line in p['text'].splitlines() if len(line)>20)
        def payload(q):
            return json.dumps({'insufficient_evidence':False,'claims':[{'text':'Test claim','supports':[{'source_id':p['id'],'quote':q}]}]})
        bad=payload('INVENTED QUOTATION THAT IS ABSENT')
        good=payload(quote)
        for repaired in [good,bad]:
            with self.subTest(repaired=repaired==good), patch.object(wiki,'generate',side_effect=[(bad,{}),(repaired,{})]) as model:
                record=wiki.ask('alignment')
                self.assertEqual(model.call_count,2)
                self.assertEqual(len(record['citation_validation_attempts']),2)
                self.assertTrue(record['citation_validation_attempts'][0]['citation_errors'])
                self.assertEqual(record['citation_validation_attempts'][0]['raw_model_answer'],bad)
                original=model.call_args_list[0].args[0]
                repair=model.call_args_list[1].args[0]
                self.assertEqual(repair[:2],original)
                self.assertEqual(bool(record['citation_errors']),repaired==bad)
                if repaired==bad:self.assertIn('Insufficient evidence',record['answer'])

    def test_chat_capabilities_and_followup_skip_retrieval(self):
        for q in ['what can we do?', 'what can you help me with?', 'make that shorter']:
            self.assertFalse(wiki.needs_notes(q))
        self.assertTrue(wiki.needs_notes('What do my notes say about tuning?'))

    def test_source_free_drafting_and_explicit_source_requests(self):
        for q in ['Draft an AI safety meetup invitation', 'Please remember a nickname only in this chat, not my wiki', 'Brainstorm governance essay ideas']:
            self.assertFalse(wiki.needs_notes(q))
        for q in ['Draft a summary using my notes', 'Explain assistance games', 'Compare the proposals in the sources', 'Summarize notes about human control', 'What does the lecture propose?']:
            self.assertTrue(wiki.needs_notes(q))

    def test_scripted_reset_terminates_and_clears_history(self):
        # Actual CLI subprocess with capability turns (which need no model).
        with tempfile.TemporaryDirectory(dir=wiki.STATE) as d:
            path=Path(d)
            (path/'turns.txt').write_text('what can we do?\n/reset\nwhat can you help me with?\n/exit\n')
            result=subprocess.run([sys.executable,str(wiki.ROOT/'wiki.py'),'chat','--script',str(path/'turns.txt'),'--save-dir',str(path)],cwd=wiki.ROOT,capture_output=True,text=True,timeout=10)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads((path/'chat-03.json').read_text())['history_messages'],0)
            self.assertEqual(len(list(path.glob('chat-*.json'))),2)

    def test_unrelated_turn_drops_carried_evidence(self):
        p={'id':'P123','text':'Original evidence'}
        with patch.object(wiki,'generate',return_value=('A suggested draft',{})), patch.object(wiki,'retrieve',side_effect=AssertionError('Unnecessary retrieval')):
            record,carried=wiki.chat_turn('Draft a birthday greeting',[],[p])
            self.assertEqual(record['passages'],[])
            self.assertEqual(carried,[])

    def test_capability_paraphrase_uses_accurate_contract(self):
        with patch.object(wiki,'generate',side_effect=AssertionError('Capability contract needs no model')):
            record,_=wiki.chat_turn('Which commands do you support?',[],[])
        self.assertFalse(record['retrieval_called'])
        self.assertIn('doctor` reports model/device',record['answer'])
        self.assertIn('review` records an inspected page',record['answer'])

    def test_note_chat_rejects_wrong_passage_quotes(self):
        passages=wiki.retrieve('alignment')
        bad=json.dumps({'insufficient_evidence':False,'claims':[{'text':'Claim','supports':[{'source_id':passages[0]['id'],'quote':'A quotation absent from the indicated original passage.'}]}]})
        with patch.object(wiki,'generate',return_value=(bad,{})) as model:
            record,_=wiki.chat_turn('What do my notes say about alignment?',[],[])
        self.assertEqual(record['interaction'],'chat')
        self.assertEqual(model.call_count,2)
        self.assertTrue(record['citation_errors'])
        self.assertIn('Insufficient evidence',record['answer'])

    def test_chat_line_selection_keeps_exact_original_provenance(self):
        passages=wiki.retrieve('assistance games')
        records,lookup=wiki.chat_lines(passages)
        self.assertTrue(lookup)
        for line in lookup.values():
            original=(wiki.ROOT/line['path']).read_text().splitlines()
            self.assertEqual(line['quote'],original[line['line_number']-1])
            self.assertFalse(line['quote'].lstrip().startswith('#'))
        selected=next(iter(lookup))
        resolved=wiki.resolve_chat_lines({'insufficient_evidence':False,'claims':[{'text':'Control-flow test','supports':[{'line_id':selected}]}]},lookup)
        self.assertFalse(wiki.assess_claims(resolved,passages)[2])
        bad=wiki.resolve_chat_lines({'insufficient_evidence':False,'claims':[{'text':'Control-flow test','supports':[{'line_id':'L999999'}]}]},lookup)
        self.assertTrue(wiki.assess_claims(bad,passages)[2])

    def test_unavailable_repair_still_retains_initial_evidence(self):
        bad=json.dumps({'insufficient_evidence':False,'claims':[{'text':'Unsupported','supports':[{'source_id':'Pmissing','quote':'Missing evidence'}]}]})
        with patch.object(wiki,'generate',side_effect=[(bad,{}),RuntimeError('Local model unavailable')]):
            record=wiki.ask('alignment')
        self.assertIn('Insufficient evidence',record['answer'])
        self.assertEqual(record['citation_validation_attempts'][0]['raw_model_answer'],bad)
        self.assertIn('repair_error',record['citation_validation_attempts'][1])
        self.assertTrue(record['citation_errors'])

    def test_generated_evidence_cannot_enter_vault(self):
        with self.assertRaisesRegex(ValueError, 'outside the Obsidian vault'):
            wiki.save_record({'interaction':'search'},wiki.ROOT/'vault/raw/generated-test.json')
        self.assertFalse((wiki.ROOT/'vault/raw/generated-test.json').exists())

    def test_stale_source_rejected(self):
        original_read = wiki.read_json
        with patch.object(wiki,'read_json',side_effect=lambda p, default=None: {} if p.name == 'index-manifest.json' else original_read(p, default)):
            with self.assertRaisesRegex(RuntimeError,'changed since indexing'):
                wiki.retrieve('budget')

if __name__=='__main__': unittest.main()
