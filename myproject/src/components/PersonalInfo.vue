<template>
  <div>
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
    <el-row type="flex" justify="space-around">
        <el-col :span="4"><el-link>Front Page</el-link></el-col>
        <el-col :span="4"><el-link>Diligentia College</el-link></el-col>
        <el-col :span="4"><el-link>Shaw College</el-link></el-col>
        <el-col :span="4"><el-link>Student Centre</el-link></el-col>
        <el-col :span="4"><el-link>LeTian Building</el-link></el-col>
    </el-row>
    <el-divider></el-divider>
    <el-row type="flex">
      <el-col :span="3" :offset="1">
        <a-list itemLayout="horizontal" :dataSource="data">
          <a-list-item slot="renderItem" slot-scope="item">
            <a-list-item-meta>
              <a slot="title" href="http://localhost:8080/#/personalinfo">{{item.title}}</a>
            </a-list-item-meta>
          </a-list-item>
        </a-list>
      </el-col>
      <el-col :span="1">
        <div class="verticalBar"></div>
      </el-col>
      <el-col>
          
      </el-col>
    </el-row>
  </div>
</template>

<script>
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
    name: 'PersonalInfo',
    data(){
        return {
          loginFormVisible: false,
          loginForm: {
            email: '',
            password: ''
        },
        data,

        };
    },
  }
</script>

<style scoped>
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