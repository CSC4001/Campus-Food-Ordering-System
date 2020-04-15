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
                <div style="text-align: center;">
                    <el-avatar shape="square" :size=100 :src="squareUrl"></el-avatar>
                    <div>
                        <el-link>Modified avatar</el-link>
                        <p style="font-size: 40px;">User Name</p>
                        <el-form :model="infoForm" ref="infoForm" label-width="auto" size="small">
                            <el-form-item label="ID">
                                <el-input v-model="infoForm.id"></el-input>
                            </el-form-item>
                            <el-form-item label="Email">
                                <el-input v-model="infoForm.email"></el-input>
                            </el-form-item>
                            <el-form-item label="Password">
                                <el-input v-model="infoForm.password"></el-input>
                            </el-form-item>
                            <el-form-item label="UserName">
                                <el-input v-model="infoForm.userName"></el-input>
                            </el-form-item>
                            <el-form-item label="PhoneNumber">
                                <el-input v-model="infoForm.phoneCode"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-button type="primary" @click="onSubmit">Confirm</el-button>
                                <el-button>Cancel</el-button>
                            </el-form-item>
                        </el-form>
                        
                    </div>
                </div>
                
            </el-main>
        </el-container>
    </el-container>   
    </div>
</template>

<script>
import Sidebar from '@/components/UserInterface/Sidebar'
import Header from '@/components/UserInterface/Header'
// import Main from '@/components/UserInterface/Main'
export default {
    name: 'Home',
    data() {
        return {
            squareUrl:"https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png",
            infoForm: {
                id: "test",
                email: "test@test.com",
                password: "testtest",
                userName: "test",
                phoneCode: '1234567890',
            }
        };
    },
    methods: {
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