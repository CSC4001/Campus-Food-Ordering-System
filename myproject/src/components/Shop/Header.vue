<template>
<div style="height:100%; overflow:hidden;">
    <el-menu :default-active="activeIndex" mode="horizontal" justify="start" align="middle" @select="handleSelect">
        <el-menu-item index="1"><router-link to="/shopsystem">Front Page</router-link></el-menu-item>
        <el-menu-item index="2"><router-link to="/shop/dishesmanagement">Dishes Management</router-link></el-menu-item>
        <el-menu-item index="3"><router-link to="/shop/ordermanagement">Order Management</router-link></el-menu-item>
        <el-menu-item index="4"><router-link to="/shop/information">Information</router-link></el-menu-item>
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
        shop_id: '',
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
            sessionStorage.clear();
            this.$message.success('You have successfully logout');
            this.$router.push({path:'/login'}).catch(err => {err})
        },
    },
    components: {
    },
    created() {
        this.$data.shop_id = sessionStorage.getItem('shop_id')
    },
}
</script>
