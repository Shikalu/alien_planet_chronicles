# 吸引力审读记录格式

执行前读[专项规范](../../../异星录/05_写作规范/黄金开篇与持续追读规范.md)。记录必须来自真实阅读，不复制测试数据到生产记录。JSON只是可核验的交接格式；审读结论和独立性仍由真实过程负责。

## 写前承诺

prepare生成的reader_contract填写四个非空字段：expectation（本批读者等待什么）、payoff（哪章/什么场景局部交付）、cost（兑现要付什么）、next_expectation（本批选择会引出什么）。同步到本批执行卡；不只写“更爽、反转、期待感”。

## 审后记录

放`harness/reader-reviews/实际批次ID.json`。以下字段均须按实际情况填写：

- schema_version为1；kind为review；profile为serial或opening。作者自查使用kind=diagnostic，不计通过。
- writer与批次/返修记录中的主笔一致；reviewer是真实读者标识，须不同于主笔；independent=true、body_first=true必须有未参与改写、先正文后资料的真实过程。原初审/终审读者可在同一次真实终审中给出吸引力专项结论，不强制再开一个审读者。
- manuscripts按实际顺序登记chapter/path/sha256。chapter为正文章号；0只指现有发布目录中的真实楔子。路径是项目相对路径。触及前3章时必须同时加载1、2、3以及实际前置楔子，不能只挑强段。
- source_digest按manuscripts中上述三字段列表计算：`hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode()).hexdigest()`。稿件有任何变化即失效；不要只改摘要沿用旧结论。
- checks为对象列表，每项为criterion/chapter/quote/reason/verdict。quote必须逐字出现在对应稿件，reason说明对读者选择、期待或回报的具体作用；不能以“有钩子/通过”替代原因。verdict为pass或needs_revision，未通过项还须action写修改方向。
- 每个正文章号有规范中的五项，整篇有两项。开篇另有四项；first_page_hook必须引用真实入口正文的前100纯汉字窗口（不计标题）。允许承压章延后回报，但reason须说明延后到哪章、当前给了什么变化，独立读者判断是否成立。
- 总verdict仅在所有必审项通过时写pass。先保存问题版本，再修后重读、另留历史记录，不能直接删掉失败项凑通过。

把该JSON的path和sha256登记到任务reader_review。gate检查摘要、实际原句、范围、主笔、覆盖和结论，无法自动证明“商业爆款”或阅读过程真实。final重新seal会清空旧reader_review；正文再改必须重新读实际终稿。

历史已发布正文的专项复审也可保存此格式，覆盖统计只计实际当前字节的独立通过记录；旧报告缺本标准就保留未审状态。新返修必须登记reader_policy_version=1；不推进连载状态。
