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
          <el-row type="flex" justify="center">    
            <el-col :span=10>
              <div>
                <a-list item-layout="vertical" size="large" :pagination="pagination" :data-source="favouriteData">
                  <a-list-item slot="renderItem" key="item.shop_id" slot-scope="item">
                      <el-button type="text" @click="handleShopURL(item.shop_id)"> {{ item.shop_name }} </el-button>
                  </a-list-item>
                 </a-list>
              </div>
            </el-col>
                <!-- content end -->
            </el-row>
        </el-main>
      </el-container>
    </el-container>   
  </div>
</template>

<script>
import Sidebar from '@/components/UserInterface/Sidebar'
import Header from '@/components/UserInterface/Header'
import Vue from 'vue'
export default {
    name: 'Favourite',
    data() {
        return {
            favouriteData: [],
            pagination: {
                onChange: page => {
                console.log(page);
                },
                pageSize: 3,
            },
        };
    },
    beforeMount() {
      Vue.axios.get('/api/getFavourite',{
        params: {
          'user_id': sessionStorage.getItem('accessToken'),
        }
      }).then((response) => {
        var data = response.data
        this.favouriteData = data
        console.log(data)
        // this.favouriteData = data.data.list
      })
    },
    methods: {
        handleShopURL(id) {
        let shopid=id
        this.$router.push({path:`/shops/${shopid}`}).catch(err => {err})
      },

    },
    components: {
        Header,
        Sidebar,
    }
}
</script>

<style>

</style>