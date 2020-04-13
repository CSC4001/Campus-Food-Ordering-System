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
                <Main/> <!-- Alterable Main Content-->
            </el-main>
        </el-container>
    </el-container>   

    </div>
</template>

<script>
import Sidebar from '@/components/Sidebar'
import Header from '@/components/Header'
import Main from '@/components/Main'
export default {
    name: 'Home',
    data() {
        return {
        };
    },
    methods: {
    },
    components: {
        Header,
        Sidebar,
        Main
    }
}
</script>

<style>

</style>