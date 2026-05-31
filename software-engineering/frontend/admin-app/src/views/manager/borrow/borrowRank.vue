<template>
  <div class="app-container-publish" >

    <el-breadcrumb separator="/" style="font-size: 90%;margin-left: 1%">
      <el-breadcrumb-item :to="{path:'../home'}">首页</el-breadcrumb-item>
      <el-breadcrumb-item>借阅排行</el-breadcrumb-item>
    </el-breadcrumb>
    <div style="margin-left: 3%;margin-right: 3%;margin-top: 3%">

      <br>
      <!--表格-->
      <template>
        <el-table :data="tableData" style="width: 100%"  max-height="540" >
          <el-table-column prop="title" label="图书名称" align="center" width="130%"></el-table-column>
          <el-table-column prop="book_id" label="图书编号" align="center" width="150%"></el-table-column>
          <el-table-column prop="author" label="作者" align="center" width="150%"></el-table-column>
          <el-table-column prop="publisher" label="出版社" align="center" width="150%"></el-table-column>
          <el-table-column prop="publish_date" label="出版日期" align="center" width="150%"></el-table-column>
          <el-table-column prop="intro" label="简介" align="center" ></el-table-column>
          <el-table-column prop="all_count" label="总借阅次数" align="center" width="150%"></el-table-column>
        </el-table>

      </template>

    </div>

  </div>
</template>

<script>
import {
  getTop
} from "@/api/getBook.js";

export default {
  data() {
    return {
      // 表格数据
      tableData: [],
    };
  },

  mounted() {
    this.getBorrowRank(); //当页面加载完成后，发送异步请求，获取数据
  },

  methods: {
    // 查询分页数据
    getBorrowRank() {
      getTop().then((res) => {
        if(res.code===200)
          this.tableData = res.books
        else {
          this.$message.warning(res.message)
        }
      }).catch(err=>{
        this.$alert(err.message)
      })
    },

  },
};
</script>
<style>
.app-container-publish {
  margin-top: 1%;
  left: 15%;

}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  line-height: 100px;
  text-align: center;
}

.avatar {
  width: 100px;
  height: 100px;
  display: block;
}
.el_dialog_publish{
  margin-top: 7vw;
  margin-left: 7vw;
}
</style>
