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
                  size="small"
                >
                  <a-table-column key="shop_id" title="ID">
                    <template slot-scope="record">
                      <span> {{record.shop_id}} </span>
                    </template>
                  </a-table-column>
                  <a-table-column key="shop_name" title="Name">
                    <template slot-scope="record">
                      <span> {{record.shop_name}}</span>
                    </template>
                  </a-table-column>
                  <a-table-column key="status" title="Status">
                    <template slot-scope="record">
                      <span>{{record.shop_status}}</span>
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
                          <span>ID:</span><span> {{shop_detail.application_id}} </span>
                          <br>
                          <span>Shop:</span><span> {{shop_detail.shop_name}} </span>
                          <br>
                          <span>Status:</span><span> {{shop_detail.shop_status}} </span>
                          <br>
                          <span>Location:</span><span> {{shop_detail.shop_location}} </span>
                          <br>
                          <span>Relevant Information</span>
                          <div>
                            {{shop_detail.shop_info}}
                          </div>
                          <!-- block confirm -->
                          <el-dialog
                            width="30%"
                            :visible.sync="blockDialogVisible"
                            append-to-body>
                            Are you sure to block?
                            <span slot="footer" class="dialog-footer">
                              <el-button size="medium" type="text" @click="blockDialogVisible = false">No</el-button>
                              <el-button size="medium" type="primary" @click="handleBlock()">Yes</el-button>
                            </span>
                          </el-dialog>
                          <!-- unblock confirm -->
                          <el-dialog
                            width="30%"
                            :visible.sync="unblockDialogVisible"
                            append-to-body>
                            Are you sure to unblock?
                            <span slot="footer" class="dialog-footer">
                              <el-button size="medium" type="text" @click="unblockDialogVisible = false">No</el-button>
                              <el-button size="medium" type="primary" @click="handleUnblock()">Yes</el-button>
                            </span>
                          </el-dialog>
                          <span slot="footer" class="dialog-footer">
                            <el-button size="medium" type="text" @click="blockDialogVisible = true">Block</el-button>
                            <el-button size="medium" type="text" @click="unblockDialogVisible = true">Unblock</el-button>
                          </span>
                        </el-dialog>
                      </span>
                    </template>
                  </a-table-column>
    <!-- <span slot="name" slot-scope="name">{{name.last}}</span>
    <span slot="location" slot-scope="location">{{location.city}}</span>
    <span slot="action">
        <el-button type="text" @click="detailsVisible = true">Details</el-button>
        <el-dialog
          :visible.sync="detailsVisible"
          width="30%"
          center>
          <span>ID:</span><span> id </span>
          <br>
          <span>Shop:</span><span> a shop </span>
          <br>
          <span>Status:</span><span> {{shop_status}} </span>
          <br>
          <span>
            <el-button type="text" @click="blockShop">Block</el-button>
            <span>/</span>
            <el-button type="text" @click="unblockShop">Unblock</el-button>
          </span>
          <br>
          <span>Location:</span><span> Letian </span>
          <br>
          <span slot="footer" class="dialog-footer">
            <el-button type="primary" @click="detailsVisible = false">Confirm</el-button>
          </span>
        </el-dialog>
    </span> -->
    <!-- <span slot="shop_id" slot-scope="location">{{location.postcode}}</span> -->
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
    name: 'ShopManagement',
    data() {
      return {
        shop_detail:{
          shop_id: '',
          shop_name: '',
          shop_status: '',
          shop_location: '',
          shop_info: '',
        },
        blockDialogVisible: false,
        unblockDialogVisible: false,
        data: [],
        pagination: {},
        loading: false,
        detailsVisible: false,
      };
    },
    methods: {
        onSearch(value) {
          Vue.axios.get('/api/searchShop', {
            params: {
              id: value
            }
          }).then((response) => {
            var data = response.data
            this.data = data
          })
      },
      handleBlock(){
        this.blockDialogVisible = false;
        this.detailsVisible = false;
        Vue.axios.post('/api/blockShop', {
          shop_id: this.shop_detail.shop_id
        }).then(function (response) {
          console.log(response.data)
        }).catch(function (error) {
          console.log(error)
        });
      },
      handleUnblock(){
        this.unblockDialogVisible = false;
        this.detailsVisible = false;
        Vue.axios.post('/api/unblockShop', {
          shop_id: this.shop_detail.shop_id
        }).then(function (response) {
          console.log(response.data)
        }).catch(function (error) {
          console.log(error)
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
      viewDetails(record){
        this.shop_detail.shop_id = record.shop_id
        this.shop_detail.shop_name = record.shop_name
        this.shop_detail.shop_status = record.shop_status
        this.shop_detail.shop_location = record.shop_location
        this.shop_detail.shop_info = record.shop_info
        this.detailsVisible = true;
      },
    //   fetch(params = {}) {
    //     console.log('params:', params);
    //     this.loading = true;
    //     reqwest({
    //       url: 'https://randomuser.me/api',
    //       method: 'get',
    //       data: {
    //         results: 10,
    //         ...params,
    //       },
    //       type: 'json',
    //     }).then(data => {
    //       const pagination = { ...this.pagination };
    //       // Read total count from server
    //       // pagination.total = data.totalCount;
    //       pagination.total = 200;
    //       this.loading = false;
    //       this.data = data.results;
    //       this.pagination = pagination;
    //     });
    //   },
    },
    created: function(){
      Vue.axios.get('/api/getAllShop', {
      }).then((response) => {
        var data = response.data
        this.data = data
      })
    },
      components: {
      Header,
      Sidebar,
    },

  };
</script>
