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
          <!-- main -->
          <el-row>
            <el-col>
              <div>
                <p v-if='orderData.length==0'>You haven't had any order.</p>
                <a-list :dataSource="orderData" v-if="orderData.length" :pagination="{pageSize:6}">
                  <a-list-item slot="renderItem" slot-scope="item">
                    <a-list-item-meta :description="`Status: ${item.order_status}`">
                      <!-- dishes or order id -->
                      <a slot="title" @click='handleOrder(item)'>My order: {{item.order_id}}</a> 
                    </a-list-item-meta>
                  </a-list-item>
                </a-list>
                <el-dialog
                  title="Order information"
                  :visible.sync="orderVisible"
                  width="60%"
                  @closed="orderVisible=false">
                  <a-descriptions>
                    <a-descriptions-item label="Order ID">{{activeData.order_id}}</a-descriptions-item>
                    <a-descriptions-item label="Shop name">{{activeData.shop_name}}</a-descriptions-item>
                    <a-descriptions-item label="Location">{{activeData.user_location}}</a-descriptions-item>
                    <a-descriptions-item label="Contact">{{activeData.user_contact}}</a-descriptions-item>
                    <a-descriptions-item label="Create time">{{activeData.create_time,}}</a-descriptions-item>
                    <a-descriptions-item label="Order Status">{{activeData.order_status}}</a-descriptions-item>
                  </a-descriptions>
                  <p>Ordered dishes:</p>
                  <a-table :columns="columns" 
                    :data-source="orderDetail"
                    :pagination="{pageSize:6}"
                  ></a-table>
                  <p>Total:{{calculateTotal()}} yuan</p>
                  <span slot="footer">
                    <div v-if='activeData.order_status=="pending"'>
                      <el-popconfirm
                        confirmButtonText='Confirm'
                        cancelButtonText='Cancel'
                        title="Sure to cancel?"
                        @onConfirm="changeStatus(activeData.order_id, 'cancelled', 0)"
                      >
                        <el-button type="primary" slot="reference">Cancel</el-button>
                      </el-popconfirm>
                    </div>
                    <div v-if='activeData.order_status=="delivering"'>
                      <el-popconfirm
                        confirmButtonText='Confirm'
                        cancelButtonText='Cancel'
                        title="Sure to confirm receive?"
                        @onConfirm="changeStatus(activeData.order_id, 'finished', calculateTotal())"
                      >
                        <el-button type="primary" slot="reference">Confirm receive</el-button>
                      </el-popconfirm>
                    </div>
                    <div v-if='activeData.order_status=="finished"'>
                      <el-rate
                          v-model="rate"
                          :colors="['#99A9BF', '#F7BA2A', '#FF9900']">
                      </el-rate>
                      <el-popconfirm
                        confirmButtonText='Confirm'
                        cancelButtonText='Cancel'
                        title="Sure to rate?"
                        @onConfirm="rateOrder(activeData.shop_id)"
                      >
                        <el-button type="primary" slot="reference">Rate</el-button>
                      </el-popconfirm>
                    </div>
                  </span>
                </el-dialog>
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
  import Vue from 'vue'
  // const fakeDataUrl = 'https://randomuser.me/api/?results=5&inc=name,gender,email,nat&noinfo';
  import Sidebar from '@/components/UserInterface/Sidebar'
  import Header from '@/components/UserInterface/Header'

  export default {
    name: 'MyOrder',
    data() {
      const columns = [
        {
          title: 'Product Name',
          dataIndex: 'product_name',
          key: 'product_name',
          ellipsis: true,
        },
        {
          title: 'Product Price',
          dataIndex: 'product_price',
          key: 'product_price',
          ellipsis: true,
        },
        {
          title: 'Quantity',
          dataIndex: 'quantity',
          key: 'quantity',
          ellipsis: true,
        },
      ]
      return {
        orderData: [],
        orderDetail: [],
        orderVisible: false,
        activeData: '',
        columns,
        rate:5
      };
    },
    beforeMount() {
      Vue.axios.get('/api/my_orders',{
        params: {
          'user_id': sessionStorage.getItem('accessToken'),
        }
      }).then((response) => {
        console.log(response)
        var data = response.data
        this.orderData = data.data.list
      })
    },
    methods: {
      handleOrder(item) {
        this.orderVisible = true
        Vue.axios.get('/api/order_detail',{
          params: {
            'order_id': item.order_id,
          }
        }).then((response) => {
          var data = response.data
          this.orderDetail = data.data.list
        })
        this.activeData = item
      },
      changeStatus(id, status, price) {
        if (status == 'cancelled') {
          Vue.axios.post('/api/cancel_order',{
            'order_id' :id
          }).then((response) => {
            var data = response.data.message
            this.orderVisible = false
            this.$message.success(data)
          })
        } else if (status == 'finished') {
          Vue.axios.post('/api/pay_order',{
            'order_id' :id,
            'price': price
          }).then((response) => {
            var data = response.data.message
            this.orderVisible = false
            this.$message.success(data)
          })
        }
      },
      rateOrder(id) {
        Vue.axios.post('/api/rate_order',{
          'shop_id' :id,
          'rate': this.$data.rate
        }).then((response) => {
          var data = response.data.message
          this.orderVisible = false
          this.$message.success(data)
        })
      },
      calculateTotal() {
        var sum = 0
        for (var i = 0; i < this.orderDetail.length; i++) {
          var obj = this.orderDetail[i]
          sum += obj.product_price * obj.quantity
        }
        return sum
      }
    },
    components: {
      Header,
      Sidebar,
    }
  };
</script>


<style>

</style>