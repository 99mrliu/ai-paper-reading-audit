#!/usr/bin/env python3
"""Check locations/literal values. Passing is not semantic verification."""
import argparse
import ast
import hashlib
import json
import math
import operator
import re
import sys
import unicodedata
from decimal import Decimal,InvalidOperation
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def norm(s):
    return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',str(s or ''))).strip()


NUM=re.compile(r'(?<![\w.])[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][-+]?\d+)?(?:\s*%)?(?!\d|\.\d)')


def numbers(s):
    found=[]
    for m in NUM.finditer(norm(s)):
        raw=m.group().replace(',','').replace('−','-').replace(' ','')
        try: found.append((Decimal(raw.rstrip('%')),raw.endswith('%')))
        except InvalidOperation: pass
    return found


def refs(value):
    if isinstance(value,list): return value
    return [x for x in re.split(r'[,，\s]+',str(value or '')) if x]


def safe_eval(expr):
    if len(expr)>200: raise ValueError('Expression too long')
    tree=ast.parse(expr,mode='eval')
    if len(list(ast.walk(tree)))>50: raise ValueError('Expression too complex')
    ops={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}
    def walk(n):
        if isinstance(n,ast.Expression): return walk(n.body)
        if isinstance(n,ast.Constant) and type(n.value) in (int,float): value=float(n.value)
        elif isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.USub,ast.UAdd)):
            value=walk(n.operand)*(-1 if isinstance(n.op,ast.USub) else 1)
        elif isinstance(n,ast.BinOp) and type(n.op) in ops:
            a,b=walk(n.left),walk(n.right)
            if isinstance(n.op,ast.Pow) and abs(b)>12: raise ValueError('Exponent out of bounds')
            value=ops[type(n.op)](a,b)
        else: raise ValueError('Only bounded numeric arithmetic is supported')
        if not math.isfinite(value) or abs(value)>1e15: raise ValueError('Non-finite or excessive result')
        return value
    return walk(tree)


def verify(doc,pages,meta):
    errors=[]
    if not isinstance(doc.get('claims'),list) or not doc.get('claims'):
        raise ValueError('At least one claim is required')
    if not isinstance(doc.get('parameters',[]),list): raise ValueError('Parameters must be an array')
    rows=doc['claims']+doc.get('parameters',[])
    ids=[r.get('id') for r in rows]
    if any(not isinstance(x,str) or not x for x in ids) or len(ids)!=len(set(ids)):
        raise ValueError('IDs must be nonempty and unique')
    page_map={p['page']:p['flat'] for p in pages}
    checked=[]
    for c in rows:
        label=c.get('class','FACT' if c in doc.get('parameters',[]) else '')
        row={'id':c.get('id'),'class':label,'status':'PASS','notes':[]}
        if label not in ['FACT','INFERRED','UNKNOWN']:
            row.update(status='FAIL',notes=['Invalid evidence class'])
        elif not str(c.get('statement',c.get('name',''))).strip():
            row.update(status='FAIL',notes=['Missing statement'])
        elif label=='UNKNOWN':
            probes=c.get('absence_probe')
            if not isinstance(probes,list) or not probes or not all(isinstance(p,str) and p.strip() for p in probes):
                row.update(status='FAIL',notes=['UNKNOWN requires nonempty search terms'])
            elif not c.get('search_scope') or not c.get('reasoning'):
                row.update(status='FAIL',notes=['UNKNOWN requires scope and uncertainty explanation'])
            else:
                row['search_results']=[]
                for probe in probes:
                    hits=[]
                    for p,text in page_map.items():
                        pos=norm(text).casefold().find(norm(probe).casefold())
                        if pos>=0: hits.append({'page':p,'context':norm(text)[max(0,pos-60):pos+len(probe)+160]})
                    row['search_results'].append({'term':probe,'hits':hits})
                row.update(status='WARN',notes=['Search describes supplied pages only; keywords cannot establish semantic absence.'])
        else:
            q,page=norm(c.get('quote')),c.get('page')
            if not q or not isinstance(page,int) or isinstance(page,bool) or page not in page_map:
                row.update(status='FAIL',notes=['Quote and existing 1-based PDF page required'])
            elif q not in norm(page_map[page]):
                row.update(status='FAIL',notes=['Quote absent from declared page'],other_pages=[p for p,t in page_map.items() if q in norm(t)])
            else:
                row.update(found_page=page,quote=c['quote'],semantic_support='requires_reader_review')
                if len(q)<20:
                    row['status']='WARN';row['notes'].append('Short quote: check conditions manually')
                if label=='INFERRED':
                    if not c.get('reasoning'): row.update(status='FAIL',notes=['Inference requires reasoning'])
                    if c.get('value') is not None and not c.get('derivation_id'):
                        row.update(status='FAIL',notes=['Numeric inference requires referenced derivation'])
                else:
                    expected,got=numbers(c.get('value')),numbers(q)
                    missing=[str(v)+('%' if pc else '') for v,pc in expected if (v,pc) not in got]
                    if missing: row.update(status='FAIL',notes=['Numeric tokens absent from quote itself: '+', '.join(missing)])
                    elif c.get('value') is not None and not expected and norm(c['value']) not in q:
                        row.update(status='FAIL',notes=['Literal value absent from quote'])
        checked.append(row)
    byid={x['id']:x for x in checked}
    derivations=[]
    for d in doc.get('derivations',[]):
        row={'id':d.get('id'),'status':'PASS','notes':[]}
        try:
            dependencies=refs(d.get('source_claims'))
            if not dependencies or any(x not in byid or byid[x]['status']=='FAIL' or byid[x]['class']!='FACT' for x in dependencies):
                raise ValueError('Derivation must reference located FACT operands')
            operands=[v for c in rows if c['id'] in dependencies for v,_ in numbers(c.get('value'))]
            constants=[n.value for n in ast.walk(ast.parse(str(d['expr']),mode='eval')) if isinstance(n,ast.Constant) and type(n.value) in (int,float)]
            if any(Decimal(str(x)) not in operands and x not in (0,1,100) for x in constants):
                raise ValueError('Expression operand absent from referenced FACT values')
            got,expected=safe_eval(str(d['expr'])),float(d['expected'])
            tolerance=float(d.get('absolute_tolerance',0.05))
            if not math.isfinite(expected) or not 0<=tolerance<=0.5: raise ValueError('Invalid rounding tolerance/value')
            row.update(computed=got,expected=expected,absolute_tolerance=tolerance)
            if abs(got-expected)>tolerance: raise ValueError('Arithmetic disagrees with declared rounding tolerance')
        except (ValueError,TypeError,KeyError,ZeroDivisionError,OverflowError,SyntaxError) as exc:
            row.update(status='FAIL',notes=[str(exc)])
        derivations.append(row)
    dmap={x['id']:x for x in derivations}
    for c in rows:
        if c.get('derivation_id') and (c['derivation_id'] not in dmap or dmap[c['derivation_id']]['status']=='FAIL'):
            byid[c['id']].update(status='FAIL',notes=['Referenced derivation missing or failed'])
    for t in doc.get('transfer',[]):
        used=refs(t.get('because'))
        if t.get('verdict') not in ['可直接用','需改造','不可用','信息不足']: errors.append('Invalid transfer verdict')
        if not used or any(x not in byid or byid[x]['status']=='FAIL' for x in used):
            errors.append('Transfer references absent or failed evidence')
        if t.get('verdict')=='可直接用' and used and all(byid.get(x,{}).get('class')=='UNKNOWN' for x in used):
            errors.append('Unknown evidence cannot establish direct applicability')
    if doc.get('verdict_overall')=='可直接用' and any(t.get('verdict')!='可直接用' for t in doc.get('transfer',[])):
        errors.append('Overall verdict contradicts unresolved/incompatible steps')
    for c in doc.get('coverage',[]):
        if c.get('status')=='covered' and (not refs(c.get('claim_ids')) or any(x not in byid for x in refs(c.get('claim_ids')))):
            errors.append('Covered item must reference existing evidence')
    positive=[x for x in checked if x['class'] in ['FACT','INFERRED']]
    failures=sum(x['status']=='FAIL' for x in checked+derivations)+len(errors)
    return {'schema_version':'2.0','scope':meta.get('scope'),'errors':errors,'claims':checked,'derivations':derivations,
            'summary':{'claims_and_parameters':len(checked),'failures':failures,'warnings':sum(x['status']=='WARN' for x in checked),
                       'located_positive_claims':sum('found_page' in x for x in positive),'positive_claims':len(positive)},
            'interpretation':'Mechanical checks do not certify scientific meaning or completeness.'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--claims',required=True);ap.add_argument('--index',required=True);ap.add_argument('--out',required=True)
    a=ap.parse_args()
    try:
        idx=Path(a.index);meta=json.loads((idx/'index.json').read_text())
        if meta.get('status')!='ok' or meta.get('pages_sha256')!=digest(idx/'pages.jsonl'):
            raise ValueError('Index unusable or page data changed since extraction')
        pages=[json.loads(x) for x in (idx/'pages.jsonl').read_text().splitlines() if x.strip()]
        result=verify(json.loads(Path(a.claims).read_text()),pages,meta)
        result['binding']={'claims_sha256':digest(a.claims),'pages_sha256':digest(idx/'pages.jsonl'),
                           'index_sha256':digest(idx/'index.json'),'source_sha256':meta['sha256']}
    except (ValueError,OSError,KeyError,TypeError) as exc:
        result={'schema_version':'2.0','errors':[str(exc)],'claims':[],'derivations':[],'summary':{'failures':1}}
    Path(a.out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result['summary'],ensure_ascii=False))
    return 1 if result['summary']['failures'] else 0


if __name__=='__main__': sys.exit(main())
