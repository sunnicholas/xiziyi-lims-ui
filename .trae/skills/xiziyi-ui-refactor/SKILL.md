---
name: "xiziyi-ui-refactor"
description: "Refines LIMS record-entry UI with minimal changes. Invoke when reorganizing tabs/fields, merging duplicate info, or adding per-tab uploads and online/offline modes."
---

# Xiziyi LIMS UI Refactor

用于在不重做架构的前提下，把“检验录入/预览页”这类页面改得更符合真实业务录入习惯：信息不重复、分组清晰、切换更快、上传就近放置，并且能用两条演示数据覆盖两种场景。

## 何时调用

当用户提出以下诉求时调用：

- “同一字段每个 Tab 都重复展示，能否抽出来只显示一次”
- “把某些区块改为 Tab/子 Tab，点击切换更快”
- “原始凭证/现场记录不要单独 Tab，要在各自业务 Tab 内上传，且可多张，位置靠后”
- “表单要区分在线/离线两种模式，并且两套字段不一样；一个委托单只能属于一种模式；需要至少两条委托单演示”
- “优化 UI 逻辑，尽量最简实现，符合 GitHub Pages 部署”

## 设计与实现原则

- 以“最小改动”实现目标：优先复用现有结构、字段、组件与数据源；避免引入新依赖。
- 信息只在一个地方出现：同一主键字段（如编号、使用单位等）优先放在头部/公共区，不在每个 Tab 复写。
- 切换优先：把高频录入区块改为 Tab 切换（同一层级），避免深层嵌套导致来回滚动。
- 上传就近：现场记录/原始凭证放到对应业务 Tab 的末尾，并绑定该 Tab 自己的 `fileList`，支持多张。
- 模式互斥：在线/离线必须显式选择（如 `valveType`），并做到：
  - UI 上一眼可见当前模式（标题栏 Tag/标注）
  - 数据结构上两套字段独立（如 `valveOnline.*` 与 `valveOffline.*`）
  - 演示数据上至少两条委托单分别覆盖两种模式（`valveMode: 'online' | 'offline'`）
- 演示可对照：在线与离线委托单的备注/设备列表要能看出差异点，便于对照验证。

## 推荐落地模式（Vue2 + Element UI）

### 1) 抽取重复字段

- 若多个 Tab 重复展示同一字段（例如“编号”），只保留头部/公共区域的展示。
- Tab 内保留与该 Tab 强相关、且录入频率高的字段。

### 2) 区块改 Tab 以加速切换

- 将“外观/内部/瓶口/瓶阀/签字”等同类录入项改为同一层级的 `el-tabs`。
- 保持每个 Tab 内的表单宽度与 label 对齐一致。

### 3) “现场记录”按 Tab 分散上传

- 每个业务 Tab 末尾增加一个上传卡片（例如 `el-upload` 的 `picture-card`）。
- 每个 Tab 独立绑定自己的 `fileList`，避免不同 Tab 上传互相覆盖。

### 4) 在线/离线双模式（两套字段 + 互斥选择）

- 在标题栏增加模式切换（例如 `el-radio-group`），并在标题区域加一个 Tag 做醒目标注。
- 数据结构建议：
  - `recordForm.valveType: 'online' | 'offline'`
  - `recordForm.valveOnline: {...}`
  - `recordForm.valveOffline: {...}`

### 5) 演示委托单最小集

- 需要两条委托单：
  - 在线：`{ type: 'valve', valveMode: 'online', ... }`
  - 离线：`{ type: 'valve', valveMode: 'offline', ... }`
- 每条委托单至少 2 台设备，便于演示列表状态差异（已提交/未录入等）。

## 输出要求（交付标准）

- 给出修改点与对应位置（文件与关键片段范围）。
- 若改动了页面文件：在该文件页面顶部 Navbar 增加/更新“更新时间”（北京时间，格式 `YYYY-MM-DD HH:mm:ss`），且不修改未更新文件。
- 变更完成后说明如何在页面上验证：点击哪条委托单、应看到什么模式标识、表单展示哪些字段。

## 示例提示词

### 示例 A：重复字段抽取

“`preview_record.html` 里气瓶编号不要每个 Tab 都重复展示，只在头部显示一次，保持录入不受影响。”

### 示例 B：在线/离线互斥 + 两条演示委托单

“把安全阀录入分为在线与离线两种模式，两套字段不一样；标题栏要标注当前模式；并在演示数据里新增一条在线委托单和一条离线委托单。”

