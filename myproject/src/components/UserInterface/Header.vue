<template>
<div class = "header" style="height:100%;">
    <el-menu :default-active="activeIndex" mode="horizontal" justify="start" align="middle" @select="handleSelect">
        <el-menu-item index="1"><router-link to="/">Front Page</router-link></el-menu-item>
        <el-menu-item index="2">Diligentia College</el-menu-item>
        <el-menu-item index="3">Shaw College</el-menu-item>
        <el-menu-item index="4">Student Centre</el-menu-item>
        <el-menu-item index="5">LeTian Building</el-menu-item>
        <el-button @click="logout" style="margin-top:10px">Log out</el-button>
    </el-menu>
</div>
</template>

<script>
export default {
    name: 'Header',
     data() {
      return {
        activeIndex: '1',
        activeIndex2: '1',
        formSearch: {
          searchtype: '',
          searchkey: '',
        },
      };
    },
    methods: {
        logout() {
            sessionStorage.removeItem('accessToken');
            this.$message.success('You have successfully logout');
            this.$router.push({path:'/login'}).catch(err => {err});
        },
        handleSelect(key, keyPath) {
            console.log(key, keyPath);
        },
        handleOpen(key, keyPath) {
            console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);
        },
    },
    components: {
    },
}
</script>

<style>
    .header {
        overflow:hidden;
    }
</style>