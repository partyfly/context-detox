# context-detox 上下文清毒

一个 Claude Code / Agent 技能:大任务收尾后,按上下文工程理论对"会沉淀下去的持久物"做一次清毒——防止被污染的记忆、技能、摘要在下一次任务里劣化结果。

A Claude Code skill: post-task context detox. Audit the seven components of your agent's context stack for the four failure modes (poisoning / distraction / confusion / clash), then clean with the four verbs (write / select / compress / isolate).

## 理论骨架

| 层 | 来源 | 用途 |
|---|---|---|
| 七件套(指令/输入/检索/工具/短期笔记/长期记忆/输出格式) | 上下文栈 | **审计面**:污染住在哪 |
| 四失败模式(中毒/分心/混淆/冲突) | 上下文失败分类 | **病理**:污染长什么样 |
| 四步法(写出去/挑选/压缩/隔离) | 上下文管理 | **处方**:怎么清 |
| 四标准(相关/结构/时机/压缩) | 好上下文的定义 | **验收**:清完什么样算干净 |

理论之外补了三条实践纪律:**重读纪律**(凭摘要写下的断言一律待验证——压缩即中毒源)、**优先级链**(权威冲突靠写死在源头文件里的排序,不靠临场判断)、**修源头**(败方条目当场改掉,不立注意事项)。

## 安装

```bash
mkdir -p ~/.claude/skills/context-detox
curl -o ~/.claude/skills/context-detox/SKILL.md https://raw.githubusercontent.com/partyfly/context-detox/main/SKILL.md
```

用法:大任务收尾时对 Claude 说 **"清毒"** / **"context detox"**。它会逐面审计本次任务读写过的持久物,产出"问题→病理→动作→改哪个文件"的清理清单,确认后执行。

## 为什么需要它

这个技能诞生于一次真实事故:我们在制作一期讲"上下文工程"的科普视频时,执行任务的 AI 自己撞上了全部四种失败模式——凭压缩摘要断言文件实现方式(中毒)、迁就积累的规则清单而不做新判断(分心)、被明示"不要参照"的旧稿仍在带偏产出(混淆)、风格包与用户给的参照源打架时信错了旧的(冲突)。于是把片子里的方法论吃回自己肚子,变成收工必跑的清理工序。

License: MIT
