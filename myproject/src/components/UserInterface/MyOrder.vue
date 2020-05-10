<template>
  <div>
    <!-- main -->
    <el-row>
      <el-col>
        <div>
          <p  v-if='orderData.length+1'>You haven't had any order.</p>
          <a-list :dataSource="orderData" v-if="orderData.length" pagination={pageSize:6}>
            <a-list-item slot="renderItem" slot-scope="item" @click-native='handleOrder(item)'>
              <a-list-item-meta :description="`Status: ${item.order_status}`">
                <!-- dishes or order id -->
                <a slot="title">My order: {{item.order_id}}</a> 
              </a-list-item-meta>
              <el-dialog
                title="Order information"
                :visible.sync="orderVisible"
                width="60%"
                @close="orderVisible=false">
                <a-descriptions>
                  <a-descriptions-item label="Order ID">{{item.order_id}}</a-descriptions-item>
                  <a-descriptions-item label="Shop name">{{item.shop_name}}</a-descriptions-item>
                  <a-descriptions-item label="Location">{{item.user_location}}</a-descriptions-item>
                  <a-descriptions-item label="Contact">{{item.user_contact}}</a-descriptions-item>
                  <a-descriptions-item label="Create time">{{item.create_time,}}</a-descriptions-item>
                  <a-descriptions-item label="Order Status">{{item.order_status}}</a-descriptions-item>
                </a-descriptions>
                <p>Ordered dishes:</p>
                <a-table :columns="columns" 
                  :data-source="orderDetail"
                  pagination={pageSize:6}
                ></a-table>
                <p>Total:{{calculateTotal()}} yuan</p>
                <span slot="footer">
                  <div v-if='item.order_status=="pending"'>
                    <el-popconfirm
                      confirmButtonText='Confirm'
                      cancelButtonText='Cancel'
                      title="Sure to cancel?"
                      :onConfirm="changeStatus(item.order_id, 'cancelled')"
                    >
                      <el-button type="primary">Cancel</el-button>
                    </el-popconfirm>
                  </div>
                  <div v-if='item.order_status=="delivering"'>
                    <el-popconfirm
                      confirmButtonText='Confirm'
                      cancelButtonText='Cancel'
                      title="Sure to confirm receive?"
                      :onConfirm="changeStatus(item.order_id, 'finished')"
                    >
                      <el-button type="primary">Confirm receive</el-button>
                    </el-popconfirm>
                  </div>
                  <div v-if='item.order_status=="finished"'>
                    <el-rate
                        v-model="rate"
                        :colors="['#99A9BF', '#F7BA2A', '#FF9900']">
                    </el-rate>
                    <el-popconfirm
                      confirmButtonText='Confirm'
                      cancelButtonText='Cancel'
                      title="Sure to rate?"
                      :onConfirm="rateOrder(item.shop_id)"
                    >
                      <el-button type="primary">Rate</el-button>
                    </el-popconfirm>
                  </div>
                </span>
              </el-dialog>
            </a-list-item>
          </a-list>
        </div>
      </el-col>
      <!-- content end -->
    </el-row>
  </div>
</template>

<script>
  import Vue from 'vue'
  export default {
    name: 'OrderManagementMain',
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
          console.log(response)
          var data = response.data
          this.orderDetail = data.data.list
        })
      },
      changeStatus(id, status) {
        if (status == 'cancelled') {
          Vue.axios.post('/api/change_order_status',{
            'order_id' :id
          }).then((response) => {
            console.log(response)
            var data = response.data.message
            this.orderVisible = false
            this.$message.success(data)
          })
        } else if (status == 'finished') {
          Vue.axios.post('/api/pay_order',{
            'order_id' :id
          }).then((response) => {
            console.log(response)
            var data = response.data.message
            this.orderVisible = false
            this.$message.success(data)
          })
        }
      },
      rateOrder(id) {
        Vue.axios.post('/api/change_order_status',{
          'shop_id' :id,
          'rate': this.$data.rate
        }).then((response) => {
          console.log(response)
          var data = response.data.message
          this.orderVisible = false
          this.$message.success(data)
        })
      }
    },
  };
</script>


<style>

</style>