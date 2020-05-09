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
          <el-row>
            <!-- shop info  -->
            <el-col :span="4">
              <h1>Name</h1>
              <p>ID:</p>
              <p>rate:</p>          
              <el-button type="text" @click="favourite()">Favoutite</el-button>
            </el-col>
            <!-- search -->
            <el-col :span="6" :offset="2">
              <a-input-search placeholder="input search text" @search="onSearch" enterButton />
              <br /><br />
            </el-col>
            <!-- shopping cart  -->
            <el-col :span="4" :offset="2">
              <el-button @click="drawer = true" type="primary" style="margin-left: 16px;">
                Shopping cart
              </el-button>
              <el-drawer
                title="我是标题"
                :visible.sync="drawer"
                :direction="direction">
                <span>我来啦!</span>
              </el-drawer>
            </el-col>
          </el-row>
          <el-row type="flex" justify="center">
            <el-col :span="20">
              <!-- dishes list -->
              <a-list item-layout="vertical"
              :grid="{gutter: 20, column: 3}"
              :size="large" 
              :pagination="pagination" 
              :data-source="listData">
                <a-list-item slot="renderItem" key="item.title" slot-scope="item">
                  <a-card >
                    <el-row type="flex" justify="space-between">
                      <el-col>
                        <span>Name:</span><span>
                          <el-button type="text" size="mini" @click="viewDetail(item)">{{ item.name }}</el-button>
                        </span>
                        <el-dialog
                        :visible.sync="dishDialogVisible"
                        width="30%"
                        center>
                        <span>Name:</span><span>{{dishDetails.product_name}}</span>
                        <span slot="footer" class="dialog-footer">
                          <el-button type="primary" @click="dishDialogVisible = false">Confirm</el-button>
                        </span>
                        </el-dialog>
                        <br>
                      </el-col>
                      <el-col>
                        <span>Rate:</span><span>{{item.rate}}</span>
                        <br>
                        <span>Sales:</span><span>{{item.sales}}</span>
                      </el-col>
                    </el-row>
                    <el-row type="flex" justify="end">
                      <el-col>
                          <el-input-number size="mini" v-model="item.count"></el-input-number>
                      </el-col>
                    </el-row>
                  </a-card>
                </a-list-item>
              </a-list>
            </el-col>
          </el-row>
        </el-main>
      </el-container>
    </el-container>
   </div>
</template>

<script>
// import Vue from 'vue'
import Sidebar from '@/components/UserInterface/Sidebar'
import Header from '@/components/UserInterface/Header'

const listData = [];
for (let i = 0; i < 23; i++) {
  listData.push({
    name: `dishes ${i}`,
    rate: '5.0',
    sales: i,
    count: 0,
  });
}

export default {
  data() {
    return {
      shop_info: {
        shop_id:'',
        shop_name:'',
        shop_rate: '',
      },
      dishes: {

      },
      dishDetails: {
        product_name: '',
        product_price: '',
        product_info: '',
      },
      dishDialogVisible: false,
      shopping_cart: [],
      listData,
      pagination: {
        onChange: page => {
          console.log(page);
        },
        pageSize: 6,
      },
      direction: "btt",
      drawer: false,

    }
  },
  methods: {
    favourite(){

    },
    onSearch(){

    },
    viewDetail(item){
      this.dishDetails.product_name=item.name
      this.dishDialogVisible = true
    },
    
  },
  created() {
    // var shop_id = this.$route.params.shopid
    //get all info
    // Vue.axios.get('/api/getShopInfo', {
    //   params: {
    //     id: shop_id
    //   }
    // }).then((Response) => {
    //   var data = response.data
    // })
    
  },
  components: {
    Header,
    Sidebar,
  }
}
</script>

<style>

</style>