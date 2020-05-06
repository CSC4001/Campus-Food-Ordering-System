<template>
<div style="overflow:hidden;">
<el-row class="tac" style="height:100%;">
    <el-col style="height:100%;">
        <el-menu
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose" style="height:100%;">
        <el-menu-item index="1">
            <i class="el-icon-menu"></i>
            <span slot="title">Help</span>
        </el-menu-item>
        <router-link to="/">
        <el-menu-item index="2">
            <i class="el-icon-menu"></i>
            <span slot="title">Back to Previous</span>
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

