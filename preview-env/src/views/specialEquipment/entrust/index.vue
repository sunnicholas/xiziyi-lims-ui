<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="委托单号" prop="entrustNo">
        <el-input v-model="queryParams.entrustNo" placeholder="请输入委托单号" clearable @keyup.enter.native="handleQuery"/>
      </el-form-item>
      <el-form-item label="委托单位" prop="companyName">
        <el-input v-model="queryParams.companyName" placeholder="请输入委托单位" clearable @keyup.enter.native="handleQuery"/>
      </el-form-item>
      <el-form-item label="业务类型" prop="businessType">
        <el-select v-model="queryParams.businessType" placeholder="请选择业务类型" clearable>
          <el-option label="气瓶" value="gas_cylinder" />
          <el-option label="安全阀" value="safety_valve" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择状态" clearable>
          <el-option label="待流转" value="1" />
          <el-option label="待分配" value="2" />
          <el-option label="进行中" value="3" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 操作按钮区域 -->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" plain icon="el-icon-plus" size="mini" @click="handleAdd">新增委托</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="success" plain icon="el-icon-s-promotion" size="mini" :disabled="multiple" @click="handleBatchFlow">批量流转</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="warning" plain icon="el-icon-download" size="mini" @click="handleExport">导出</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <!-- 列表区域 -->
    <el-table v-loading="loading" :data="entrustList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="委托单号" align="center" prop="entrustNo" width="160">
        <template slot-scope="scope">
          <el-link type="primary" @click="handleView(scope.row)">{{ scope.row.entrustNo }}</el-link>
        </template>
      </el-table-column>
      <el-table-column label="委托单位" align="center" prop="companyName" :show-overflow-tooltip="true" />
      <el-table-column label="联系人" align="center" prop="contactPerson" width="100" />
      <el-table-column label="业务类型" align="center" prop="businessType" width="100">
        <template slot-scope="scope">
           <el-tag v-if="scope.row.businessType === 'gas_cylinder'" type="info">气瓶</el-tag>
           <el-tag v-else type="warning">安全阀</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="剩余天数" align="center" width="100">
        <template slot-scope="scope">
          <el-tag :type="getRiskColor(scope.row.remainingDays)">
            <i class="el-icon-time"></i> {{ scope.row.remainingDays }} 天
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="检测期限" align="center" prop="deadline" width="100">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.deadline, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="当前状态" align="center" prop="status" width="100">
        <template slot-scope="scope">
           <!-- 这里可以替换为字典组件 -->
           <dict-tag :options="dict.type.sys_common_status" :value="scope.row.status"/>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width" width="180">
        <template slot-scope="scope">
          <el-tooltip content="流转" placement="top">
            <el-button size="mini" type="text" icon="el-icon-s-promotion" @click="handleFlow(scope.row)"></el-button>
          </el-tooltip>
          <el-tooltip content="分配" placement="top">
            <el-button size="mini" type="text" icon="el-icon-user" @click="handleAssign(scope.row)"></el-button>
          </el-tooltip>
          <el-tooltip content="原始记录" placement="top">
            <el-button size="mini" type="text" icon="el-icon-edit-outline" @click="handleRecord(scope.row)"></el-button>
          </el-tooltip>
          <el-tooltip content="流程追踪" placement="top">
            <el-button size="mini" type="text" icon="el-icon-time" @click="handleTrack(scope.row)"></el-button>
          </el-tooltip>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 流程追踪对话框 -->
    <el-dialog title="流程追踪" :visible.sync="trackOpen" width="600px" append-to-body>
      <el-timeline>
        <el-timeline-item
          v-for="(activity, index) in activities"
          :key="index"
          :timestamp="activity.timestamp"
          :color="activity.color">
          {{ activity.content }}
        </el-timeline-item>
      </el-timeline>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "EntrustList",
  dicts: ['sys_common_status'], // 假设有字典
  data() {
    return {
      // 遮罩层
      loading: true,
      // 选中数组
      ids: [],
      // 非多个禁用
      multiple: true,
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 0,
      // 表格数据
      entrustList: [],
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        entrustNo: null,
        companyName: null,
        businessType: null,
        status: null
      },
      // 追踪弹窗
      trackOpen: false,
      activities: []
    };
  },
  created() {
    this.getList();
  },
  methods: {
    /** 查询列表 */
    getList() {
      this.loading = true;
      // Mock数据
      setTimeout(() => {
        this.entrustList = [
          { entrustNo: '20240114-GC-001', companyName: '上海某某气体公司', contactPerson: '张三', businessType: 'gas_cylinder', remainingDays: -1, deadline: '2024-01-13', status: '1' },
          { entrustNo: '20240114-SV-002', companyName: '江苏化工集团', contactPerson: '李四', businessType: 'safety_valve', remainingDays: 3, deadline: '2024-01-17', status: '2' },
          { entrustNo: '20240114-GC-003', companyName: '浙北石化', contactPerson: '王五', businessType: 'gas_cylinder', remainingDays: 10, deadline: '2024-01-24', status: '3' },
        ];
        this.total = 3;
        this.loading = false;
      }, 500);
    },
    /** 获取风险颜色 */
    getRiskColor(days) {
      if (days < 0) return 'danger';
      if (days <= 3) return 'warning';
      return 'success';
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.resetForm("queryForm");
      this.handleQuery();
    },
    /** 多选框选中数据 */
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.entrustNo)
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.$message.success("跳转到新增委托页面");
    },
    /** 批量流转 */
    handleBatchFlow() {
      this.$confirm('是否确认流转选中的数据项？', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(() => {
          this.$message.success("流转成功");
        }).catch(() => {});
    },
    /** 流程追踪 */
    handleTrack(row) {
      this.trackOpen = true;
      // Mock 追踪数据
      this.activities = [
        { content: '委托登记完成 (操作人: 管理员)', timestamp: '2024-01-14 09:00', color: '#0bbd87' },
        { content: '流转至气瓶检测科 (操作人: 管理员)', timestamp: '2024-01-14 10:00', color: '#0bbd87' },
        { content: '等待分配', timestamp: '2024-01-14 10:00' }
      ];
    },
    handleView(row) {
        // 跳转详情
    },
    handleFlow(row) {},
    handleAssign(row) {},
    handleRecord(row) {},
    handleExport() {}
  }
};
</script>

<style scoped>
/* 紧凑型调整 */
.el-table .cell {
  padding-left: 5px;
  padding-right: 5px;
}
</style>
