
1、符合 UI 专业设计与逻辑
2、符合最简实现方式
3、符合 github page 部署要求
4、如果有疑问先与我确认、确认后再执行。
5、每次更改后都要在被更新的文件的页面顶部导航栏（Navbar） 增加"更新时间"，格式为"YYYY-MM-DD HH:mm:ss"，不需要更改其他未更新文件的导航栏。
6、注意我们使用的是北京时间。
7、每一次对话后都想想是否有什么有用的信息可以加入到 skills 或规则中，如果有就对其进行更新。

## Project Goals and Requirements (Added 2026-02-02)
1. **Online Preview Prototype**: The primary goal of the project is to create a prototype that can be previewed online using GitHub Pages.
2. **Smooth Navigation**: Ensure smooth page browsing and menu navigation between different functional modules.
3. **Complete Design Logic**: Focus on comprehensive design logic and sufficient page use cases to cover the entire business process.
4. **GitHub Pages Deployment**: Ensure all files are properly structured for GitHub Pages deployment without any build processes.
5. **Prototype Functionality**: The prototype should demonstrate complete business flows and user interactions, even if some features are simulated.

## UI Design Patterns (Added 2026-01-21)
1. **Document-Style Forms**: For official report previews, use a "Paper" metaphor (white background, padding, shadow, standard fonts like SimSun).
2. **Inline Editing**: For document-style forms, use underline-only input boxes (`.inline-input`) to mimic handwritten/typed lines.
3. **Dynamic Read-only/Edit**: Use bold colored text (e.g., `.text-blue-bold`) for existing values and inputs for missing values in reports.
4. **System Fields**: System-generated numbers/codes should be text-only (read-only), not input fields.
5. **Tab Organization**: Place "Basic Information" as the first tab by default.
6. **Tracking/Audit Logs**: Use `el-timeline` with `el-card` to display process history (time, status, executor, remarks).

## Status Flow Design (Added 2026-02-28)
1. **Status-Based Button Display**: Use `v-if` conditions to show different buttons based on status:
   ```html
   <el-button v-if="scope.row.status === '待出发'" ...>撤销</el-button>
   <el-button v-if="scope.row.status === '已财务确认'" ...>确认已出发</el-button>
   <el-button v-if="scope.row.status === '已出发'" disabled>派单结束</el-button>
   ```
2. **Final State Indicator**: Use disabled button with different text (e.g., "派单结束") to indicate process completion.
3. **Status Tag Colors**: Use consistent color coding:
   - `info` (blue): Initial/pending states (待出发)
   - `success` (green): Confirmed states (已财务确认)
   - `warning` (orange): In-progress states (已出发)

## Cross-Page Navigation (Added 2026-02-28)
1. **URL Parameter Navigation**: Use URL parameters for cross-page navigation:
   ```html
   <a href="preview_business.html?page=on-site-pre-entrust">预委托受理</a>
   ```
2. **Parameter Handling**: Read URL parameters in `created()` hook:
   ```javascript
   created() {
     const urlParams = new URLSearchParams(window.location.search)
     const page = urlParams.get('page')
     if (page) { this.activeMenu = page }
   }
   ```
3. **Menu Consistency**: Add the same menu structure to all pages for consistent navigation experience.

## Financial Confirmation Pattern (Added 2026-02-28)
1. **Detail-First Approach**: Show full details in a dialog before confirmation, not just a simple confirm dialog.
2. **Partial Edit Mode**: Use `:disabled` binding to allow editing only specific fields during sensitive operations:
   ```html
   <el-input v-model="form.amount" :disabled="!isFinanceMode">
   <el-input v-model="form.other" :disabled="isFinanceMode">
   ```
3. **State Flag**: Use a flag (e.g., `fromFinanceConfirm`) to control form behavior in different modes.
4. **Dialog Title**: Change dialog title based on operation mode for clarity.

## Data Model Best Practices (Added 2026-02-28)
1. **Always Include Status**: Every task/entrust record should have a `status` field with a default value.
2. **Consistent Field Naming**: Use consistent field names across related data structures (e.g., `taskNo`, `status`, `createTime`).
3. **Test Data Completeness**: Ensure test data includes all required fields for proper UI rendering.
