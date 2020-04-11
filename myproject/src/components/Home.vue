<template>
<div>
  <!-- header -->
    <!-- login -->
    <el-row type=flex justify="end">
      <el-col :span="2">
        <el-button type="text" @click="dialogFormVisible = true">Sign in</el-button>
        <el-dialog title="Sign in" :visible.sync="dialogFormVisible">
          <el-form :model="form">
            <el-form-item label="Email">
              <el-input v-model="form.email" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="Password">
              <el-input v-model="form.password" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item>
            <el-button @click="dialogFormVisible = false">cancel</el-button>
            <el-button type="primary" @click="submitForm('form')">confirm</el-button>
            </el-form-item>
          </el-form>
        </el-dialog>
      </el-col>
    </el-row>
    <!-- location -->
    <el-row type="flex" justify="space-around">
        <el-col :span="4"><el-link v-on:click="test">Front Page</el-link></el-col>
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
        <a-list itemLayout="horizontal" :dataSource="data">
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
        <!-- upper content -->
        <el-row>
          <!-- recommended shop -->
          <el-col :span="12">
            <div style="background-color: #ececec; padding: 20px;">
              <a-row :gutter="16">
                <a-col :span="8">
                  <a-card style="width: 120px" :bodered="true">
                    <p>Card content</p>
                  </a-card>
                  <a-card style="width: 120px" :bodered="true">
                    <p>Card content</p>
                  </a-card>
                </a-col>
                <a-col :span="8">
                  <a-card style="width: 120px" :bodered="true">
                    <p>Card content</p>
                  </a-card>
                  <a-card style="width: 120px" :bodered="true">
                    <p>Card content</p>
                  </a-card>
                </a-col>
                <a-col :span="8">
                  <a-card style="width: 120px" :bodered="true">
                    <p>Card content</p>
                  </a-card>
                  <a-card style="width: 120px" :bodered="true">
                    <p>Card content</p>
                  </a-card>
                </a-col>
              </a-row>
            </div>
          </el-col>
          <!-- search -->
          <el-col :span="10" :offset="1">
            <el-form :inline="true" :model="formSearch" size="mini">
              <el-form-item >
                <el-select v-model="formSearch.searchtype" placeholder="Shop">
                  <el-option label="Shop" value="shop"></el-option>
                  <el-option label="Dishes" value="dishes"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item >
                <el-input v-model="formSearch.searchkey"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button @click="onSubmit">Search</el-button>
              </el-form-item>
            </el-form>
          </el-col>
        </el-row>
        <!-- horizontalbar -->
        <el-divider></el-divider>
        <!-- lower content -->
        <el-row>
          <div style="background-color: #ececec; padding: 20px;">
            <a-row :gutter="16">
              <a-col :span="4">
                <a-card style="width: 120px" :bodered="true">
                  <p>Card content</p>
                </a-card>
                <a-card style="width: 120px" :bodered="true">
                  <p>Card content</p>
                </a-card>
              </a-col>
              <a-col :span="4">
                <a-card style="width: 120px" :bodered="true">
                  <p>Card content</p>
                </a-card>
                <a-card style="width: 120px" :bodered="true">
                  <p>Card content</p>
                </a-card>
              </a-col>
              <a-col :span="4">
                <a-card style="width: 120px" :bodered="true">
                  <p>Card content</p>
                </a-card>
                <a-card style="width: 120px" :bodered="true">
                  <p>Card content</p>
                </a-card>
              </a-col>
              <a-col :span="4">
                <a-card style="width: 120px" :bodered="true">
                  <p>Card content</p>
                </a-card>
                <a-card style="width: 120px" :bodered="true">
                  <p>Card content</p>
                </a-card>
              </a-col>
              <a-col :span="4">
                <a-card style="width: 120px" :bodered="true">
                  <p>Card content</p>
                </a-card>
                <a-card style="width: 120px" :bodered="true">
                  <p>Card content</p>
                </a-card>
              </a-col>
              <a-col :span="4">
                <a-card style="width: 120px" :bodered="true">
                  <p>Card content</p>
                </a-card>
                <a-card style="width: 120px" :bodered="true">
                  <p>Card content</p>
                </a-card>
              </a-col>
            </a-row>
          </div>
        </el-row>
      </el-col>
      <!-- content end -->
    </el-row>
</div>
</template>

<script>
  import axios from 'axios'
  
  const data = [
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
    name: 'Home',
    data() {
      return {
        activeIndex: '1',
        activeIndex2: '1',
        dialogFormVisible: false,
        outerVisible: false,
        innerVisible: false,
        form: {
            email: '',
            password: ''
        },
        formSearch: {
          searchtype: '',
          searchkey: '',

        },
        data,

      };
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },
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
      test() {
        axios.get('http://127.0.0.1:5000').then(function (r) {
            console.log(r.data)
        })
      }

    }
  }
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
</style>
