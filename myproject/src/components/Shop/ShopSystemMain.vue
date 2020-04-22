<template>
  <div>
    <!-- main -->
    <el-row type="flex">
      <!-- basic info -->
      <el-col :span="18">
        <a-card  style="width: 300px">
          <p>name:</p>
          <p>rate:</p>
          <p>status:</p>
        </a-card>
      </el-col>
    </el-row>
    <el-row>
        <el-button>close shop</el-button>
        <el-button>open shop</el-button>
    </el-row>
  </div>
</template>

<script>
export default {
    name: 'ShopSystemMain',
}
</script>