#!/usr/bin/env python3
"""Create the isolated PDF translation environment without changing system Python."""
import argparse,json,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AUX=ROOT.parent/'analysis-source-audit/paper-zh-20261109'
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--python',required=True,help='Path to an existing Python 3.12 interpreter')
a=p.parse_args();uv=shutil.which('uv')
if not uv:raise SystemExit('uv is required; no system package installation is attempted.')
AUX.mkdir(parents=True,exist_ok=True);env=AUX/'venv';cache=ROOT.parent/'analysis-source-audit/pdf-zh-cache'
if not (env/'bin/python').exists():subprocess.run([uv,'--cache-dir',str(cache),'venv','--python',a.python,str(env)],check=True)
subprocess.run([uv,'--cache-dir',str(cache),'pip','install','--python',str(env/'bin/python'),'pdf2zh==1.9.11','babeldoc==0.2.33','tencentcloud-sdk-python-tmt==3.1.70','bitstring>=4.3,<5'],check=True)
site=env/'lib/python3.12/site-packages';patches=[
('pdf2zh/cache.py','cache_folder = os.path.join(os.path.expanduser("~"), ".cache", "pdf2zh")','cache_folder = os.environ.get("PDF2ZH_CACHE_DIR", os.path.join(os.path.expanduser("~"), ".cache", "pdf2zh"))'),
('pdf2zh/config.py','self._config_path = Path.home() / ".config" / "PDFMathTranslate" / "config.json"','self._config_path = Path(os.environ.get("PDF2ZH_CONFIG_PATH", str(Path.home() / ".config" / "PDFMathTranslate" / "config.json")))'),
('babeldoc/const.py','CACHE_FOLDER = Path.home() / ".cache" / "babeldoc"','CACHE_FOLDER = Path(os.environ.get("BABELDOC_CACHE_DIR", str(Path.home() / ".cache" / "babeldoc")))')]
for rel,old,new in patches:
 file=site/rel;text=file.read_text()
 if new in text:continue
 if old not in text:raise SystemExit('Unexpected dependency source; review compatibility before patching '+rel)
 backup=AUX/(rel.replace('/','_')+'.original')
 if not backup.exists():backup.write_text(text)
 file.write_text(text.replace(old,new,1))
print(json.dumps({'environment':str(env),'cache':str(cache),'systemPythonChanged':False},ensure_ascii=False))
