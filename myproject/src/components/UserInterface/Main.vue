<template>
    <el-col>
        <!-- upper content -->
        <el-row>
        <!-- recommended shop -->
        <el-col :span="12">
            <div style="background-color: #ececec; padding: 20px;">
            <a-row :gutter="16">
                <a-col :span="8">
                <a-card :bordered="true">
                    <p>Card content</p>
                </a-card>
                <a-card :bordered="true">
                    <p>Card content</p>
                </a-card>
                </a-col>
                <a-col :span="8">
                <a-card :bordered="true">
                    <p>Card content</p>
                </a-card>
                <a-card :bordered="true">
                    <p>Card content</p>
                </a-card>
                </a-col>
                <a-col :span="8">
                <a-card :bordered="true">
                    <p>Card content</p>
                </a-card>
                <a-card :bordered="true">
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
                <a-card :bordered="true">
                <p>Card content</p>
                </a-card>
                <a-card :bordered="true">
                <p>Card content</p>
                </a-card>
            </a-col>
            <a-col :span="4">
                <a-card :bordered="true">
                <p>Card content</p>
                </a-card>
                <a-card :bordered="true">
                <p>Card content</p>
                </a-card>
            </a-col>
            <a-col :span="4">
                <a-card :bordered="true">
                <p>Card content</p>
                </a-card>
                <a-card :bordered="true">
                <p>Card content</p>
                </a-card>
            </a-col>
            <a-col :span="4">
                <a-card :bordered="true">
                <p>Card content</p>
                </a-card>
                <a-card :bordered="true">
                <p>Card content</p>
                </a-card>
            </a-col>
            <a-col :span="4">
                <a-card :bordered="true">
                <p>Card content</p>
                </a-card>
                <a-card :bordered="true">
                <p>Card content</p>
                </a-card>
            </a-col>
            <a-col :span="4">
                <a-card :bordered="true">
                <p>Card content</p>
                </a-card>
                <a-card :bordered="true" @click="test">
                <p>Card content</p>
                </a-card>
            </a-col>
            </a-row>
        </div>
        </el-row>
    </el-col>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'MainTest',
    data() {
      return {
        formSearch: {
          searchtype: '',
          searchkey: '',
        },
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
        axios.get('http://127.0.0.1:5000/my_shop/apiTest').then(function (r) {
            console.log(r.data)
        })
      }

    }
  }
</script>

<style>
    a-card{
        width: 80%;
        height: 80%;
    }
    p{
        overflow: hidden;
    }
</style>