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
          <AdminSystemMain/> <!-- Alterable Main Content-->
        </el-main>
      </el-container>
    </el-container>   
  </div>
</template>

<script>
  import Header from '@/components/Admin/Header'
  import Sidebar from '@/components/Admin/Sidebar'
  import AdminSystemMain from '@/components/Admin/AdminSystemMain'

  export default {
    name: 'AdminSystem',

    data() {
      return {

      };
    },
    methods: {

    },
    components: {
      Header,
      Sidebar,
      AdminSystemMain,
    },

  };
</script>
