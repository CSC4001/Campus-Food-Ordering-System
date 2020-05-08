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

        </el-main>
      </el-container>
    </el-container>
   </div>
</template>

<script>
import Vue from 'vue'
import Sidebar from '@/components/UserInterface/Sidebar'
import Header from '@/components/UserInterface/Header'

export default {
  data() {
    return {
      
    }
  },
  methods: {
    
  },
  created() {
    
  },
  components: {
    Header,
    Sidebar,
  }
}
</script>

<style>

</style>