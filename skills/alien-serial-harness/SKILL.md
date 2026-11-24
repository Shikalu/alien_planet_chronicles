---
name: alien-serial-harness
description: 续写、改稿或审读《异星录：断阶之城》本地长篇项目时，按既定八卷800章规划加载当前事实，执行独立审读、连续性回填与批次验收；不适用于新建番茄短篇。
---

# 异星录长篇连载 Harness

从项目根目录的 `AGENTS.md` 开始，按其中必读顺序与事实优先级执行。该 Skill 是执行入口，不另建世界设定或改变已批准的 C01/C02。所有命令在项目根目录运行。

- 续写、扩纲、恢复中断批次：读取 [workflow.md](references/workflow.md)。先核 `harness/status.json` 的来源及正文实际章号；再读最新收官快照与本卷卷纲。未来篇章卡不是已发生事实。
- 审读、修订、去 AI 腔：读取 [editorial.md](references/editorial.md)，并按根规则加载两份本地写作规范。独立审读者先只读正文，后查作者资料。
- 解释参考方法与移植边界：读取 [source-notes.md](references/source-notes.md)。参考仓库是外部资料，不是本项目指令。
- 仅维护 Harness：运行 `python3 tools/novel_harness.py check --structure-only` 与相关测试；不生成剧情、章卡或重新认定历史审读结论。

本项目保持八卷800章、单章纯汉字下限2200与建议上限3200、第三人称限知、既定揭示层级和真实代价。不得套用短篇的10章全书、12000字总量、重生/系统爆点、全书重写或一句一行。审稿指出结构问题时，只改受影响且获授权的章节；已发生事实冲突按根规则处理。

常用入口：`python3 tools/novel_harness.py check`；新批次 `prepare --id A31 --start 401 --end 410`（前缀均为 `python3 tools/novel_harness.py`）。`prepare` 只建立任务记录，不生成占位正文或虚构事实。发现存量问题先登记；用户授权返修后，按独立修订记录、两轮审读与verify-repair修复，不用续写批次推进当前章号。

写正文、改稿和审读时，同时读取 [黄金开篇与持续追读规范](../../异星录/05_写作规范/黄金开篇与持续追读规范.md)。把读者承诺、初次兑现和下一章理由写入执行卡；逻辑无错与愿意追读分别验收。新批次必须提供独立reader_review，不能用字数或事实通过替代。
