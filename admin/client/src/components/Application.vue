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
          <ApplicationMain/> <!-- Alterable Main Content-->
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Header from '@/components/Header.vue';
import Sidebar from '@/components/Sidebar.vue';
import ApplicationMain from '@/components/ApplicationMain.vue';

export default {
  name: 'Application',

  data() {
    return {

    };
  },
  methods: {

  },
  components: {
    Header,
    Sidebar,
    ApplicationMain,
  },

};
</script>
