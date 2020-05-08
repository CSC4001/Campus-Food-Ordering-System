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
          <a-table


    :dataSource="data"
    :pagination="pagination"
    :loading="loading"
    @change="handleTableChange"
    size="middle"
  >
    <a-table-column key="application_id" title="Application ID" >
    <template slot-scope="record">
      <span> {{record.application_id}} </span>
    </template>
  </a-table-column>
  <a-table-column key="shop_name" title="Shop">
    <template slot-scope="record">
      <span> {{record.shop_name}}</span>
    </template>
  </a-table-column>
  <!-- <a-table-column key="contact" title="Contact">
    <template slot-scope="record">
      <span> {{record.contact}}</span>
    </template>
  </a-table-column>
  <a-table-column key="location" title="Location">
    <template slot-scope="record">
      <span>{{record.location}}</span>
    </template>
  </a-table-column>
  <a-table-column key="info" title="Overview">
    <template slot-scope="record">
      <span>{{record.info}}</span>
    </template>
  </a-table-column> -->
    <a-table-column key="action" title="Action">
      <template slot-scope="record">
        <span>
          <el-button type="text" @click="viewDetails(record)"> details</el-button>
          <el-dialog

            :before-close="handleClose"
            :visible.sync="detailsVisible"
            width="30%"
            center>
            <span>ID:</span><span> {{app_detail.application_id}} </span>
            <br>
            <span>User ID:</span><span> {{app_detail.user_id}}</span>
            <br>
            <span>Shop:</span><span> {{app_detail.shop_name}} </span>
            <br>
            <!-- <span>Location:</span><span> {{app_detail.location}} </span>
            <br>
            <span>Contact:</span><span> {{app_detail.contact}} </span>
            <br> -->
            <span>License:</span><span> {{app_detail.license}} </span>
            <br>
            <!-- <span>Relevant Information</span>
            <div>
              {{app_detail.info}}
            </div> -->
            <!-- deny confirm -->
            <el-dialog
              width="30%"
              :visible.sync="denyDialogVisible"
              append-to-body>
              Are you sure to deny?
              <span slot="footer" class="dialog-footer">
                <el-button size="medium" type="text" @click="denyDialogVisible = false">No</el-button>
                <el-button size="medium" type="primary" @click="handleDeny()">Yes</el-button>
              </span>
            </el-dialog>
            <!-- approve confirm -->
            <el-dialog
              width="30%"
              :visible.sync="approveDialogVisible"
              append-to-body>
              Are you sure to approve?
              <span slot="footer" class="dialog-footer">
                <el-button size="medium" type="text" @click="approveDialogVisible = false">No</el-button>
                <el-button size="medium" type="primary" @click="handleApprove()">Yes</el-button>
              </span>
            </el-dialog>
            <span slot="footer" class="dialog-footer">
              <el-button size="medium" type="text" @click="denyDialogVisible = true">Deny</el-button>
              <el-button size="medium" type="primary" @click="approveDialogVisible = true">Approve</el-button>
            </span>
          </el-dialog>
        </span>
      </template>
    </a-table-column>
  </a-table>
        </el-main>
      </el-container>
    </el-container>   
  </div>
</template>

<script>
  import Header from '@/components/Admin/Header'
  import Sidebar from '@/components/Admin/Sidebar'

  export default {
    name: "CloseApplication",
    // mounted() {
    //   this.fetch();
    // },
    data() {
      return {
        detailsVisible: false,
        denyDialogVisible: false,
        approveDialogVisible: false,
        data: [],
        pagination: {},
        loading: false,
      };
    },
    methods: {
      cancel(e) {
        console.log(e);
        this.$message.error('Click on No');
      },
      handleDeny(){
        this.detailsVisible = false;
        this.denyDialogVisible = false;
        Vue.axios.post('/api/operateApplication', {
          app_id: this.app_detail.application_id,
          op_type: 'denied'
        })
        .then(function (response) {
          console.log(response.data)
        })
        .catch(function (error) {
          console.log(error)
        });
      },
      handleApprove(){
        this.detailsVisible = false;
        this.approveDialogVisible = false;
        Vue.axios.post('/api/operateApplication', {
          app_id: this.app_detail.application_id,
          op_type: 'approved'
        })
        .then(function (response) {
          console.log(response.data)
        })
        .catch(function (error) {
          console.log(error)
        });
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
    handleClose(done) {
        this.$confirm('Sure to close?')
          .then(_ => {
            console.log(_)
            done();
          })
          .catch(_ => {
            console.log(_)
          });
    },
    viewDetails(record){
      this.app_detail.application_id = record.application_id
      this.app_detail.user_id = record.user_id
      this.app_detail.shop_name = record.shop_name
      this.app_detail.contact = record.contact
      this.app_detail.license = record.license
      this.app_detail.info = record.info
      this.detailsVisible = true;
      console.log(record)
    },


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
      Vue.axios.get('/api/getCloseApplication', {
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

