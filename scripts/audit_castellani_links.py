"""Explicit, bounded network audit. Not part of the offline build or validation gate."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json, re, html

ROOT = Path(__file__).resolve().parents[1]
rows = json.loads((ROOT/'data/comparator-castellani-links.json').read_text())['links']
def check(row):
    out = {k: row[k] for k in ['source_link_id','href','display_label','alt','title','label_disagreement']}
    out.update(checked='2026-10-08', semantic_review='Not inferred from HTTP response')
    try:
        with urlopen(Request(row['href'], headers={'User-Agent':'NecessaryTangle-LinkAudit/0.31 (+https://transduction.systems/)'}), timeout=18) as response:
            body = response.read(300000).decode('utf-8',errors='replace')
            title = re.search(r'<title[^>]*>(.*?)</title>',body,re.I|re.S)
            out.update(http_status=response.status,final_url=response.url,reachability='Responded',page_title=html.unescape(re.sub(r'\s+',' ',title.group(1))).strip() if title else '')
    except HTTPError as e:
        out.update(http_status=e.code,final_url=e.url,reachability='Unavailable in this check' if e.code in [404,410] else 'Access or server response requires review',page_title='')
    except Exception as e:
        out.update(http_status=None,final_url='',reachability='Could not verify',page_title='',error=type(e).__name__)
    return out
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=6) as pool: results=list(pool.map(check,rows))
    dest=ROOT/'sources/update-2026-10-08/castellani-link-audit.json'
    dest.write_text(json.dumps({'checked':'2026-10-08','scope':'HTTP reachability and returned page title for all 307 source-published destinations. A successful response does not establish a correct attribution or destination. Original comparator data is unchanged.','links':results},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Checked',len(results),'destinations;',sum(x.get('http_status')==200 for x in results),'HTTP 200 responses')
