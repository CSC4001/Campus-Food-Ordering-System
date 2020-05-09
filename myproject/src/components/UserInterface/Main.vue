<template>
  <el-col>
      <!-- upper content -->
    <el-row>
      <!-- recommended shop -->
      <el-col :span="10">
          <div style="background-color: #ececec; padding: 20px;">
            <!--a-list :dataSource="shopData" :grid="{ column: 3 }">
              <a-list-item slot="renderItem" slot-scope="item">
                <el-card class="box-card" 
                  :body-style="{ padding: '0px', }" 
                  @click.native='gotoShop(item.shop_id)'
                >
                  <div slot="header" class="clearfix">
                    <span style='overflow:hidden'>{{item.shop_name}}</span>
                  </div>
                  <span style='overflow:hidden'>{{item.shop_info}}</span>
                </el-card>
                <br/>
              </a-list-item>
            </a-list-->
            <el-carousel height="200px" 
              ref='poster' 
              indicator-position='outside' 
              @click.native='gotoShop("poster")'
            >
              <el-carousel-item v-for="(item, index) in shopData" :key="index">
                <p>{{ item.shop_name }}</p>
              </el-carousel-item>
            </el-carousel>
          </div>
      </el-col>
      <!-- search -->
      <el-col :span="10" :offset="1">
          <el-form :inline="true" :model="formSearch" size="mini">
          <el-form-item >
              <el-select v-model="formSearch.searchtype" placeholder="Shop">
              <el-option label="Shop" value="shop"></el-option>
              <el-option label="Dishes" value="dishes"></el-option>
              </el-select>
          </el-form-item>
          <el-form-item >
              <el-input v-model="formSearch.searchkey"></el-input>
          </el-form-item>
          <el-form-item>
              <el-button @click="onSubmit">Search</el-button>
          </el-form-item>
          </el-form>
      </el-col>
      <el-col :span="2">
        <el-button @click="drawer = true" size="mini" type="primary">
          shopping cart
        </el-button>
      </el-col>
    </el-row>
      <!-- horizontalbar -->
    <el-divider></el-divider>
      <!-- lower content -->
    <el-row>
      <div style="background-color: #ececec; padding: 20px;">
          <a-row :gutter="16">
          <a-list :dataSource="dishData" :grid="{ column: 6 }">
              <a-list-item slot="renderItem" slot-scope="item">
                <el-card class="box-card" 
                  @click.native='gotoDishShop(item.shop_id)'
                  style="height:120px"
                >
                  <div slot="header" class="clearfix">
                    <span style='overflow:hidden'>{{item.product_name}}</span>
                  </div>
                  <p style='overflow:hidden;text-align:center'>Sales: {{item.total_sale}}</p>
                </el-card>
                <br/>
              </a-list-item>
            </a-list>
        </a-row>
      </div>
    </el-row>
    <el-row>
      <!-- shopping cart -->
      <el-drawer
        :visible.sync="drawer"
        :direction="direction">
        <span>我来啦!</span>
        <el-button type="primary">purchase</el-button>
      </el-drawer>
    </el-row>
  </el-col>
</template>

<script>
  import Vue from 'vue'

  export default {
    name: 'Main',
    data() {
      return {
        formSearch: {
          searchtype: '',
          searchkey: '',
        },
        shopData: [],
        dishData: [],
        drawer: false,
        direction: 'rtl'
      };
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('submit!');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      onSubmit() {
        console.log('submit!');
      },
      gotoShop(refName){
        var index = this.$refs[refName].activeIndex
        var shopid = this.shopData[index]['shop_id']
        this.$router.push({path:`/shops/${shopid}`}).catch(err => {err})
      },
      gotoDishShop(id){
        this.$router.push({path:`/shops/${id}`}).catch(err => {err})
      }
    },
    created() {
      Vue.axios.get('/api/getRatedShops').then((response) => {
        this.shopData = response.data
      })
      Vue.axios.get('/api/getRatedDishes').then((response) => {
        this.dishData = response.data
      })
    },
  }
</script>

<style>
  a-card{
      width: 80%;
      height: 80%;
  }
  p{
      overflow: hidden;
  }
  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
</style>