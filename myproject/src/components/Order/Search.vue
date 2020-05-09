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
          <!--h3>{{shopData.name}}</h3-->
          <h1>Name</h1>
          <el-col :span='2'>
            <p>ID:</p>
          </el-col>
          <el-col :span='2'>
            <el-button type="text" @click="favourite()">Favoutite</el-button>
          </el-col>  
          <el-col>
            <el-row>
              <el-col :span="10"></el-col>

              <el-col :span="10"></el-col>
            </el-row>
          </el-col>
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
  name:'Search',
  data() {
    return {
      searchKey: '',
      shopData: [],
    }
  },
  methods: {
    
  },
  created() {
    this.searchKey = this.$route.params.searchKey
    this.searchType = this.$route.params.searchType
    Vue.axios.get('/api/getDishes', {
      params: {
        searchKey: searchKey,
        searchType: searchType
      }
    }).then((response) => {
      var data = response.data
      this.shopData = data
    })
  },
  components: {
    Header,
    Sidebar,
  }
}
</script>

<style>

</style>