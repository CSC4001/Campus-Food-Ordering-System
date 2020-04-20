<template>
<div style="height:100%;">
    <el-menu :default-active="activeIndex" mode="horizontal" justify="start" align="middle" @select="handleSelect">
        <el-menu-item index="1"><el-link href="http://localhost:8080/#/shopsystem" v-on:click="test">Front Page</el-link></el-menu-item>
        <el-menu-item index="2"><el-link href="http://localhost:8080/#/shop/dishesmanagement">Dishes Management</el-link></el-menu-item>
        <el-menu-item index="3"><el-link href="http://localhost:8080/#/shop/ordermanagement">Order Management</el-link></el-menu-item>
        <el-menu-item index="4"><el-link href="http://localhost:8080/#/shop/information">Infomation</el-link></el-menu-item>
        <!-- sign in button -->
        <el-button @click="loginFormVisible = true">Sign in</el-button>
        <el-dialog title="Sign in" :visible.sync="loginFormVisible">
          <el-form :model="loginForm">
            <el-form-item label="Email">
              <el-input v-model="loginForm.email" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="Password">
              <el-input v-model="loginForm.password" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button @click="loginFormVisible = false">cancel</el-button>
              <el-button type="primary" @click="submitForm('form')">confirm</el-button>
            </el-form-item>
          </el-form>
        </el-dialog>
        <!-- sign up button -->
        <el-button @click="registFormVisible = true">Sign up</el-button>
        <el-dialog title="Sign up" :visible.sync="registFormVisible">
          <el-form :model="registForm">
            <el-form-item label="Email">
              <el-input v-model="registForm.email" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="Password">
              <el-input v-model="registForm.password" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button @click="registFormVisible = false">cancel</el-button>
              <el-button type="primary" @click="submitForm('form')">confirm</el-button>
            </el-form-item>
          </el-form>
        </el-dialog>
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
