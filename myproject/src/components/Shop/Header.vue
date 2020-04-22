<template>
<div style="height:100%;">
    <el-menu :default-active="activeIndex" mode="horizontal" justify="start" align="middle" @select="handleSelect">
        <el-menu-item index="1"><el-link href="http://localhost:8080/#/shopsystem" v-on:click="test">Front Page</el-link></el-menu-item>
        <el-menu-item index="2"><el-link href="http://localhost:8080/#/shop/dishesmanagement">Dishes Management</el-link></el-menu-item>
        <el-menu-item index="3"><el-link href="http://localhost:8080/#/shop/ordermanagement">Order Management</el-link></el-menu-item>
        <el-menu-item index="4"><el-link href="http://localhost:8080/#/shop/information">Infomation</el-link></el-menu-item>
        <el-button @click="logout">Log out</el-button>
    </el-menu>
</div>
</template>

<script>
export default {
    name: 'Header',
     data() {
      return {
        activeIndex: '1',
      };
    },
    methods: {
        handleSelect(key, keyPath) {
            console.log(key, keyPath);
        },
        handleOpen(key, keyPath) {
            console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);
        },
        logout() {
            sessionStorage.removeItem('accessToken');
            this.$router.push({path:'/login'}).catch(err => {err})
        },
    },
    components: {
    },
}
</script>
