<template>
<div class="sidebar">
<el-row class="tac" style="height:100%;">
    <el-col style="height:100%;">
        <el-menu
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose" style="height:100%;">
        
        <router-link to="/personalinfo">
            <el-menu-item index="1">
                <i class="el-icon-menu"></i>
                <span slot="title">Personal Info</span>
            </el-menu-item>
        </router-link>

        <router-link to="/favourite">
            <el-menu-item index="2">
                <i class="el-icon-menu"></i>
                <span slot="title">Favourite</span>
            </el-menu-item>
        </router-link>

        <router-link to="/personalinfo">
            <el-menu-item index="3">
                <i class="el-icon-menu"></i>
                <span slot="title">Help</span>
            </el-menu-item>
        </router-link>

        <router-link to="/myorder">
            <el-menu-item index="4">
                <i class="el-icon-menu"></i>
                <span slot="title">My Order</span>
            </el-menu-item>
        </router-link>

        <router-link to="/myshop">
            <el-menu-item index="5">
                <i class="el-icon-menu"></i>
                <span slot="title">My Shop</span>
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
      },
      toPI() {
        this.$router.push('/personalinfo');
      }
    }
  }
</script>


<style>
    .sidebar {
        overflow:hidden;
    }
</style>