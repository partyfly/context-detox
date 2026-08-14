#!/usr/bin/env python3
"""context-detox 机械预扫:输出"嫌疑清单"(嫌疑≠有罪,人工判定)。零依赖。
用法: python3 scan.py --memory ~/.claude/projects/<proj>/memory --skills ~/.claude/skills
检查:①分层追加(压缩处方) ②无日期裁定(中毒风险) ③断链 [[x]] ④触发面过宽 ⑤重名/超长文件"""
import re, os, sys, glob, argparse

def scan_memory(mdir):
    issues=[]; names=set()
    files=sorted(glob.glob(os.path.join(mdir,'*.md')))
    for f in files:
        base=os.path.basename(f)
        if base=='MEMORY.md': continue
        s=open(f,encoding='utf-8').read()
        m=re.search(r'^name:\s*(\S+)',s,re.M)
        if m:
            if m.group(1) in names: issues.append(('冲突',base,'name 重复: '+m.group(1)))
            names.add(m.group(1))
        layers=len(re.findall(r'(追加|补充|再追加)[（(：:]',s))
        if layers>=2: issues.append(('压缩',base,f'分层追加 ×{layers},触发合并重写'))
        body=s.split('---',2)[-1]
        if not re.search(r'20\d\d[-年.]\d{1,2}',body):
            issues.append(('中毒',base,'裁定无日期,无法判断新旧'))
        if len(body)>4000: issues.append(('压缩',base,f'正文 {len(body)} 字,考虑拆分或压缩'))
    # 断链与索引
    all_names={os.path.basename(f)[:-3] for f in files}|names
    for f in files:
        s=open(f,encoding='utf-8').read()
        for link in re.findall(r'\[\[([^\]]+)\]\]',s):
            if link not in all_names:
                issues.append(('中毒',os.path.basename(f),f'断链 [[{link}]](可能是待写占位,也可能指向已删条目)'))
    idx=os.path.join(mdir,'MEMORY.md')
    if os.path.exists(idx):
        s=open(idx,encoding='utf-8').read()
        for mf in re.findall(r'\]\(([^)]+\.md)\)',s):
            if not os.path.exists(os.path.join(mdir,mf)):
                issues.append(('中毒','MEMORY.md',f'索引指向不存在的 {mf}'))
        for f in files:
            b=os.path.basename(f)
            if b!='MEMORY.md' and b not in s:
                issues.append(('挑选','MEMORY.md',f'{b} 未入索引(孤儿,不会被召回)'))
    return issues

def scan_skills(sdir):
    issues=[]
    for f in sorted(glob.glob(os.path.join(sdir,'*','SKILL.md'))):
        name=os.path.basename(os.path.dirname(f))
        s=open(f,encoding='utf-8').read()
        m=re.search(r'^description:\s*(.+)$',s,re.M)
        if m:
            d=m.group(1)
            if not re.search(r'当|时使用|use when|triggers',d,re.I):
                issues.append(('挑选',name,'description 无触发时机描述,召回面可能过宽'))
            if len(d)<40: issues.append(('挑选',name,'description 过短,可能召回不准'))
        if re.search(r'(注意|切记|不要忘)',s) and '优先级' not in s:
            issues.append(('冲突',name,'含"注意事项"式条目且无优先级链——考虑修源头'))
    return issues

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--memory'); ap.add_argument('--skills')
    a=ap.parse_args()
    if not(a.memory or a.skills): ap.error('至少提供 --memory 或 --skills')
    out=[]
    if a.memory: out+=scan_memory(os.path.expanduser(a.memory))
    if a.skills: out+=scan_skills(os.path.expanduser(a.skills))
    if not out: print('预扫无嫌疑。'); sys.exit(0)
    print(f'{len(out)} 条嫌疑(按处方分组;嫌疑≠有罪,逐条人工判):\n')
    for rx in ['中毒','压缩','挑选','冲突','隔离','写出去']:
        rows=[o for o in out if o[0]==rx]
        if rows:
            print(f'## {rx}')
            for _,f,msg in rows: print(f'- {f}: {msg}')
            print()
