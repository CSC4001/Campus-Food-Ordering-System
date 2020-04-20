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
          <SystemMain/> <!-- Alterable Main Content-->
        </el-main>
      </el-container>
    </el-container>   
  </div>
</template>

<script>
  import Header from '@/components/Shop/Header'
  import Sidebar from '@/components/Shop/Sidebar'
  import SystemMain from '@/components/Shop/ShopSystemMain'

  export default {
    name: 'ShopSystem',

    data() {
      return {

      };
    },
    methods: {

    },
    components: {
      Header,
      Sidebar,
      SystemMain,
    },

  };
</script>
