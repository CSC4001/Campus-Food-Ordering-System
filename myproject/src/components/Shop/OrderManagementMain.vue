<template>
  <div>
    <!-- main -->
    <el-row>
      <el-col >
        <div>
          <p  v-if='orderData.length+1'>No order now.{{orderData.length}}</p>
          <a-list :dataSource="orderData" v-if="orderData.length" pagination={pageSize:6}>
            <a-list-item slot="renderItem" slot-scope="item" @click-native='handleOrder(item)'>
              <a-list-item-meta :description="`Status: ${item.order_status}`">
                <!-- dishes or order id -->
                <a slot="title">Order: {{item.order_id}}</a> 
              </a-list-item-meta>
              <el-dialog
                title="Order information"
                :visible.sync="orderVisible"
                width="60%"
                @close="orderVisible=false">
                <a-descriptions>
                  <a-descriptions-item label="Order ID">{{item.order_id}}</a-descriptions-item>
                  <a-descriptions-item label="User ID">{{item.user_id}}</a-descriptions-item>
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
                      title="Sure to accept?"
                      :onConfirm="changeStatus(item.order_id, 'approved')"
                    >
                      <el-button type="primary">Accept</el-button>
                    </el-popconfirm>
                    <el-popconfirm
                      confirmButtonText='Confirm'
                      cancelButtonText='Cancel'
                      title="Sure to reject?"
                      :onConfirm="changeStatus(item.order_id, 'denied')"
                    >
                      <el-button>Reject</el-button>
                    </el-popconfirm>
                  </div>
                  <div v-if='item.order_status=="approved"'>
                    <el-popconfirm
                      confirmButtonText='Confirm'
                      cancelButtonText='Cancel'
                      title="Sure to deliver?"
                      :onConfirm="changeStatus(item.order_id, 'delivering')"
                    >
                      <el-button type="primary">deliver</el-button>
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
        columns
      };
    },
    beforeMount() {
      Vue.axios.get('/api/order_management',{
        params: {
          'shop_id': sessionStorage.getItem('shop_id'),
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
        Vue.axios.get('/api/change_order_status',{
          params: {
            'order_id': id,
            'status': status
          }
        }).then((response) => {
          console.log(response)
          var data = response.data
          this.orderVisible = false
          this.$message.success(data)
        })
      }
    },
  };
</script>


<style>

</style>