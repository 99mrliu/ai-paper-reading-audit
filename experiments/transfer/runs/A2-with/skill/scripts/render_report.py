#!/usr/bin/env python3
"""Render passing, content-bound evidence; label semantic uncertainty."""
import argparse
import json
import sys
from pathlib import Path
from verify_claims import digest,refs


def esc(s): return str(s if s is not None else '').replace('|','\\|').replace('\n',' ')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ['claims','verification','index','out']: ap.add_argument('--'+key,required=True)
    a=ap.parse_args()
    try:
        idx=Path(a.index);ver=json.loads(Path(a.verification).read_text());binding=ver.get('binding',{})
        expected={'claims_sha256':digest(a.claims),'pages_sha256':digest(idx/'pages.jsonl'),'index_sha256':digest(idx/'index.json')}
        if ver.get('summary',{}).get('failures',1) or any(binding.get(k)!=v for k,v in expected.items()):
            raise ValueError('Failed/stale/unbound verification; rerun verification after fixes')
        doc=json.loads(Path(a.claims).read_text());meta=json.loads((idx/'index.json').read_text())
        if binding.get('source_sha256')!=meta.get('sha256'): raise ValueError('Source hash mismatch')
        paper=doc.get('paper',{});checks={x['id']:x for x in ver['claims']}
        L=[f"# 论文方法适配审计：{paper.get('title',meta['source'])}",'',f"目标：{paper.get('question','未提供')}",
           f"材料：{meta['source']}，所供 PDF {meta['pages']} 页，范围 {meta['scope']}。",f"原件 SHA-256：`{meta['sha256']}`",'',
           '**核验边界：通过仅表示引文位置、数值字面或算术检查通过；结论语义、实验条件和迁移建议仍须依据上下文审阅。**','',
           '## 材料和解释限制','']
        L+=['- '+str(x) for x in paper.get('limitations_of_this_audit',[])]+['- '+meta.get('scope_warning','')]
        L+=['','## 任务覆盖','','| 关注项 | 状态 | 证据 |','| --- | --- | --- |']
        for c in doc.get('coverage',[]): L.append(f"| {esc(c.get('item'))} | {esc(c.get('status'))} | {esc(', '.join(refs(c.get('claim_ids'))))} |")
        L+=['','## 结论与证据','']
        for c in doc.get('claims',[])+doc.get('parameters',[]):
            v=checks[c['id']]
            L += [f"### {c['id']} · {c.get('class','FACT')}",str(c.get('statement',c.get('name',''))),f"值：{esc(c.get('value'))}；机械检查：{v['status']}。"]
            if c.get('class')=='UNKNOWN':
                L += [f"检索范围：{c.get('search_scope')}。",f"不确定性：{c.get('reasoning')}"]
                for search in v.get('search_results',[]):
                    hits=', '.join(str(h['page']) for h in search['hits']) or '无关键词命中'
                    L.append(f"- `{search['term']}`：{hits}。")
                L.append('关键词检索不证明论文语义上没有讨论此项；这里只描述所供材料的证据不足。')
            else:
                L += [f"原文位置：PDF p.{v['found_page']}；{c.get('source','未细分章节')}。",'> '+c['quote']]
                if c.get('reasoning'): L.append('推断过程：'+c['reasoning'])
                if c.get('conditions'): L.append('成立条件：'+str(c['conditions']))
            L.append('')
        if doc.get('derivations'):
            L+=['## 派生量','']
            for d,v in zip(doc['derivations'],ver['derivations']): L.append(f"- {d['id']}：`{d['expr']}` = {v.get('computed')}；来源 {refs(d.get('source_claims'))}；容差 {v.get('absolute_tolerance')}。")
        L+=['','## 方法适配判断','','| 环节 | 判断 | 依据 | 待补条件 |','| --- | --- | --- | --- |']
        for t in doc.get('transfer',[]): L.append(f"| {esc(t.get('step'))} | {esc(t.get('verdict'))} | {esc(', '.join(refs(t.get('because'))))} | {esc(t.get('needs'))} |")
        L+=['','**总体判断：'+str(doc.get('verdict_overall','信息不足'))+'**','','## 后续阅读与核验','']
        for g in doc.get('gaps',[]): L.append(f"- {g.get('gap')}；影响：{g.get('impact')}；下一步：{g.get('close')}。")
        L+=['- '+str(x) for x in doc.get('boundaries',[])]
        Path(a.out).write_text('\n'.join(L)+'\n');print(json.dumps({'status':'rendered','output':Path(a.out).name,'verification_bound':True}))
        return 0
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print('REFUSED: '+str(exc),file=sys.stderr);return 1


if __name__=='__main__': sys.exit(main())
