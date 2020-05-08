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
          :customRow="rowClick"
    :columns="columns"
    :dataSource="data"
    :pagination="pagination"
    :loading="loading"
    @change="handleTableChange"
    size="middle"
  >
    <span slot="application_id" slot-scope="application_id">{{application_id}}</span>
    <span slot="shop_name" slot-scope="shop_name">{{shop_name}}</span>
    <span slot="contact" slot-scope="contact">{{contact}}</span>
    <span slot="location" slot-scope="location">{{location}}</span>
    <span slot="info" slot-scope="info">{{info}}</span>
    <span slot="action">
        <!-- <el-button type="text" @click="viewDetails()">Details</el-button> -->
        <el-dialog
          :before-close="handleClose"
          :visible.sync="detailsVisible"
          width="30%"
          center>
          <span>ID:</span><span> {{this.app_detail.application_id}} </span>
          <br>
          <span>User ID:</span><span> {{this.app_detail.user_id}}</span>
          <br>
          <span>Shop ID:</span><span> {{this.app_detail.shop_id}}</span>
          <br>
          <span>Shop:</span><span> {{this.app_detail.shop_name}} </span>
          <br>
          <span>Location:</span><span> {{this.app_detail.location}} </span>
          <br>
          <span>Contact:</span><span> {{this.app_detail.contact}} </span>
          <br>
          <span>License:</span><span> {{this.app_detail.license}} </span>
          <br>
          <span>Relevant Information</span>
          <div>
            {{this.app_detail.info}}
          </div>
          <!-- reject confirm -->
          <el-dialog
            width="30%"
            :visible.sync="rejectDialogVisible"
            append-to-body>
            Are you sure to reject?
            <span slot="footer" class="dialog-footer">
              <el-button size="medium" type="text" @click="rejectDialogVisible = false">No</el-button>
              <el-button size="medium" type="primary" @click="handleReject">Yes</el-button>
            </span>
          </el-dialog>
          <!-- pass confirm -->
          <el-dialog
            width="30%"
            :visible.sync="passDialogVisible"
            append-to-body>
            Are you sure to pass?
            <span slot="footer" class="dialog-footer">
              <el-button size="medium" type="text" @click="passDialogVisible = false">No</el-button>
              <el-button size="medium" type="primary" @click="handlePass">Yes</el-button>
            </span>
          </el-dialog>
          <span slot="footer" class="dialog-footer">
            <el-button size="medium" type="text" @click="rejectDialogVisible = true">Reject</el-button>
            <el-button size="medium" type="primary" @click="passDialogVisible = true">Pass</el-button>
          </span>
        </el-dialog>
    </span>
    <span slot="shop_id" slot-scope="location">{{location.postcode}}</span>
  </a-table>
        </el-main>
      </el-container>
    </el-container>   
  </div>
</template>

<script>
  import Vue from 'vue'
  import Header from '@/components/Admin/Header'
  import Sidebar from '@/components/Admin/Sidebar'
  const columns = [
    {
      title: 'Application ID',
      dataIndex: 'application_id',
      sorter: true,
      width: '13%',
      scopedSlots: { customRender: 'application_id'},
    },
    {
      title: 'Shop',
      dataIndex: 'shop_name',
      sorter: true,
      width: '10%',
      scopedSlots: { customRender: 'shop_name' },
    },
    {
      title: 'Contact',
      dataIndex: 'contact',
      sorter: true,
      width: '10%',
      scopedSlots: { customRender: 'contact'}
    },
    {
      title: 'Location',
      dataIndex: 'location', 
      width: '15%',
      scopedSlots: {customRender: 'location'}
    },
    {
        title: 'Overview',
        dataIndex: 'info',
        scopedSlots: {customRender: 'info'}
    },
    {

        key: 'action',
        scopedSlots: { customRender: 'action' },
        width: '10%'
    },
  ];

  export default {
    name: "OpenApplication",
    // mounted() {
    //   this.fetch();
    // },
    data() {
      return {
        detailsVisible: false,
        rejectDialogVisible: false,
        passDialogVisible: false,
        data: [],
        app_detail: {
          application_id: '',
          user_id: '',
          shop_id: '',
          shop_name: '',
          contact: '',
          location: '',
          license: '',
          info: '',
        },
        pagination: {},
        loading: false,
        columns,
      };
    },
    methods: {
      cancel(e) {
        console.log(e);
        this.$message.error('Click on No');
      },
      handleReject(){
        this.detailsVisible = false;
        this.rejectDialogVisible = false;
      },
      handlePass(){
        this.detailsVisible = false;
        this.passDialogVisible = false;
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
      rowClick(record){
        return {
          on: {
            click: () => {
              this.app_detail.application_id = record.application_id
                 this.app_detail.user_id = record.user_id
                 this.app_detail.shop_id = record.shop_id
                 this.app_detail.shop_name = record.shop_name
                 this.app_detail.contact = record.contact
                 this.app_detail.license = record.license
                 this.app_detail.info = record.info
                 this.app_detail.location = record.location
                //  console.log(this.app_detail.application_id
                  this.detailsVisible = true;
               }
            }
        }
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
      })
    },
    components: {
      Header,
      Sidebar,
    },
  };



</script>

