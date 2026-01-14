<template>
  <div class="app-container flex-container">
    <!-- 左侧：待办列表 -->
    <div class="left-panel">
      <div class="panel-header">
        <el-input
          placeholder="搜索委托单号..."
          prefix-icon="el-icon-search"
          v-model="filterText"
          size="small"
          clearable
          style="margin-bottom: 10px;"
        >
        </el-input>
        <div class="filter-tabs">
          <el-radio-group v-model="auditType" size="mini" fill="#409EFF">
            <el-radio-button label="record">原始记录</el-radio-button>
            <el-radio-button label="report">报告</el-radio-button>
          </el-radio-group>
        </div>
      </div>
      
      <div class="task-list" v-loading="listLoading">
        <div 
          v-for="(item, index) in taskList" 
          :key="index"
          class="task-item"
          :class="{ active: currentTask && currentTask.id === item.id }"
          @click="selectTask(item)"
        >
          <div class="task-title">
            <span class="no">{{ item.entrustNo }}</span>
            <el-tag size="mini" effect="plain">{{ item.type }}</el-tag>
          </div>
          <div class="task-info">{{ item.company }}</div>
          <div class="task-meta">
            <span><i class="el-icon-user"></i> {{ item.submitter }}</span>
            <span>{{ item.date }}</span>
          </div>
        </div>
      </div>
      
      <div class="pagination-mini">
        <el-pagination
          small
          layout="prev, pager, next"
          :total="total"
          :page-size="10"
          @current-change="handlePageChange"
        >
        </el-pagination>
      </div>
    </div>

    <!-- 右侧：审核详情区 -->
    <div class="right-panel">
      <div v-if="currentTask" class="audit-workspace">
        <!-- 顶部操作栏 -->
        <div class="workspace-header">
          <div class="title">
            正在审核: {{ currentTask.entrustNo }} 
            <el-tag type="warning" size="small" style="margin-left: 10px">待审核</el-tag>
          </div>
          <div class="actions">
            <el-button type="success" icon="el-icon-check" size="small" @click="handlePass">通过</el-button>
            <el-button type="danger" icon="el-icon-close" size="small" @click="handleReject">退回</el-button>
            <el-divider direction="vertical"></el-divider>
            <el-button type="text" icon="el-icon-arrow-left" :disabled="isFirst" @click="prevTask">上一条</el-button>
            <el-button type="text" @click="nextTask" :disabled="isLast">下一条 <i class="el-icon-arrow-right"></i></el-button>
          </div>
        </div>

        <!-- 内容区域 -->
        <div class="workspace-content">
          <!-- 这里可以是原始记录表单，也可以是 PDF 预览 -->
          <div class="record-preview">
            <h3>原始记录表 - {{ currentTask.type }}</h3>
            <el-descriptions border :column="2" size="medium">
              <el-descriptions-item label="委托单位">{{ currentTask.company }}</el-descriptions-item>
              <el-descriptions-item label="检测日期">2024-01-14</el-descriptions-item>
              <el-descriptions-item label="设备状态">正常</el-descriptions-item>
              <el-descriptions-item label="环境温度">24℃</el-descriptions-item>
            </el-descriptions>
            
            <div class="data-section" style="margin-top: 20px;">
               <h4>检测数据</h4>
               <el-table :data="mockGridData" border style="width: 100%">
                 <el-table-column prop="param" label="检测参数" width="180"></el-table-column>
                 <el-table-column prop="std" label="标准值" width="180"></el-table-column>
                 <el-table-column prop="val" label="实测值"></el-table-column>
                 <el-table-column prop="result" label="判定">
                   <template slot-scope="scope">
                     <el-tag type="success" v-if="scope.row.result === '合格'">合格</el-tag>
                     <el-tag type="danger" v-else>不合格</el-tag>
                   </template>
                 </el-table-column>
               </el-table>
            </div>
            
             <div class="image-section" style="margin-top: 20px;">
               <h4>现场图片</h4>
               <el-image 
                 style="width: 100px; height: 100px; margin-right: 10px"
                 src="https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg" 
                 :preview-src-list="['https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg']">
               </el-image>
             </div>
          </div>
        </div>
      </div>
      
      <div v-else class="empty-state">
        <i class="el-icon-document-checked" style="font-size: 64px; color: #ccc;"></i>
        <p>请从左侧选择一条待办任务</p>
      </div>
    </div>

    <!-- 退回原因弹窗 -->
    <el-dialog title="退回原因" :visible.sync="rejectOpen" width="500px">
      <el-form ref="rejectForm" :model="rejectForm" :rules="rejectRules">
        <el-form-item label="退回原因" prop="reason">
          <el-input 
            type="textarea" 
            v-model="rejectForm.reason" 
            :rows="4" 
            placeholder="请输入退回原因（必填）..."
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="rejectOpen = false">取 消</el-button>
        <el-button type="primary" @click="confirmReject">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "AuditWorkbench",
  data() {
    return {
      filterText: '',
      auditType: 'record',
      listLoading: false,
      taskList: [],
      total: 0,
      currentTask: null,
      
      // 退回相关
      rejectOpen: false,
      rejectForm: { reason: '' },
      rejectRules: {
        reason: [{ required: true, message: "退回原因不能为空", trigger: "blur" }]
      },
      
      // Mock数据
      mockGridData: [
        { param: '公称压力', std: '≥ 10MPa', val: '12MPa', result: '合格' },
        { param: '气密性', std: '无泄漏', val: '无泄漏', result: '合格' },
      ]
    };
  },
  computed: {
    isFirst() {
      // 简化逻辑
      return false;
    },
    isLast() {
      return false;
    }
  },
  created() {
    this.getTaskList();
  },
  methods: {
    getTaskList() {
      this.listLoading = true;
      setTimeout(() => {
        this.taskList = [
          { id: 1, entrustNo: '20240114-GC-001', type: '气瓶', company: '上海某某气体公司', submitter: '张三', date: '01-14 10:00' },
          { id: 2, entrustNo: '20240114-SV-002', type: '安全阀', company: '江苏化工', submitter: '李四', date: '01-14 11:30' },
          { id: 3, entrustNo: '20240114-GC-005', type: '气瓶', company: '浙北石化', submitter: '王五', date: '01-13 16:00' },
        ];
        this.total = 30;
        this.listLoading = false;
        // 默认选中第一条
        if (this.taskList.length > 0) {
          this.selectTask(this.taskList[0]);
        }
      }, 300);
    },
    selectTask(item) {
      this.currentTask = item;
    },
    handlePageChange(page) {
      // 翻页逻辑
    },
    handlePass() {
      this.$confirm(`确认通过委托单 ${this.currentTask.entrustNo} 吗？`, "提示", {
        type: "success"
      }).then(() => {
        this.$message.success("审核通过");
        this.nextTask();
      });
    },
    handleReject() {
      this.rejectForm.reason = '';
      this.rejectOpen = true;
    },
    confirmReject() {
      this.$refs.rejectForm.validate(valid => {
        if (valid) {
          this.$message.warning("已退回");
          this.rejectOpen = false;
          this.nextTask();
        }
      });
    },
    prevTask() {
      // 切换上一条逻辑
    },
    nextTask() {
      // 切换下一条逻辑
      this.$message.info("切换到下一条");
    }
  }
};
</script>

<style scoped lang="scss">
.flex-container {
  display: flex;
  height: calc(100vh - 84px); /* 减去 RuoYi 顶栏高度 */
  padding: 0 !important; /* 去除默认 padding 填满 */
}

.left-panel {
  width: 320px;
  border-right: 1px solid #e6e6e6;
  display: flex;
  flex-direction: column;
  background: #fff;
  
  .panel-header {
    padding: 15px;
    border-bottom: 1px solid #f0f0f0;
  }
  
  .task-list {
    flex: 1;
    overflow-y: auto;
    
    .task-item {
      padding: 15px;
      border-bottom: 1px solid #f5f5f5;
      cursor: pointer;
      transition: background 0.2s;
      
      &:hover {
        background: #f9f9f9;
      }
      
      &.active {
        background: #e6f7ff;
        border-right: 3px solid #1890ff;
      }
      
      .task-title {
        display: flex;
        justify-content: space-between;
        font-weight: 500;
        margin-bottom: 5px;
      }
      
      .task-info {
        font-size: 13px;
        color: #666;
        margin-bottom: 5px;
        @include text-ellipsis; /* 假设有 mixin */
      }
      
      .task-meta {
        font-size: 12px;
        color: #999;
        display: flex;
        justify-content: space-between;
      }
    }
  }
  
  .pagination-mini {
    padding: 10px;
    text-align: center;
    border-top: 1px solid #f0f0f0;
  }
}

.right-panel {
  flex: 1;
  background: #f7f8fa;
  padding: 15px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  
  .audit-workspace {
    display: flex;
    flex-direction: column;
    height: 100%;
    
    .workspace-header {
      background: #fff;
      padding: 10px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-radius: 4px;
      margin-bottom: 10px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.05);
      
      .title {
        font-size: 16px;
        font-weight: bold;
      }
    }
    
    .workspace-content {
      flex: 1;
      background: #fff;
      padding: 20px;
      border-radius: 4px;
      overflow-y: auto;
      box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
  }
  
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #999;
  }
}
</style>
