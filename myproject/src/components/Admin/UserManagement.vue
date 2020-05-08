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
                  <a-table-column key="user_id" title="ID">
                    <template slot-scope="record">
                      <span> {{record.user_id}} </span>
                    </template>
                  </a-table-column>
                  <a-table-column key="user_name" title="Name">
                    <template slot-scope="record">
                      <span> {{record.user_name}} </span>
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
  import Vue from 'vue'
  import Header from '@/components/Admin/Header'
  import Sidebar from '@/components/Admin/Sidebar'

  export default {
    name: 'UserManagement',
    // mounted() {
    //   this.fetch();
    // },
    data() {
      return {
        data: [],
        pagination: {},
        loading: false,
        detailsVisible: false,
      };
    },
    methods: {
      // only search for id
        onSearch(value) {
          Vue.axios.get('/api/searchUser', {
            params: {
              id: value
            }
          }).then((response) => {
            var data = response.data
            this.data = data
          })
      },
      // handleTableChange(pagination, filters, sorter) {
      //   console.log(pagination);
      //   const pager = { ...this.pagination };
      //   pager.current = pagination.current;
      //   this.pagination = pager;
      //   this.fetch({
      //     results: pagination.pageSize,
      //     page: pagination.current,
      //     sortField: sorter.field,
      //     sortOrder: sorter.order,
      //     ...filters,
      //   });
      // },
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
    created: function(){
      Vue.axios.get('/api/getUser', {
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
