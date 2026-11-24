# R004 WB正文外部验收依赖最终对接

- 时间：2026-11-07T10:15:17+08:00（Asia/Shanghai）
- 本轮核验者：`01a1b38d-1b86-7c03-af8e-960353eaa510`；实际session：`01a1b38a-c83e-7372-95f1-36c86e256305`。
- 正文外部审读者：Boyle（用户称谓），真实reviewer：`01a1b38c-ca54-7bf0-894c-84d73c3a1b59`。
- **结论：仅 WB-13／17／20 的外部正文验收依赖现已对接关闭。**
- `handoff_pass=true`；`R004_pass=false`；`ready_for_publish=false`。不替正文作者/审读者签全文，不签R004发布或50/400章。

## 1. 真实终审与覆盖边界

外部终审：`harness/maintenance/R004/B10/approved-v3-recheck.json`，SHA256 `73c05766cf11176b2ed588719b56ea4dab36edbc9eeaa8828b0ecf8377d9c2d4`，与用户给定SHA完全一致。
其 `/fact_logic_verdict`、`/attraction_verdict`、`/verdict` 均为 `pass`；`/release_allowed=false` 明确不是发布签署。
`/chapters_full_reread_this_round` 为091/093/094/095/099/100；`/chapters_inherited_same_sha` 为092/096/097/098。35项closed只是该真实报告的状态索引，本核验者不声称把35项重新逐一正文审读。
092继承来源：`harness/maintenance/R004/B10/approved-v2-final.json`，SHA256 `4aa43d3fd2a3eaeae75bdbd787d4dfa863e7559d50ef6e52ee91f0c1759da542`；其 `/reading_order` 记录原091—100全文审读，但整份 `/verdict=needs_revision` 的历史结论保持。这里只继承当时已closed的具体092条目，再由现终审保持闭合。
Boyle `/writeback_review/status=not_reviewed_this_round`：其不代签WB；本报告以本方WB v3同字节结论与其正文终审对接，职责没有混签。

## 2. 阅读顺序与本轮新核

1. 读取根AGENTS、skill/editorial和用户限定；本次是外部证据交接，不声称新一轮先正文全文盲读。
2. 读取旧三项/原recheck/v3所留外部依赖，锁定具体要求；未重新审查其余19旧问题。
3. 核用户指定Boyle终审真实SHA；读取身份、结论、阅读范围、35项状态索引及与三项直接有关的具体闭环/规范条目。
4. 核B10 v2相关具体关闭条目和092同SHA全文继承来源；保留其当时整份needs_revision，不把它改写为历史整体pass。
5. 读取manifest并核九WB完整字节SHA与本方v3一致；核原三项WB当前原句及7处直接接口行。
6. 核Boyle十章工作稿SHA与报告及本方v3绑定一致；只核所引局部原句/行号，不全文重读。
7. 封存前后检查所有本报告已读输入未变，仅新建两份handoff报告。

本轮新核：真实终审SHA/身份/针对性证据、九WB新取SHA、十章工作稿SHA绑定、三项引文与依赖覆盖。继承：WB v3语义结论、Boyle对应新读或同SHA继承的正文判断。**本轮没有新增全文审读。**

## 3. 三项逐一对接

### R004-WB-13 — 外部依赖已关闭

089留置短撑与090回收旧短梁已分开；092几段来源仍待核

原要求与真实源pointer：
- `harness/maintenance/R004/writeback-review.json` `/issues/12`；SHA256 `e768f8ec5bff8c6d8406d3c06ef7d43fda56516afc6c6a965e3f6983052832ae`。
- `harness/maintenance/R004/writeback-recheck.json` `/prior_22_item_rechecks/12`；SHA256 `be20b0c67f6f6cc317674fa0f1b08d8b29a97cbc47d60e091eea42dfddcb27f5`。
- `harness/maintenance/R004/writeback-approved-v3-recheck.json` `/historical_22_issue_index/12`；SHA256 `f0b588bc21520707a11251812e17e31faa16df81c324faae511c1a72d50e1d69`。

> 原recheck：089短撑留置/090唯一旧短梁回收交岑野已分；092箱框搭接受力及撤退链明示待B10，不因WB记入即闭合。

原问题finding：已重读主笔最新090：用原回收绳牵出门框唯一短梁、修端后交岑野，封板短撑仍留原处。因此“089门框梁如何接091”旧疑问已在新稿补足，不再列正文缺口。但091只见可带短梁，092起“几段短梁”的具体分段／其他来源仍未见；不能抽回089明确留置短撑或增造整梁。

要求覆盖：
1. 089封板短撑不得抽回；090回收唯一旧梁到091的既有WB闭环保持。
2. 092只有一根旧梁、拆箱两条长边料的来源；搭接受力、两绳兜套与锁结外牵引尾段必须可区分。
3. 外側边料损毁后的山侧暂持、末人撤离与不可解绳扣弃失须有独立正文验收，而非凭WB补写通过。
- 092材料来源与搭接/受力/弃失：Boyle `/issue_closures/8`、`/issue_closures/8/evidence/0`、`/issue_closures/8/evidence/1`、`/issue_closures/8/evidence/2`、`/issue_closures/8/evidence/3`。
- 第二根绳的带线与两岸连接，非人物位置误读：Boyle `/issue_closures/34/evidence/0`。
- 093/094携回只是非承重小片及半扣，不是桥框/新增整梁：Boyle `/issue_closures/30`。
- 相邻095新改没有恢复确定退路；仅绳路仍在时回送：Boyle `/issue_closures/0`。

**本轮结论：092独立正文验收依赖已由Boyle /issue_closures/8、/34对接：092当前SHA与其v2全文审读一致，材料/受力/撤退为同字节具体闭环继承；其v3不是新读092。089—091既有WB语义及原段继承本方v3，不在本轮重审；095新改另有Boyle全文关闭且不恢复092弃失。仅关闭外部正文验收依赖，不作现实承载认证。**

历史状态不改：原review为 `open`，recheck为 `pending`，本方v3为 `pending_external_body_acceptance_not_signed_here`。本附录仅追加 `closed_external_body_acceptance_dependency_only`。

### R004-WB-17 — 外部依赖已关闭

机械读档与供能范围过宽，不能凭回填恢复精读

原要求与真实源pointer：
- `harness/maintenance/R004/writeback-review.json` `/issues/16`；SHA256 `e768f8ec5bff8c6d8406d3c06ef7d43fda56516afc6c6a965e3f6983052832ae`。
- `harness/maintenance/R004/writeback-recheck.json` `/prior_22_item_rechecks/16`；SHA256 `be20b0c67f6f6cc317674fa0f1b08d8b29a97cbc47d60e091eea42dfddcb27f5`。
- `harness/maintenance/R004/writeback-approved-v3-recheck.json` `/historical_22_issue_index/16`；SHA256 `f0b588bc21520707a11251812e17e31faa16df81c324faae511c1a72d50e1d69`。

> 原recheck：084手动读档、088接口不充电已修；094局部回位与永久死针仍待B10同字节复核。

原问题finding：084是目视薄片、人工日序转换，非机械针读档。073现稿明确录音耗电，不能写纯机械无电播放；059耗尽该类精读能力也不应由报告扩大为任何电路绝对零。088只借墙内既有供能作局部接口试合，未充电。094弹簧断，098手摇灯接线而非仪器电源。

要求覆盖：
1. 059/073能力与用电、084人工目视档案、088墙内节点局部供能不充电的已核WB边界继承，不把未重读章倒签。
2. 094局部接口、指针报位、人工控杆与管压做功须有同字节独立复核；仪器不供阀动力。
3. 094弹簧断后永久失读，旧六小时参照/最后回摆粗估不能变成新精确读数；后续灯线/铜片供能不能恢复仪器。
- 094接口/回位触点、管压与人工控杆/止位退出：Boyle `/issue_closures/12`。
- 永久死针与短延迟仅粗估：Boyle `/issue_closures/2/evidence/0`、`/issue_closures/2/evidence/1`。
- 半扣与旧线撤回而非新增电源：Boyle `/issue_closures/30/evidence/2`。
- 098续摇恢复照明，099仍墙内供能，非仪器复活：Boyle `/issue_closures/32`、`/standards_recheck/6`。

**本轮结论：094已由Boyle本轮全文新核 /issue_closures/12、/2明确关闭，含触点/人工/管压分工和弹簧断永久失读；093/094半扣取回及098同SHA供能继承、099能力边界也有真实条目。当前WB永久无读数、接口无新增电池的原段未变。059/073/084/088与101既有边界只继承本方v3，不新签那些正文；该项所欠的B10同字节验收已满足。**

历史状态不改：原review为 `open`，recheck为 `pending`，本方v3为 `pending_external_body_acceptance_not_signed_here`。本附录仅追加 `closed_external_body_acceptance_dependency_only`。

### R004-WB-20 — 外部依赖已关闭

100末物资留置不可回库，约量不是完整可用件

原要求与真实源pointer：
- `harness/maintenance/R004/writeback-review.json` `/issues/19`；SHA256 `e768f8ec5bff8c6d8406d3c06ef7d43fda56516afc6c6a965e3f6983052832ae`。
- `harness/maintenance/R004/writeback-recheck.json` `/prior_22_item_rechecks/19`；SHA256 `be20b0c67f6f6cc317674fa0f1b08d8b29a97cbc47d60e091eea42dfddcb27f5`。
- `harness/maintenance/R004/writeback-approved-v3-recheck.json` `/historical_22_issue_index/19`；SHA256 `f0b588bc21520707a11251812e17e31faa16df81c324faae511c1a72d50e1d69`。

> 原recheck：100最后完整普通卡扣/磨毛绳留置，铜片灯线回收与约量非完整件已写；092/094新增半扣/材料链不越过B10待审。

原问题finding：约1卷半、接头不足3件不能代替逐件留失记录，也不保证尚有完整卡扣。089—092材料来源另见WB-13。

要求覆盖：
1. 100最后完整普通卡扣与磨毛绳留置，不由约1卷半/不足3件余额倒推出完整载人绳或完整卡扣；铜片灯线与弃件分开。
2. 092/093/094半扣及非承重小框片跨章材料链须由B10独立正文验收，不使桥料或完整蓝扣复活。
3. 100新托臂动作必须仍控绳，末态弃绳弃扣不得被小改取消；092搭接链依赖不得绕过。
- 半扣/非承重小片来源、093取回、094复用收妥：Boyle `/issue_closures/30`。
- 092桥料/绳扣弃失和094材料用途：Boyle `/issue_closures/8`、`/issue_closures/12`。
- 100仍一手控绳、弃绳弃扣不回库：Boyle `/issue_closures/4/evidence/0`、`/issue_closures/4/evidence/1`、`/issue_closures/4/evidence/2`。
- 098撤铜片复线续摇区别于已弃物：Boyle `/issue_closures/32`。

**本轮结论：Boyle /issue_closures/30由092同SHA继承＋093/094全文新核，明确小片非承重、半扣非第三完整扣；/4在100当前全文核一手压绳及绳扣仍留置，未取消受力代价。092/094正文依赖由/8、/12补足。WB资源221与收官快照44的约量/不回库存原句均与v3同段同SHA，故仅该外部验收依赖闭合，不重算库存或新签全部材料工程。**

历史状态不改：原review为 `open`，recheck为 `pending`，本方v3为 `pending_external_body_acceptance_not_signed_here`。本附录仅追加 `closed_external_body_acceptance_dependency_only`。

## 4. 外部关闭证据原引文（本轮只核定位与当前SHA）

本节各pointer均相对 `harness/maintenance/R004/B10/approved-v3-recheck.json`，SHA256 `73c05766cf11176b2ed588719b56ea4dab36edbc9eeaa8828b0ecf8377d9c2d4`；完整结构及quote SHA见JSON。

### R004-B10-AV2-N01 · `/issue_closures/0`
- 外部状态：`closed`，reopened=false。
- 外部当前理由：末人自行套好回送套绳，再松无人接替的来岸桩；桩翻时可能拉不住，既有绳仍准备送回。之后热汽、轨枕松动和桩/轨坠落实际打断救援，才失去通路。未新增保证必死的工程限制，也未倒用后果证明事前必死；保留失联而非确认死亡。原中等因果问题及095选择/情绪两项阻断均关闭。
- `/issue_closures/0/evidence/0`；095 L15；外部方式 `full_reread_current`；工作稿 SHA256 `a8abd33c94196304c1d51674221cdba9805e48197cb54077e68c1240ba5bae0b`：
> 其他人过去时有他稳住来岸；等套绳最后送回，他得自己套好，再放开桩根沿残轨过去。桩若在这时翻倒，对岸未必来得及把他拉住。
- `/issue_closures/0/evidence/1`；095 L31；外部方式 `full_reread_current`；工作稿 SHA256 `a8abd33c94196304c1d51674221cdba9805e48197cb54077e68c1240ba5bae0b`：
> “最后没人替你压桩。”杜姨说。
- `/issue_closures/0/evidence/2`；095 L37；外部方式 `full_reread_current`；工作稿 SHA256 `a8abd33c94196304c1d51674221cdba9805e48197cb54077e68c1240ba5bae0b`：
> 林渡当面说清，只要绳路还在，就把套绳送回接他；桩和残轨撑不到那时，便没有第二条路。
- `/issue_closures/0/evidence/3`；095 L77；外部方式 `full_reread_current`；工作稿 SHA256 `a8abd33c94196304c1d51674221cdba9805e48197cb54077e68c1240ba5bae0b`：
> 槐七想把余绳送回去，阿九按住他，指向下方正在松开的轨枕。
- `/issue_closures/0/evidence/4`；095 L81；外部方式 `full_reread_current`；工作稿 SHA256 `a8abd33c94196304c1d51674221cdba9805e48197cb54077e68c1240ba5bae0b`：
> 他让册上添失联，不添死亡。

### R004-B10-AV2-A02 · `/issue_closures/2`
- 外部状态：`closed`，reopened=false。
- 外部当前理由：不到半时辰归属于弥娅依据最后回摆的估计；风向再变就催行，不等待喷发证实时辰。旧六小时核对周期和报废后不得继续读数仍区分，未添精确倒数。
- `/issue_closures/2/evidence/0`；094 L81；外部方式 `full_reread_current`；工作稿 SHA256 `f4b45e6d31f90719a8449ad7a933fbdcef84709bca4005fae403b1cf646bf384`：
> 弥娅照最后一次回摆粗估，争来的延迟还不到半个时辰。风又开始向内吸，她催前面的人接着走，不能等下一次喷发替他们核准时辰。
- `/issue_closures/2/evidence/1`；094 L71；外部方式 `full_reread_current`；工作稿 SHA256 `f4b45e6d31f90719a8449ad7a933fbdcef84709bca4005fae403b1cf646bf384`：
> 弹簧在壳里断开，指针斜落在裂盘上，再没有回去。

### R004-B10-AV2-A04 · `/issue_closures/4`
- 外部状态：`closed`，reopened=false。
- 外部当前理由：旧绳先经固定铁耳，阿九保持牵制；槐七明确一手仍压绳，另一手仅托小臂帮林渡搭回，未写成两手离绳或把整人提起。其后仍弃绳弃扣，不取消受力代价。
- `/issue_closures/4/evidence/0`；100 L39；外部方式 `full_reread_current`；工作稿 SHA256 `32db9e0550214c18626f3c07320d6540fd83c23b7a0765be12b86431e9d70dca`：
> 槐七把绳套绕过止动环，另一端先走箱座下的固定铁耳，才同阿九一起向侧后方拉。
- `/issue_closures/4/evidence/1`；100 L75；外部方式 `full_reread_current`；工作稿 SHA256 `32db9e0550214c18626f3c07320d6540fd83c23b7a0765be12b86431e9d70dca`：
> 槐七一手仍压住绳，另一手伸来托住他的小臂，帮他搭回平台。
- `/issue_closures/4/evidence/2`；100 L77；外部方式 `full_reread_current`；工作稿 SHA256 `32db9e0550214c18626f3c07320d6540fd83c23b7a0765be12b86431e9d70dca`：
> 绳不再回收，卡扣也留在门上。

### R004-B10-I02 · `/issue_closures/8`
- 外部状态：`closed`，reopened=false。
- 外部继承的原关闭理由：短梁加拆箱两边料错搭；两侧兜绳锁牢，牵引尾段与受力段隔离。闸断海外边料，山侧暂承，桥下绳扣弃失；小说因果可读，不作承载认证。
- 外部当前理由：指定关闭证据在本轮工作稿仍成立；涉及六个改章的段落已随全文重核，另四章只按同SHA继承。12条补丁未改回该旧问题，故不重开。
- 原具体闭环：`harness/maintenance/R004/B10/approved-v2-final.json` `/issue_closures/1`；当时该项 `closed`，不改整份 `needs_revision`。
- `/issue_closures/8/evidence/0`；092 L9；外部方式 `same_sha_inherited_quote_match`；工作稿 SHA256 `486afd303d9e697fe371ed417cf500b0b9a107d42b6589b4df972b79647cde6c`：
> 能承重的旧梁料只剩这一根。
- `/issue_closures/8/evidence/1`；092 L11；外部方式 `same_sha_inherited_quote_match`；工作稿 SHA256 `486afd303d9e697fe371ed417cf500b0b9a107d42b6589b4df972b79647cde6c`：
> 阿九拆开撤离箱，从框上取出两条还实的长边料，让它们并排向上行岸伸，尾端分别压上对岸梁头，另一端与短梁错搭。
- `/issue_closures/8/evidence/2`；092 L53；外部方式 `same_sha_inherited_quote_match`；工作稿 SHA256 `486afd303d9e697fe371ed417cf500b0b9a107d42b6589b4df972b79647cde6c`：
> 过桩后剩下的绳尾留给抬手牵引，与梁下受力段隔着锁结；松收绳尾，兜套仍收着接头。
- `/issue_closures/8/evidence/3`；092 L79；外部方式 `same_sha_inherited_quote_match`；工作稿 SHA256 `486afd303d9e697fe371ed417cf500b0b9a107d42b6589b4df972b79647cde6c`：
> 兜在桥下的绳段不能硬拽，卡死的扣也没去拿；阿九把能收的线盘好，分清短残段与还能继续使用的两卷余料。

### R004-B10-I06 · `/issue_closures/12`
- 外部状态：`closed`，reopened=false。
- 外部继承的原关闭理由：自然插入既有平口接回位触点；测针给位置，槐七控杆，管压做功，止位槽锁住才退。仪器不供阀动力。同字节实读复核。
- 外部当前理由：指定关闭证据在本轮工作稿仍成立；涉及六个改章的段落已随全文重核，另四章只按同SHA继承。12条补丁未改回该旧问题，故不重开。
- 原具体闭环：`harness/maintenance/R004/B10/approved-v2-final.json` `/issue_closures/5`；当时该项 `closed`，不改整份 `needs_revision`。
- `/issue_closures/12/evidence/0`；094 L41；外部方式 `full_reread_current`；工作稿 SHA256 `f4b45e6d31f90719a8449ad7a933fbdcef84709bca4005fae403b1cf646bf384`：
> 半扣只接仪器底座与这处触点。
- `/issue_closures/12/evidence/1`；094 L29；外部方式 `full_reread_current`；工作稿 SHA256 `f4b45e6d31f90719a8449ad7a933fbdcef84709bca4005fae403b1cf646bf384`：
> “力从管内来，不是她的仪器推得动。”
- `/issue_closures/12/evidence/2`；094 L75；外部方式 `full_reread_current`；工作稿 SHA256 `f4b45e6d31f90719a8449ad7a933fbdcef84709bca4005fae403b1cf646bf384`：
> 等前端站稳，槐七将检修杆压进原有止位槽才退手。

### R004-B10-RF-N04 · `/issue_closures/30`
- 外部状态：`closed`，reopened=false。
- 外部继承的原关闭理由：092留非承重零碎小片夹半扣，093误触后隔离抽回，094复用收妥。不是桥框复活、第三完整蓝扣或随队新灯。
- 外部当前理由：指定关闭证据在本轮工作稿仍成立；涉及六个改章的段落已随全文重核，另四章只按同SHA继承。12条补丁未改回该旧问题，故不重开。
- 原具体闭环：`harness/maintenance/R004/B10/approved-v2-final.json` `/issue_closures/23`；当时该项 `closed`，不改整份 `needs_revision`。
- `/issue_closures/30/evidence/0`；092 L13；外部方式 `same_sha_inherited_quote_match`；工作稿 SHA256 `486afd303d9e697fe371ed417cf500b0b9a107d42b6589b4df972b79647cde6c`：
> 弥娅从拆下的零碎框料里留出一小片，在仪器侧边取下槐七先前试录音用的半枚蓝扣，把扣与松散旧接线一并夹在木片上，免得断口扎破包布。
- `/issue_closures/30/evidence/1`；093 L85；外部方式 `full_reread_current`；工作稿 SHA256 `f46f4087286e66417566e662c1b0fd2700d796a0732fb6df4f785276b9d6f3ef`：
> 阿九仍压住它，让弥娅从侧面抽回木片和半扣，裹进原包布。
- `/issue_closures/30/evidence/2`；094 L75；外部方式 `full_reread_current`；工作稿 SHA256 `f4b45e6d31f90719a8449ad7a933fbdcef84709bca4005fae403b1cf646bf384`：
> 弥娅撤下半扣和旧线，抽回晶片钥匙，将它们分开收妥，再合上仪器侧盖。

### R004-B10-RR-A01 · `/issue_closures/32`
- 外部状态：`closed`，reopened=false。
- 外部继承的原关闭理由：撤铜片、复线、缓转手柄才亮，未靠余电自动恢复补解释。
- 外部当前理由：指定关闭证据在本轮工作稿仍成立；涉及六个改章的段落已随全文重核，另四章只按同SHA继承。12条补丁未改回该旧问题，故不重开。
- 原具体闭环：`harness/maintenance/R004/B10/approved-v2-final.json` `/issue_closures/25`；当时该项 `closed`，不改整份 `needs_revision`。
- `/issue_closures/32/evidence/0`；098 L65；外部方式 `same_sha_inherited_quote_match`；工作稿 SHA256 `0d2012a2c86c87da8800bb501e316750aac9b6f3e3a7ab31935f333b328e55d4`：
> 再缓缓转动灯柄。灯重新亮起，她才照向缝里。

### R004-B10-R2-A01 · `/issue_closures/34`
- 外部状态：`closed`，reopened=false。
- 外部继承的原关闭理由：是裴七把绳带过岸，不是将裴七送到第二根绳；同带线过程一致。
- 外部当前理由：指定关闭证据在本轮工作稿仍成立；涉及六个改章的段落已随全文重核，另四章只按同SHA继承。12条补丁未改回该旧问题，故不重开。
- 原具体闭环：`harness/maintenance/R004/B10/approved-v2-final.json` `/issue_closures/27`；当时该项 `closed`，不改整份 `needs_revision`。
- `/issue_closures/34/evidence/0`；092 L53；外部方式 `same_sha_inherited_quote_match`；工作稿 SHA256 `486afd303d9e697fe371ed417cf500b0b9a107d42b6589b4df972b79647cde6c`：
> 裴七把第二根绳带到对岸后，阿九将两根绳分置桥面两侧，各在短梁与箱框边料的搭接处绕出一只兜套。

供能补充：Boyle `/standards_recheck/6` 的 `pass` 及理由：
> 94仪器给位置、管压/手动杆改阀，99仍墙内线路供能，手摇灯不推整墙；100仅牵偏机械臂，不变全能破解。

## 5. 当前WB三项原句对齐

- R004-WB-13：`/historical_22_issue_index/12/tracked_original_segments/0`（本方v3）；`异星录/06_执行计划/工作区/R004-WB/资源与时间台账.md` L221，与v3同段同文件SHA：
> | 绳索与接头 | 091坠落门板及挂住绳段不回收；092短梁搭既有箱框边料并损失留置；095回线断绝；098短铰链扭损卡门、099未回收；100最后完整卡扣留检修门，磨毛绳限制机械臂后再损留置 | 无完整退路线；余绳约1卷半、接头不足3件只是约量，不保证完整载人绳或完整卡扣；完整可用、磨毛非载人与已弃置分开，铜片/灯线已收回 |
- R004-WB-13：`/historical_22_issue_index/12/tracked_original_segments/1`（本方v3）；`异星录/06_执行计划/工作区/R004-WB/逐章卡.md` L380，与v3同段同文件SHA：
> | 089 | 短梁承力、尺定位；照伤肩限制多人救父；分步开缝救出孩子；呼吸确认短暂昏迷 | 新增墙后孩子单列，不填066失联；破墙露上行路 |
- R004-WB-13：`/historical_22_issue_index/12/tracked_original_segments/2`（本方v3）；`异星录/06_执行计划/工作区/R004-WB/逐章卡.md` L381，与v3同段同文件SHA：
> | 090 | 现成护板布带托肩；逐项记录签改孔位及点火；尺短暂校对后交林渡；证物分别包护 | 林岑存活且未获免责；原护送册、后会合者与封墙孩子分栏，不合并失联；远船启动、第一灯亮 |
- R004-WB-17：`/historical_22_issue_index/16/tracked_original_segments/0`（本方v3）；`异星录/06_执行计划/工作区/R004-WB/资源与时间台账.md` L192，与v3同段同文件SHA：
> | 测潮仪 | 第73章被槐七夺走，075交换完成，076由弥娅收妥并固定侧盖；电子读数仍黑屏；076记“下方抽气、七息未复位”，077记约七息机械回弹 | 弥娅持有，只能用机械余量指针和风声判断；侧盖以旧铜线固定，精确潮汐读数不可用 |
- R004-WB-17：`/historical_22_issue_index/16/tracked_original_segments/1`（本方v3）；`异星录/06_执行计划/工作区/R004-WB/资源与时间台账.md` L206，与v3同段同文件SHA：
> | 测潮仪与频率钥匙 | 测潮仪继续黑屏；084机械槽只稳住可见薄片，靠目视与人工日序转换比对；088只借墙内既有节点试合局部接口，未充电；旧维修室取出潮汐晶片钥匙，拆闸钥匙仍由槐七持有 | 弥娅持测潮仪；两把钥匙分别用于节点确认和旧锁，尚未形成完整开启条件 |
- R004-WB-17：`/historical_22_issue_index/16/tracked_original_segments/2`（本方v3）；`异星录/06_执行计划/工作区/R004-WB/逐章卡.md` L258，与v3同段同文件SHA：
> | 84 | 弥娅比对衡陆木牌与澜陆薄片，确认同一日期都存在非自然空白；祝衡沿旧配重井去找上传名单 | 机械槽只稳住可见薄片，人工换算日序比对，未恢复完整记录或精读；空白制造者和时间仍未知 | 两份记录的缺口和蓝色纤维相互对应，但不能据此确认双陆删史责任 |
- R004-WB-17：`/historical_22_issue_index/16/tracked_original_segments/3`（本方v3）；`异星录/06_执行计划/工作区/R004-WB/逐章卡.md` L262，与v3同段同文件SHA：
> | 88 | 弥娅确认蓝色图案是一处两端接口记号，本地锁位与她保存的旧档案图样能对上，但不能据此确认建造者、来源或更早历史；钥匙与测潮仪同时回应 | 只借墙内既有节点供能试合局部接口，机械针偏转而黑屏不复、未充电；维修室结构开始下沉 | 两组旧频率可接通局部旧路线，但确认者来源和完整网络仍未知 |
- R004-WB-20：`/historical_22_issue_index/19/tracked_original_segments/0`（本方v3）；`异星录/06_执行计划/工作区/R004-WB/资源与时间台账.md` L221，与v3同段同文件SHA：
> | 绳索与接头 | 091坠落门板及挂住绳段不回收；092短梁搭既有箱框边料并损失留置；095回线断绝；098短铰链扭损卡门、099未回收；100最后完整卡扣留检修门，磨毛绳限制机械臂后再损留置 | 无完整退路线；余绳约1卷半、接头不足3件只是约量，不保证完整载人绳或完整卡扣；完整可用、磨毛非载人与已弃置分开，铜片/灯线已收回 |
- R004-WB-20：`/historical_22_issue_index/19/tracked_original_segments/1`（本方v3）；`异星录/06_执行计划/工作区/R004-WB/第一卷收官状态快照.md` L44，与v3同段同文件SHA：
> | 接头 | 剩余接头不足3件为约量，不保证完整件；最后完整卡扣留白船舱门，不回库存 |

直接接口补充（完整文件SHA列下一节）：

- `异星录/06_执行计划/工作区/R004-WB/资源与时间台账.md` L219：
> | 测潮仪 | 第94章为校准喷口连续使用机械指针，表盘和内部弹簧断裂 | 彻底失去读数功能；弥娅只能依靠风向、蒸汽凝结和旧档案判断 |
- `异星录/06_执行计划/工作区/R004-WB/资源与时间台账.md` L221：
> | 绳索与接头 | 091坠落门板及挂住绳段不回收；092短梁搭既有箱框边料并损失留置；095回线断绝；098短铰链扭损卡门、099未回收；100最后完整卡扣留检修门，磨毛绳限制机械臂后再损留置 | 无完整退路线；余绳约1卷半、接头不足3件只是约量，不保证完整载人绳或完整卡扣；完整可用、磨毛非载人与已弃置分开，铜片/灯线已收回 |
- `异星录/06_执行计划/工作区/R004-WB/资源与时间台账.md` L817：
> | 短梁089—092 | 089封板短撑留置；090门框清人后用原回收绳抽出唯一旧短梁，实段交岑野；091搭门板后仅余短梁；092拆箱取两条长边料与短梁搭接 | 箱横框分扣压；两根旧绳分处桥面两侧，由来岸桩经搭接处兜套升至上行岸桩并锁牢，承重段与锁结外牵引绳尾分开；避闸只放低绳尾，桥下绳段不动。外侧边料削断后，山侧边料、短梁与兜绳仅暂持最后撤手；过口只回收可解余料，木框、大半桥面、桥下不可解绳段及卡死扣留置。该092受力链的验收证据查R004独立审读与维护记录，本表不替代审读。 |
- `异星录/06_执行计划/工作区/R004-WB/资源与时间台账.md` L818：
> | 蓝扣068—094 | 068两枚完整扣分给祝衡/弥娅；074祝衡明确其扣留入口不可取回。073另出现半枚断扣，槐七抵仪器侧槽试录音，075随仪器返回 | 092弥娅取侧边半扣夹非承重小框片并携行，093触灯座后隔离取回，094仍用同一半扣后收回；完整扣、半扣与普通卡扣不混计。 |
- `异星录/06_执行计划/工作区/R004-WB/资源与时间台账.md` L820：
> | 晶片钥匙/测潮仪094 | 钥匙试既有阀槽平口，半扣/旧线只接局部回位触点；弥娅读针给手势，槐七人工控杆，管内压力使连杆回位 | 杆落原止位槽后撤接口、收钥匙和半扣；仪器弹簧断裂，永久无读数。接口与止位动作的验收另查R004独立报告，未新增阀用电池。 |
- `异星录/06_执行计划/工作区/R004-WB/逐章卡.md` L398：
> | 091/092 | 担架抬头产生滑移勒带风险；救援者明确上行岸；单短梁与两条箱框长边料搭接；两根旧绳在两岸桩上锁定桥下兜套，锁结外余尾另作牵引；避闸只降余尾，外侧边料毁后由山侧搭接暂持末人，桥下不可解段留置 | 不恢复坠落门板或新生整梁；092搭接与撤退受力链待B10重审 |
- `异星录/06_执行计划/工作区/R004-WB/逐章卡.md` L399：
> | 093/094 | 保留原件者明确知情选择；未在场者由林渡承担毁卷责任并记明；半扣实际隔离回收；局部读数→手势→人工压杆→管内回位 | 不声称全体同意，不给仪器动力；旧六小时参照不变、永久失读仍发生；接口链验收证据见R004独立审读 |

章卡398“092搭接与撤退受力链待B10重审”保留原执行记录；本附录作为其外部验收对接证据，不视为小说事实矛盾，不编辑标签。资源817/820“验收另查”由本附录精确指向真实报告。

## 6. 九份WB当前SHA（全部与v3相同）

| 文件 | SHA256 |
|---|---|
| 人物状态台账.md | `9936b39b0e3bf3aa1b105ac5123f25794899cc8966ab869a15e613de715bc6c0` |
| 资源与时间台账.md | `f2f847459c6cbce1314aff9dae9838f1df645728152b64652db4967d02351612` |
| 伏笔与悬念台账.md | `4e57a8d2ed89ae15227967a05b21820b5eda065ac8f1bf33977dbca00d035be0` |
| 事件与地点时间线.md | `b0ab624736073e8f416c8a9335a243354f5efecfab598089982552b6cc0a6f13` |
| 术语与命名表.md | `09cc4251e38b6b352a8d3fd28e9e75f6b0c3902b8d899f11c80d91905a686795` |
| 术语词典.md | `d1c00162f077b77bc0f4d62ee8e5b4ca1cc7e4f4d79e74cecbdd4b71a0693033` |
| 逐章卡.md | `14ff61a5feddeffee994daffc3534bd7650ba931e16509804e238fa818e0fd59` |
| 第一卷收官状态快照.md | `abcc36de0a6a784753e9631342f526588fa5c467973f47eb56329a281fe54294` |
| 后七卷设定决策与执行约束.md | `fbdf6296ba79a44afab8f089ed96d4c49b4be474b40292a301fe3b412a323462` |

manifest：`异星录/06_执行计划/工作区/R004-WB/manifest.json`，SHA256 `c2ad803e8eb1a61c0099e3a6a0064529730930da50b0029979c9b165ed5dfeb6`；仍为九文件，未改pending_review等执行状态。

## 7. 正文工作稿当前SHA绑定（不是本轮全文签名）

Boyle的正式目标path不是已发布证明；下表SHA取实际R004-B10工作稿。各条均同时匹配本方WB v3 `/prose_fingerprints`。

| 章 | 当前工作稿SHA256 | Boyle覆盖方式 |
|---|---|---|
| 091 | `bac5d3c7e849fe0fa9665710ab8127aed1013154fdf1af4abdbc3c403cc1e679` | Boyle_current_full_reread |
| 092 | `486afd303d9e697fe371ed417cf500b0b9a107d42b6589b4df972b79647cde6c` | same_sha_inherited_from_full_read_v2 |
| 093 | `f46f4087286e66417566e662c1b0fd2700d796a0732fb6df4f785276b9d6f3ef` | Boyle_current_full_reread |
| 094 | `f4b45e6d31f90719a8449ad7a933fbdcef84709bca4005fae403b1cf646bf384` | Boyle_current_full_reread |
| 095 | `a8abd33c94196304c1d51674221cdba9805e48197cb54077e68c1240ba5bae0b` | Boyle_current_full_reread |
| 096 | `fbea581ff571ab1d02348e0a3bcb81aca7b50cef9b4fde9f4b19b95e21e7d6b0` | same_sha_inherited_from_full_read_v2 |
| 097 | `7b6fcdcda14b8fc01005f40f51d4d0e74ea398795930bea0424f7e9d3e62c1fd` | same_sha_inherited_from_full_read_v2 |
| 098 | `0d2012a2c86c87da8800bb501e316750aac9b6f3e3a7ab31935f333b328e55d4` | same_sha_inherited_from_full_read_v2 |
| 099 | `935dd042d289c5ad20cad1eaf713b170ec81e13db21e8cd56b09bca40bc776f6` | Boyle_current_full_reread |
| 100 | `32db9e0550214c18626f3c07320d6540fd83c23b7a0765be12b86431e9d70dca` | Boyle_current_full_reread |

## 8. 源报告SHA与历史保留

| 源文件 | SHA256 |
|---|---|
| `harness/maintenance/R004/writeback-approved-v3-recheck.json` | `f0b588bc21520707a11251812e17e31faa16df81c324faae511c1a72d50e1d69` |
| `harness/maintenance/R004/B10/approved-v3-recheck.json` | `73c05766cf11176b2ed588719b56ea4dab36edbc9eeaa8828b0ecf8377d9c2d4` |
| `harness/maintenance/R004/writeback-review.json` | `e768f8ec5bff8c6d8406d3c06ef7d43fda56516afc6c6a965e3f6983052832ae` |
| `harness/maintenance/R004/writeback-recheck.json` | `be20b0c67f6f6cc317674fa0f1b08d8b29a97cbc47d60e091eea42dfddcb27f5` |
| `harness/maintenance/R004/B10/approved-v2-final.json` | `4aa43d3fd2a3eaeae75bdbd787d4dfa863e7559d50ef6e52ee91f0c1759da542` |
| `harness/maintenance/R004/writeback-recovery2-final.json` | `efb07e3274b7192acd471a841b261c7f2b1ebce86b8dd447e3c1592b391bdf08` |
| `harness/maintenance/R004/writeback-approved-v3-recheck.md` | `b6ca98c2423a055aeeb9d6d6eecd852515f6020de5ee291ae0324eae5821aa1b` |
| `harness/maintenance/R004/writeback-approved-v2.json` | `486c70bcec9f0e5ef5703540534cf7587cdd66b368fd9d70517ec7985f0999de` |
| `harness/maintenance/R004/writeback-approved-v2.md` | `07aea49af6124350f62c900fd258120b9d6db3bf8b08708a85202c6ce82f014d` |

本方v3原结论仍为 `writeback_delta_pass_dependencies_pending`，不覆盖、不回写历史pending。recovery2 `/issue_group_closures/1` 仍为 `closed_in_current_stage_only`，其不代签正文工程的边界通过本附录接到真实Boyle报告，而非改写旧记录。

## 9. 仍保留的范围外与执行限制

- B09 RF-N04、E01仅保留本方v3 `/B09_closures/0`、`/B09_closures/1` 的 `closed_for_writeback_scope_only`；本轮不扩大签收。
- WBV2-X48仍为本方v3 `/cross_scope_handoffs/0` 的 `handoff_not_closed`；约48依赖不因本次三项关闭消失。
- 没有新增全文、吸引力、实际工程承载、101—400或R004发布签名。其余19旧问题未重新裁定。
- 没有新建事实变更；没有改工作稿、九WB、旧报告、正式原件或导航；未执行check/gate/close/verify-repair/发布。
- 仅写本MD及同名JSON。所有本报告读取输入封存前后字节一致；检查只验证证据定位与SHA，不以脚本替代文学判断。
