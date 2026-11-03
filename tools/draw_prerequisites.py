#!/usr/bin/env python3
"""Deterministic teaching diagrams, never plotted experimental measurements."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '说明/插图'
GREEN = '#256d59'; BLUE = '#dcebf7'; GOLD = '#f6e7bf'; MINT = '#dceee2'


def text(x, y, value, size=21, color='#24443b', anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(str(value))}</text>'


def rect(x, y, w, h, fill=MINT, label='', size=22):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="#b8d1c2"/>' + (text(x+w/2, y+h/2+size/3, label, size, anchor='middle') if label else '')


def arrow(x1, y1, x2, y2):
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{GREEN}" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>'


def save(name, title, subtitle, body, height=460, footer='教学示意，不是新增实验结果。'):
    OUT.mkdir(parents=True, exist_ok=True)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle+' '+footer)}</desc>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="{GREEN}"/></marker></defs>
<rect width="1000" height="{height}" rx="16" fill="#f5faf7"/>
<g font-family="Arial, Noto Sans CJK SC, sans-serif">{text(35,48,title,29)}{text(35,82,subtitle,18)}{body}{text(35,height-25,footer,16)}</g></svg>'''
    (OUT / (name+'.svg')).write_text(svg, encoding='utf-8')


def main():
    body = rect(60,145,230,90,BLUE,'UE 应用')+rect(385,145,230,90,GOLD,'UPF 侧应用')+rect(710,145,230,90,MINT,'UE 应用')
    body += arrow(290,190,380,190)+arrow(615,190,705,190)
    for x, label in [(175,'t₀：发送'),(500,'t₁：接收 / t₂：回复'),(825,'t₃：收到回复')]:
        body += text(x,280,label,20,anchor='middle')
    body += text(335,135,'上行 UL',20,anchor='middle')+text(665,135,'下行 DL',20,anchor='middle')
    body += text(500,340,'同一事务：闭环 = 上行 + 回复处理 + 下行',23,anchor='middle')
    save('应用测量边界','先确定时延测到了哪里','应用边界示意；不等于纯空口，也不等于每层 CPU 耗时。',body,410)

    body = ''
    for i, direction in enumerate(['D','D','D','S','U']):
        body += rect(65+i*180,135,168,70,BLUE if direction=='D' else GOLD if direction=='S' else MINT,f'{i}: {direction}')
    body += text(500,240,'一个配置周期：0.625 ms；5 个标称时隙；完整槽 D:U = 3:1',21,anchor='middle')
    body += '<g id="tdd-symbols">'
    for i, direction in enumerate('D'*6+'F'*4+'U'*4):
        body += f'<g data-direction="{direction}">'+rect(65+i*62,295,56,55,BLUE if direction=='D' else GOLD if direction=='F' else MINT,direction,20)+text(93+i*62,377,i,15,anchor='middle')+'</g>'
    body += '</g>'+text(65,420,'S 展开：6 个 D + 4 个 F + 4 个 U；F 在此实验中留作保护。',21)
    body += text(65,458,'全周期按符号计数：D = 48，F = 4，U = 18，总计 70。',21)
    save('TDD实验配置','从 RRC 配置读懂 D / F / U','示例取自原实验配置；正常 CP、参考/数据 SCS 均 120 kHz、未配置 SBFD。',body,525,'位置与符号顺序示意，不表示精确 CP 时长；此配比不是协议强制方案。')

    body=''
    for row,(index,direction) in enumerate([(0,'D'),(1,'U'),(2,'F')]):
        y=135+row*80;body+=text(45,y+35,f'格式 {index}',20)
        body+=f'<g data-format="{index}">'
        for col in range(14):body+=rect(165+col*55,y,49,52,BLUE if direction=='D' else MINT if direction=='U' else GOLD,direction,19)
        body+='</g>'
    save('3GPP时隙格式摘录','3GPP 表 11.1.1-1：三个基础格式','按 TS 38.213 V19.5.0 §11.1.1 原表摘录重排；列为符号 0 至 13。',body,445,'仅摘录格式 0、1、2；SFI 格式表不是公共 TDD 配比的穷举清单。')

    body=''
    for row,(scs,count) in enumerate([(30,2),(60,4),(120,8),(240,16)]):
        y=125+row*72;body+=text(35,y+33,f'{scs} kHz',21)
        body+=f'<g data-scs="{scs}">'
        for col in range(count):body+=rect(175+col*760/count,y,760/count-4,46,MINT,str(col) if count<10 else '',17)
        body+='</g>'
    save('SCS与标称时隙','同一个 1 ms 子帧，时隙数如何变化','依据 TS 38.211 V19.5.0 表 4.3.2-1；正常 CP 标称时间网格。',body,465,'240 kHz 行用于参数集教学，不表示 n261 业务已经支持或实测通过。')

    body=text(60,135,'固定每 UE 负载：每条业务 2 Mbps',23)+text(555,135,'固定总负载：总计 8 Mbps',23)
    for row,n in enumerate([1,2,4,8]):
        y=175+row*57;body+=text(65,y+25,f'{n} UE → 总计 {2*n} Mbps',21)
        body+=rect(340,y,140,37,MINT,str(2*n)+' Mbps',18)
        body+=text(560,y+25,f'{n} UE → 每 UE {8/n:g} Mbps',21)
    save('多UE负载口径','UE 数量变了，负载怎样保持可比','这里表示业务生成速率，不是调度器实际分配的无线资源。',body,465,'等分总业务量是实验设定，不代表协议保证每 UE 得到相同吞吐。')

    body=''
    layers=['SDAP','PDCP','RLC','MAC','PHY']
    for i,label in enumerate(layers):
        y=125+i*57;body+=rect(80,y,210,43,BLUE,label,20)+rect(710,y,210,43,MINT,label,20)
        if i<4:body+=arrow(185,y+44,185,y+55)+arrow(815,y+55,815,y+44)
    body+=arrow(295,375,705,375)+text(500,340,'RFsim：代替真实射频链路',20,anchor='middle')
    body+=text(185,440,'UE 侧',22,anchor='middle')+text(815,440,'gNB 侧',22,anchor='middle')
    save('分层测量概念','用户面协议层与测量边界','层次依据 TS 38.300 §6.1；图示不包含每个真实软件线程或处理耗时。',body,505,'gNB 至 UPF 还有 NG-U/GTP-U 路径；测量段名称必须以实际时间戳位置定义。')

    body=text(55,133,'五个教学样本：1、2、3、4、10 ms（不是实验数据）',23)
    for i,value in enumerate([1,2,3,4,10]):
        x=105+i*175;h=value*20
        body+=rect(x,360-h,110,h,BLUE if i<4 else GOLD)+text(x+55,395,f'{value} ms',20,anchor='middle')
    body+=text(500,445,'线性插值 P99 = 9.76 ms；平均值 = 4 ms',23,anchor='middle')
    save('尾时延教学样本','平均值相同的量纲，为什么还要看尾部','分位数依赖样本数及计算方法；本例只演示计算，不估计真实违约概率。',body,505,'五个样本不足以论证极端尾可靠性；报告必须保留采样、丢包与分位方法。')

    body=''
    labels=['业务到达','队列与 HOL','资格/方向','评分与资源','交付与统计']
    for i,label in enumerate(labels):
        x=35+i*195;body+=rect(x,160,175,85,BLUE if i<2 else GOLD if i==2 else MINT,label,20)
        if i<4:body+=arrow(x+177,202,x+192,202)
    body+=text(500,310,'比较算法前：先锁定相同业务、相同程序、相同资源及测量口径',22,anchor='middle')
    body+=text(500,355,'3GPP 定义 QoS 特征与信令；实验算法及工程参数必须单独说明',21,anchor='middle')
    save('算法实验共同条件','算法得分以外，还需要哪些前置条件','流程是研究实现的教学归纳，不是 3GPP 指定的唯一调度流程。',body,425)


if __name__ == '__main__':
    main()
