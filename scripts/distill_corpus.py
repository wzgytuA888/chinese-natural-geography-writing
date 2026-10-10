"""Measure a private PDF corpus; export only aggregate statistics and bibliography.

Python 3.10+, PyMuPDF. Raw text stays in --cache, outside the skill repository.
Sentence metrics describe extracted prose, not a normative writing target.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import io
import csv
from datetime import date
import json
import os
from pathlib import Path
import re
import statistics
import unicodedata
import zipfile

import pymupdf

TERMS = ['而', '但', '但是', '因此', '同时', '由于', '进一步', '随着', '此外', '进而',
         '然而', '一方面', '另一方面', '结果表明', '结果显示', '表明', '呈现', '影响',
         '驱动', '导致', '决定', '证明', '证实', '显著', '不确定性', '权衡', '协同',
         '高值区', '低值区', '尺度', '阈值', '供需', '服务流']
METHODS = ['InVEST', 'PLUS', 'FLUS', 'SWAT', 'WRF', 'ARIES', 'Budyko', 'Kappa',
           'NSE', '地理探测器', '随机森林', 'XGBoost', '结构方程', '地理加权回归',
           'Mann-Kendall', '自组织', '电路理论', '袋状图', '约束线', '耦合协调']
HAN = re.compile(r'[\u4e00-\u9fff]')
HEADING = re.compile(r'^([1-9](?:[.．]\d{1,2})*)\s+(.{2,60})$')
FONT_MAP = json.loads(Path(__file__).with_name('ecology-font-map.json').read_text(encoding='utf-8'))['mapping']


def canonical(text):
    # Certain legacy journal ToUnicode maps use Yi characters for punctuation.
    text=text.translate(str.maketrans({'ꎬ':',','ꎮ':'。','ꎻ':';','ꎺ':':','￣':'—'}))
    return unicodedata.normalize('NFKC', text).replace('\r', '')


def page_blocks(page):
    """Read two-column paragraphs column-wise within full-width heading bands."""
    blocks = []
    for b in page.get_text('dict')['blocks']:
        if 'lines' not in b: continue
        lines = []
        for line in b['lines']:
            texts = []
            for span in line['spans']:
                text=span['text']
                if span['font'].startswith('E-'):
                    text=''.join(FONT_MAP.get(c,c) for c in text)
                texts.append(text)
            lines.append(''.join(texts))
        text='\n'.join(lines)
        if text.strip(): blocks.append((*b['bbox'],text,len(blocks),0))
    width = page.rect.width
    full = sorted([b for b in blocks if b[2]-b[0] > width*.64], key=lambda b: b[1])
    narrow = [b for b in blocks if b not in full]
    out = []
    lower = -1
    for anchor in full + [None]:
        upper = anchor[1] if anchor else float('inf')
        band = [b for b in narrow if lower <= b[1] < upper]
        right = [b for b in band if b[0] > width*.46]
        left = [b for b in band if b not in right]
        # A right column requires substantial Chinese prose, not a page number.
        two_columns = any(len(HAN.findall(b[4])) > 60 for b in right)
        ordered = sorted(left, key=lambda b: (b[1],b[0])) + sorted(right,key=lambda b:(b[1],b[0])) if two_columns else sorted(band,key=lambda b:(b[1],b[0]))
        out.extend(ordered)
        if anchor:
            out.append(anchor)
            lower = upper
    return [canonical(b[4]) for b in out]


def classify_heading(title):
    if '讨论' in title and '结果' in title: return 'results_discussion'
    if '讨论' in title: return 'discussion'
    if '结论' in title or '结语' in title: return 'conclusion'
    if '结果' in title or '分析' in title: return 'results'
    if '引言' in title or title == '前言': return 'introduction'
    if any(x in title for x in ['方法', '数据', '研究区', '资料']): return 'methods'
    return None


def measure_text(text):
    # Count terms in Chinese-containing sentences only; omit English references.
    sentences = []
    for s in re.split(r'[。！？]', text):
        s = re.sub(r'\s+', '', s)
        n = len(HAN.findall(s))
        if 15 <= n and 20 <= len(s) <= 400 and n/len(s) >= .45:
            sentences.append(s)
    prose = '\n'.join(sentences)
    chars = len(HAN.findall(prose))
    return {'sentences': len(sentences), 'sentence_lengths': [len(s) for s in sentences],
            'han_chars': chars, 'terms': {t: prose.count(t) for t in TERMS}}


def extract_one(job):
    archive, entry, metadata, cache = job
    ident = metadata['paper_id']
    with zipfile.ZipFile(archive) as z:
        raw = z.read(entry)
    pdf_hash = hashlib.sha256(raw).hexdigest()
    with pymupdf.open(stream=raw, filetype='pdf') as doc:
        pages = [{'pdf_page':i+1, 'blocks':page_blocks(p)} for i,p in enumerate(doc)]
        legacy_fonts=any('E-' in f[3] for p in doc for f in p.get_fonts())
    # Drop repeated page-edge boilerplate only; keep real mid-page headings.
    edges = Counter()
    for p in pages:
        b = p['blocks']
        if b:
            for x in {b[0].strip(),b[-1].strip()}:
                edges[x] += 1
    repeated = {x for x,n in edges.items() if n > len(pages)/2}
    sections = defaultdict(list)
    state = 'front'
    headings = []
    cleaned_pages = []
    for p in pages:
        cleaned = []
        for i, block in enumerate(p['blocks']):
            if i in (0,len(p['blocks'])-1) and (block.strip() in repeated or re.fullmatch(r'\s*\d{1,4}\s*',block)):
                continue
            lines = block.splitlines()
            for line in lines:
                stripped = line.strip()
                if re.match(r'^(参考文献|References)(?:\s|\(|:|：|$)',stripped,re.I): state = 'references'
                h = HEADING.match(stripped)
                if h and len(stripped) <= 70 and int(h[1].split('.')[0]) <= 9:
                    # Decimal tables and figure values are not section headings.
                    title = h[2].strip()
                    if len(HAN.findall(title)) >= 2 and not re.search(r'[。；;,，=<>]',title) and not re.match(r'期|年|卷',title):
                        if state == 'front' and not classify_heading(title): continue
                        headings.append({'number':h[1],'title':title,'pdf_page':p['pdf_page']})
                        kind = classify_heading(title)
                        if kind and '.' not in h[1]: state = kind
                        elif '.' not in h[1]: state = 'body_other'
                        continue
                if state != 'references' and not re.match(r'^(图\s*\d|表\s*\d|Fig\.?|Table\s*\d|https?://)',stripped,re.I):
                    sections[state].append(line)
            cleaned.append(block)
        cleaned_pages.append({'pdf_page':p['pdf_page'],'text':'\n\n'.join(cleaned)})
    body = '\n'.join('\n'.join(v) for k,v in sections.items() if k not in ('references','front'))
    if len(HAN.findall(body)) < 1000:
        body = '\n'.join('\n'.join(v) for k,v in sections.items() if k != 'references')
    metrics = measure_text(body)
    section_metrics = {k:measure_text('\n'.join(v)) for k,v in sections.items() if k not in ('references','front')}
    private = dict(metadata,sha256=pdf_hash,pages=cleaned_pages,headings=headings,sections={k:'\n'.join(v) for k,v in sections.items()})
    Path(cache,f'{ident}.json').write_text(json.dumps(private,ensure_ascii=False),encoding='utf-8')
    public = dict(metadata,sha256=pdf_hash,pdf_pages=len(pages),han_body_chars=metrics['han_chars'],
                  sentence_count=metrics['sentences'],heading_count=len(headings),
                  section_sentence_counts={k:v['sentences'] for k,v in section_metrics.items()},
                  extraction_warning=metrics['han_chars']<1500)
    compact=re.sub(r'\s+','',body)
    public['methods_mentioned'] = [t for t in METHODS if (
        re.search(r'(?<![A-Za-z])'+re.escape(t)+r'(?![A-Za-z])',compact,re.I)
        if re.search('[A-Za-z]',t) else t in compact)]
    public['legacy_font_repair'] = legacy_fonts
    return public,metrics,section_metrics


def summarize(metrics):
    chars=sum(m['han_chars'] for m in metrics)
    lengths=[n for m in metrics for n in m['sentence_lengths']]
    quartiles=statistics.quantiles(lengths,n=4,method='inclusive') if len(lengths)>1 else [None]*3
    terms={t:sum(m['terms'][t] for m in metrics) for t in TERMS}
    return {'papers':len(metrics),'han_chars':chars,'sentences':len(lengths),
            'length_definition':'non-whitespace characters per Chinese-containing filtered sentence',
            'sentence_length_median':statistics.median(lengths) if lengths else None,
            'sentence_length_q1':quartiles[0], 'sentence_length_q3':quartiles[2],
            'term_counts':terms,'term_per_10000_han':{t:round(n/chars*10000,3) if chars else 0 for t,n in terms.items()}}


def file_sha256(path):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(4*1024*1024),b''):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive',type=Path)
    parser.add_argument('--cache',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--workers',type=int,default=min(8,os.cpu_count() or 1))
    parser.add_argument('--date',default=date.today().isoformat(),help='Batch date, YYYY-MM-DD')
    args=parser.parse_args()
    repo=Path(__file__).resolve().parents[1]
    cache=args.cache.resolve()
    if cache == repo or repo in cache.parents:
        parser.error('--cache must be outside the repository (contains private source text)')
    if args.workers < 1: parser.error('--workers must be positive')
    try: date.fromisoformat(args.date)
    except ValueError: parser.error('--date must be YYYY-MM-DD')
    cache.mkdir(parents=True,exist_ok=True)
    args.output.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.archive) as z:
        csv_entry=next(n for n in z.namelist() if n.endswith('论文清单.csv'))
        rows=list(csv.DictReader(io.StringIO(z.read(csv_entry).decode('utf-8-sig'))))
        pdfs=sorted(n for n in z.namelist() if n.lower().endswith('.pdf'))
        lookup={r['文件名']:r for r in rows}
        jobs=[]
        for i,entry in enumerate(pdfs,1):
            r=lookup[Path(entry).name]
            meta={'paper_id':f'p{i:03d}','journal':r['期刊'],'year':int(r['年份']),
                  'title':r['标题'],'authors':r['作者'],'doi':r['DOI'],
                  'filename':Path(entry).name,'position':r['卷期页']}
            jobs.append((str(args.archive.resolve()),entry,meta,str(cache)))
    results=[]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures=[pool.submit(extract_one,j) for j in jobs]
        for future in as_completed(futures):
            results.append(future.result())
            if len(results)%10==0: print(f'Extracted {len(results)}/{len(jobs)} PDFs',flush=True)
    results.sort(key=lambda r:r[0]['paper_id'])
    bibliography=[r[0] for r in results]
    groups=defaultdict(list)
    sections=defaultdict(list)
    for public,metric,sm in results:
        groups[public['journal']].append(metric)
        for section,m in sm.items(): sections[section].append(m)
    stats={'schema_version':1,'generated':args.date,
           'archive_sha256':file_sha256(args.archive),
           'extractor':f'PyMuPDF {pymupdf.VersionBind}; column-aware blocks; font-aware legacy E-* repair; NFKC normalization',
           'workers':args.workers,'total_pdf_pages':sum(p['pdf_pages'] for p in bibliography),
           'journal_counts':dict(Counter(p['journal'] for p in bibliography)),
           'year_counts':dict(sorted(Counter(p['year'] for p in bibliography).items())),
           'overall':summarize([r[1] for r in results]),
           'by_journal':{k:summarize(v) for k,v in groups.items()},
           'by_section':{k:summarize(v) for k,v in sections.items()},
           'method_paper_coverage':{t:sum(t in p['methods_mentioned'] for p in bibliography) for t in METHODS},
           'limitations':['Automatic section headings are heuristic and require manual checks.',
                         'Term matches overlap; single-character conjunction counts include compounds.',
                         'References, detected captions and page boilerplate are excluded heuristically; tables/formula fragments can remain.',
                         'No OCR or semantic evaluation of all sentences; prose extraction cannot verify model parameter thresholds.']}
    for filename,obj in [('corpus-statistics.json',stats),('corpus-bibliography.json',bibliography)]:
        (args.output/filename).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'pdfs':len(results),'pages':stats['total_pdf_pages'],'han_chars':stats['overall']['han_chars'],
                      'warnings':[p['paper_id'] for p in bibliography if p['extraction_warning']],
                      'cache':str(cache)},ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
