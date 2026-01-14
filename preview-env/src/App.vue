<template>
  <div id="app">
    <el-container style="height: 100vh;">
      <el-aside width="220px" style="background-color: #304156; color: #fff;">
        <div style="padding: 20px; font-weight: bold; font-size: 18px; text-align: center;">
          西自仪 LIMS
        </div>
        <el-menu
          default-active="entrust"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
          router
        >
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-s-cooperation"></i>
              <span>特种设备检测</span>
            </template>
            <el-menu-item index="/special-equipment/entrust">委托管理</el-menu-item>
            <el-menu-item index="/special-equipment/record-entry">原始记录录入</el-menu-item>
            <el-menu-item index="/special-equipment/audit">审核工作台</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      
      <el-container>
        <el-header style="text-align: right; font-size: 12px; border-bottom: 1px solid #e6e6e6; line-height: 60px;">
          <el-dropdown>
            <i class="el-icon-setting" style="margin-right: 15px"></i>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>个人中心</el-dropdown-item>
              <el-dropdown-item>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <span>Admin</span>
        </el-header>
        
        <el-main style="background-color: #f0f2f5; padding: 20px;">
          <router-view/>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style>
body { margin: 0; padding: 0; }
.app-container {
  padding: 20px;
  background-color: #fff;
  border-radius: 4px;
  min-height: calc(100vh - 100px);
}
</style>
