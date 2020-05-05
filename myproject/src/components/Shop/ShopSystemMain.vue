<template>
  <div >
    <p style="font-size: 25px;">Shop information</p>
    <!-- main -->
    <el-row type="flex">
      <!-- basic info -->
      <el-col :span="24">
        <a-card  style="width: 300px">
          <p>Name:{{shopInfo.name}}</p>
          <p>Rate:{{shopInfo.rateTotal}}</p>
          <p>Status:{{shopInfo.status}}</p>
          <p>Infomation:{{shopInfo.info}}</p>
        </a-card>
        <el-button @click='submitCancelApply' style='margin-top:10px' type="primary" plain>Close this shop</el-button>
        <el-button @click='submitUnblockApply' style='margin-top:10px' type="primary" plain>Apply to unblock</el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
    name: 'ShopSystemMain',
    data() {
      return {
        shopInfo: {
          shopid: '',
          userid: '',
          name: '',
          info: '',
          status: '',
          rateTotal: '',
          rateNum: ''
        }
      }
    },
    methods: {
      submitCancelApply() {
        Vue.axios.get('/api/submitCancelApply', {
          params: {
            id: this.$route.params['shop_id']
          }
        }).then((response) => {
          var status = response.data['status']
          if (status === 'invalid') {
            this.$message.error('Cannot do this operation.')
          } else {
            this.$message.success('Successfully submitted the cancelling shop application!')
          }
        })
      },
      submitUnblockApply() {
        Vue.axios.get('/api/submitUnblockApply', {
          params: {
            id: this.$route.params['shop_id']
          }
        }).then((response) => {
          var status = response.data['status']
          if (status === 'invalid') {
            this.$message.error('Cannot do this operation.')
          } else {
            this.$message.success('Successfully submitted the unblock shop application!')
          }
        })
      }
    },
    created() {
      Vue.axios.get('/api/getShopIndex', {
        params: {
          user_id: sessionStorage.getItem('accessToken'),
          shop_id: this.$route.params['shop_id']
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
          this.shopInfo.info = data['info']
          this.shopInfo.status = data['shopStatus']
          this.shopInfo.rateTotal = data['rateTotal']
          this.shopInfo.rateNum = data['rateNum']
        }
      })
    },
}
</script>