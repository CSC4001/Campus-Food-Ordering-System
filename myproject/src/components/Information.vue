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
        <el-col :span="4"><el-link href="http://localhost:8080/#/shopsystem">Front Page</el-link></el-col>
        <el-col :span="4"><el-link href="http://localhost:8080/#/dishesmanagement">Dishes Management</el-link></el-col>
        <el-col :span="4"><el-link href="http://localhost:8080/#/ordermanagement">Order Management</el-link></el-col>
        <el-col :span="4"><el-link href="http://localhost:8080/#/information">Infomation</el-link></el-col>
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
        <!-- information -->
        <el-row>
          <el-col :span="8" :offset="5">
            <a-list itemLayout="horizontal" :dataSource="infoData">
              <a-list-item slot="renderItem" slot-scope="item">
                <a slot="actions"><el-button type="text" @click="infoFormVisible = true">edit</el-button></a>  
                <el-dialog title="information" :visible.sync="infoFormVisible">
                  <el-form :model="infoForm">
                    <el-form-item label="name">
                      <el-input v-model="infoForm.name" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="location">
                      <el-input v-model="infoForm.location" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="opening time">
                      <el-time-picker
                        is-range
                        v-model="infoForm.date"
                        range-separator="to"
                        start-placeholder="start"
                        end-placeholder="end"
                        >
                      </el-time-picker>
                      <!-- <el-col :span="7">
                        <el-time-picker placeholder="choose time" v-model="infoForm.date1" style="width: 100%;"></el-time-picker>
                      </el-col>
                      <el-col class="line" :span="2">-</el-col>
                      <el-col :span="7">
                        <el-time-picker placeholder="choose time" v-model="infoForm.date2" style="width: 100%;"></el-time-picker>
                      </el-col> -->
                    </el-form-item>
                    <el-form-item label="contact info">
                      <el-input v-model="infoForm.contact" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="relative info">
                      <el-input v-model="infoForm.relative" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item>
                      <div class="block">
                        <span class="demonstration">delivery fee</span>
                        <el-slider
                          v-model="infoForm.fee"
                          :step="1"
                          :min="0"
                          :max="5"
                          show-stops>
                        </el-slider>
                      </div>
                    </el-form-item>

                    <el-form-item>
                    <el-button @click="infoFormVisible = false">cancel</el-button>
                    <el-button type="primary" @click="submitForm('form')">confirm</el-button>
                    </el-form-item>
                  </el-form>
                </el-dialog>
                <a-list-item-meta>
                  <span slot="title">{{item.title}} : {{item.content}}</span>
                
                </a-list-item-meta>
              </a-list-item>
            </a-list>
            <el-button>close shop</el-button>
            <el-button>open shop</el-button>
          </el-col>
        </el-row>

        <!-- apply -->
        <!-- <el-row type="flex" justify="center">
          <el-button>close shop</el-button>
        </el-row>
        <el-row type="flex" justify="center">
          <el-button>open shop</el-button>
        </el-row> -->
      </el-col>
      <!-- content end -->
    </el-row>
</div>
</template>

<script>


  const siderData = [
    {
      title: 'Help',
      link: '',
    },
    {
      title: 'Back to Previous',
      link: '',
    },

  ];

    const infoData = [
    {
      title: 'name',
      content: 'content',
    },
    {
      title: 'location',
      content: '',
    },
    {
      title: 'opening time',
      content: '',
    },
    {
      title: 'contact info',
      content: '',
    },
    {
      title: 'relative info',
      content: '',
    },
    {
      title: 'delivery fee',
      content: '',
    },
  ];

  export default {
    name: 'Information',
    data() {
      return {
        loginFormVisible: false,
        infoFormVisible: false,
        loginForm: {
            email: '',
            password: ''
        },
        infoForm: {
          name: '',
          location: '',
          date: '',
          // date1: '',
          // date2: '',
          contact: '',
          relative: '',
          fee: '',


        },
        siderData,
        infoData,

      };
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

