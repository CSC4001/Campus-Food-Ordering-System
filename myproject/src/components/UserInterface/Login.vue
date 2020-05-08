<template>
<el-row type='flex' justify='center'>
<el-col :span=12>
    <div style="text-align: center; padding: 10%;">
    <h1>Campus Food Ordering System</h1>
    <h1><small>校园订餐系统</small></h1>
    <h1><strong>Log in</strong></h1>
    <el-form :model="loginForm">
        <el-form-item label="Email">
            <el-input v-model="loginForm.email" autocomplete="on"></el-input>
        </el-form-item>
        <el-form-item label="Password">
            <el-input type="password" v-model="loginForm.password" autocomplete="on"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button @click="loginFormVisible = false">Cancel</el-button>
            <el-button type="primary" @click="submitForm">Confirm</el-button>
            <el-button type="primary"><router-link to="/register">Register</router-link></el-button>
        </el-form-item>
    </el-form>
    <footer class="text-center">
            <small> &copy; 2020 <a href="https://github.com/CSC4001/Campus-Food-Ordering-System" title="CSC4001 Project">Campus Food Ordering System</a> /
            </small>
            <p><a id="bottom" href="#" title="Go Top">&uarr;</a></p>
    </footer>
    </div>
</el-col>
</el-row>
</template>

<script>
//Logic of validating the form:
//1. <el-form:rules="rules"> for rules in data
//2. prop for each form item
//3. props corresponding to rules. validator in rules is defined in data as well.
//4. fetch example can be visited in Register.vue, and axios example can be checked in PersonalInfo.vue
//5. reference link: https://developer.mozilla.org/zh-CN/docs/Web/API/Fetch_API
//                   https://blog.csdn.net/qq_41115965/article/details/80780264
export default {
    name: 'login',
    data() {
        return{
            loginForm: {
                email: '',
                password: ''
            }
        };
    },
    methods: {
        submitForm() {
            fetch("http://localhost:5000/api/login",{
                method:"post",
                headers:{
                    'content-type':'application/json'
                },
                body: JSON.stringify(this.loginForm)
                }).then((r) => {
                return r.json()  //
                }).then((data) => {
                if (data.status == 'ok'){
                    sessionStorage.setItem('accessToken',data.session)
                    this.$router.push({path:'/'}).catch(err => {err})
                    this.$message.success(data.info);
                } else if (data.status == 'admin') {
                    sessionStorage.setItem('accessToken',data.session)
                    this.$router.push({path:'/admin'}).catch(err => {err})
                    this.$message.success('welcome back, admin!');
                } else {
                    this.$message.error(data.info);
                    return false;
                }
            })
        },
    },
}
</script>

<style>

</style>