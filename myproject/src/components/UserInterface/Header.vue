<template>
<div class = "header" style="height:100%;">
    <el-menu :default-active="activeIndex" mode="horizontal" justify="start" align="middle" @select="handleSelect">
        <el-menu-item index="1">Front Page</el-menu-item>
        <el-menu-item index="2">Diligentia College</el-menu-item>
        <el-menu-item index="3">Shaw College</el-menu-item>
        <el-menu-item index="4">Student Centre</el-menu-item>
        <el-menu-item index="5">LeTian Building</el-menu-item>
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
                <el-button @click="registerFormVisible = true">Register</el-button>
                <el-button @click="loginFormVisible = false">Cancel</el-button>
                <el-button type="primary" @click="submitForm('form')">Confirm</el-button>
            </el-form-item>
        </el-form>
        </el-dialog>
        <el-dialog title="Sign in" :visible.sync="registerFormVisible">
        <el-form :model="registerForm">
            <el-form-item label="Email">
            <el-input v-model="registerForm.email" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="Password">
            <el-input v-model="registerForm.password" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item>
            <el-button @click="registerFormVisible = false">Cancel</el-button>
            <el-button type="primary" @click="submitForm('form')">Confirm</el-button>
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
        activeIndex2: '1',
        loginFormVisible: false,
        registerFormVisible: false,
        loginForm: {
            email: '',
            password: ''
        },
        registerForm: {
            email: '',
            password: ''
        },
        formSearch: {
          searchtype: '',
          searchkey: '',

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
      onSubmit() {
        console.log('submit!');
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