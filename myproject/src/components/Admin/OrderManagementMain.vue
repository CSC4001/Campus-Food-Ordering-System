<template>
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
        :columns="columns"
        :rowKey="record => record.login.uuid"
        :dataSource="data"
        :pagination="pagination"
        :loading="loading"
        
        @change="handleTableChange"
        size="small"
      >
        <span slot="name" slot-scope="name">{{name.last}}</span>
        <span slot="location" slot-scope="location">{{location.city}}</span>
        <span slot="action">
          <el-button type="text" @click="detailsVisible = true">Details</el-button>
          <el-dialog
            :visible.sync="detailsVisible"
            width="30%"
            center>
            <span>Order ID:</span><span> id </span>
            <br>
            <span>User ID:</span><span> user id </span>
            <br>
            <span>Shop ID:</span><span> shop id </span>
            <br>
            <span>Dishes List:</span><span> a dishes </span>
            <br>
            <span>User Name:</span><span> a name </span>
            <br>
            <span>Address:</span><span> an address </span>
            <br>
            <span>Fee:</span><span> 1$ </span>
            <br>
            <span>Total Price</span><span> 10$ </span>
            <br>
            <span>Order Status:</span><span> finished </span>
            <br>
            <span>Time Created:</span><span> a day </span>
            <br>
            <span slot="footer" class="dialog-footer">
              <el-button type="primary" @click="detailsVisible = false">Confirm</el-button>
            </span>
          </el-dialog>
        </span>
        <span slot="shop_id" slot-scope="location">{{location.postcode}}</span>
      </a-table>
    </el-col>
  </el-row>
</div>
</template>
<script>
import reqwest from 'reqwest';
  const columns = [
    // {
    //   title: 'No.', //from 1-10
    //   dataIndex: 'number', //data index in result (json)
    //   width: '7%',
    // },
    {
        title: 'Shop ID',
        dataIndex: 'location',
        sorter: true,
        width: '10%',
        scopedSlots: { customRender: 'shop_id'}
    },
    {
      title: 'Shop',
      dataIndex: 'name',
      sorter: true,
      width: '10%',
      scopedSlots: { customRender: 'name' },
    },

    {
        title: 'Action',
        key: 'action',
        scopedSlots: { customRender: 'action' },
        width: '10%'
    },

  ];

  export default {
    name: 'OrderManagementMain',
    mounted() {
      this.fetch();
    },
    data() {
      return {
        data: [],
        pagination: {},
        loading: false,
        columns,
        detailsVisible: false,
      };
    },
    methods: {
        onSearch(value) {
        console.log(value);
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
      fetch(params = {}) {
        console.log('params:', params);
        this.loading = true;
        reqwest({
          url: 'https://randomuser.me/api',
          method: 'get',
          data: {
            results: 10,
            ...params,
          },
          type: 'json',
        }).then(data => {
          const pagination = { ...this.pagination };
          // Read total count from server
          // pagination.total = data.totalCount;
          pagination.total = 200;
          this.loading = false;
          this.data = data.results;
          this.pagination = pagination;
        });
      },
    },
  };
</script>