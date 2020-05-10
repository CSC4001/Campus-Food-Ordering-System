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
              <h1><span>Name:</span><span>{{shop_info[0].shop_name}}</span></h1>
              <span>ID:</span><span>{{shop_info[0].shop_id}}</span>
              <br>
              <span>Rate:</span><span>{{shop_info[0].shop_rate_number}}</span>
              <br>       
              <el-button type="text" @click="favourite()">Favoutite</el-button>
            </el-col>
            <!-- search -->
            <el-col :span="6" :offset="2">
              <a-input-search placeholder="input search text" @search="onSearch" enterButton />
              <br /><br />
            </el-col>
            <!-- shopping cart  -->
            <el-col :span="4" :offset="2">
              <a-affix :offset-top="top">
                <el-button @click="openShoppingCart" type="primary" style="margin-left: 16px;">
                  Shopping cart
                </el-button>
              </a-affix>
              <el-drawer
                :visible.sync="drawer"
                :direction="direction">
                <a-list item-layout="vertical"
                  :size="small" 
                  :pagination="cart_pagination"
                  :data-source="cart_data">
                <a-list-item slot="renderItem" key="item" slot-scope="item">
                  <a-card >
                    <el-row type="flex" justify="space-between">
                      <el-col>
                        <span>Name:</span><span>{{item.name}}</span>
                        <br>
                      </el-col>
                      <el-col>
                        <span>Price:</span><span>{{item.price}}</span>
                        <br>
                        <span>Quantity:</span><span>{{item.quantity}}</span>
                      </el-col>
                    </el-row>
                  </a-card>
                </a-list-item>
              </a-list>
              <span>Total:</span><span>{{this.total_price}}</span>
              <br>
              <el-button @click="openSubmitDialog">submit order</el-button>
              <el-dialog
                :visible.sync="submitFormVisible">
                <el-form ref="submitForm" :model="submitForm" :rules="rules">
                  <el-form-item label="Phone number" prop="user_contact" :label-width="formLabelWidth">
                    <el-input v-model="submitForm.user_contact" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="Location" prop="user_location" :label-width="formLabelWidth">
                    <el-select v-model="submitForm.user_location" placeholder="Please choose">
                      <el-option
                        v-for="item in locationOptions"
                        :key="item.value"
                        :label="item.value"
                        :value="item.value">
                      </el-option>
                    </el-select>
                  </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                  <el-button @click="submitFormVisible = false">Cancel</el-button>
                  <el-button type="primary" @click="openPayConfirmDialog('submitForm')">Pay</el-button>
                  <!-- pay double check -->
                  <el-dialog
                    :visible.sync="payConfirmDialogVisible"
                    width="30%">
                    <span>Total:</span><span>{{this.total_price}}</span>
                    <br>
                    <span>Are you sure to pay?</span>
                    <div slot="footer" class="dialog-footer">
                      <el-button @click="payConfirmDialogVisible=false">NO</el-button>
                      <el-button @click="pay" type="primary">YES</el-button>
                    </div>
                  </el-dialog>
                </div>
              </el-dialog>
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
                :data-source="dishes">
                <a-list-item slot="renderItem" key="item.title" slot-scope="item, index">
                  <a-card >
                    <el-row type="flex" justify="space-between">
                      <el-col>
                        <span>Name:</span>
                        <span>
                          <el-button type="text" size="mini" @click="viewDetail(item, index)">{{ item.name }}</el-button>
                        </span>
                        <el-dialog
                          :visible.sync="dishDialogVisible"
                          width="30%"
                          center>
                          <span>Name:</span><span>{{dish_info.name}}</span>
                          <br>
                          <span>Price:</span><span>{{dish_info.price}}</span>
                          <br>
                          <span>Sale:</span><span>{{dish_info.sale}}</span>
                          <br>
                          <span>Info:</span><span>{{dish_info.info}}</span>
                          <br>
                          <el-input-number size="mini" v-model="count"></el-input-number>
                          <span slot="footer" class="dialog-footer">
                            <el-button type="primary" @click="addDishes(item)">Add</el-button>
                          </span>
                        </el-dialog>
                        <br>
                      </el-col>
                      <el-col>
                        <span>Sale:</span><span>{{item.sale}}</span>
                        <br>
                        <span>Price:</span><span>{{item.price}}</span>
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
import Vue from 'vue'
import Sidebar from '@/components/UserInterface/Sidebar'
import Header from '@/components/UserInterface/Header'

export default {
  name: 'Shop',
  data() {
    var validateContact = (rule, value, callback) => {
      const userContact = /^[0-9]/;
      if (value === '') {
        callback(new Error('Please input contact'));
      } else {
        if (userContact.test(value) && value.length === 11) {
          callback();
        } else{
          callback(new Error('Length should be 11'));
        }
      }
    };
    return {
      count:0,
      user_fund: '',
      shop_info: [],
      dishes: [],
      dishDialogVisible: false,
      shopping_cart: {},
      cart_data:[],
      total_price: '',
      product: {
        id:'',
        name: '',
        price: '',
        quantity: '',
      },
      dish_info:{
        product_id:'',
        name:'',
        price: '',
        sale: '',
        info: '',
        index: '',
      },
      pagination: {
        onChange: page => {
          console.log(page);
        },
        pageSize: 6,
      },
      cart_pagination: {
        onChange: page => {
          console.log(page);
        },
        pageSize: 3,
      },
      direction: "rtl",
      drawer: false,
      submitFormVisible: false,
      submitForm: {
        user_contact: '',
        user_location: '',
      },
      locationOptions: [
          {value: 'Student Center'},
          {value: 'Shaw College'},
          {value: 'Muse College'},
          {value: 'Deligentia College'},
          {value: 'Harmonia College'},
          {value: 'Le Tian Building'},
          {value: 'Zhi Ren Building'},
          {value: 'Zhi Xin Building'},
          {value: 'Research A'},
          {value: 'Research B'},
          {value: 'Teaching A'},
          {value: 'Teaching B'},
          {value: 'Teaching C'},
          {value: 'Teaching D'}
        ],
      rules: {
          user_contact: [
            { required: true, validator: validateContact, trigger: 'blur' }
          ],
          user_location: [
            { required: true, message: 'Please choose location' },
          ],
        },
      payConfirmDialogVisible: false,

    }
  },
  methods: {
    favourite(){

    },
    onSearch(){

    },
    openSubmitDialog(){
      if (this.cart_data.length == 0) {
       this.$message('No product in shopping cart');
      } else{
        this.submitFormVisible=true
      }

    },
    openPayConfirmDialog(formName){
      // get user available fund 
      Vue.axios.get('/api/personalInfo',{
      params: {
        id: sessionStorage.getItem('accessToken')
      }
    }).then((response) => {
      var data = response.data
      this.user_fund = data.available;
    })
    // check if form valid 
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.payConfirmDialogVisible=true
        }else {
           this.$message('Invalid info');
        }
      })
    },
    pay(){
      if (this.user_fund < this.total_price){
        this.$message('Not sufficient fund');
      } else {
        this.submitOrder()
      }
    },
    changeFund(){
      fetch("http://localhost:5000/api/submitWithdraw?id="+sessionStorage.getItem('accessToken'),{
        method:"post",
        headers:{
          'content-type':'application/json'
        },
        body: JSON.stringify({"withdraw":this.total_price})
      }).then((r) => {
        return r.json()
      }).then((data) => {
        if (data.status == 'ok'){
          this.$message.success(data.info);
          this.$data.infoForm.available = data.available;
        } else {
          this.$message.error(data.info);
          return false;
        }
      })
    },
    submitOrder(){
      Vue.axios.post('/api/submitOrder', {
        dishes: this.shopping_cart,
        user_id: sessionStorage.getItem('accessToken'),
        shop_id: this.$route.params.shopid,
        price: this.total_price,
        user_contact: this.submitForm.user_contact,
        user_location: this.submitForm.user_location,
        delivery_fee: this.shop_info[0].delivery_fee,
      }).then(function (response) {
        console.log(response.data)
      }).catch(function (error) {
        console.log(error)
      })
      this.drawer=false
      this.submitFormVisible=false
      this.payConfirmDialogVisible=false
      this.$router.push({path:`/myorder`}).catch(err => {err})
    },
    addDishes(){
      if (this.count == 0) {
        this.$message('Quantity should be larger than 0');
      }
      else {
        this.dishDialogVisible = false
        let index = this.dish_info.index
        // this.product.id = this.dish_info.productid
        this.product.name = this.dish_info.name
        this.product.price = this.dish_info.price
        this.product.quantity = this.count
        let _product = JSON.stringify(this.product)
        let productClone = JSON.parse(_product)
        // // console.log(productClone)
        this.shopping_cart[productClone.name] = productClone
        this.dishes[index].count = productClone.quantity
      }
    },
    viewDetail(item, index){
      this.dish_info.index = index
      this.dish_info.product_id = item.product_id
      this.dish_info.name = item.name
      this.dish_info.price = item.price
      this.dish_info.sale = item.sale
      this.dish_info.info = item.info
      this.count = item.count
      this.dishDialogVisible = true
    },
    openShoppingCart(){
      this.drawer = true
      this.cart_data=Object.values(this.shopping_cart)
      let temp = 0
      for (var item of this.cart_data) {
        temp = temp + item.price*item.quantity
      }
      this.total_price = temp + this.shop_info[0].delivery_fee
    }
    
  },
  created() {
    var shop_id = this.$route.params.shopid
    // get all dishes
    Vue.axios.get('/api/getDishesInfo', {
      params: {
        id: shop_id
      }
    }).then((response) => {
      var data = response.data
      let _data = JSON.stringify(data)
      let dataClone = JSON.parse(_data)
      this.dishes = dataClone
    })
    //get shop info
    Vue.axios.get('api/searchShop', {
      params: {
        id: shop_id
      }
    }).then((response) => {
      var data = response.data
      this.shop_info = data
    })
    
  },
  components: {
    Header,
    Sidebar,
  },
  watch :{
    '$route': function (to, from) {
      this.$router.go(0)
      console.log(to, from)
    }
  }
}
</script>

<style>

</style>