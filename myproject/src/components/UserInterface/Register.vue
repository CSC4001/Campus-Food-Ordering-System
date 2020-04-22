<template>
<el-row type='flex' justify='center'>
<el-col span=12>
    <div style="text-align: center; padding: 10%;">
    <h1>Campus Food Ordering System</h1>
    <h1><small>校园订餐系统</small></h1>
    <h1><strong>Register</strong></h1>
    <el-form :model="registerForm" status-icon ref="registerForm" :rules="rules">
        <el-form-item label="Email" prop="email">
            <el-input v-model="registerForm.email" autocomplete="on"></el-input>
        </el-form-item>
        <el-form-item label="Username" prop="username">
            <el-input v-model="registerForm.username" autocomplete="on"></el-input>
        </el-form-item>
        <el-form-item label="Password" prop="password">
            <el-input type="password" v-model="registerForm.password" autocomplete="on"></el-input>
        </el-form-item>
        <el-form-item label="Confirm password" prop="password2">
            <el-input type="password" v-model="registerForm.password2" autocomplete="on"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button><router-link to='/login'>Cancel</router-link></el-button>
            <el-button type="primary" @click="submitForm('registerForm')">Confirm</el-button>
        </el-form-item>
    </el-form>
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
    name: 'register',
    data() {
        var validateEmail = (rule, value, callback) => {
            const mailReg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
            if (value === '') {
                callback(new Error('请输入邮箱'));
            } else {
                if (mailReg.test(value) && value.length >= 1 && value.length <= 254) {
                    callback();
                } else{
                    callback(new Error('请输入正确的邮箱'));
                }
            }
        };
        var validateUser = (rule, value, callback) => {
            const userReg = /^[a-zA-Z0-9_-]/;
            if (value === '') {
                callback(new Error('请输入用户名'));
            } else {
                if (userReg.test(value) && value.length >= 1 && value.length <= 20) {
                    callback();
                } else{
                    callback(new Error('请输入正确的用户名'));
                }
            }
        };
        var validatePass = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入密码'));
            } else if (value.length <= 8 || value.length >= 128){
                callback(new Error('密码长度在8-128之间'));
            } else
                {
                if (this.registerForm.password2 !== '') {
                    this.$refs.registerForm.validateField('password2');
                }
            callback();
            }
        };
        var validatePass2 = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请再次输入密码'));
            } else if (value !== this.registerForm.password) {
                callback(new Error('两次输入密码不一致!'));
            } else {
                callback();
            }
        };
        return{
            registerForm: {
                email: '',
                username: '',
                password: '',
                password2: '',
            },
            // Validate rules for form.
            rules: {
                email: [
                    { validator: validateEmail, trigger: 'blur' }
                ],
                username: [
                    { validator: validateUser, trigger: 'blur' }
                ],
                password: [
                    { validator: validatePass, trigger: 'blur' }
                ],
                password2: [
                    { validator: validatePass2, trigger: 'blur' }
                ]
            }
        };
    },
    methods: {
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    console.log(JSON.stringify(this.registerForm))
                    fetch("http://localhost:5000/api/register",{
                        method:"post",
                        headers:{
                            'content-type':'application/json'
                        },
                        body: JSON.stringify(this.registerForm)
                        }).then((r) => {
                            return r.json()
                        }).then((data) => {
                            console.log(data)
                            if (data.status == 'ok'){
                                // sessionStorage.setItem('accessToken',data.session)
                                this.$router.push({path:'/login'}).catch(err => {err})
                                this.$message.success(data.info);
                            }else{
                                this.$message.error(data.info);
                                return false;
                        }
                    })
                } else {
                    console.log('error submit!!');
                    return false;
                }
            })
        },
    },
}
</script>

<style>

</style>