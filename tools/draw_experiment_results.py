#!/usr/bin/env python3
"""Plot frozen, completed experiment aggregates; never starts an experiment.

Run with a Python environment containing matplotlib, e.g. /usr/bin/python3 on
the research host. Reading the exported site needs neither Python nor matplotlib.
"""
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / '说明/五类时延分析'
INPUT = BASE / '数据/共同规则短流汇总.json'
CASES = json.loads(INPUT.read_text())['cases']
BY_ID = {c['case']: c for c in CASES}
COLORS = ['#1877a5', '#d47b22', '#229b83']
plt.rcParams.update({'font.family': ['Arial', 'DejaVu Sans'], 'font.size': 11,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.titlepad': 14, 'savefig.facecolor': 'white'})
plots = []


def figure(title, subtitles, note):
    fig, axes = plt.subplots(1, 2, figsize=(12.6, 6.4))
    fig.subplots_adjust(left=.08, right=.98, bottom=.25, top=.77, wspace=.30)
    fig.suptitle(title, x=.07, y=.97, ha='left', fontsize=17, weight='bold')
    for ax, text in zip(axes, subtitles):
        ax.set_title(text, loc='left', fontsize=13)
        ax.grid(axis='y', color='#e6ebee', linewidth=.8)
        ax.set_axisbelow(True)
    fig.text(.07, .12, note, va='top', color='#52616c', fontsize=10, linespacing=1.6)
    return fig, axes


def save(fig, name, case_ids, metric):
    path = BASE / '图片' / name
    fig.savefig(path, dpi=150)
    plt.close(fig)
    plots.append({'file': '图片/' + name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                  'cases': case_ids, 'metric': metric,
                  'cohort': 'common-policy-rerun/short',
                  'operation': 'Replot completed aggregate values; no raw packet recomputation or new experiment'})


def p99(cid):
    c = BY_ID[cid]
    assert c['completed'] and c['worst_ue_p99_ms'] is not None
    return c['worst_ue_p99_ms']


def main():
    fig, axes = figure('TDD periods | completed common-policy rerun', ['UL', 'DL'],
        'Application one-way P99; one UE, 4,000 statistical packets per condition.\n'
        '5 / 10 ms: failed before RF / UDP; no values plotted. Other radio fields also vary with period.')
    ids = []
    for ax, direction in zip(axes, ['ul', 'dl']):
        rows = [c for c in CASES if c['phase'] == 'tdd' and c['case'].startswith('period-') and c['direction'].lower() == direction and c['completed']]
        ids += [c['case'] for c in rows]
        x = np.arange(len(rows))
        y = [p99(c['case']) for c in rows]
        ax.plot(x, y, 'o-', color=COLORS[0], linewidth=2)
        ax.set_xticks(x, [f"{c['radio']['period_ms']:g}" for c in rows])
        ax.set_xlabel('Configured period (ms)'); ax.set_ylabel('Application P99 (ms)')
        ax.set_ylim(0, max(y) * 1.25)
        for xi, yi in zip(x, y): ax.annotate(f'{yi:.2f}', (xi, yi), xytext=(0, 9), textcoords='offset points', ha='center', fontsize=9)
    save(fig, 'TDD_共同规则周期结果.png', ids, 'worst_ue_p99_ms')

    fig, axes = figure('SCS x TDD | 12 completed conditions', ['UL', 'DL'],
        '30 kHz: n78 / 273 PRB; 120 kHz: n261 / 66 PRB; period 2.5 ms, 4,000 samples / UE.\n'
        'Labels show full-slot D:U counts. Band, PRB count and symbol shares differ: no isolated SCS effect.')
    groups = [('30 kHz', ['mu1-d1u3', 'mu1-d2u2', 'mu1-d3u1']), ('120 kHz', ['mu3-d10u9', 'mu3-d5u14', 'mu3-d14u5'])]
    labels = ['30k\n1:3', '30k\n2:2', '30k\n3:1', '120k\n10:9', '120k\n5:14', '120k\n14:5']
    ids = []
    for ax, direction in zip(axes, ['ul', 'dl']):
        case_ids = [c + '-' + direction for _, entries in groups for c in entries]; ids += case_ids
        y = [p99(c) for c in case_ids]; bars = ax.bar(range(6), y, color=[COLORS[0]] * 3 + [COLORS[2]] * 3, width=.64)
        ax.set_xticks(range(6), labels, fontsize=9); ax.set_ylabel('Application P99 (ms)')
        ax.set_ylim(0, max(y) * 1.24); ax.bar_label(bars, fmt='%.2f', padding=5, fontsize=9)
    save(fig, 'SCS_共同规则交叉结果.png', ids, 'worst_ue_p99_ms')

    fig, axes = figure('Multi-UE | per-UE load vs total load', ['UL', 'DL'],
        'Per-UE: 2 Mbps each. Total: 8 Mbps shared. 4,000 statistical packets per UE. Logarithmic y axes.\n'
        'At N=4 the inputs coincide; the same measured condition is reused, not an independent repeat.')
    ids = []
    for ax, direction in zip(axes, ['ul', 'dl']):
        for mode, color, label in [('fixed_per_ue', COLORS[0], '2 Mbps / UE'), ('fixed_total', COLORS[1], '8 Mbps total')]:
            case_ids = [f'n{n}-{direction}-' + ('fixed_per_ue' if n == 4 else mode) for n in [1, 2, 4, 8]]; ids += case_ids
            ax.plot(range(4), [p99(c) for c in case_ids], 'o-', label=label, color=color, linewidth=2)
        ax.set_yscale('log'); ax.set_xticks(range(4), ['1', '2', '4', '8']); ax.set_xlabel('UE count')
        ax.set_ylabel('Worst UE P99 (ms)'); ax.legend(fontsize=9)
    save(fig, '多UE_共同规则负载对照.png', ids, 'worst_ue_p99_ms; N4 shared input/result reused')

    fig, axes = figure('Multi-UE x TDD | 12 completed conditions', ['UL', 'DL'],
        '2 Mbps / UE; 4,000 statistical packets / UE; common-policy rerun. Logarithmic y axes.\n'
        'Historical access failures belong to earlier cohorts; these 12 completed conditions do not erase them.')
    ids = []
    for ax, direction in zip(axes, ['ul', 'dl']):
        for n, color in [(2, COLORS[0]), (4, COLORS[1])]:
            case_ids = [f'n{n}-{direction}-d{d}u{u}' for d, u in [(3, 1), (2, 2), (1, 3)]]; ids += case_ids
            ax.plot(range(3), [p99(c) for c in case_ids], 'o-', label=f'N={n}', color=color, linewidth=2)
        ax.set_yscale('log'); ax.set_xticks(range(3), ['3:1', '2:2', '1:3']); ax.set_xlabel('Full-slot D:U ratio')
        ax.set_ylabel('Worst UE P99 (ms)'); ax.legend(fontsize=9)
    save(fig, '多UE_TDD共同规则结果.png', ids, 'worst_ue_p99_ms')

    fig, axes = figure('Layer tracing | OFF / ON / ON repeat', ['UL', 'DL'],
        '4,000 samples / UE; common-policy rerun. Bars show application P99; logarithmic y axes.\n'
        'Runs occurred at different times. Differences are not causal estimates of tracing overhead or algorithm benefit.')
    ids = []
    for ax, direction in zip(axes, ['ul', 'dl']):
        cases = [f'n{n}-{direction}-{arm}' for n, arm in [(1, 'off'), (1, 'on'), (2, 'on'), (4, 'off'), (4, 'on'), (4, 'on-repeat')]]
        ids += cases; y = [p99(c) for c in cases]
        bars = ax.bar(range(6), y, color=[COLORS[0], COLORS[2], COLORS[2], COLORS[0], COLORS[2], COLORS[1]])
        ax.set_yscale('log'); ax.set_xticks(range(6), ['N1\nOFF', 'N1\nON', 'N2\nON', 'N4\nOFF', 'N4\nON', 'N4\nrepeat'], fontsize=9)
        ax.set_ylim(min(y) / 2, max(y) * 2.5); ax.set_ylabel('Worst UE P99 (ms)'); ax.bar_label(bars, fmt='%.2f', padding=5, fontsize=8)
    save(fig, '分层_探针条件结果.png', ids, 'worst_ue_p99_ms')

    fig, axes = figure('Same-packet layer intervals | selected UE', ['All statistical packets: means', 'Same slowest 40 packets: means'],
        'UE selected by highest application P99 in each condition. Stacks use the same packet set.\n'
        'Mixed interval includes scheduling / radio / reassembly; it is not standalone HARQ or CPU service time.')
    ids = ['n1-ul-on', 'n1-dl-on', 'n4-ul-on', 'n4-dl-on']
    for ax, slow in zip(axes, [False, True]):
        mixed, others = [], []
        for cid in ids:
            f = max(BY_ID[cid]['internal_flows'], key=lambda x: x['p99_ms'])
            parts = f['same_slowest_40_segment_mean_ms' if slow else 'segment_mean_ms']
            mixed.append(parts['rlc_radio_reassembly_mixed']); others.append(sum(v for k, v in parts.items() if k != 'rlc_radio_reassembly_mixed'))
        ax.bar(range(4), mixed, color=COLORS[0], label='RLC / radio / reassembly mixed')
        ax.bar(range(4), others, bottom=mixed, color=COLORS[1], label='Other 14 intervals')
        ax.set_xticks(range(4), ['N1 UL', 'N1 DL', 'N4 UL', 'N4 DL']); ax.set_ylabel('Mean interval sum (ms)')
        ax.set_ylim(0, max(a+b for a,b in zip(mixed, others)) * 1.32)
        for i, (a, b) in enumerate(zip(mixed, others)): ax.text(i, a+b+.015*ax.get_ylim()[1], f'{a+b:.3f}', ha='center', fontsize=9)
        ax.legend(fontsize=8, loc='upper left')
    save(fig, '分层_同包均值与慢包.png', ids, 'sum of same-packet segment means; highest-P99 UE per condition')
    report = {'status': 'PASS', 'input': str(INPUT.relative_to(ROOT)),
              'input_sha256': hashlib.sha256(INPUT.read_bytes()).hexdigest(), 'plots': plots,
              'font': 'Arial requested; DejaVu Sans fallback when Arial is unavailable',
              'scope': 'Offline plots of previously completed aggregates only.'}
    (BASE / '数据/重绘图片核验.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({'plots': len(plots), 'status': 'PASS'}))


if __name__ == '__main__':
    main()
