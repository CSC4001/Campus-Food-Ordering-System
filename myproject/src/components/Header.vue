<template>
  <el-row>
    <el-col :span="20">
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <el-menu-item index="1">Front Page</el-menu-item>
        <el-menu-item index="2">
          <template slot="title">Diligentia College</template>
        </el-menu-item>
        <el-menu-item index="3">Shaw College</el-menu-item>
        <el-menu-item index="4">Student Centre</el-menu-item>
        <el-menu-item index="5">LeTian Building</el-menu-item>
      </el-menu>
    </el-col>
    <el-col :span="4">
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <el-menu-item index="1">Sign in</el-menu-item>
        <el-menu-item index="2">
          <template slot="title">Sign up</template>
        </el-menu-item>
      </el-menu>
    </el-col>
  </el-row>
  
</template>

<script>
  export default {
    name: 'Header',
    data() {
      return {
        activeIndex: '1',
        activeIndex2: '1'
      };
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      }
    }
  }
</script>