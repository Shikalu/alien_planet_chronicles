# 批次执行与恢复

## 写前上下文

1. 按根 `AGENTS.md` 读取总纲、索引、当前卷纲/篇章卡/实际章卡、世界与角色规则、全部动态台账、写作与揭示规范。`harness/status.json` 是导航记录；若它与正文/已发生台账冲突，停止接写并查证，不静默取较大章号。
2. 从最新收官快照和上一篇实录确认当前时间、各组地点、伤病、物权与借期、已知信息、未送达消息。第401章从第四卷D320快照接写，不能把来客、返棚回条或会面意向写成已抵达/已履约。
3. 写前先读黄金开篇与持续追读规范，在当前批次卡记录读者期待、局部兑现、代价与新期待；再细化目标、阻碍、主动选择、真实代价、至少两项推进、旧伏笔、两处反转前置和钩子类型。不要提前拆完第五至八卷400张章卡。
4. `prepare` 建立批次记录，锁定已有正文与输入资料的指纹。`context` 中填写实际阅读依据与章卡路径；不得声称“已读”尚未读取的内容。正文工作稿放 `异星录/06_执行计划/工作区/{批次}/`，不提前进入 `正文/`。

## 机器记录与人工责任

`harness/batches/{批次}.json` 是可恢复检查点，格式由 `prepare` 生成。它保存输入指纹、正文清单、两轮封稿、审读报告指纹、问题关闭记录、连续性回填证据及周期审计。指纹只证明文件一致，不证明审读独立性或剧情正确；`independent` 和 `body_first` 必须有真实审读过程支撑。

- 草稿完成：将按章排序的 `chapters` 写为 `{"chapter":401,"path":"异星录/06_执行计划/工作区/A31/第401章_实际标题.md"}` 等真实文件；填写 `writer`；运行 `seal --id A31 --phase draft`。
- 独立初审：依据 [editorial.md](editorial.md) 调用未参与改写的读者子智能体。给它真实稿件路径，先读正文，记录稿件摘要对应的 `draft.digest`；然后再给设定对照资料。将报告、真实审读者标识、`independent:true`、`body_first:true` 及所审稿件摘要登记到 `reviews.initial`。
- 按问题修订：每项有章号、原句、严重程度、处理、复核证据。修改范围由问题决定，不强制全文重写。已有事实冲突或双合理解释按根规则进入待审核区；未决项不能假装关闭。
- 修后封稿：`seal --phase final`，再由独立读者重新读实际终稿，填写 `reviews.final`，绑定 `final.digest`。终稿任何字节变化都必须重新封稿与复核；不能只更新摘要来沿用旧结论。无改动也需要短复核，draft与final摘要可相同。
- `reviews` 的每条记录包含 `reviewer`、`independent`、`body_first`、`input_digest`、`path`、`sha256`、`verdict:"pass"`；初审可记录 `verdict:"issues"`，但末轮只能pass。`issues` 每条为 `id/chapter/severity/status/resolution`；严重、中等未关闭则阻断；基本设定待决定列入 `conflicts`，未解决不得继续相关正文。

## 回填与发布

写后先在工作区准备各权威文件的回填补丁，不将未审核草稿提前认定为已发生。`writebacks` 覆盖六份连续性文件与本批 `context.chapter_cards`（需要时先细化本批实际章卡）；每项登记 `path/sha256/status/note`，status为 `updated` 或 `unchanged`，note说明实际变化或为何无需新增术语。四项动态台账及章卡须按根规则逐章回填；即使事实未变，也记录核对范围与继承状态。不把不变当作未检查。

- `continuity_report`：每完成10章的真实连续性报告，记录路径与SHA256。达到50章边界，`periodic_audits.fifty` 必须有审计；达到100章，另登记 `periodic_audits.volume` 与收官快照。记录均为 `path/sha256`。既有每次正文后审读规则对不足10章的批次同样适用。
- `gate --id A31`：检查终稿、两轮报告、问题闭环、回填文件、周期审计、输入变化说明和旧正文保护。返回0只代表机器可核验条件齐备，不能代替读者审读。
- 回填正式权威文件后，`writebacks` 必须绑定其最终实际字节。`context_changes` 解释写前输入指纹变化的每个路径，不能以此豁免旧正文变化或代替设定变更批准。
- 验收通过才把终稿逐字节复制到正确卷 `正文/`，同步目录；记录所有步骤。随后 `close --id A31 --story-day 实际日次 --next-batch A32` 复查发布字节和回填指纹，再更新状态导航。脚本不代写、不复制或删除小说正文。
- 门禁失败停在当前检查点，不回滚或覆盖其他人的改动。中断恢复先核批次记录、输入差异和已发布文件；复制完成但close未完成时，确认完全一致后重跑close。close以状态文件为提交点，重复执行会复验后补齐published标记。

本工具不提供跨文件原子发布。发布中断时，按最终封稿、回填清单和Git差异逐项检查，补齐一致状态再close；不能只改 `last_published_chapter` 跳过验收。修改旧正文的独立任务需要自己的授权、基线和审读，不走续写门禁豁免。

## 已授权旧章返修

在独立maintenance记录中保存修改前后正文指纹、真实用户授权、分组草稿/终稿摘要、初审/复核报告、问题关闭和六文件/章卡回填。verify-repair检查这条证据链及未改正文保护范围；不推进400/D320等连载状态。修后只维护发布正文的唯一版本，完成的工作稿副本清理，报告和指纹留证。

## 吸引力审读接入

新prepare登记reader_policy_version=1，reader_review起始为空。独立复核实际终稿后，按黄金开篇与持续追读规范写 `harness/reader-reviews/批次ID.json`，填主笔/真实读者/先正文后资料、manuscripts（chapter/path/sha256）、source_digest（对这三字段列表按JSON sort_keys序列化取SHA256）、profile、checks和verdict。每项checks含criterion/chapter/quote/reason/verdict；未过项另有action。

将审读JSON的path/sha256填回批次reader_review，gate会核本批终稿覆盖和未过项。final重新seal会清空旧reader_review，须重审。历史返修记录没有此项就如实标未按追读标准审读，不补造旧报告。`python3 tools/check_reader_pull.py --coverage`显示通过覆盖；加`--require-complete`在未覆盖全体已发布章节时失败。

批次reader_contract必须填写expectation/payoff/cost/next_expectation四个实际内容，不能留空。新旧章返修同样登记reader_policy_version=1和reader_review；只有配置中按原始指纹固定的历史记录可保留原标准，删除版本号不能跳过门禁。字段和证据要求见[审读记录格式](reader-review-format.md)。
