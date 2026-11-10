"""Read a user-provided binary Word original through an auxiliary conversion.

Never put the conversion in the official-original directory or relabel it as an
original. No network is used. The original's SHA remains the source identity.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
import zipfile


def reading_docx(source, workspace):
    source = Path(source)
    if source.suffix.lower() == '.docx':
        return source
    if source.suffix.lower() != '.doc':
        raise ValueError('Unsupported Word format: ' + str(source))
    original = source.read_bytes()
    if not original.startswith(bytes.fromhex('d0cf11e0a1b11ae1')):
        raise ValueError('Invalid binary Word original: ' + str(source))
    digest = hashlib.sha256(original).hexdigest()
    folder = Path(workspace)/'analysis-source-audit/protocol-word-conversion'/digest
    folder.mkdir(parents=True, exist_ok=True)
    target = folder/(source.stem + '.docx')
    if not target.is_file():
        command = ['soffice', '-env:UserInstallation='+(folder/'profile').as_uri(),
                   '--headless', '--norestore', '--convert-to', 'docx',
                   '--outdir', str(folder), str(source)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=300,
                                env=dict(os.environ, GSETTINGS_BACKEND='memory', SAL_USE_VCLPLUGIN='svp'))
        (folder/'conversion.json').write_text(json.dumps({
            'command': command, 'exit': result.returncode, 'stdout': result.stdout,
            'stderr': result.stderr, 'sourceSHA': digest,
            'notice': 'Auxiliary local conversion, not an official original.'}, ensure_ascii=False, indent=2))
        if result.returncode or not target.is_file():
            raise RuntimeError('Local Word conversion failed; see ' + str(folder/'conversion.json'))
    with zipfile.ZipFile(target) as archive:
        if archive.testzip():
            raise ValueError('Unreadable auxiliary DOCX')
        ET.fromstring(archive.read('word/document.xml'))
    if hashlib.sha256(source.read_bytes()).hexdigest() != digest:
        raise ValueError('Original changed during read conversion')
    return target
