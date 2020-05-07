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
          <el-button>Search</el-button>
        </el-form-item>
      </el-form>
    </el-row>
    <!-- add dishes -->
    <el-row type="flex" justify="center">
      <el-button @click="dishesFormVisible = true" style='margin-bottom:20px;'>add dishes</el-button>
      <el-dialog title="dishes information" :visible.sync="dishesFormVisible">
        <el-form ref="form" :model="dishesForm" label-width="80px">
          <el-form-item label="Name">
            <el-input v-model="dishesForm.name"></el-input>
          </el-form-item>
          <el-form-item label="Price">
            <el-input v-model="dishesForm.price"></el-input>
          </el-form-item>
          <el-form-item label="Discription">
            <el-input v-model="dishesForm.info"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button @click="dishesFormVisible = false">Cancel</el-button>
            <el-button type="primary" @click="submitDishForm('form')">Submit</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
    </el-row>
    <!-- dishes  -->
    <el-row>
      <div class="demo-infinite-container">
        <a-list :dataSource="dishesData" :grid="{ column: 2 }">
          <a-list-item slot="renderItem" slot-scope="item">
            <el-card class="box-card">
              <div slot="header" class="clearfix">
                <span>{{item.name}}</span>
                <el-button style="float: right; padding: 3px 0" type="text"  @click='dishDetailHandle(item)'>Edit</el-button>
                <el-popconfirm
                  confirmButtonText='Yes'
                  cancelButtonText='Cancel'
                  icon="el-icon-info"
                  iconColor="red"
                  title="Are you sure to delete the dish?"
                  @onConfirm="dishDelete(item.productid)"
                >
                <el-button style="float: right; padding: 3px 5px" type="text" slot="reference">Delete</el-button>
                </el-popconfirm>
              </div>
              <span>{{item.info}}</span>
              <el-row type="flex" justify="space-between">
                <span>Sales: {{item.sale}}</span>
                <span>Price: {{item.price}}</span>
              </el-row>
            </el-card>
            <br/>
          </a-list-item>
        </a-list>
      </div>
    </el-row>
    <el-dialog
      title="Edit dishes"
      :visible.sync="editFormVisible"
      width="50%"
      @close="editFormVisible=false">
      <el-form :model="editForm" ref="editModel" label-width="160px">
        <el-form-item label="Dish name">
          <el-input v-model="editForm.name"></el-input>
        </el-form-item>
        <el-form-item label="Dish price">
          <el-input v-model.number="editForm.price"></el-input>
        </el-form-item>
        <el-form-item label="Dish discription">
          <el-input v-model="editForm.info"></el-input>
        </el-form-item>
      </el-form>
      
      <span slot="footer">
        <el-button @click="editFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="submitDishEdit('editModel')">Confirm</el-button>
      </span>
    </el-dialog>
    
  </el-col>
</el-row>
</template>

<script>
  import Vue from 'vue'
  // import reqwest from 'reqwest';
  import infiniteScroll from 'vue-infinite-scroll';

  export default {
    name: 'DishesManagementMain',
    directives: { infiniteScroll },
    data() {
      return {
        dishesFormVisible: false,
        editFormVisible: false,
        dishesData: [],
        editForm: {
          name: '',
          price: '',
          info: '',
        },
        dishesForm: {
          shopid: '',
          userid: '',
          name: '',
          price: '',
          info: '',
        },
        formSearch: {
          searchtype: '',
          searchkey: '',
        },
      };
    },
    beforeMount() {
      // this.fetchData(res => {
      //   this.dishesData = res.results;
      // });
      Vue.axios.get('/api/getDishes', {
        params: {
          user_id: sessionStorage.getItem('accessToken'),
          shop_id: sessionStorage.getItem('shop_id')
        }
      }).then((response) => {
        var data = response.data
        this.dishesData = data
      })
    },
    methods: {
      submitDishForm(formName) {
        this.$data.dishesForm['shopid'] = sessionStorage.getItem('shop_id')
        this.$data.dishesForm['userid'] = sessionStorage.getItem('accessToken')
        this.$refs[formName].validate((valid) => {
          if (valid) {
            fetch("/api/submitDish",{
              method:"post",
              headers:{
                'content-type':'application/json'
              },
              body: JSON.stringify(this.dishesForm)
            }).then((r) => {
              return r.json()
            }).then((data) => {
              console.log(data)
              if (data.status == 'ok'){
                this.$message.success('Add dish success!');
                this.$data.dishesFormVisible = false;
                setTimeout(() =>{
                  location.reload();
                },1000);
              } else {
                this.$message.error('Add dish failed.');
                return false;
              }
            })
          } else {
            this.$message.error('Error submit!!');
            return false;
          }
        });
      },
      submitDishEdit(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            fetch("/api/editDish",{
              method:"post",
              headers:{
                'content-type':'application/json'
              },
              body: JSON.stringify(this.editForm)
            }).then((r) => {
              return r.json()
            }).then((data) => {
              console.log(data)
              if (data.status == 'ok'){
                this.$message.success('Edit dish success!');
                this.$data.editFormVisible = false;
                setTimeout(() =>{
                  location.reload();
                },1000);
              } else {
                this.$message.error('Edit dish failed.');
                return false;
              }
            })
          } else {
            this.$message.error('Error submit!!');
            return false;
          }
        });
      },
      dishDelete(id) {
        let form = {
          userid: sessionStorage.getItem('accessToken'),
          shopid: sessionStorage.getItem('shop_id'),
          productid: id
        }
        fetch("/api/deleteDish",{
          method:"post",
          headers:{
            'content-type':'application/json'
          },
          body: JSON.stringify(form)
        }).then((r) => {
          return r.json()
        }).then((data) => {
          console.log(data)
          if (data.status == 'ok'){
            this.$message.success('Delete dish success!');
            this.$data.editFormVisible = false;
            setTimeout(() =>{
              location.reload();
            },1000);
          } else {
            this.$message.error('Eelete dish failed.');
            return false;
          }
        })
      },
      dishDetailHandle(item) {
        this.editFormVisible = true
        for (let key in item) {
          this.editForm[key] = item[key]
        }
        console.log('im working')
        this.editForm['shopid'] = sessionStorage.getItem('shop_id')
        this.editForm['userid'] = sessionStorage.getItem('accessToken')
      },
      handleInfiniteOnLoad() {
        const data = this.dishesData;
        this.loading = true;
        if (data.length > 14) {
          this.$message.warning('Infinite List loaded all');
          this.busy = true;
          this.loading = false;
          return;
        }
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

</style>