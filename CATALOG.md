# 技能索引

当前归档 22 个技能、208 个文件。每个技能仅保存一个选定版本。

## 技能清单

| 技能标识 | 名称与用途 | 归档路径 | 创作来源类别 | 公开出处 | 许可证信息 |
| --- | --- | --- | --- | --- | --- |
| agent-builder | Agent 架构与工具开发 | [技能包](skills/agent-builder/) | 待确认 | 待确认 | 待确认 |
| audio-to-srt | Qwen3 转写、强制对齐与 SRT 生成 | [技能包](skills/audio-to-srt/) | 待确认 | 待确认 | 待确认 |
| cli-anything-shotcut | Shotcut MLT 命令行编辑与检查 | [技能包](skills/cli-anything-shotcut/) | 待确认 | [HKUDS / CLI-Anything](https://github.com/HKUDS/CLI-Anything/blob/main/skills/cli-anything-shotcut/SKILL.md) | [Apache-2.0](skills/cli-anything-shotcut/LICENSE) |
| code-review | 安全、性能与可维护性审查 | [技能包](skills/code-review/) | 待确认 | 待确认 | 待确认 |
| generate-genshin-pretrain | 世界观预训练语料生成与校验 | [技能包](skills/generate-genshin-pretrain/) | 待确认 | 待确认 | 待确认 |
| git-create-readme | 项目 README 编写 | [技能包](skills/git-create-readme/) | 待确认 | 待确认 | 待确认 |
| git-pr-description | PR 标题与描述生成 | [技能包](skills/git-pr-description/) | 待确认 | 待确认 | 待确认 |
| git-release-note | 发布说明与变更日志 | [技能包](skills/git-release-note/) | 待确认 | 待确认 | 待确认 |
| git-smart-commit | 按功能拆分 Git 提交 | [技能包](skills/git-smart-commit/) | 待确认 | 待确认 | 待确认 |
| git-worktree-design | 并行分支与 worktree 规划 | [技能包](skills/git-worktree-design/) | 待确认 | 待确认 | 待确认 |
| mcp-builder | MCP 服务开发 | [技能包](skills/mcp-builder/) | 待确认 | 待确认 | 待确认 |
| pdf | PDF 提取、创建与合并 | [技能包](skills/pdf/) | 待确认 | 待确认 | 待确认 |
| rigorous-code-review | 严格工程审查与风险评估 | [技能包](skills/rigorous-code-review/) | 待确认 | 待确认 | 待确认 |
| sdd | 规范驱动调查、规划与实施 | [技能包](skills/sdd/) | 待确认 | 待确认 | 待确认 |
| sdd-task-driver | SDD 任务推进与审阅交接 | [技能包](skills/sdd-task-driver/) | 待确认 | 待确认 | 待确认 |
| skill-development | 简洁中文通用技能编写指南 | [技能包](skills/skill-development/) | 待确认 | 待确认 | 待确认 |
| srt-card-annotator | 字幕参考卡片标注 | [技能包](skills/srt-card-annotator/) | 待确认 | 待确认 | 待确认 |
| srt-enhancer | 对照原稿优化字幕 | [技能包](skills/srt-enhancer/) | 待确认 | 待确认 | 待确认 |
| srt-social-summary | 从字幕生成社交平台简介 | [技能包](skills/srt-social-summary/) | 待确认 | 待确认 | 待确认 |
| ui-ux-pro-max | UI/UX 指南与可搜索设计数据 | [技能包](skills/ui-ux-pro-max/) | 待确认 | 待确认 | 待确认 |
| video-workflow | 音频优先的视频制作与验收 | [技能包](skills/video-workflow/) | 待确认 | 待确认 | 待确认 |
| web-video-presentation | 音频同步的网页视频演示 | [技能包](skills/web-video-presentation/) | 待确认 | [ConardLi / garden-skills](https://github.com/ConardLi/garden-skills/tree/main/skills/web-video-presentation) | [MIT](skills/web-video-presentation/LICENSE) |

归档路径使用可点击的相对链接，指向 `skills/<技能标识>/`。公开出处仅填写已确认的公开作者与原始链接；许可证信息链接到仓库内许可证文件，或填写已确认的授权说明。缺失信息标为“待确认”，不得推断。

## 归档与验证说明

所有技能直接复制，未修改正文、脚本或资源，也未优化合并。已按相对文件清单和 SHA-256 核对全部 208 个文件；复制前后源技能包的文件内容未变化。排除 10 个 `__pycache__` 下的 `.pyc` 生成缓存文件，保留测试、依赖锁和资源。

- `agent-builder`、`code-review`、`mcp-builder`、`pdf` 选用现有 LF 副本；三个存在名称写法差异的 Git 技能选用小写短横线名称的副本，保留原 CRLF。
- `skill-development` 选用简洁中文通用版；`audio-to-srt` 选用 Qwen3 实现。未导入另外两份插件开发指南、通用音频转换实现和 `verify` 占位技能。
- 公开出处来自技能包内明确的来源链接或主页字段，许可证信息来自随包文件。仅有出处不能确定是否经过改进，因此创作类别仍为待确认；不把依赖项目的作者或许可证视为技能本身的作者或授权。
- 此次验证证明备份文件完整，不代表技能通过运行测试；未安装依赖或执行归档脚本。
- 管理文档空白检查通过。归档文件保留原换行和空白；识别 CRLF 后仍有 79 处原有尾随空白或文件末尾空行提示，均未修改，暂存内容已核对为原始字节。

## 恢复依赖与已知缺失

- `audio-to-srt`、`video-workflow`、`cli-anything-shotcut` 存在跨技能调用，应按说明恢复到目标项目的 `.agent/skills/`，不能直接假定备份目录可运行。相关 Python 项目要求 Python 3.12、UV；媒体流程还需要 FFmpeg、Shotcut 等外部工具，转写需下载模型。
- `audio-to-srt` 与 `video-workflow` 引用包外 `docs/视频制作工作流.md`；前者还提到 `docs/公开来源.md`。这些项目文档未归档，恢复时需提供相应文档或配置，未擅自补写。
- `web-video-presentation` 的 README 引用 `references/PRINCIPLES.md`、`references/PATTERNS.md`，包内缺少这两个文件；另有包外演示目录及上级 README 链接。原链接保持不变，未扩展复制范围。生成网页还需按原说明配置 Node.js 和相关依赖。
- 其他技能的目标项目文档、输入数据、API 凭据和工具环境由使用者按原说明提供，不属于此次技能包备份。

## 后续索引规则

创作类别仅使用“网络获取”“基于网络改进”“自行编写”“待确认”。后续修改仅记录公开创作信息、技术变化和验证结果；完全一致的技能只保留一条记录。

不记录私人项目名称或标识、项目目录、所用 Agent、备份日期及使用记录，也不另建私人来源台账。不得添加私人地址、个人机器路径、密钥或访问凭据。仅保留公开创作出处，不根据开发工具推断作者。
