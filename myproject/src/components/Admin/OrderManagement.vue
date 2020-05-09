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
          <div>
            <el-row type=flex justify="center">
              <el-col :span="8">
                <a-input-search placeholder="input search text" @search="onSearch" enterButton />
                <br /><br />
              </el-col>
            </el-row>
            <el-row type=flex justify="center">
              <el-col :span="16">
                <a-table
                  :dataSource="data"
                  :pagination="pagination"
                  :loading="loading"
                  @change="handleTableChange"
                  size="small"
                >
                  <a-table-column key="order_id" title="Order ID">
                    <template slot-scope="record">
                      <span>{{record.order_id}}</span>
                    </template>
                  </a-table-column>
                  <a-table-column key="user_id" title="User ID">
                    <template slot-scope="record">
                      <span>{{record.user_id}}</span>
                    </template>
                  </a-table-column>
                  <a-table-column key="shop_id" title="Shop ID">
                    <template slot-scope="record">
                      <span>{{record.shop_id}}</span>
                    </template>
                  </a-table-column>
                  <a-table-column key="status" title="Status">
                    <template slot-scope="record">
                      <span>{{record.order_status}}</span>
                    </template>
                  </a-table-column>
                  <a-table-column key="action" title="Action">
                    <template slot-scope="record">
                      <span>
                        <el-button type="text" @click="viewDetails(record)"> details</el-button>
                        <el-dialog
                          :visible.sync="detailsVisible"
                          width="30%"
                          center>
                            <span>Order ID:</span><span> {{order_detail.order_id}} </span>
                            <br>
                            <span>User ID:</span><span> {{order_detail.user_id}} </span>
                            <br>
                            <span>Shop ID:</span><span> {{order_detail.shop_id}} </span>
                            <br>
                            <span>Dishes List:</span><span> {{order_detail.purchased_products}} </span>
                            <br>
                            <span>User Contact:</span><span> {{order_detail.user_contact}} </span>
                            <br>
                            <span>Address:</span><span> {{order_detail.user_location}} </span>
                            <br>
                            <span>Delievry Fee:</span><span> {{order_detail.delivery_fee}} </span>
                            <br>
                            <!-- <span>Total Price</span><span> 10$ </span>
                            <br> -->
                            <span>Order Status:</span><span> {{order_detail.order_status}} </span>
                            <br>
                            <span>Time Created:</span><span> {{order_detail.create_time}} </span>
                            <br>
                            <span slot="footer" class="dialog-footer">
                              <el-button size="medium" type="primary" @click="detailsVisible = false">Confirm</el-button>
                            </span>
                        </el-dialog>
                      </span>
                    </template>
                  </a-table-column>
                </a-table>
              </el-col>
            </el-row>
          </div>
        </el-main>
      </el-container>
    </el-container>   
  </div>
</template>

<script>
  import Header from '@/components/Admin/Header'
  import Sidebar from '@/components/Admin/Sidebar'
  import Vue from 'vue'

  export default {
   name: 'OrderManagement',
    // mounted() {
    //   this.fetch();
    // },
    data() {
      return {
        data: [],
        pagination: {},
        loading: false,
        detailsVisible: false,
        order_detail:{
          order_id: '',
          user_id: '',
          shop_id: '',
          purchased_products: '',
          user_contact: '',
          user_location: '',
          delivery_fee: '',
          create_time: '',
          order_status: '',
        },
      };
    },
    methods: {
        onSearch(value) {
          Vue.axios.get('api/searchOrder', {
            params: {
              id: value
            }
          }).then((response) => {
            var data = response.data
            this.data = data
            console.log(response)
          })
      },
      handleTableChange(pagination, filters, sorter) {
        console.log(pagination);
        const pager = { ...this.pagination };
        pager.current = pagination.current;
        this.pagination = pager;
        this.fetch({
          results: pagination.pageSize,
          page: pagination.current,
          sortField: sorter.field,
          sortOrder: sorter.order,
          ...filters,
        });
      },
      viewDetails(record) {
        this.order_detail.order_id = record.order_id
        this.order_detail.user_id = record.user_id
        this.order_detail.shop_id = record.shop_id
        this.order_detail.purchased_products = record.purchased_products
        this.order_detail.user_contact = record.user_contact
        this.order_detail.user_location = record.user_location
        this.order_detail.delivery_fee = record.delivery_fee
        this.order_detail.create_time = record.create_time
        this.order_detail.order_status = record.order_status
        this.detailsVisible = true
      }
      // fetch(params = {}) {
      //   console.log('params:', params);
      //   this.loading = true;
      //   reqwest({
      //     url: 'https://randomuser.me/api',
      //     method: 'get',
      //     data: {
      //       results: 10,
      //       ...params,
      //     },
      //     type: 'json',
      //   }).then(data => {
      //     const pagination = { ...this.pagination };
      //     // Read total count from server
      //     // pagination.total = data.totalCount;
      //     pagination.total = 200;
      //     this.loading = false;
      //     this.data = data.results;
      //     this.pagination = pagination;
      //   });
      // },
    },
    created: function() {
      Vue.axios.get('/api/getAllOrder', {
      }).then((response) => {
        var data = response.data
        this.data = data
        console.log(data)
      })
    },
    components: {
      Header,
      Sidebar,
    },

  };


</script>
