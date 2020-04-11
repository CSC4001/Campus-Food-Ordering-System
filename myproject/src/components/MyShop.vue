<template>
<div>
  <!-- header -->
    <!-- login -->
    <el-row type=flex justify="end">
      <el-col :span="2">
        <el-button type="text" @click="loginFormVisible = true">Sign in</el-button>
        <el-dialog title="Sign in" :visible.sync="loginFormVisible">
          <el-form :model="loginForm">
            <el-form-item label="Email">
              <el-input v-model="loginForm.email" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="Password">
              <el-input v-model="loginForm.password" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item>
            <el-button @click="loginFormVisible = false">cancel</el-button>
            <el-button type="primary" @click="submitForm('form')">confirm</el-button>
            </el-form-item>
          </el-form>
        </el-dialog>
      </el-col>
    </el-row>
    <!-- location -->
    <el-row type="flex" justify="space-around">
        <el-col :span="4"><el-link>Front Page</el-link></el-col>
        <el-col :span="4"><el-link>Diligentia College</el-link></el-col>
        <el-col :span="4"><el-link>Shaw College</el-link></el-col>
        <el-col :span="4"><el-link>Student Centre</el-link></el-col>
        <el-col :span="4"><el-link>LeTian Building</el-link></el-col>
    </el-row>
    <!-- horizontalbar -->
    <el-divider></el-divider>
  <!-- header end -->

  <!-- main -->
    <el-row type="flex">
      <!-- sidebar -->
      <el-col :span="3" :offset="1">
        <a-list itemLayout="horizontal" :dataSource="siderData">
          <a-list-item slot="renderItem" slot-scope="item">
            <a-list-item-meta>
              <a slot="title" href="http://localhost:8080/#/personalinfo">{{item.title}}</a>
            </a-list-item-meta>
          </a-list-item>
        </a-list>
      </el-col>
      <!-- verticalBar -->
      <el-col :span="1">
        <div class="verticalBar"></div>
      </el-col>
      <!-- content -->
      <el-col :span="18">
        <div
          class="demo-infinite-container"
          v-infinite-scroll="handleInfiniteOnLoad"
          :infinite-scroll-disabled="busy"
          :infinite-scroll-distance="10"
        >
          <a-list :dataSource="data" :grid="{ column: 2 }">
            <a-list-item slot="renderItem" slot-scope="item">
              <a-card :title="item.name.last" style="width: 300px">
                <a href="#" slot="extra">enter shop</a>
                <p>{{item.email}}</p>
                </a-card>
                <br />
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


  const siderData = [
    {
      title: 'Personal Info',
      link: '/',
    },
    {
      title: 'Favourite',
      link: '',
    },
    {
      title: 'My Order',
      link: '',
    },
    {
      title: 'My Shop',
      link: '',
    },
    {
      title: 'Help',
      link: '',
    },
  ];

  export default {
    name: 'MyShop',
    directives: { infiniteScroll },
    data() {
      return {
        loginFormVisible: false,
        data: [],
        loading: false,
        busy: false,
        loginForm: {
            email: '',
            password: ''
        },
        formSearch: {
          searchtype: '',
          searchkey: '',

        },
        siderData,

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
  };
</script>


<style>
  .verticalBar {
      width: 2px;
      height: 600px;
      background: grey;
      display: inline-block;
      margin-top: 10px;
      vertical-align: top;
      margin-right: 29px;
      margin-left: 30px;
  }
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
