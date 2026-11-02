# TEST-072 新版PDF内容与旧版删除核验

pdf技能：创建交付PDF前成功运行一次PDF的mark_artifact_operation_started.mjs --operation-kind create --expected-output-count 1 --output-format pdf；与Word编辑的marker属于两个不同格式的操作。缓存Python+pypdf读取最终渲染PDF，24页，提取内容含44000、2459、7.49、34/74；Word SHA与v7一致。复制到analysis-documents稳定同名PDF路径后逐字节核对相同，版式对应已经逐页打开检查的24张最终PNG，无新增内容变化。

旧渲染目录归属nobody:nogroup，普通用户不能删除目录内文件；按环境提权请求后sudo -n chown仅调整5个具名QA目录属主，退出0。随后只按预先生成的精确同名清单及SHA删除5份旧/QA总结PDF，退出0；再次递归查analysis-documents，仅剩稳定路径1份新版总结PDF。原文、论文、教材和Word备份未触及。实际删除清单/各旧版页数/前SHA及新版SHA在本地records/pdf_replacement_manifest.json。

新版文件与Word仅本地保存，本项Git只上传修改/测试说明。工程文件替换验证，3GPP/数学推导不适用，通信内容来源见CHG-042至044和TEST-068至070。

## 依据与适用边界 2026-10-20补注

本段已按2026-10-20用户提供的新原文重新核查并替换旧补注。当前依据：本项为工程操作，3GPP通信参数与新数学推导不适用；依据E01/E03，不硬贴协议条款。

依据编号：E01、E03。英文原版文献章节/PDF页序、教材章节/PDF页序、原Word段落定位与哈希见[统一依据表](../../docs/10_协议文献教材依据与参数溯源.md)。Word无PDF页码，不沿用旧PDF页序。

本记录对应范围：Git、文件隔离、边界修复、哈希、结果一致性或排版属于工程追溯，不修改通信协议；没有对应3GPP强制条款。相关实验条件仍以对应报告和M01为准。

原始命令、日期、原引用和运行结果保留历史事实，不改写成当时已采用新版本；本文新补注用于当前解释。2026-10-21适用边界更正：后续已核实默认DRB的UL SDAP头及N3 QFI问题，受影响完整业务已按新配置另批重测；当前数据见standards-review/evidence/current及逐阶段正文。旧业务性能仅作历史审计，不冒称新实验；独立核验的网格/TBS/模型按其声明假设保留。精确原因、条款与影响见docs/10第12及15节。
