<template>
  <div class="sidebar">
    <el-row class="tac" style="height:100%;">
      <el-col style="height:100%;">
        <el-menu
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose" style="height:100%;">
        <router-link to="/admin/openapplication">
          <el-menu-item index="1">
            <i class="el-icon-menu"></i>
            <span slot="title">Open Shop Application</span>
          </el-menu-item>
        </router-link>
        <router-link to="/admin/closeapplication">
          <el-menu-item index="2">
            <i class="el-icon-menu"></i>
            <span slot="title">Close Shop Application</span>
          </el-menu-item>
        </router-link>
        </el-menu>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  export default {
    name: 'Sidebar',
    methods: {
      handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      }
    }
  }
</script>

<style>
    .sidebar {
        overflow:hidden;
    }
</style>
