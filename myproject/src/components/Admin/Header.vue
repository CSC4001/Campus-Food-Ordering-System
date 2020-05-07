<template>
<div style="height:100%;">
    <el-menu :default-active="activeIndex" mode="horizontal" justify="start" align="middle" @select="handleSelect">
        <el-menu-item index="1"><el-link href="http://localhost:8080/#/admin" v-on:click="test">Front Page</el-link></el-menu-item>
        <el-menu-item index="2"><el-link href="http://localhost:8080/#/admin/usermanagement">User Management</el-link></el-menu-item>
        <el-menu-item index="3"><el-link href="http://localhost:8080/#/admin/shopmanagement">Shop Management</el-link></el-menu-item>
        <el-menu-item index="4"><el-link href="http://localhost:8080/#/admin/ordermanagement">Order Management</el-link></el-menu-item>
        <!-- sign in button -->
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
        loginFormVisible: false,
        registFormVisible: false,
        loginForm: {
            email: '',
            password: ''
        },
        registForm: {
          email: '',
          password: '',
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
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('submit!');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
    },
    components: {
    },
}
</script>
