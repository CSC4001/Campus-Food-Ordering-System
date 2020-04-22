<template>
  <!-- main -->
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
      </el-col>
    </el-row>

    <!-- apply -->
    <!-- <el-row type="flex" justify="center">
        <el-button>close shop</el-button>
    </el-row>
    <el-row type="flex" justify="center">
        <el-button>open shop</el-button>
    </el-row> -->
</template>
<script>

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
    name: 'InformationMain',
    data() {
      return {
        infoFormVisible: false,
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