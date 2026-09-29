from pathlib import Path
import json, re, statistics, hashlib
B=Path(__file__).resolve().parent
R=B/'isolated-first'
load=lambda p:json.loads(p.read_text())
expected=load(B/'expectations.json'); mechanical=load(R/'mechanical-case-assessment.json')
assessment=[]
for case,observed in zip(expected['cases'],mechanical):
    if case['id']=='B05-two-source':
        verdict='PARTIAL'
        coverage=[{'claim':case['expected_claims'][0],'status':'PARTIAL','reason':'Western/English skew is stated; lack of consensus is omitted.'},{'claim':case['expected_claims'][1],'status':'PASS','reason':'Manipulability and external preference shaping are explicitly stated.'},{'claim':case['expected_claims'][2],'status':'FAIL','reason':'Conflicting interests among multiple humans are omitted although retrieved passage Pd36e317f50b9 includes the point.'}]
        reason='Both expected sources retrieved; all four answer claims are entailed by exact cited quotes. Completeness fails the full frozen expectation.'
    else:
        verdict='PASS';coverage=[{'claim':x,'status':'PASS'} for x in case['expected_claims']]
        reason='Every predeclared expected point is answered and materially supported by its cited quote.' if case['required_passages'] else 'Explicit insufficient-evidence response with no fabricated schedule or citations.'
    assessment.append({'id':case['id'],'question':case['question'],'verdict':verdict,'retrieval_verdict':'PASS' if case['required_passages'] else 'EXPECTED_NO_ANSWER_IN_SOURCES','citation_semantic_support':'PASS' if case['required_passages'] else 'NOT_APPLICABLE','coverage':coverage,'reason':reason,'confidence':'high','record':f'isolated-first/records/{case["id"]}.json'})
chat=[load(p) for p in sorted((R/'chat').glob('*.json'))]
draft_words=len(chat[2]['answer'].split());short_words=len(chat[3]['answer'].split())
reingest=load(R/'reingestion-assessment.json');prooffirst=load(B/'isolation-first/run.json');proofrestart=load(B/'isolation-restart/run.json')
records=[load(p) for p in (R/'records').glob('*.json')]+[load(p) for p in (R/'restart-check/records').glob('*.json')]
generations=[]
for x in records+chat:
 if 'generation' in x:generations.append(x['generation'])
 for y in x.get('results',[]):
  if 'generation' in y:generations.append(y['generation'])
asktimes=[x['generation']['metrics']['wall_seconds'] for x in records if x.get('interaction')=='ask']
checks={
 'main_research_cases':'4/4 PASS (3 answerable plus 1 missing evidence)',
 'additional_cross_source_case':'PARTIAL; grounded but incomplete',
 'capability_chat':{'verdict':'PASS','retrieval_called':[x['retrieval_called'] for x in chat[:2]],'model_calls':[x['model_calls'] for x in chat[:2]],'origin':'Explicit deterministic harness capability contract, not Gemma generation'},
 'draft_followup':{'verdict':'PASS','draft_words':draft_words,'shorter_words':short_words,'both_suggestion_label':all(x['answer'].startswith('Suggestion:') for x in chat[2:4]),'both_skip_retrieval':all(not x['retrieval_called'] for x in chat[2:4]),'same_subject':'one-page study guide; extract, condense, structure'},
 'notes_chat':{'verdict':'PASS_FOR_PREDECLARED_MODE_CRITERION','retrieval_called':chat[4]['retrieval_called'],'citation_ids':chat[4]['citations'],'material_claims_supported':True,'additional_observation':'Chooses reward-model limitations as its second broad obstacle and omits Western/English skew. Main fixed ask handles both expected obstacles exactly.'},
 'ask_chat_isolation':{'verdict':'PASS','chat_hypothetical_acknowledged':True,'standalone_ask':load(R/'records/B04-after-chat.json')['answer'],'hypothetical_search_passages':len(load(R/'records/chat-fact-not-indexed.json')['passages'])},
 'search_and_model_unavailable':load(B/'no-model-direct/assessment.json'),
 'reingestion':{'verdict':'PASS','originals_unchanged':reingest['originals_unchanged'],'same_note_paths':reingest['same_note_paths'],'notes_byte_identical':reingest['notes_byte_identical'],'model_calls_on_repeat':0},
 'fresh_server_persistence':{'verdict':'PASS','first_pid':prooffirst['server_pid'],'second_pid':proofrestart['server_pid'],'distinct_pids':prooffirst['server_pid']!=proofrestart['server_pid'],'first_answer_equals_restarted_answer':load(R/'records/B01-values.json')['answer']==load(R/'restart-check/records/B01-after-server-restart.json')['answer'],'both_servers_fresh_then_stopped':all(x['server_launched_fresh'] and x['server_stopped_after_run'] for x in [prooffirst,proofrestart]),'post_cleanup_port11435_connect_errno':61},
 'model':{'actual_generation_count':len(generations),'identity':generations[0]['identity'],'all_same_model_digest':len({x['identity']['digest'] for x in generations})==1,'all_local_loopback':all(x['identity']['endpoint']=='http://127.0.0.1:11435' for x in generations),'ask_count':len(asktimes),'ask_latency_seconds':{'min':min(asktimes),'max':max(asktimes),'median':statistics.median(asktimes)},'latest_loaded_allocation_bytes':generations[-1]['metrics'].get('loaded_models',[{}])[0].get('size'),'runtime_rss_unavailable':all(x['metrics'].get('runtime_rss_after',{}).get('available') is False for x in generations)}
}
(B/'semantic-assessment.json').write_text(json.dumps({'cases':assessment,'checks':checks},indent=2,ensure_ascii=False)+'\n')
report=f'''# Independent evaluator B — completed runtime review

**Result:** all four principal research tests pass: three answerable questions produce supported cited answers, and the missing-evidence question abstains. The additional two-source stress case is **PARTIAL** because it omits expected points despite retrieving them. Confidence is **high for these observed tests**, **moderate for similar questions**, and **unknown for broad reliability**.

## Independence and execution scope

Questions, expected claims and verbatim source passages were frozen in [expectations.json](expectations.json) before reading implementation or README. The [hash](expectations.sha256) remains unchanged. Only assignment and original-source contents informed question selection. Directory inventory exposed earlier evidence filenames but no existing evaluation contents were read. No evaluator A outputs were read. No harness or source files were edited by this evaluator, and no stubs or alternative models were used.

Privacy cleanup renamed one raw source. [Reconciliation](privacy-source-reconciliation.json) verifies that every frozen expected technical passage remains byte-for-byte present under the disclosed alias. Test intent and expected answers were not changed after observing results.

The evaluator copied only code, prompts, catalog and raw sources into its own clean [workspace](isolated-first/workspace/), initially with no index or wiki pages. All expectations and output records remained outside the searchable vault. There were **24 main CLI commands, 2 direct deny-all checks, and 1 fresh-server restart check**. The CLI and real Ollama server were both OS-isolated from external networking while loopback remained available. This is **process-level external-network denial**, not physical Wi-Fi disconnection; Wi-Fi stayed on.

Actual model: **{generations[0]['identity']['name']}**, **Q4_0**, Ollama **{generations[0]['identity']['runtime']['version']}**, digest `{generations[0]['identity']['digest']}`. All **{len(generations)} actual generations** used this model at the isolated loopback endpoint. Two capability responses came from the explicitly labelled deterministic harness contract and are not counted as model generations.

## Fixed research results

| Case | Retrieval | Answer and citation assessment |
|---|---|---|
| [B01: value-alignment obstacles](isolated-first/records/B01-values.md) | PASS | PASS: Western/English skew and lack of consensus; both exact quotes support the claims. |
| [B02: mountaintop paraphrase](isolated-first/records/B02-mountaintop.md) | PASS | PASS: agency matters beyond outcome, and removing non-optimal choices violates autonomy. |
| [B03: ICAO/IMO versus IAEA](isolated-first/records/B03-oversight.md) | PASS | PASS: regulator oversight versus direct inspection; stronger powers are politically harder. It answers what the notes say, without asserting enacted AI inspection law. |
| [B04: next-workshop schedule](isolated-first/records/B04-next-workshop.md) | Expected absence | PASS: explicitly insufficient evidence; no invented date, time or room. |
| [B05: cultural skew plus preference manipulation](isolated-first/records/B05-two-source.md) | PASS, both sources | PARTIAL: every generated claim is grounded, but lack of consensus and conflicting interests among multiple humans are omitted despite appearing in retrieved context. |

This separates retrieval success from answer completeness. B05 is not a citation failure or hallucination; it is a failure to cover the full independently frozen expectation. No setting was changed and no favorable replacement result was substituted. [Claim-by-claim assessments](semantic-assessment.json) preserve the distinction.

## Mode boundaries and persistence

- Both exact capability checks pass without retrieval, unrelated citations, or an insufficient-evidence response. They accurately describe supported capabilities and limitations.
- Real Gemma drafting and `make that shorter` pass. Output falls from **{draft_words} to {short_words} words**, retains extract/condense/structure for a one-page guide, labels the proposal Suggestion, and skips retrieval. [Chat records](isolated-first/chat/)
- Notes chat retrieves originals and gives supporting citation IDs. Its second broad obstacle is reward-model limitations rather than the Western/English-skew point used by the fixed ask; this is a framing/completeness observation, not a retroactively invented test failure.
- An explicitly hypothetical date/time/room inserted only into chat does not become source evidence. The subsequent standalone ask abstains, and searching the distinctive room label returns no passages. [Separation evidence](isolated-first/records/B04-after-chat.md)
- Exact assignment-style `search "workshop location"` returns original passages with no synthesized answer; `ask "Where is the workshop?" --mode local` correctly abstains for this corpus.
- Search succeeds under an OS profile denying **all networking including loopback**, returning two exact original passages with zero model calls. Ask under the same profile fails with a useful local-Ollama-unavailable/EPERM error and no cloud fallback. [Direct denial assessment](no-model-direct/assessment.json)
- Initial missing-index search, missing ingestion directory, and unsupported online mode each produce explicit errors. These intentional negative outcomes are retained in [command logs](isolated-first/commands/).
- Fresh `ingest ./vault/raw` makes six readable notes and an eight-passage index using six real generations, in **{load(R/'records/fresh-ingest.json')['wall_seconds']:.3f} seconds**. [Ingestion](isolated-first/records/fresh-ingest.md)
- Re-ingestion makes no model calls, creates no duplicates, leaves all original bytes and all six note bytes unchanged, and preserves the same note paths. [Hash audit](isolated-first/reingestion-assessment.json)
- All six filenames are readable and match their first headings; internal/source links resolve unambiguously, topic index and source catalog exist, and machine files remain outside the vault. Freshly generated pages are correctly pending review; this test does not pretend generation itself supplies editorial review.
- Fresh CLI processes read the persisted index successfully. A second isolated model server with a different PID loads the local weights and reproduces B01's grounded answer using the same persisted workspace. Both servers are stopped afterward and port 11435 was verified closed. [Restart response](isolated-first/restart-check/records/B01-after-server-restart.md)

## Offline proof and measurements

The first and restart launches preserve server-side probes, client probes before/after, sandbox-profile hashes and fresh-server lifecycle records: [first run](isolation-first/) and [restart](isolation-restart/). External probes fail with EPERM; loopback succeeds. The evaluator also independently required IPv4/IPv6 TCP/UDP denial before inference. [Inherited-policy check](isolated-first/inherited-isolation-check.json)

Model calls report local identity, digest, prompts, raw responses, token counts and timing. Across {len(asktimes)} actual asks, recorded model-call latency spans **{min(asktimes):.3f}–{max(asktimes):.3f} seconds**, median **{statistics.median(asktimes):.3f} seconds**. These are sequential observations, not a controlled performance benchmark. The restarted answer reports a **3,734,492,937-byte runtime model allocation** at 8,192 context. Process RSS is unavailable inside this sandbox and should not be reported as a measured value for this run. Runtime allocation is not total application or peak unified-memory use.

## Assignment and README audit boundaries

The runtime portions independently verified here cover local Gemma, fresh ingestion, separate modes, original-source retrieval/citation fidelity, three supported asks, one unsupported ask, source isolation, re-ingestion and restart persistence. Installation/download of Ollama and weights was not repeated; local availability was tested under external-network denial.

The README read after expectation freeze was still an older working draft. It contained a stale renamed source link, old unchanged-originals/provenance wording, a fixed-port claim, prior resource measurements, and pending Wi-Fi-disconnection language. The parent is rewriting it; those observations are not claims about its eventual final version. Final documentation must distinguish sanitized source baselines from historical originals and process isolation from physical disconnection, link this run's evidence, and include B05's observed limitation.

Existing screenshots, prior evals, prior evidence cards and evaluator A's results were deliberately not used in this independent evaluation. Consequently **current Obsidian GUI navigation/screenshots, final README link integrity, signed-out public-repository accessibility and portal submission are not certified by this report**. No publication or submission occurred in this evaluator.

One observed ingestion limitation remains visible: the fresh Alignment and Interpretability draft omits the requested Useful details section and phrases the individual-alignment point awkwardly. Other generated drafts sometimes present discussion claims as declarative statements. The pages remain pending review, appropriately; editorial checking is still required before treating these fresh drafts as final wiki notes.

A concrete next improvement is to test answer coverage against each requested subquestion, alongside existing citation checks. B05 demonstrates why quote-valid claims alone do not ensure a complete answer. Evaluate such a change on this unchanged test and additional held-out cases, preserving the initial partial result.
'''
(B/'REPORT.md').write_text(report)
print(json.dumps({'report':'REPORT.md','model_generations':len(generations),'ask_count':len(asktimes),'draft_words':draft_words,'shorter_words':short_words,'cases':[{'id':x['id'],'verdict':x['verdict']} for x in assessment]},indent=2))
