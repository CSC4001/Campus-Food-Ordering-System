<template>
  <!-- header -->
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
          <p style="font-size: 25px;">My shop list</p>
          <el-col :span="18">
            <a-list
              v-if="shopList.length"
              :dataSource="shopList"
              :header="`${shopList.length} ${shopList.length > 1 ? 'shops' : 'shop'}`"
              itemLayout="horizontal"
            >
              <a-list-item slot="renderItem" slot-scope="item">
                <a-list-item-meta
                  :description = "item.shop_info"
                >
                  <a slot="title" @click="handleShopURL(item.shop_id)">{{ item.shop_name }}</a>
                </a-list-item-meta>
                <div>Status: {{ item.shop_status }}</div>
              </a-list-item>
            </a-list>
            <!-- Apply form for shop-->
            <el-button type="primary" @click="applyFormVisible=true">Create a new shop</el-button>
            <el-dialog title='Application of creating your own shop' :visible.sync='applyFormVisible' width="50%">
              <el-form ref="applyModel" :model="applyForm" :rules="rules" label-width="30%">
                <el-form-item label="Shop name" prop='name'>
                  <el-input v-model='applyForm.name'></el-input>
                </el-form-item>
                <el-form-item label="Shop contact" prop='contact'>
                  <el-input v-model='applyForm.contact'></el-input>
                </el-form-item>
                <el-form-item label="Shop location" prop='location'>
                  <el-select v-model="applyForm.location" placeholder="Please choose">
                    <el-option
                      v-for="item in locationOptions"
                      :key="item.value"
                      :label="item.value"
                      :value="item.value">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="Detailed location" prop='locationDetail'>
                  <el-input v-model='applyForm.locationDetail' 
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 5 }"
                            maxlength="256"
                            show-word-limit>
                  </el-input>
                </el-form-item>
                <el-form-item label="ID number" prop='licenseNum'>
                  <el-input v-model='applyForm.licenseNum'></el-input>
                </el-form-item>
                <el-form-item label="Shop information" prop='info'>
                  <el-input v-model='applyForm.info'
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 5 }"
                            maxlength="256"
                            show-word-limit>
                  </el-input>
                </el-form-item>
              </el-form>
              <el-button @click="applyFormVisible = false">Cancel</el-button>
              <el-button type="primary" @click="submitApplyForm('applyModel')">Submit</el-button>
            </el-dialog>
          </el-col>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
  import Vue from 'vue'
  // const fakeDataUrl = 'https://randomuser.me/api/?results=5&inc=name,gender,email,nat&noinfo';
  import Sidebar from '@/components/UserInterface/Sidebar'
  import Header from '@/components/UserInterface/Header'

  export default {
    name: 'MyShop',
    data() {
      var validateContact = (rule, value, callback) => {
        const userContact = /^[0-9]/;
        if (value === '') {
          callback(new Error('Please input Shop contact'));
        } else {
          if (userContact.test(value) && value.length === 11) {
            callback();
          } else{
            callback(new Error('Length should be 11'));
          }
        }
      };
      var validateLicense = (rule, value, callback) => {
        const userLicense = /^[0-9]/;
        if (value === '') {
          callback(new Error('Please input ID number'));
        } else {
          if (userLicense.test(value) && value.length === 32) {
            callback();
          } else{
            callback(new Error('Length should be 32'));
          }
        }
      };
      return {
        shopList: [],
        locationOptions: [
          {value: 'Student Center'},
          {value: 'Shaw College'},
          {value: 'Muse College'},
          {value: 'Deligentia College'},
          {value: 'Harmonia College'},
          {value: 'Le Tian Building'},
          {value: 'Zhi Ren Building'},
          {value: 'Zhi Xin Building'},
          {value: 'Research A'},
          {value: 'Research B'},
          {value: 'Teaching A'},
          {value: 'Teaching B'},
          {value: 'Teaching C'},
          {value: 'Teaching D'}
        ],
        applyFormVisible: false,
        applyForm: {
          id: sessionStorage.getItem('accessToken'),
          name: '',
          contact: '',
          location: '',
          locationDetail: '',
          licenseNum: '',
          info: ''
        },
        rules: {
          name: [
            { required: true, message: 'Please input Shop name', trigger: 'blur' },
            { min: 1, max: 32, message: 'Length should be 1 to 32', trigger: 'blur' },
          ],
          contact: [
            { required: true, validator: validateContact, trigger: 'blur' }
          ],
          location: [
            { required: true, message: 'Please choose location' },
          ],
          locationDetail: [
            { required: true, message: 'Please input Detailed location', trigger: 'blur' },
          ],
          licenseNum: [
            { required: true, validator: validateLicense, trigger: 'blur' }
          ],
          info: [
            { required: true, message: 'Please input Detailed location', trigger: 'blur' },
          ],
        }
      };
    },
    created: function() {
      Vue.axios.get('/api/getMyShop', {
        params: {
          id: sessionStorage.getItem('accessToken')
        }
      }).then((response) => {
        var data = response.data
        this.shopList = data
      })
    },
    methods: {
      handleShopURL(id) {
        this.$router.push({path:`/shopsystem/${id}`}).catch(err => {err})
      },
      submitApplyForm(formName){
        this.$refs[formName].validate((valid) => {
          if (valid) {
            console.log(JSON.stringify(this.applyForm))
            fetch("/api/submitShopApply",{
              method:"post",
              headers:{
                'content-type':'application/json'
              },
              body: JSON.stringify(this.applyForm)
            }).then((r) => {
              return r.json()
            }).then((data) => {
              console.log(data)
              if (data.status == 'ok'){
                this.$message.success(data.info);
              } else {
                this.$message.error(data.info);
                return false;
              }
            })
          } else {
            console.log('error submit!!');
            return false;
          }
        })
      }
    },
    components: {
      Header,
      Sidebar,
    }
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
