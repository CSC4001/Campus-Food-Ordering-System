<template>
   <a-table
    :columns="columns"
    :rowKey="record => record.login.uuid"
    :dataSource="data"
    :pagination="pagination"
    :loading="loading"
    @change="handleTableChange"
    size="middle"
  >
    <span slot="name" slot-scope="name">{{name.last}}</span>
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
          <span>Location:</span><span> Letian </span>
          <br>
          <span>Relevant Information</span>
          <div>
            some info
          </div>
          <span slot="footer" class="dialog-footer">
            <el-button size="medium" type="text" @click="handleReject">Reject</el-button>
            <el-button size="medium" type="primary" @click="handlePass">Pass</el-button>
          </span>
        </el-dialog>
    </span>
    <span slot="shop_id" slot-scope="location">{{location.postcode}}</span>
  </a-table>
</template>
<script>
// import reqwest from 'reqwest';
// const columns = [
//   // {
//   //   title: 'No.', //from 1-10
//   //   dataIndex: 'number', //data index in result (json)
//   //   width: '7%',
//   // },
//   {
//     title: 'Application ID',
//     dataIndex: 'phone',
//     sorter: true,
//     width: '13%',
//   },
//   {
//     title: 'Shop',
//     dataIndex: 'name',
//     sorter: true,
//     width: '10%',
//     scopedSlots: { customRender: 'name' },
//   },
//   {
//     title: 'Shop ID',
//     dataIndex: 'location',
//     sorter: true,
//     width: '10%',
//     scopedSlots: { customRender: 'shop_id'}
//   },
//   {
//     title: 'Location',
//     dataIndex: 'location',
//     width: '15%',
//     scopedSlots: {customRender: 'location'}
//   },
//   {
//       title: 'Overview',
//       dataIndex: 'overview',
//   },
//   {
//       title: 'Action',
//       key: 'action',
//       scopedSlots: { customRender: 'action' },
//       width: '10%'
//   },

// ];

// export default {
//   mounted() {
//     this.fetch();
//   },
//   data() {
//     return {
//       detailsVisible: false,
//       popVisible: false,
//       data: [],
//       pagination: {},
//       loading: false,
//       columns,
//     };
//   },
//   methods: {
//     cancel(e) {
//       console.log(e);
//       this.$message.error('Click on No');
//     },
//     handleReject(){
//       this.detailsVisible = false;
//     },
//     handlePass(){
//       this.detailsVisible = false;
//     },
//     handleTableChange(pagination, filters, sorter) {
//       console.log(pagination);
//       const pager = { ...this.pagination };
//       pager.current = pagination.current;
//       this.pagination = pager;
//       this.fetch({
//         results: pagination.pageSize,
//         page: pagination.current,
//         sortField: sorter.field,
//         sortOrder: sorter.order,
//         ...filters,
//       });
//     },
//     fetch(params = {}) {
//       console.log('params:', params);
//       this.loading = true;
//       reqwest({
//         url: 'https://randomuser.me/api',
//         method: 'get',
//         data: {
//           results: 10,
//           ...params,
//         },
//         type: 'json',
//       }).then(data => {
//         const pagination = { ...this.pagination };
//         // Read total count from server
//         // pagination.total = data.totalCount;
//         pagination.total = 200;
//         this.loading = false;
//         this.data = data.results;
//         this.pagination = pagination;
//       });
//     },
//   },
// };
</script>
