<template>
  <div>
    <!-- main -->
    <el-row>
      <el-col >
        <div>
          <p v-if='orderData.length==0'>No order now.{{orderData.length}}</p>
          <a-list :dataSource="orderData" v-if="orderData.length" :pagination="{pageSize:6}">
            <a-list-item slot="renderItem" slot-scope="item" >
              <a-list-item-meta :description="`Status: ${item.order_status}`">
                <!-- dishes or order id -->
                <a slot="title" @click='handleOrder(item)'>Order: {{item.order_id}}</a> 
              </a-list-item-meta>
              <el-dialog
                title="Order information"
                :visible.sync="orderVisible"
                width="60%"
                @close="orderVisible=false">
                <a-descriptions>
                  <a-descriptions-item label="Order ID">{{activeData.order_id}}</a-descriptions-item>
                  <a-descriptions-item label="User ID">{{activeData.user_id}}</a-descriptions-item>
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
                  <div v-show='activeData.order_status==="pending"'>
                    <el-popconfirm
                      confirmButtonText='Confirm'
                      cancelButtonText='Cancel'
                      title="Sure to accept?"
                      @onConfirm="changeStatus(activeData.order_id, 'approved')"
                    >
                      <el-button type="primary" slot="reference">Accept</el-button>
                    </el-popconfirm>
                    <el-popconfirm
                      confirmButtonText='Confirm'
                      cancelButtonText='Cancel'
                      title="Sure to reject?"
                      @onConfirm="changeStatus(activeData.order_id, 'denied')"
                    >
                      <el-button slot="reference">Reject</el-button>
                    </el-popconfirm>
                  </div>
                  <div v-show='activeData.order_status==="approved"'>
                    <el-popconfirm
                      confirmButtonText='Confirm'
                      cancelButtonText='Cancel'
                      title="Sure to deliver?"
                      @onConfirm="changeStatus(activeData.order_id, 'delivering')"
                    >
                      <el-button type="primary" slot="reference">Deliver</el-button>
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
        activeData: '',
      };
    },
    beforeMount() {
      Vue.axios.get('/api/order_management',{
        params: {
          'shop_id': sessionStorage.getItem('shop_id'),
        }
      }).then((response) => {
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
      changeStatus(id, status) {
        Vue.axios.post('/api/change_order_status',{
          'order_id': id,
          'status': status
        }).then((response) => {
          var data = response.data.data.message
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
  };
</script>


<style>

</style>