<template>
  <div>
    <!-- main -->
    <el-row>
      <el-col >
        <div
          class="demo-infinite-container"
          v-infinite-scroll="handleInfiniteOnLoad"
          :infinite-scroll-disabled="busy"
          :infinite-scroll-distance="10"
        >
          <a-list :dataSource="data">
            <a-list-item slot="renderItem" slot-scope="item">
              <!-- cancelled -->
              <!-- <a-list-item-meta description="status: cancelled"> -->

              <!-- finished -->
              <!-- <a-list-item-meta description="status: finished"> -->

              <!-- delivering -->
              <!-- <a-list-item-meta description="status: delivering"> -->

              <!-- received -> delivering -->
              <!-- <a slot="actions">
                <a-popconfirm title="Are you sure？">
                  <a-icon slot="icon" type="question-circle-o" style="color: red" />
                  <a href="#">deliver</a>
                </a-popconfirm>
              </a>
              <a-list-item-meta description="status: received"> -->

              <!-- unreceived -> accept or reject -->
              <a slot="actions">
                <a-popconfirm title="Are you sure？">
                  <a-icon slot="icon" type="question-circle-o" style="color: red" />
                  <a href="#">receive</a>
                </a-popconfirm>
              </a>
              <a slot="actions">
                <a-popconfirm title="Are you sure？">
                <a-icon slot="icon" type="question-circle-o" style="color: red" />
                  <a href="#">reject</a>
                </a-popconfirm>
              </a>
              <a-list-item-meta description="status: unreceived">

                <!-- dishes or order id -->
                <a slot="title" href="https://www.antdv.com/">{{item.name.last}}</a> 
              </a-list-item-meta>
            </a-list-item>
            <div v-if="loading && !busy" class="demo-loading-container">
              <a-spin />
            </div>
          </a-list>
        </div>
      </el-col>
      <!-- content end -->
    </el-row>
  </div>
</template>

<script>
  import reqwest from 'reqwest';
  import infiniteScroll from 'vue-infinite-scroll';
  const fakeDataUrl = 'https://randomuser.me/api/?results=5&inc=name,gender,email,nat&noinfo';

  export default {
    name: 'OrderManagementMain',
    directives: { infiniteScroll },
    data() {
      return {
        data: [],
        loading: false,
        busy: false,
      };
    },
    beforeMount() {
      this.fetchData(res => {
        this.data = res.results;
      });
    },
    methods: {
       fetchData(callback) {
        reqwest({
          url: fakeDataUrl,
          type: 'json',
          method: 'get',
          contentType: 'application/json',
          success: res => {
            callback(res);
          },
        });
      },
      handleInfiniteOnLoad() {
        const data = this.data;
        this.loading = true;
        if (data.length > 14) {
          this.$message.warning('Infinite List loaded all');
          this.busy = true;
          this.loading = false;
          return;
        }
        this.fetchData(res => {
          this.data = data.concat(res.results);
          this.loading = false;
        });
      },
    },
  };
</script>


<style>
  .demo-infinite-container {
    border: 1px solid #e8e8e8;
    border-radius: 4px;
    overflow: auto;
    padding: 8px 24px;
    height: 300px;
  }
  .demo-loading-container {
    position: absolute;
    bottom: 40px;
    width: 100%;
    text-align: center;
  }

</style>