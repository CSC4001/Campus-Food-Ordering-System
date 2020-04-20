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
          <ShopManagementMain/> <!-- Alterable Main Content-->
        </el-main>
      </el-container>
    </el-container>   
  </div>
</template>

<script>
  import Header from '@/components/Admin/Header'
  import Sidebar from '@/components/Admin/Sidebar'
  import ShopManagementMain from '@/components/Admin/ShopManagementMain'

  export default {
    name: 'ShopManagement',

    data() {
      return {

      };
    },
    methods: {

    },
    components: {
      Header,
      Sidebar,
      ShopManagementMain,
    },

  };
</script>
