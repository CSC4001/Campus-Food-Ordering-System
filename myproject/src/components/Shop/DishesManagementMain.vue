<template>
<el-row type="flex">
  <!-- content -->
  <el-col>
    <!-- search -->
    <el-row type="flex" justify="center">
      <el-form :inline="true" :model="formSearch" size="mini">
        <el-form-item >
          <el-input v-model="formSearch.searchkey"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="onSubmit">Search</el-button>
        </el-form-item>
      </el-form>
    </el-row>
    <!-- add dishes -->
    <el-row type="flex" justify="center">
      <el-button @click="dishesFormVisible = true">add dishes</el-button>
      <el-dialog title="dishes information" :visible.sync="dishesFormVisible">
        <el-form ref="form" :model="dishesForm" label-width="80px">
          <el-form-item label="name">
            <el-input v-model="dishesForm.name"></el-input>
          </el-form-item>
          <el-form-item label="price">
            <el-input v-model="dishesForm.price"></el-input>
          </el-form-item>
          <el-form-item label="discription">
            <el-input v-model="dishesForm.discription"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button @click="loginFormVisible = false">cancel</el-button>
            <el-button type="primary" @click="submitForm('form')">create</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
    </el-row>
    <!-- dishes  -->
    <el-row>
      <div
      class="demo-infinite-container"
      v-infinite-scroll="handleInfiniteOnLoad"
      :infinite-scroll-disabled="busy"
      :infinite-scroll-distance="10"
      >
        <a-list :dataSource="data" :grid="{ column: 4 }">
          <a-list-item slot="renderItem" slot-scope="item">
            <el-card class="box-card" >
              <div slot="header" class="clearfix">
                <span>{{item.name.last}}</span>
                <el-button style="float: right; padding: 3px 0" type="text">delete</el-button>
              </div>
            <!-- <div v-for="o in 4" :key="o" class="text item">
            {{'列表内容 ' + o }}
            </div> -->
              <el-row type="flex" justify="space-between">
                <span>sales</span>
                <span>price</span>
              </el-row>
            </el-card>
            <br/>
          </a-list-item>
          <div v-if="loading && !busy" class="demo-loading-container">
            <a-spin/>
          </div>
        </a-list>
      </div>
    </el-row>
  </el-col>
</el-row>
</template>

<script>
  import reqwest from 'reqwest';
  import infiniteScroll from 'vue-infinite-scroll';
  const fakeDataUrl = 'https://randomuser.me/api/?results=5&inc=name,gender,email,nat&noinfo';

  export default {
    name: 'DishesManagementMain',
    directives: { infiniteScroll },
    data() {
      return {
        dishesFormVisible: false,
        data: [],
        loading: false,
        busy: false,
        dishesForm: {
          name: '',
          price: '',
          discription: '',
        },
        formSearch: {
          searchtype: '',
          searchkey: '',
        },
      };
    },
    beforeMount() {
      this.fetchData(res => {
        this.data = res.results;
      });
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('submit!');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      onSubmit() {
        console.log('submit!');
      },
      
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

}
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
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    width: 180px;
  }

</style>