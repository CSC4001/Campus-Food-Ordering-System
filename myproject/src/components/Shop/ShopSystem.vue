<template>
  <div style="height:100%;">
    <el-container direction='vertical'>
      <el-header style="margin:1px;">
        <ShopHeader/> <!-- Fixed Header-->
      </el-header>
      <el-container>
        <el-aside width="15%">
          <ShopSidebar/> <!-- Fixed Sidebar-->
        </el-aside>
        <el-main>
          <ShopSystemMain/> <!-- Alterable Main Content-->
        </el-main>
      </el-container>
    </el-container>   
  </div>
</template>

<script>
  import ShopHeader from '@/components/Shop/Header'
  import ShopSidebar from '@/components/Shop/Sidebar'
  import ShopSystemMain from '@/components/Shop/ShopSystemMain'

  export default {
    name: 'ShopSystem',

    data() {
      return {

      };
    },
    methods: {

    },
    components: {
      ShopHeader,
      ShopSidebar,
      ShopSystemMain,
    },

  };
</script>


<style>
  .verticalBar {
      width: 2px;
      height: 600px;
      background: grey;
      display: inline-block;
      margin-top: 10px;
      vertical-align: top;
      margin-right: 29px;
      margin-left: 30px;
  }
  .demo-infinite-container {
    border: 1px solid #e8e8e8;
    border-radius: 4px;
    overflow: auto;
    padding: 8px 24px;
    height: 300px;
  }
  .demo-loading-container {
    position: absolute;
    bottom: 40px;
    width: 100%;
    text-align: center;
  }

</style>

