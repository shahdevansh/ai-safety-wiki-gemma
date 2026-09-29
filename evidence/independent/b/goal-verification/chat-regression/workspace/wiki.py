#!/usr/bin/env python3
"""Pip: a standard-library-only local Gemma CLI and inspectable RAG harness."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import resource
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / '.state'
MODEL = 'gemma4:e2b-it-qat'
PORT = int(os.environ.get('WIKI_PORT', '11434'))
if not 1024 <= PORT <= 65535:
    raise ValueError('WIKI_PORT must be an unprivileged local port.')
API = f'http://127.0.0.1:{PORT}'  # Host is fixed; a remote endpoint is never accepted.
STOP = set('a an and are as at be been by can did do does each for from had has have how i in is it me my of on or our should that the their them they this to was we were what when which who why will with would you your were many new between about were much'.split())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    tmp.replace(path)


def request(endpoint, data=None):
    # Ignore all proxy environment variables: inference must remain on loopback.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    req = urllib.request.Request(API + endpoint,
        data=None if data is None else json.dumps(data).encode(),
        headers={'Content-Type': 'application/json'})
    try:
        with opener.open(req, timeout=180) as response:
            return json.load(response)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f'Local Ollama unavailable: {exc}. Start Ollama; run ollama pull {MODEL} while online. No cloud fallback.') from exc


def model_identity():
    model = next((m for m in request('/api/tags')['models'] if m['name'] == MODEL), None)
    if not model:
        raise RuntimeError(f'Model missing locally. While online, run: ollama pull {MODEL}')
    if model.get('remote_host') or model.get('remote_model'):
        raise RuntimeError('Remote model refused; only downloaded local weights are allowed.')
    return {'name': MODEL, 'digest': model['digest'], 'details': model['details'],
            'download_bytes': model['size'], 'runtime': request('/api/version'), 'endpoint': API}


def runtime_rss():
    """Snapshot only the isolated server tree when its parent PID is provided."""
    try:
        lines = subprocess.check_output(['ps','-axo','pid=,ppid=,rss=,comm='], text=True).splitlines()
        all_rows = []
        for line in lines:
            parts=line.strip().split(None,3)
            if len(parts)==4:
                all_rows.append({'pid':int(parts[0]),'parent':int(parts[1]),'rss_bytes':int(parts[2])*1024,'process':Path(parts[3]).name,'command':parts[3]})
        root_pid = int(os.environ.get('WIKI_SERVER_PID','0'))
        if root_pid:
            family={root_pid}
            for _ in range(8):
                family |= {r['pid'] for r in all_rows if r['parent'] in family}
            rows=[r for r in all_rows if r['pid'] in family]
            scope='Isolated Ollama server and descendants after generation; summed RSS may double-count shared pages, not peak unified GPU memory.'
        else:
            rows=[r for r in all_rows if '/Ollama.app/' in r['command']]
            scope='Desktop Ollama processes after generation; summed RSS may double-count shared pages, not peak unified GPU memory.'
        for row in rows:row.pop('command')
        return {'available':True,'processes':rows,'summed_rss_bytes':sum(r['rss_bytes'] for r in rows),'scope':scope}
    except (OSError,subprocess.SubprocessError,ValueError):
        return {'available':False}


def generate(messages, structured=False, max_tokens=650, schema=None):
    identity = model_identity()
    payload = {'model': MODEL, 'messages': messages, 'stream': False, 'think': structured,
               'keep_alive': '10m', 'options': {'num_ctx': 8192, 'num_predict': max_tokens,
                                              'temperature': 0, 'seed': 42}}
    if structured:
        payload['format'] = schema or 'json'
    started = time.perf_counter()
    response = request('/api/chat', payload)
    metrics = {'wall_seconds': round(time.perf_counter() - started, 3),
               'cli_peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               'loaded_models': request('/api/ps').get('models', []),
               'runtime_rss_after': runtime_rss(),
               **{k: response.get(k) for k in ('total_duration', 'load_duration', 'prompt_eval_count', 'prompt_eval_duration', 'eval_count', 'eval_duration', 'done_reason')}}
    if response.get('done_reason') == 'length':
        raise RuntimeError('Gemma hit the output limit; result is incomplete. Shorten context or increase num_predict.')
    return response['message']['content'].strip(), {'identity': identity, 'metrics': metrics, 'request': payload, 'response': response}


def catalog():
    entries = read_json(ROOT / 'sources.json')
    names = set()
    for e in entries:
        path = ROOT / e['path']
        if path.is_symlink() or not path.resolve().is_relative_to((ROOT / 'vault/raw').resolve()):
            raise ValueError('Source paths must be ordinary files inside vault/raw.')
        if path.suffix not in {'.md', '.txt'} or not path.is_file():
            raise ValueError(f'Missing or unsupported source: {e["path"]}')
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9 -]{2,60}', e['title']) or '/' in e['folder'] or '..' in e['folder']:
            raise ValueError('Use short readable titles and a single topic folder.')
        if e['title'].casefold() in names:
            raise ValueError('Duplicate wiki title; choose a meaningful qualifier.')
        names.add(e['title'].casefold())
    return entries


def chunks(entry):
    """Contiguous original lines, approximately 1,500 characters, 3-line overlap."""
    raw = (ROOT / entry['path']).read_text()
    lines = raw.splitlines(keepends=True)
    start = 0
    section = entry['title']
    while start < len(lines):
        end = start
        length = 0
        while end < len(lines) and (length < 1500 or end == start):
            length += len(lines[end]); end += 1
        text = ''.join(lines[start:end])
        for line in lines[:start + 1]:
            if line.startswith('#'):
                section = line.lstrip('# ').strip()
        if text.strip():
            key = digest((entry['path'] + str(start) + text).encode())[:12]
            yield {'id': 'P' + key, 'path': entry['path'], 'title': entry['title'],
                   'section': section, 'line_start': start + 1, 'line_end': end, 'text': text,
                   'source_sha256': digest((ROOT / entry['path']).read_bytes())}
        if end == len(lines):
            break
        start = max(start + 1, end - 3)


def rebuild():
    STATE.mkdir(exist_ok=True)
    rows = list({c['id']: c for entry in catalog() for c in chunks(entry)}.values())
    db = sqlite3.connect(STATE / 'index.sqlite3')
    with db:
        db.execute('DROP TABLE IF EXISTS passages')
        db.execute("CREATE VIRTUAL TABLE passages USING fts5(id UNINDEXED, path UNINDEXED, title, section, text, metadata UNINDEXED, tokenize='porter unicode61')")
        for c in rows:
            db.execute('INSERT INTO passages VALUES (?,?,?,?,?,?)',
                       (c['id'], c['path'], c['title'], c['section'], c['text'], json.dumps(c)))
    db.close()
    write_json(STATE / 'index-manifest.json', {e['path']: digest((ROOT / e['path']).read_bytes()) for e in catalog()})
    return len(rows)


def retrieve(query, top_k=4):
    if not (STATE / 'index.sqlite3').exists():
        raise RuntimeError('No index. Run ./wiki ingest or ./wiki reindex first.')
    current = {e['path']: digest((ROOT / e['path']).read_bytes()) for e in catalog()}
    if current != read_json(STATE / 'index-manifest.json'):
        raise RuntimeError('Original sources changed since indexing. Run ./wiki reindex; review changed wiki pages.')
    terms = sorted(set(re.findall(r'[a-z0-9]+', query.lower())) - STOP)
    if not terms:
        return []
    match = ' OR '.join('"' + t + '"' for t in terms)
    db = sqlite3.connect(STATE / 'index.sqlite3')
    rows = db.execute('SELECT metadata, bm25(passages,0,0,2,1.5,1,0) FROM passages WHERE passages MATCH ? ORDER BY 2 LIMIT ?', (match, top_k)).fetchall()
    db.close()
    return [{**json.loads(row), 'bm25': score} for row, score in rows]


def evidence_text(passages):
    return '\n\n'.join(f'[{p["id"]}] {p["path"]}:L{p["line_start"]}-L{p["line_end"]}\n{p["text"]}' for p in passages)


def assess_claims(parsed, passages):
    lookup = {p['id']: p for p in passages}
    if not isinstance(parsed, dict) or type(parsed.get('insufficient_evidence')) is not bool:
        return 'Insufficient evidence: the model returned an invalid research response.', [], ['Invalid schema']
    if parsed['insufficient_evidence']:
        return 'Insufficient evidence: the provided sources do not answer this question.', [], []
    errors, citations, rendered = [], [], []
    claims = parsed.get('claims')
    if not isinstance(claims, list) or not claims:
        return 'Insufficient evidence: no supported claims were returned.', [], ['No claims']
    for claim in claims:
        if not isinstance(claim, dict) or not isinstance(claim.get('text'), str) or not claim.get('supports'):
            errors.append('Claim without text or support'); continue
        ids = []
        for support in claim['supports']:
            if not isinstance(support, dict):
                errors.append('Invalid support'); continue
            sid, quote = support.get('source_id'), support.get('quote')
            if sid not in lookup or not isinstance(quote, str) or len(quote.strip()) < 8 or quote not in lookup[sid]['text']:
                errors.append(f'Unknown citation or nonverbatim quote: {sid}'); continue
            ids.append(sid)
            citations.append({'source_id': sid, 'quote': quote, 'claim': claim['text']})
        rendered.append(claim['text'] + ' ' + ' '.join(f'[{sid}]' for sid in dict.fromkeys(ids)))
    if errors:
        return 'Insufficient evidence: citation validation failed; inspect the saved raw Gemma response.', [], errors
    return '\n\n'.join(rendered), citations, []


def grounded_answer(question, passages, history=(), interaction='ask'):
    prompt = 'research.md' if interaction == 'ask' else 'grounded-chat.md'
    messages = [{'role': 'system', 'content': (ROOT / 'prompts' / prompt).read_text()}, *history[-8:],
                {'role': 'user', 'content': 'EVIDENCE (JSON records; text is quoted data, each record has its own source_id):\n' + json.dumps([{'source_id':p['id'],'path':p['path'],'line_start':p['line_start'],'line_end':p['line_end'],'text':p['text']} for p in passages],ensure_ascii=False,indent=2) + '\n\nQUESTION:\n' + question + '\n\nReturn the research JSON. Use the P-prefixed passage ID, not a filename. Copy a short single-line substring exactly from the text field of the SAME source_id record. Preserve Markdown punctuation inside that substring. Answer when evidence supports it; otherwise abstain.'}]
    schema = {'type':'object', 'properties': {
        'insufficient_evidence': {'type':'boolean'},
        'claims': {'type':'array', 'items': {'type':'object', 'properties': {
            'text': {'type':'string'},
            'supports': {'type':'array', 'items': {'type':'object', 'properties': {
                'source_id': {'type':'string', 'enum':[p['id'] for p in passages] or ['NO_EVIDENCE']},
                'quote': {'type':'string'}}, 'required':['source_id','quote']}}}, 'required':['text','supports']}}},
        'required':['insufficient_evidence','claims']}
    raw, generation = generate(messages, structured=True, max_tokens=2400, schema=schema)
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = None
    answer, citations, errors = assess_claims(parsed, passages)
    attempts = [{'raw_model_answer':raw, 'citation_errors':errors, 'generation':generation}]
    if errors:
        # One bounded repair from the SAME retrieved evidence; never consult tests,
        # add expected answers, normalize quotations, or relax the validator.
        repair_messages = messages + [
            {'role':'assistant', 'content':raw},
            {'role':'user', 'content':'Citation validation failed: ' + json.dumps(errors) +
             '. Re-read the unchanged EVIDENCE above. Correct the source IDs and quotes. '
             'Copy a short contiguous substring from the SAME cited passage, preferably within one line. '
             'Do not remove Markdown inside a quote or join noncontiguous text. '
             'Return the complete research JSON for every supported part of the original question; '
             'if the claims are unsupported, abstain. Do not invent new evidence.'}]
        try:
            repaired_raw, repaired_generation = generate(repair_messages, structured=True, max_tokens=2400, schema=schema)
        except RuntimeError as exc:
            # Preserve the initial failed response even if local inference fails
            # during repair. The result stays closed and can still be saved.
            attempts.append({'repair_error':str(exc), 'citation_errors':errors})
        else:
            raw, generation = repaired_raw, repaired_generation
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                parsed = None
            answer, citations, errors = assess_claims(parsed, passages)
            attempts.append({'raw_model_answer':raw, 'citation_errors':errors, 'generation':generation})
    if citations:
        answer = 'According to the retrieved meeting notes:\n\n' + answer
    return {'interaction': interaction, 'execution': 'local', 'question': question, 'history_messages': len(history[-8:]),
            'retrieval_called': True, 'passages': passages, 'raw_model_answer': raw, 'answer': answer,
            'citations': citations, 'citation_errors': errors, 'generation': generation,
            'citation_validation_attempts': attempts,
            'assessment': 'Quote identity and source IDs checked automatically; semantic support requires reviewer assessment.'}


def ask(question):
    # Research always starts with empty conversation context.
    return grounded_answer(question, retrieve(question))


def capability_request(message):
    return bool(re.search(r'what can (we do|you help|you do)', message, re.I) or (
        re.search(r'\b(commands|capabilities|features|tools)\b', message, re.I)
        and re.search(r'\b(you|your)\b', message, re.I)
        and re.search(r'\b(what|which|list|show|support|available)\b', message, re.I)))


def needs_notes(message):
    """Retrieve for a source-dependent request, not a bare mention of the wiki."""
    if capability_request(message):
        return False
    reference = re.search(r'\b(notes|lecture|workshop|session|wiki|sources|corpus|assistance games|alignment|interpretability|governance|infrastructure|disempowerment|AI safety)\b', message, re.I)
    request_words = re.search(r'\b(what|why|how|when|where|which|who|explain|compare|summari[sz]e|describe|tell|find|search|according)\b', message, re.I)
    # Drafting uses conversation unless the user asks to draw on source material.
    drafting = re.search(r'\b(draft|brainstorm|plan|rewrite|shorter|shorten)\b', message, re.I)
    explicit_source = re.search(r'\b(according to|based on|using|from)\b.{0,25}\b(notes|wiki|sources|corpus)\b', message, re.I)
    return bool(reference and (explicit_source or (request_words and not drafting)))


def chat_turn(message, history, carried):
    if capability_request(message):
        answer = (ROOT / 'prompts/capabilities.md').read_text().strip()
        count = len(history[-8:])
        history.extend([{'role':'user','content':message}, {'role':'assistant','content':answer}])
        return {'interaction':'chat','execution':'local','question':message,'history_messages':count,
                'retrieval_called':False,'passages':[],'answer':answer,'citations':[],
                'citation_errors':[],'model_calls':0,'response_origin':'harness capability contract; no model generation'}, carried
    lookup = needs_notes(message)
    # Keep original evidence for referential follow-ups, not every later topic.
    followup = re.search(r'\b(that|those|it|they|them|shorter|shorten|elaborate)\b', message, re.I)
    new_topic = re.search(r'\b(unrelated|new topic|change (the )?subject|separately)\b', message, re.I)
    passages = retrieve(message) if lookup else (carried if followup and not new_topic else [])
    if lookup or passages:
        record = grounded_answer(message, passages, history, interaction='chat')
        record['retrieval_called'] = lookup
        history.extend([{'role':'user','content':message}, {'role':'assistant','content':record['answer']}])
        return record, passages
    system = (ROOT / 'prompts/persona.md').read_text()
    messages = [{'role': 'system', 'content': system}, *history[-8:], {'role': 'user', 'content': message}]
    raw, generation = generate(messages, max_tokens=650)
    cited = re.findall(r'\bP[a-f0-9]{12}\b', raw)
    errors = [c for c in cited if c not in {p['id'] for p in passages}]
    answer = raw if not errors else 'I could not verify the source labels in this response. Please try ask mode.'
    history.extend([{'role': 'user', 'content': message}, {'role': 'assistant', 'content': answer}])
    return {'interaction': 'chat', 'execution': 'local', 'question': message, 'history_messages': len(messages) - 2,
            'retrieval_called': lookup, 'passages': passages, 'raw_model_answer': raw, 'answer': answer,
            'citations': cited, 'citation_errors': errors, 'generation': generation}, passages


def ingest(force=False, only=None):
    started = time.perf_counter()
    manifest = read_json(STATE / 'wiki-manifest.json', {})
    outputs = []
    for entry in catalog():
        if only and entry['title'] != only:
            continue
        source = ROOT / entry['path']
        sha = digest(source.read_bytes())
        target = ROOT / 'vault/wiki' / entry['folder'] / (entry['title'] + '.md')
        previous = manifest.get(entry['title'], {})
        if target.exists() and not previous and ('source_sha256: ' + sha) in target.read_text():
            previous = {'source_sha256':sha, 'wiki_path':str(target.relative_to(ROOT)),
                        'reviewed':'review_status: reviewed' in target.read_text()}
            manifest[entry['title']] = previous
        if target.exists() and previous.get('source_sha256') == sha and not force:
            outputs.append({'path': str(target.relative_to(ROOT)), 'status': 'unchanged; reviewed edits preserved'})
            continue
        text = source.read_text()
        if entry.get('sections'):
            blocks = re.split(r'(?=^### )', text, flags=re.M)
            text = '\n'.join(b for b in blocks if any(b.startswith('### ' + heading) for heading in entry['sections']))
            if not text.strip():
                raise ValueError('No matching ingestion sections: ' + entry['title'])
        if len(text) > 20000:
            raise ValueError('Ingestion limit is 20,000 characters per source; split large documents by subject before registering them.')
        raw, generation = generate([{'role': 'system', 'content': (ROOT / 'prompts/ingest.md').read_text()},
                                    {'role': 'user', 'content': text}], max_tokens=600)
        source_ref = f'[[raw/{source.stem}|Original: {source.name}]]'
        content = f'---\nsource: {entry["path"]}\nsource_sha256: {sha}\nreview_status: pending\n---\n\n# {entry["title"]}\n\n{raw}\n\n## Source\n\n{source_ref}\n\n## Related notes\n\n'
        content += '\n'.join(f'- [[{r["title"]}]] — {r["reason"]}' for r in entry['related']) + '\n'
        if target.exists():
            backup = STATE / 'note-backups' / (datetime.now().strftime('%Y%m%dT%H%M%S%f') + '-' + target.name)
            backup.parent.mkdir(parents=True, exist_ok=True); backup.write_bytes(target.read_bytes())
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        manifest[entry['title']] = {'source_sha256': sha, 'wiki_path': str(target.relative_to(ROOT)), 'reviewed': False}
        outputs.append({'path': str(target.relative_to(ROOT)), 'source_sha256': sha, 'raw_model_answer': raw, 'generation': generation, 'status': 'generated; review required'})
    count = rebuild()
    write_json(STATE / 'wiki-manifest.json', manifest)
    index = '# AI Safety Wiki\n\nMy AI safety learning: concepts, governance, and human control. These pages summarize recorded meeting notes; they do not independently verify the speakers’ claims. Redacted source copies are frozen unchanged in raw/.\n\n'
    for folder in sorted({e['folder'] for e in catalog()}):
        index += '## ' + folder + '\n\n'
        index += '\n'.join(f'- [[{e["title"]}]] — {e["description"]}' for e in catalog() if e['folder'] == folder) + '\n\n'
    index += '## Trace the evidence\n\nFollow [[Assistance Games]] → [[Alignment and Interpretability]] → its original source. See [[Source Catalog]] for public source aliases, locations, and hashes. Generated suggestions and evaluation answers are outside this vault.\n'
    (ROOT / 'vault/index.md').write_text(index)
    cat = '# Source Catalog\n\nThree redacted meeting-summary bodies form the frozen public source corpus. Private originals remain local. These are secondary notes, not verbatim transcripts; claims may be incomplete or inaccurate. Identifying metadata, biographies, and personal follow-ups are omitted.\n\n'
    for path in dict.fromkeys(e['path'] for e in catalog()):
        entries = [e for e in catalog() if e['path'] == path]
        e = entries[0]
        cat += f'## {e["source_title"]}\n\n- Public source: redacted and frozen before ingestion\n- Original: [[raw/{Path(path).stem}]]\n- Wiki: ' + ', '.join('[[' + x['title'] + ']]' for x in entries) + f'\n- SHA-256: `{digest((ROOT / path).read_bytes())}`\n\n'
    (ROOT / 'vault/Source Catalog.md').write_text(cat)
    return {'interaction': 'ingest', 'execution': 'local', 'results': outputs, 'passage_count': count,
            'wall_seconds': round(time.perf_counter() - started, 3)}


def save_record(record, path=None):
    record['network_policy'] = os.environ.get('WIKI_NETWORK_POLICY', 'not-enforced-by-launcher')
    record['recorded_at_utc'] = datetime.now(timezone.utc).isoformat()
    record['source_hashes'] = {e['path']: digest((ROOT / e['path']).read_bytes()) for e in catalog()}
    dest = Path(path).resolve() if path else STATE / 'runs' / (datetime.now().strftime('%Y%m%dT%H%M%S%f') + '-' + record['interaction'] + '.json')
    if dest.is_relative_to((ROOT / 'vault').resolve()):
        raise ValueError('Generated evidence must be saved outside the Obsidian vault and original sources.')
    write_json(dest, record)
    md = f'# {record["interaction"].title()} evidence\n\nExecution: **local**. Recorded: {record["recorded_at_utc"]}.\n\n'
    if 'generation' in record:
        g = record['generation']; md += f'Model: `{g["identity"]["name"]}`; digest `{g["identity"]["digest"]}`. Wall time: {g["metrics"]["wall_seconds"]} s.\n\n'
    if 'question' in record:
        md += '## Input\n\n' + record['question'] + '\n\n'
    if 'answer' in record:
        md += '## Actual displayed result\n\n' + record['answer'] + '\n\n'
    if record.get('passages'):
        md += '## Retrieved original passages\n\n'
        for p in record['passages']:
            md += f'### [{p["id"]}] {p["path"]}:L{p["line_start"]}-L{p["line_end"]}\n\n```text\n{p["text"]}\n```\n\n'
    md += f'Full model request, raw response, metrics, and validation fields: [{dest.name}]({dest.name}).\n'
    dest.with_suffix('.md').write_text(md)
    return dest


def show(record):
    print(f'Pip | {record["interaction"]} | local | ' + (MODEL if record['interaction'] != 'search' else 'retrieval only; no model call'))
    if 'answer' in record:
        print('\n' + record['answer'])
    if record.get('passages'):
        print('\nOriginal evidence:')
        print(evidence_text(record['passages']))
    if record['interaction'] == 'search' and not record['passages']:
        print('No matching original passages. Try another keyword.')
    if record['interaction'] == 'ingest':
        for r in record['results']:
            print(f'{r["path"]}: {r["status"]}')
        print(f'{record["passage_count"]} passages indexed; {record["wall_seconds"]} s')
    if 'generation' in record:
        print(f'\nModel time: {record["generation"]["metrics"]["wall_seconds"]} s')


def main(argv=None):
    parser = argparse.ArgumentParser(description='Pip: local Gemma personal wiki. No cloud fallback; Python standard library only.')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('help', help='Show commands')
    sub.add_parser('doctor', help='Inspect local model and device')
    sub.add_parser('reindex', help='Rebuild original-source retrieval without calling Gemma')
    p = sub.add_parser('ingest', help='Generate wiki drafts and index registered originals')
    p.add_argument('source_dir', nargs='?', default='./vault/raw', help='Registered original-source folder (default ./vault/raw)')
    p.add_argument('--mode', choices=['local'], default='local')
    p.add_argument('--only', choices=[e['title'] for e in catalog()], help='Ingest one registered topic')
    p.add_argument('--force', action='store_true', help='Regenerate pages; preserve previous versions in .state/note-backups')
    p.add_argument('--save', help='Save reviewable evidence JSON and Markdown')
    p = sub.add_parser('review', help='Explicitly mark a checked wiki page as reviewed')
    p.add_argument('title')
    for name in ('ask', 'search'):
        p = sub.add_parser(name, help='Independent grounded answer' if name == 'ask' else 'Original passages; no model call')
        p.add_argument('question'); p.add_argument('--save'); p.add_argument('--mode', choices=['local'], default='local')
    p = sub.add_parser('chat', help='Conversational assistant; /exit to end, /reset to clear history')
    p.add_argument('--script', help='Local text file, one turn per line; used for reproducible demonstrations')
    p.add_argument('--save-dir', help='Explicit directory for transcript evidence; default stays private in .state')
    args = parser.parse_args(argv)
    if args.command == 'help':
        parser.print_help(); return
    if args.command == 'doctor':
        print(json.dumps({'model': model_identity(), 'python': sys.version,
                         'device': subprocess.check_output(['system_profiler', 'SPHardwareDataType', 'SPDisplaysDataType'], text=True).split('Serial Number')[0]}, indent=2)); return
    if args.command == 'reindex':
        print(f'{rebuild()} original passages indexed; no model called.'); return
    if args.command == 'review':
        e = next((e for e in catalog() if e['title'] == args.title), None)
        if not e: raise ValueError('Unknown title')
        target = ROOT / 'vault/wiki' / e['folder'] / (e['title'] + '.md')
        target.write_text(target.read_text().replace('review_status: pending', 'review_status: reviewed'))
        manifest = read_json(STATE / 'wiki-manifest.json', {})
        manifest[e['title']]['reviewed'] = True
        manifest[e['title']]['reviewed_page_sha256'] = digest(target.read_bytes())
        write_json(STATE / 'wiki-manifest.json', manifest)
        print('Recorded explicit review: ' + args.title); return
    if args.command == 'chat':
        history, carried = [], []
        turns = Path(args.script).read_text().splitlines() if args.script else None
        print('Pip | chat | local | ' + MODEL + '\n/exit to end; /reset clears conversation. Chat never becomes searchable source evidence.')
        i = 0
        while True:
            if turns is not None:
                if i >= len(turns): break
                message = turns[i]; print('You> ' + message)
            else:
                try: message = input('You> ')
                except (EOFError, KeyboardInterrupt): break
            if message == '/exit': break
            if message == '/reset':
                history, carried = [], []
                i += 1
                continue
            if not message.strip():
                i += 1; continue
            record, carried = chat_turn(message, history, carried)
            show(record)
            save_record(record, Path(args.save_dir) / f'chat-{i+1:02d}.json' if args.save_dir else None)
            i += 1
        return
    if args.command == 'ingest':
        supplied = Path(args.source_dir).resolve()
        if supplied != (ROOT / 'vault/raw').resolve():
            raise ValueError('Ingest expects ./vault/raw. Register original files in sources.json first.')
        record = ingest(args.force, args.only)
    elif args.command == 'ask': record = ask(args.question)
    else: record = {'interaction': 'search', 'execution': 'local', 'question': args.question,
                   'passages': retrieve(args.question), 'model_calls': 0, 'retrieval_called': True}
    show(record)
    saved = save_record(record, args.save)
    print('\nSaved: ' + (saved.relative_to(ROOT).as_posix() if saved.is_relative_to(ROOT) else saved.name))


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, ValueError, OSError, sqlite3.Error, KeyError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)
