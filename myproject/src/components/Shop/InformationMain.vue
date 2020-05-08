<template>
<div>
  <p style="font-size: 25px;">Shop information</p>
  <!-- main -->
  <el-row>
    <el-col :span="16">
      <!-- List for information-->
      <a-list itemLayout="vertical" :dataSource="infoData">
        <a-list-item slot="renderItem" slot-scope="item">
          <a-list-item-meta>
            <span slot="title">{{item.title}} : </span>
          </a-list-item-meta>
          <p style='word-wrap:break-word;'>{{item.content}}</p>
        </a-list-item>
      </a-list>
      <el-button @click="infoFormVisible = true">Edit</el-button>
    </el-col>
  </el-row>
  <el-dialog title="Modify information" :visible.sync="infoFormVisible">
    <el-form ref='infoModel' :model="shopInfo" :rules="rules" label-width="30%">
      <el-form-item label="Shop name" prop='name'>
        <el-input v-model='shopInfo.name'></el-input>
      </el-form-item>
      <el-form-item label="Shop contact" prop='contact'>
        <el-input v-model='shopInfo.contact'></el-input>
      </el-form-item>
      <el-form-item label="Shop location" prop='location'>
        <el-select v-model="shopInfo.location" placeholder="Please choose">
          <el-option
            v-for="item in locationOptions"
            :key="item.value"
            :label="item.value"
            :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Detailed location" prop='locationDetail'>
        <el-input v-model='shopInfo.locationDetail' 
                  type="textarea"
                  :autosize="{ minRows: 2, maxRows: 5 }"
                  maxlength="256"
                  show-word-limit>
        </el-input>
      </el-form-item>
      <el-form-item label="ID number" prop='licenseNum'>
        <el-input v-model='shopInfo.licenseNum'></el-input>
      </el-form-item>
      <el-form-item label="Shop information" prop='info'>
        <el-input v-model='shopInfo.info'
                  type="textarea"
                  :autosize="{ minRows: 2, maxRows: 5 }"
                  maxlength="256"
                  show-word-limit>
        </el-input>
      </el-form-item>
      <el-form-item label='Delivery fee'>
        <div class="block">
          <el-slider
            v-model="shopInfo.delivery"
            :step="1"
            :min="0"
            :max="5"
            :marks="{
              0:'0',
              1:'1',
              2:'2',
              3:'3',
              4:'4',
              5:'5'
            }"
            show-stops>
          </el-slider>
        </div>
      </el-form-item>
      <el-form-item label="Shop status">
        <el-radio v-model="shopInfo.shopStatus" label='open'></el-radio>
        <el-radio v-model="shopInfo.shopStatus" label='closed'></el-radio>
      </el-form-item>
      <el-form-item>
        <el-button @click="infoFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="submitInfoForm('infoModel')">Confirm</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</div>
</template>

<script>
import Vue from 'vue'
let infoData = [];
const locationOptions = [
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
];
export default {
  name: 'InformationMain',
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
      infoFormVisible: false,
      shopInfo: {
        shopid: '',
        userid: '',
        name: '',
        info: '',
        contact: '',
        delivery: '',
        location: '',
        locationDetail: '',
        shopStatus: '',
        licenseNum: '',
      },
      infoData,
      locationOptions,
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

  methods: {
    submitInfoForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          console.log(JSON.stringify(this.shopInfo))
          fetch("/api/submitShopInfo",{
            method:"post",
            headers:{
              'content-type':'application/json'
            },
            body: JSON.stringify(this.shopInfo)
          }).then((r) => {
            return r.json()
          }).then((data) => {
            console.log(data)
            if (data.status == 'ok'){
              this.$message.success(data.info);
              this.$data.infoFormVisible = false;
              location.reload();
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
    },
  },

  created() {
    Vue.axios.get('/api/getShopInfo', {
      params: {
        user_id: sessionStorage.getItem('accessToken'),
        shop_id: sessionStorage.getItem('shop_id')
      }
    }).then((response) => {
      var data = response.data
      var status = data['status']
      if (status === 'invalid') {
        this.$message.warning("Invalid access. You don't have the permission to access this shop page.")
        this.$router.push({path:`/personalinfo`}).catch(err => {err})
      } else if (status === 'cancelled') {
        this.$message.error("Sorry, the shop have been shut down.")
        this.$router.push({path:`/personalinfo`}).catch(err => {err})
      } else {
        this.shopInfo.shopid = data['shopid']
        this.shopInfo.userid = data['userid']
        this.shopInfo.name = data['name']
        this.shopInfo.contact = data['contact']
        this.shopInfo.info = data['info']
        this.shopInfo.delivery = data['delivery']
        this.shopInfo.location = data['location']
        this.shopInfo.locationDetail = data['locationDetail']
        this.shopInfo.shopStatus = data['shopStatus']
        this.shopInfo.licenseNum = data['licenseNum']
        this.infoData.push({'title': 'Name','content': data['name']})
        this.infoData.push({'title': 'Shop contact','content': data['contact']})
        this.infoData.push({'title': 'Shop information','content': data['info']})
        this.infoData.push({'title': 'Delivery fee','content': data['delivery']})
        this.infoData.push({'title': 'Location','content': data['location']})
        this.infoData.push({'title': 'Detailed location','content': data['locationDetail']})
        this.infoData.push({'title': 'Shop status','content': data['shopStatus']})
        this.infoData.push({'title': 'ID number','content': data['licenseNum']})
      }
    })
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