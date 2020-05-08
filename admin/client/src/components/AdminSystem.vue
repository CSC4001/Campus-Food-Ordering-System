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
import Header from '@/components/Header.vue';
import Sidebar from '@/components/Sidebar.vue';
import AdminSystemMain from '@/components/AdminSystemMain.vue';

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
