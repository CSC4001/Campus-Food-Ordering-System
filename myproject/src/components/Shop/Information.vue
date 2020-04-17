<template>
  <div>
  <el-container direction='vertical'>
      <el-header style="margin:1px;">
        <ShopHeader/> <!-- Fixed Header-->
      </el-header>
      <el-container>
        <el-aside width="15%">
          <ShopSidebar/> <!-- Fixed Sidebar-->
        </el-aside>
        <el-main>
          <InformationMain/> <!-- Alterable Main Content-->
        </el-main>
      </el-container>
    </el-container>   
  </div>
</template>


<script>
  import ShopHeader from '@/components/Shop/Header'
  import ShopSidebar from '@/components/Shop/Sidebar'
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
      ShopHeader,
      ShopSidebar,
      InformationMain,
    },
  };
</script>



