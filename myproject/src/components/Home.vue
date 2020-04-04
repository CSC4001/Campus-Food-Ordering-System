<template>
<div>
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
              <a slot="title" href="link">{{item.title}}</a>
            </a-list-item-meta>
          </a-list-item>
        </a-list>
      </el-col>
      <el-col :span="2">
        <div class="verticalBar"></div>
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
