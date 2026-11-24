# 长篇 Harness 操作入口

[根规则](../AGENTS.md) · [项目Skill](../skills/alien-serial-harness/SKILL.md) · [目录布局](layout.json) · [状态导航](status.json) · [维护证据索引](maintenance/README.md)

## 文档分工

| 要查什么 | 唯一维护入口 |
|---|---|
| 硬规则、事实优先级、必读资料、10/50/100章要求 | [AGENTS.md](../AGENTS.md) |
| 写作、审读、回填、发布与中断恢复流程 | [Skill工作流](../skills/alien-serial-harness/references/workflow.md) |
| 独立事实审读与修订方法 | [审读流程](../skills/alien-serial-harness/references/editorial.md) |
| 吸引力审读字段及证据口径 | [审读记录格式](../skills/alien-serial-harness/references/reader-review-format.md) |
| 当前接写任务与卷间约束 | [当前执行计划](../异星录/06_执行计划/详细执行计划.md) |
| 状态、路径和机器阈值 | [status.json](status.json)、[layout.json](layout.json)、[project.json](project.json)；不得绕过根规则修改阈值 |
| 旧章返修覆盖、历史审读与维护报告 | [维护证据索引](maintenance/README.md) |

本页只维护操作命令及其适用边界，不复制完整审读格式、写作规范或当前资源快照。正文和工作稿的位置规则见[执行目录](../异星录/06_执行计划/README.md)。

## 检查命令

所有命令在项目根运行，仅依赖 Python 标准库。

```sh
python3 tools/novel_harness.py check
python3 tools/novel_harness.py check --json
python3 tools/novel_harness.py check --structure-only
python3 tools/check_reader_pull.py --coverage --require-complete
python3 -m unittest discover -s tools -v
```

- `check` 检查权威入口、规定范围的链接、布局、状态来源、正文章号/卷归属/字数，并报告当前字节的独立吸引力审读覆盖；它不逐一重验全部历史返修链，也不调用 `verify-preservation`。
- `--structure-only` 不验正文，不能报告为全文验收。低于2200纯汉字为错误，超过3200为建议上限警示；风格词频仅供诊断。
- `--coverage --require-complete` 在未覆盖全体已发布章节时失败；覆盖只计与当前稿件字节匹配的实际审读记录，不代表机器重新读过正文。
- 退出码0为机器条件通过，1为检查失败，2为参数/数据格式错误。独立性、阅读质量和商业表现不能由退出码证明。

### 旧章返修验证

以 `status.json` 的 `latest_repair` 找到当前最新记录。以下是 **2026-11-10、R009验收后的示例**，不是永久批次号：

```sh
python3 tools/novel_harness.py verify-repair --record harness/maintenance/R009/record.json
python3 tools/check_reader_pull.py --record harness/reader-reviews/R009.json
```

返修记录在 `maintenance/返修ID/record.json`；完整流程见 [Skill工作流的旧章维护部分](../skills/alien-serial-harness/references/workflow.md)。`verify-repair` 不推进连载章号或故事日次。历史记录里的旧保护范围、全局台账字节与当时结论保留，后续合法修改可能使历史整记录不再能对当前工作树直接通过；不得为消除这种差异重签旧报告。

### 保全检查

```sh
python3 tools/novel_harness.py verify-preservation
```

该命令只比较 `project.json.preservation_baseline` 指定文件集合的字节，不检查额外新增文件，也不验证剧情质量。默认现指向 [H003当前基线](maintenance/H003/preservation.json)：按作者批准，保留R004的393个保护对象，并补齐全部406份正文及目录文件，共448份文件。第172章按R006已验收的更名映射保护现行文件，不恢复旧文件名或制造正文副本。

R004原始基线与当时结论原样保留；先前268项差异及本次切换证据见 [H003基线裁定](maintenance/H003/整理报告.md#基线裁定与执行)。后续获授权修订仍须独立留证，不能直接覆盖基线消除差异。

本轮另用 [H003正文保护清单](maintenance/H003/prose-protection.json) 核对全部正文文件的路径集合与SHA256；它服务本轮“不动正文”的边界，与默认保全检查相互补充。

## 新批次命令顺序

下列 A31 是状态导航对应的接写示例；实际执行前先核当前状态与来源指纹。本轮文档整理不运行这些命令。

```sh
python3 tools/novel_harness.py prepare --id A31 --start 401 --end 410
python3 tools/novel_harness.py seal --id A31 --phase draft
python3 tools/novel_harness.py seal --id A31 --phase final
python3 tools/novel_harness.py gate --id A31
python3 tools/novel_harness.py close --id A31 --story-day 实际日次 --next-batch A32
```

以上不是可连续粘贴的自动写稿脚本。各命令间必须完成[详细工作流](../skills/alien-serial-harness/references/workflow.md)规定的真实写稿、两轮独立审读、问题关闭、同终稿字节的吸引力审读、连续性回填与周期审计。`prepare`只建记录；`close`复查实际发布字节后才推进状态，不自动复制正文，也不提供跨文件原子发布。

第800章收官时运行 `python3 tools/novel_harness.py close --id A70 --story-day D947`，省略下一批次参数。收官登记把下一章和下一批次设为空；此命令可用于复验完结状态。
