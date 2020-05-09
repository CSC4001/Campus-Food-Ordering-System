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
          <h3>Search Result for {{searchType}}: {{searchKey}}</h3>
          <el-col :span="10">
            <a-list
              v-if="searchType=='shop'"
              :dataSource="shopData"
              :header="`${shopData.length} ${shopData.length > 1 ? 'results' : 'result'}`"
              itemLayout="vertical"
            >
              <a-list-item slot="renderItem" slot-scope="item">
                <a-list-item-meta style='word-wrap:break-word;'
                  :description = "item.shop_info"
                >
                  <span slot="title" @click="handleShopURL(item.shop_id)">{{ item.shop_name }}</span>
                </a-list-item-meta>        
              </a-list-item>
            </a-list>
            <a-list
              v-if="searchType=='dishes'"
              :dataSource="shopData"
              :header="`${shopData.length} ${shopData.length > 1 ? 'results' : 'result'}`"
              itemLayout="vertical"
            >
              <a-list-item slot="renderItem" slot-scope="item">
                <a-list-item-meta style='word-wrap:break-word;'
                  :description = "item.product_info"
                >
                  <span slot="title" @click="handleShopURL(item.shop_id)">{{ item.product_name }}</span>
                </a-list-item-meta>
              </a-list-item>
            </a-list>
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
    handleShopURL(id){
      this.$router.push({path:`/shops/${id}`}).catch(err => {err})
    }
  },
  created() {
    this.searchKey = this.$route.params.searchKey
    this.searchType = this.$route.params.searchType
    Vue.axios.get('/api/getSearch', {
      params: {
        'searchKey': this.searchKey,
        'searchType': this.searchType
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