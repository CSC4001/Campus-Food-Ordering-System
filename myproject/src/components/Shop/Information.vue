<template>
  <div>
  <el-container direction='vertical'>
      <el-header style="margin:1px;">
        <Header/> <!-- Fixed Header-->
      </el-header>
      <el-container>
        <el-aside width="15%">
          <Sidebar/> <!-- Fixed Sidebar-->
        </el-aside>
        <el-main>
          <InformationMain/> <!-- Alterable Main Content-->
        </el-main>
      </el-container>
    </el-container>   
  </div>
</template>


<script>
  import Header from '@/components/Shop/Header'
  import Sidebar from '@/components/Shop/Sidebar'
  import InformationMain from '@/components/Shop/InformationMain'

  export default {
    name: 'Information',
    data() {
      return {

      };
    },

    methods: {

    },
    components: {
      Header,
      Sidebar,
      InformationMain,
    },
  };
</script>



