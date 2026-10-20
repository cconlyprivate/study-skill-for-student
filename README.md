# major-learning-coach · 专业学习路径教练

> 一个 Agent Skill：告诉它你是什么专业的，它就按**你专业的培养逻辑**，把该学的东西排成一条**从简到难、有先修约束**的路线，然后一个点一个点带你走。

不是"什么都能聊的 AI 家教"，是**有专业骨架的教练**——它知道计科的 K03 该在数据结构之后、知道法学的请求权基础要在构成要件之前、知道临床的鉴别诊断不能跳过症状学。

---

## 它解决什么问题

| 痛点 | 普通对话的表现 | 本技能的做法 |
|---|---|---|
| 不知道该先学什么 | 给一张看起来合理的书单，顺序全靠感觉 | 每个专业有先修图（DAG）+ 难度分带，`从简到难` 是算出来的，不是排出来的 |
| 讲得不专业 | 用通用词汇解释专业问题，符号和约定对不上 | 每个专业带术语/符号约定表，讲"你老师会怎么要求" |
| 每次都要重新说一遍 | 换个对话就忘了你是谁、学到哪 | 专业、档位、进度存本地文件，下次接着来 |
| 一上来就给答案 | 抄完还是不会 | 解题走"地图 → 只给第一步 → 追问"，要全解才给全解 |

## 30 秒快速开始

```bash
git clone https://github.com/<YOUR_NAME>/major-learning-coach.git
cd major-learning-coach
./install.sh            # macOS / Linux
# 或
powershell -ExecutionPolicy Bypass -File .\install.ps1   # Windows
```

装完新开一个会话，直接说：

```
我是计科的，学过一点但说不清什么水平，想系统补一遍
```

它会问你基础 → 出 5 道分级题 → 判级 → 给路径表 → 从起点开始讲。

## 安装

### 方式一：Claude Code / 兼容 Agent Skills 的客户端

```bash
mkdir -p ~/.claude/skills
cp -r skills/major-learning-coach ~/.claude/skills/
```

### 方式二：DeepSeek Harness（DSH）

```bash
mkdir -p ~/.agents/skills
cp -r skills/major-learning-coach ~/.agents/skills/
```

### 方式三：只在本项目内使用

把 `skills/major-learning-coach` 复制到你项目的 `.agent/skills/` 或客户端指定的技能目录。

> 目录里必须保留 `SKILL.md` 与 `references/`、`majors/` 的相对位置，路由靠相对路径找文件。

## 怎么用（5 个真实说法）

```
我是软件工程的，想从零开始学操作系统
```
→ 建档 → 定级 → 出「从简到难」路径表 + 3 个里程碑。

```
这道题怎么做：求 ∫₀¹ x·ln(1+x) dx
```
→ 判专业与题型 → 解题地图 → 只展开第一步 → 追问，避免直接给答案。

```
帮我看看我学到哪了，还有多少
```
→ 读进度 → 一行摘要 → 下一步建议。

```
考考我，就考数据结构里树那部分
```
→ 3–5 题 → 逐题判分 → 错的记 `struggling`。

```
我是临床的，这个病例最可能是什么病
```
→ 加载临床分支 → 按"主诉 → 鉴别 → 证据"的套路走，而不是直接报病名。

## 支持的专业（59 个）

<!-- BEGIN:MAJORS -->
### 哲学（3）

| 专业 | 这个专业在训练什么 | 核心课 |
|------|--------------------|--------|
| [哲学](skills/major-learning-coach/majors/philosophy/) | 把模糊问题拆成可论证的命题，并给出有据可查的立场 | 哲学导论、西方哲学史、中国哲学史、伦理学、逻辑学 |
| [逻辑学](skills/major-learning-coach/majors/logic/) | 用形式语言检验推理是否有效，识别论证里的跳步 | 数理逻辑、集合论、模态逻辑、逻辑哲学、批判性思维 |
| [伦理学](skills/major-learning-coach/majors/ethics/) | 为具体情境中的"应该怎么做"建立可辩护的理由链 | 伦理学原理、应用伦理学、中西伦理思想史、道德心理学 |

### 经济学（4）

| 专业 | 这个专业在训练什么 | 核心课 |
|------|--------------------|--------|
| [经济学](skills/major-learning-coach/majors/economics/) | 用约束下的最优化解释选择，用数据检验因果 | 微观经济学、宏观经济学、计量经济学、数理经济学 |
| [金融学](skills/major-learning-coach/majors/finance/) | 给资产定价、给风险定价，并解释市场为什么这样反应 | 货币银行学、公司金融、投资学、金融工程、计量 |
| [国际经济与贸易](skills/major-learning-coach/majors/international-trade/) | 解释跨国交换的收益与摩擦，处理汇率、关税与合规 | 国际贸易学、国际金融、国际商法、外贸实务 |
| [财政学](skills/major-learning-coach/majors/public-finance/) | 解释政府收钱与花钱的效率与公平后果 | 财政学、税收学、政府预算、公共经济学 |

### 法学（4）

| 专业 | 这个专业在训练什么 | 核心课 |
|------|--------------------|--------|
| [法学](skills/major-learning-coach/majors/law/) | 在给定事实中找规范、在规范中找构成要件、推出结论 | 民法、刑法、宪法、行政法、民事诉讼法 |
| [政治学与行政学](skills/major-learning-coach/majors/political-science/) | 解释权力如何配置、制度如何影响行为 | 政治学原理、比较政治制度、公共行政学、中国政府与政治 |
| [社会学](skills/major-learning-coach/majors/sociology/) | 把个人困扰还原为结构问题，并用证据检验 | 社会学概论、社会调查方法、社会统计、社会学理论 |
| [国际政治](skills/major-learning-coach/majors/international-relations/) | 解释国家间合作与冲突的条件 | 国际关系史、国际政治理论、外交学、国际安全 |

### 教育学（4）

| 专业 | 这个专业在训练什么 | 核心课 |
|------|--------------------|--------|
| [教育学](skills/major-learning-coach/majors/education/) | 解释"人怎样学会"，并设计可验证的教学干预 | 教育学原理、课程与教学论、教育心理学、教育研究方法 |
| [教育技术学](skills/major-learning-coach/majors/educational-technology/) | 把学习目标翻译成可执行的教学设计与技术方案 | 教育技术学导论、教学设计、学习科学与技术、多媒体技术 |
| [学前教育](skills/major-learning-coach/majors/preschool-education/) | 按 3–6 岁发展规律设计活动与环境 | 学前儿童发展心理学、学前教育学、幼儿园课程、游戏论 |
| [体育教育](skills/major-learning-coach/majors/physical-education/) | 用生理与训练原理设计安全的运动负荷 | 运动生理学、学校体育学、运动训练学、体育心理学 |

### 文学（4）

| 专业 | 这个专业在训练什么 | 核心课 |
|------|--------------------|--------|
| [汉语言文学](skills/major-learning-coach/majors/chinese-literature/) | 读懂文本的形式与历史，并写出有依据的解读 | 现代汉语、古代汉语、中国古代文学史、现当代文学、文学理论 |
| [英语](skills/major-learning-coach/majors/english/) | 在语言、文学、翻译三条线上做准确的中英转换 | 综合英语、英语语言学、英美文学、翻译理论与实践 |
| [新闻学](skills/major-learning-coach/majors/journalism/) | 在时限内核实事实，并把事实组织成可发表的结构 | 新闻学概论、新闻采访与写作、传播学概论、媒介伦理与法规 |
| [广告学](skills/major-learning-coach/majors/advertising/) | 把商业目标翻译成能被记住的传播方案 | 广告学概论、广告策划与创意、消费者行为、整合营销传播 |

### 历史学（3）

| 专业 | 这个专业在训练什么 | 核心课 |
|------|--------------------|--------|
| [历史学](skills/major-learning-coach/majors/history/) | 用史料回答问题，并说清证据能撑到什么程度 | 中国古代史、中国近现代史、世界史、史学理论与方法 |
| [考古学](skills/major-learning-coach/majors/archaeology/) | 从物质遗存反推人群行为与年代序列 | 考古学通论、田野考古、中国考古、文物学 |
| [文物与博物馆学](skills/major-learning-coach/majors/museology/) | 判断文物价值、设计展览叙事、做保存决策 | 文物学概论、博物馆学、文物保护技术、藏品管理 |

### 理学（7）

| 专业 | 这个专业在训练什么 | 核心课 |
|------|--------------------|--------|
| [数学与应用数学](skills/major-learning-coach/majors/mathematics/) | 从定义出发构造证明，并判断结论成立的边界 | 数学分析、高等代数、解析几何、常微分方程、实变函数 |
| [物理学](skills/major-learning-coach/majors/physics/) | 建模型、估量级、用守恒律绕过复杂细节 | 力学、电磁学、热学、光学、量子力学、电动力学 |
| [化学](skills/major-learning-coach/majors/chemistry/) | 用结构解释性质，用机理预测产物 | 无机化学、有机化学、分析化学、物理化学、结构化学 |
| [生物科学](skills/major-learning-coach/majors/biology/) | 在分子—细胞—个体—群体多层尺度上找因果 | 普通生物学、细胞生物学、遗传学、生物化学、分子生物学 |
| [地理科学](skills/major-learning-coach/majors/geography/) | 把空间分布讲成机制，把地图读成证据 | 自然地理学、人文地理学、地图学、GIS、遥感 |
| [统计学](skills/major-learning-coach/majors/statistics/) | 从样本推断总体，并量化不确定性 | 概率论、数理统计、回归分析、随机过程、抽样调查 |
| [心理学](skills/major-learning-coach/majors/psychology/) | 把行为拆成可测量的变量并做因果推断 | 普通心理学、实验心理学、心理统计、认知心理学、发展心理学 |

### 工学（9）

| 专业 | 这个专业在训练什么 | 核心课 |
|------|--------------------|--------|
| [计算机科学与技术](skills/major-learning-coach/majors/computer-science/) | 把问题抽象成可计算的形式，并控制时间与空间代价 | 程序设计、数据结构、计算机组成原理、操作系统、计算机网络 |
| [软件工程](skills/major-learning-coach/majors/software-engineering/) | 在需求会变的前提下，交付可维护、可测试的系统 | 数据结构、面向对象程序设计、软件工程导论、数据库系统、软件测试 |
| [电子信息工程](skills/major-learning-coach/majors/electronic-information/) | 处理"信号 + 电路 + 系统"三件套，从时域到频域来回切换 | 电路分析、模拟电子技术、数字电子技术、信号与系统、通信原理 |
| [机械工程](skills/major-learning-coach/majors/mechanical-engineering/) | 让受力、运动、材料强度在图纸与实物上同时成立 | 理论力学、材料力学、机械原理、机械设计、工程制图 |
| [材料科学与工程](skills/major-learning-coach/majors/materials-science/) | 用成分—工艺—结构—性能四链条解释材料行为 | 材料科学基础、材料力学性能、材料物理、材料成型、分析测试 |
| [土木工程](skills/major-learning-coach/majors/civil-engineering/) | 在安全、造价、工期三重约束下把结构立起来 | 理论力学、材料力学、结构力学、混凝土结构、土力学与地基基础 |
| [自动化](skills/major-learning-coach/majors/automation/) | 用反馈让系统按预期收敛，并分析稳定性 | 自动控制原理、电路、模拟/数字电子、现代控制理论、过程控制 |
| [化学工程与工艺](skills/major-learning-coach/majors/chemical-engineering/) | 把实验室反应放大到工业规模，算清物料与热量 | 物理化学、化工原理、化工热力学、化学反应工程、化工设计 |
| [电气工程及其自动化](skills/major-learning-coach/majors/electrical-engineering/) | 在电压、电流、功率的约束下做发输配用 | 电路、电机学、电力电子技术、电力系统分析、自动控制原理 |

### 农学（4）

| 专业 | 这个专业在训练什么 | 核心课 |
|------|--------------------|--------|
| [农学](skills/major-learning-coach/majors/agronomy/) | 用品种、水肥、密度等可调参数换产量与品质 | 植物生理学、作物栽培学、遗传学、土壤肥料学、作物育种学 |
| [园艺](skills/major-learning-coach/majors/horticulture/) | 在设施与季节约束下管好果菜花 | 园艺植物栽培学、果树学、蔬菜学、观赏园艺、园艺植物育种 |
| [动物医学](skills/major-learning-coach/majors/animal-medicine/) | 从症状推到病因，再给治疗方案 | 动物解剖学、动物生理学、兽医病理学、兽医内科学、兽医外科 |
| [植物保护](skills/major-learning-coach/majors/plant-protection/) | 识别病虫草害，并选出经济与生态都划算的防治 | 普通植物病理学、农业昆虫学、农药学、植物检疫 |

### 医学（6）

| 专业 | 这个专业在训练什么 | 核心课 |
|------|--------------------|--------|
| [临床医学](skills/major-learning-coach/majors/clinical-medicine/) | 从主诉到诊断到处置，全程要有鉴别诊断的意识 | 系统解剖学、生理学、病理学、药理学、内科学、外科学 |
| [口腔医学](skills/major-learning-coach/majors/stomatology/) | 在毫米级空间里做结构与功能的修复 | 口腔解剖生理学、口腔组织病理学、牙体牙髓病学、口腔修复学、颌面外科学 |
| [中医学](skills/major-learning-coach/majors/traditional-chinese-medicine/) | 用证候框架把症状归到可施治的证型 | 中医基础理论、中医诊断学、中药学、方剂学、中医内科学 |
| [药学](skills/major-learning-coach/majors/pharmacy/) | 让分子成为安全有效的剂型，并控制质量 | 有机化学、药物化学、药剂学、药理学、药物分析 |
| [护理学](skills/major-learning-coach/majors/nursing/) | 用评估—诊断—计划—实施—评价的闭环照护病人 | 基础护理学、内科护理学、外科护理学、急危重症护理、社区护理 |
| [预防医学](skills/major-learning-coach/majors/preventive-medicine/) | 在人群尺度上找危险因素并设计干预 | 流行病学、卫生统计学、环境卫生学、职业卫生、营养与食品卫生 |

### 管理学（6）

| 专业 | 这个专业在训练什么 | 核心课 |
|------|--------------------|--------|
| [工商管理](skills/major-learning-coach/majors/business-administration/) | 在资源有限时做取舍，并为取舍负责 | 管理学原理、组织行为学、市场营销、财务管理、战略管理 |
| [会计学](skills/major-learning-coach/majors/accounting/) | 把经济业务翻译成可核对的报表语言 | 基础会计、中级财务会计、成本会计、审计学、财务管理 |
| [市场营销](skills/major-learning-coach/majors/marketing/) | 找到该服务谁、凭什么被选、怎么被记住 | 市场营销学、消费者行为学、市场调研、品牌管理、渠道管理 |
| [信息管理与信息系统](skills/major-learning-coach/majors/information-management/) | 让业务流程变成信息系统，并让它真的被用起来 | 管理学、数据库、信息系统分析与设计、数据挖掘、运筹学 |
| [公共事业管理](skills/major-learning-coach/majors/public-administration/) | 在多重公共利益下设计可执行的公共服务 | 管理学原理、公共管理学、公共政策、公共部门人力资源、社会调查方法 |
| [工程管理](skills/major-learning-coach/majors/engineering-management/) | 把技术方案变成能按期按预算交付的工程 | 工程经济学、工程项目管理、工程合同管理、施工组织、工程造价 |

### 艺术学（5）

| 专业 | 这个专业在训练什么 | 核心课 |
|------|--------------------|--------|
| [音乐学](skills/major-learning-coach/majors/musicology/) | 听懂结构，并能说清"为什么这里好听" | 乐理、视唱练耳、和声学、曲式与作品分析、中国音乐史 |
| [美术学](skills/major-learning-coach/majors/fine-arts/) | 用手上的功夫和眼里的判断互相校正 | 素描色彩、中国美术史、外国美术史、艺术概论、绘画技法 |
| [设计学](skills/major-learning-coach/majors/design/) | 在约束（用户、工艺、预算）里做可用的美 | 设计素描、平面构成、设计史、人机工程学、专业设计 |
| [戏剧影视文学](skills/major-learning-coach/majors/film-literature/) | 用视听语言讲一个结构完整的故事 | 影视剧作、中外电影史、影视美学、影视批评、导演基础 |
| [播音与主持艺术](skills/major-learning-coach/majors/broadcasting/) | 让声音与表达在直播压力下仍然准确、可信 | 普通话语音、播音创作基础、即兴口语表达、新闻播音、节目主持 |
<!-- END:MAJORS -->

新增专业见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 目录结构

```
major-learning-coach/
├── SKILL.md                      # 路由与协议（≤200 行，不含具体知识点）
├── references/
│   ├── major-index.md            # 59 个专业 → slug 映射 + 易混专业辨析
│   ├── curriculum-rules.md       # 难度分档、先修图、排序算法、过关标准
│   ├── diagnosis.md              # 三选一 → 5 题 → 判级 → 确认
│   ├── learning-card-template.md # 九段学习卡
│   └── progress-schema.md        # 进度目录与 JSON 字段
└── majors/
    ├── _template/SKILL.md        # 新专业从这里复制
    └── <slug>/SKILL.md           # 单个专业：课程地图 + 知识点表 + 术语 + 题型
```

## 三条设计取舍

1. **路由 + 子 skill，而不是一个大文件。** 59 个专业全塞进 SKILL.md，光加载就吃掉半个上下文，还没有一个专业讲得深。现在只加载命中的那一个。
2. **先修图，而不是章节目录。** 教材章节是"作者怎么讲"，先修图是"你必须先会什么"。用户卡住时，前者帮不上忙，后者能直接指出回补哪一点。
3. **默认引导式，而不是直接给答案。** 目标是让用户下一次自己能做。要完整解答随时可以要，但会标注"参考解，建议先自己写一遍"。

更多推理见 [docs/design.md](docs/design.md)。

## 进度存在哪

默认 `<当前目录>/.major-coach/`，其次 `~/.major-coach/`，可用环境变量 `MAJOR_COACH_HOME` 指定。纯本地，不上传。

## 开发者

```bash
python tools/validate.py     # 校验结构、索引一致性、知识点表、先修图无环
python tools/sync_readme.py  # 按 major-index.md 重建 README 专业表
```

## 许可

MIT，见 [LICENSE](LICENSE)。
