<template>
    <div style="height:100%;">
    <el-container direction='vertical'>
        <el-header style="margin:1px;">
            <Header/> <!-- Fixed Header-->
        </el-header>
        <el-container>
            <el-aside width="15%">
                <Sidebar/> <!-- Fixed Sidebar-->
            </el-aside>
            <el-main>
                <!-- Alterable Main Content-->
                
                <p style="font-size: 25px;">Basic information</p>
                <el-row type="flex" justify="center">
                <el-col :span="8">
                <div style="text-align: center;">
                    <!-- Info Form-->
                    <el-avatar shape="square" :size=100 :src="squareUrl"></el-avatar>
                    <div>
                        <el-link>Modified avatar</el-link>
                        <p style="font-size: 40px;">{{infoForm.userName}}</p>
                        <el-form :model="infoForm" ref="infoForm" :rules="rules" label-width="auto" size="small">
                            <el-form-item label="ID" >
                                <el-input v-model="infoForm.user_id" :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="Email" prop="email">
                                <el-input v-model="infoForm.email"></el-input>
                            </el-form-item>
                            <el-form-item label="Password" prop="password">
                                <el-input type="password" v-model="infoForm.password"></el-input>
                            </el-form-item>
                            <el-form-item label="UserName" prop="userName">
                                <el-input v-model="infoForm.userName"></el-input>
                            </el-form-item>
                            <el-form-item label="Contact" prop="contact">
                                <el-input v-model="infoForm.contact"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-button type="primary" @click="onSubmit('infoForm')">Confirm</el-button>
                                <el-button @click="balanceVisible=true">Balance</el-button>
                                <el-button>Cancel</el-button>
                            </el-form-item>
                        </el-form>

                    </div>
                </div>
                <el-dialog title='Balance' :visible.sync='balanceVisible' width="50%">
                    <p>Available balance: {{infoForm.available}}</p>
                    <p>Frozen balance: {{infoForm.frozen}}</p>
                    <span>
                        <div class="sub-title">Deposit</div>
                        <el-input v-model.number="deposit"></el-input>
                        <el-button @click="submitDeposit()">Confirm</el-button>
                    </span>
                    <span>
                        <div class="sub-title">Withdraw</div>
                        <el-input v-model.number="withdraw"></el-input>
                        <el-button @click="submitWithdraw()">Confirm</el-button>
                    </span>
                    <span slot="footer" class="dialog-footer">
                        <el-button @click="balanceVisible = false">Cancel</el-button>
                    </span>
                </el-dialog>
                </el-col>
                </el-row>
            </el-main>
        </el-container>
    </el-container>   
    </div>
</template>

<script>
//Logic of validating the form:
//1. <el-form:rules="rules"> for rules in data
//2. prop for each form item
//3. props corresponding to rules. validator in rules is defined in data as well.
//4. fetch example can be visited in Register.vue, and axios example can be checked in PersonalInfo.vue
//5. reference link: https://developer.mozilla.org/zh-CN/docs/Web/API/Fetch_API
//                   https://blog.csdn.net/qq_41115965/article/details/80780264
import Vue from 'vue'
import Sidebar from '@/components/UserInterface/Sidebar'
import Header from '@/components/UserInterface/Header'
// import Main from '@/components/UserInterface/Main'
export default {
    name: 'Home',
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
        var validatePassword = (rule, value, callback) => {
            if (value === '') {
                callback();
            } else if(value.length <= 8 || value.length >= 128) {
                callback(new Error('密码长度在8-128之间'));
            } 
            callback();
        };
        var validateUserName = (rule, value, callback) => {
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
        var validateContact = (rule, value, callback) => {
            const userContact = /^[0-9]/;
            if (value === '') {
                callback(new Error('请输入手机号'));
            } else {
                if (userContact.test(value) && value.length === 11) {
                    callback();
                } else{
                    callback(new Error('请输入正确的手机号'));
                }
            }
        };
        return {
            deposit:"",
            withdraw:"",
            balanceVisible: false,
            squareUrl:"https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png",
            infoForm: {
                user_id: "",
                email: "",
                password: "",
                userName: "",
                contact: "",
                available: "",
                frozen: "",
                status: ""
            },
            rules: {
                email: [{ validator: validateEmail, trigger: 'blur' }],
                password: [{ validator: validatePassword, trigger: 'blur' }],
                userName: [{ validator: validateUserName, trigger: 'blur' }],
                contact: [{ validator: validateContact, trigger: 'blur' }],
            }
        };
    },
    methods: {
        submitDeposit() {
            fetch("http://localhost:5000/api/submitDeposit?id="+sessionStorage.getItem('accessToken'),{
                method:"post",
                headers:{
                    'content-type':'application/json'
                },
                body: JSON.stringify({"deposit":this.deposit})
            }).then((r) => {
                return r.json()
            }).then((data) => {
                if (data.status == 'ok'){
                    this.$message.success(data.info);
                    this.$data.infoForm.available = data.available;
                } else {
                    this.$message.error(data.info);
                    return false;
                }
            })
        },
        submitWithdraw() {
            fetch("http://localhost:5000/api/submitWithdraw?id="+sessionStorage.getItem('accessToken'),{
                method:"post",
                headers:{
                    'content-type':'application/json'
                },
                body: JSON.stringify({"withdraw":this.withdraw})
            }).then((r) => {
                return r.json()
            }).then((data) => {
                if (data.status == 'ok'){
                    this.$message.success(data.info);
                    this.$data.infoForm.available = data.available;
                } else {
                    this.$message.error(data.info);
                    return false;
                }
            })
        },
        // validate function for submiting modify
        onSubmit(formName){
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    console.log(JSON.stringify(this.infoForm))
                    fetch("http://localhost:5000/api/submitProsonalInfo",{
                        method:"post",
                        headers:{
                            'content-type':'application/json'
                        },
                        body: JSON.stringify(this.infoForm)
                        }).then((r) => {
                            return r.json()
                        }).then((data) => {
                            console.log(data)
                            if (data.status == 'ok'){
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
        }
    },
    created: function() {
        Vue.axios.get('http://localhost:5000/api/personalInfo',{
            params: {
                id: sessionStorage.getItem('accessToken')
            }
        }).then((response) => {
            console.log(response)
            var data = response.data
            this.$data.infoForm.user_id = data.user_id;
            this.$data.infoForm.email = data.email;
            this.$data.infoForm.userName = data.userName;
            this.$data.infoForm.contact = data.contact;
            this.$data.infoForm.available = data.available;
            this.$data.infoForm.frozen = data.frozen;
            this.$data.infoForm.status = data.status;
        })
    },
    components: {
        Header,
        Sidebar,
        // Main
    }
}
</script>

<style>

</style>