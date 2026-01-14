<template>
  <div class="app-container">
    <el-card shadow="never">
      <div slot="header" class="clearfix">
        <span>原始记录录入 - {{ form.entrustNo }}</span>
        <div style="float: right;">
           <el-button type="primary" size="mini" @click="handleSubmit">提交审核</el-button>
           <el-button size="mini" @click="handleSave">暂存</el-button>
           <el-button size="mini" @click="handleBack">返回</el-button>
        </div>
      </div>
      
      <el-form ref="form" :model="form" :rules="rules" label-width="120px">
        <!-- 基础信息区 -->
        <h4 class="section-title">样品基础信息</h4>
        <el-row>
          <el-col :span="8">
            <el-form-item label="样品名称">
              <el-input v-model="form.sampleName" disabled />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="样品编号">
              <el-input v-model="form.sampleNo" disabled />
            </el-form-item>
          </el-col>
          <el-col :span="8">
             <el-form-item label="出厂编号">
              <el-input v-model="form.factoryNo" disabled />
            </el-form-item>
          </el-col>
        </el-row>
        
        <!-- 环境参数区 -->
        <h4 class="section-title">检测环境条件</h4>
        <el-row>
          <el-col :span="8">
            <el-form-item label="温度(℃)" prop="temperature">
              <el-input-number v-model="form.temperature" :precision="1" :step="0.1"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="湿度(%)" prop="humidity">
              <el-input-number v-model="form.humidity" :min="0" :max="100"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
             <el-form-item label="大气压(kPa)" prop="pressure">
              <el-input-number v-model="form.pressure"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        
        <!-- 核心检测数据区 (动态表单) -->
        <h4 class="section-title">检测数据记录</h4>
        <el-table :data="form.testItems" border style="width: 100%" size="small">
          <el-table-column label="检测项目" prop="name" width="200"></el-table-column>
          <el-table-column label="技术要求" prop="requirement" width="250"></el-table-column>
          <el-table-column label="实测值" width="200">
             <template slot-scope="scope">
               <el-input v-model="scope.row.value" placeholder="请输入数值/结果"></el-input>
             </template>
          </el-table-column>
          <el-table-column label="单项结论">
            <template slot-scope="scope">
               <el-radio-group v-model="scope.row.result" size="mini">
                 <el-radio label="pass">合格</el-radio>
                 <el-radio label="fail">不合格</el-radio>
               </el-radio-group>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 图片上传区 -->
        <h4 class="section-title">现场照片 / 图谱附件</h4>
        <el-form-item label="上传附件">
          <!-- 这里使用 Element 的 Upload 组件，实际需对接文件上传接口 -->
          <el-upload
            action="#"
            list-type="picture-card"
            :auto-upload="false">
              <i slot="default" class="el-icon-plus"></i>
              <div slot="file" slot-scope="{file}">
                <img class="el-upload-list__item-thumbnail" :src="file.url" alt="">
                <span class="el-upload-list__item-actions">
                  <span class="el-upload-list__item-preview" @click="handlePictureCardPreview(file)">
                    <i class="el-icon-zoom-in"></i>
                  </span>
                  <span class="el-upload-list__item-delete" @click="handleRemove(file)">
                    <i class="el-icon-delete"></i>
                  </span>
                </span>
              </div>
          </el-upload>
          <el-dialog :visible.sync="dialogVisible">
            <img width="100%" :src="dialogImageUrl" alt="">
          </el-dialog>
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input type="textarea" v-model="form.remark"></el-input>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "RecordEntry",
  data() {
    return {
      form: {
        entrustNo: '20240114-GC-001',
        sampleName: '工业用氧气瓶',
        sampleNo: 'S-2024-001',
        factoryNo: 'FAC-888',
        temperature: 24.5,
        humidity: 60,
        pressure: 101,
        remark: '',
        testItems: [
          { name: '外观检查', requirement: '无明显锈蚀、变形', value: '', result: 'pass' },
          { name: '音响检查', requirement: '音响清脆', value: '', result: 'pass' },
          { name: '公称工作压力', requirement: '15 MPa', value: '', result: 'pass' },
          { name: '水压试验压力', requirement: '22.5 MPa', value: '', result: 'pass' }
        ]
      },
      rules: {
        temperature: [{ required: true, message: "请输入温度", trigger: "blur" }]
      },
      dialogImageUrl: '',
      dialogVisible: false
    };
  },
  methods: {
    handleSubmit() {
      this.$confirm('确认提交原始记录吗？提交后将进入审核流程。', '提示', {
        type: 'warning'
      }).then(() => {
        this.$message.success('提交成功');
        this.handleBack();
      });
    },
    handleSave() {
      this.$message.success('暂存成功');
    },
    handleBack() {
      this.$router.go(-1); // 或者跳转回任务列表
    },
    handleRemove(file) {
      console.log(file);
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    }
  }
};
</script>

<style scoped>
.section-title {
  border-left: 4px solid #1890ff;
  padding-left: 10px;
  margin: 20px 0;
  font-size: 16px;
  color: #303133;
}
</style>
