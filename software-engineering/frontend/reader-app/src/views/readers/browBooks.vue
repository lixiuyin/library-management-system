<template>
  <div class="app-container-publish" >

    <el-breadcrumb separator="/" style="font-size: 90%;margin-left: 1%">
      <el-breadcrumb-item :to="{path:'../home'}">首页</el-breadcrumb-item>
      <el-breadcrumb-item>浏览图书</el-breadcrumb-item>
    </el-breadcrumb>
    <!--搜索表单-->
    <div style="transform: scale(1.3);width: 60%;margin-left: 12%;margin-top: 4%">
      <el-form :inline="true" :model="searchInfo" class="demo-form-inline">
        <el-form-item label="图书信息">
          <el-input v-model="searchInfo" placeholder="请输入图书信息以查找" ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">查询</el-button>
          <el-button type="info" @click="clear">清空</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div style="margin-left: 3%;margin-right: 3%">

      <br>
      <!--表格-->
      <template>
        <el-table :data="tableData" style="width: 100%"  max-height="540" >
<!--  这个是复选框，这个部分不需要        -->
<!--          <el-table-column type="selection" width="55" align="center"></el-table-column>-->
          <el-table-column prop="title" label="图书名称" align="center" width="130%"></el-table-column>
          <el-table-column prop="book_id" label="图书编号" align="center" width="150%"></el-table-column>
          <el-table-column prop="category_code" label="分类编码" align="center"></el-table-column>
          <el-table-column prop="isbn" label="ISBN" align="center"></el-table-column>
          <el-table-column prop="author" label="作者" align="center" width="150%"></el-table-column>
          <el-table-column prop="publisher" label="出版社" align="center" width="150%"></el-table-column>
          <el-table-column prop="intro" label="简介" align="center" width="100px"></el-table-column>
          <el-table-column prop="status" label="当前状态" align="center" width="100px"></el-table-column>
        </el-table>

      </template>
      <!--分页工具条-->
      <div style="text-align: center;margin-top:1%">
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :background="background"
                       :current-page="currentPage" :page-sizes="[5, 10, 15, 20]" :page-size="5"
                       layout="total, sizes, prev, pager, next, jumper" :total="totalCount">
        </el-pagination>

    </div>
    </div>
  </div>
</template>

<script>
import {
  // add,
  // deleteById,
  page,
  // update,
  // getById
} from "@/api/getBook.js";
import {
  getToken
} from '@/utils/auth.js';
export default {
  data() {
    return {
      background: true,
      // 每页显示的条数
      pageSize: 5,
      // 总记录数
      totalCount: 0,
      // 当前页码
      currentPage: 1,
      // 搜索图书信息
      searchInfo: "",
      // 表格数据
      tableData: [],
    };
  },

  mounted() {
    this.page(); //当页面加载完成后，发送异步请求，获取数据

  },

  methods: {
    // 查询分页数据
    page() {
      page(
          this.searchInfo,
          this.currentPage,
          this.pageSize
      ).then((res) => {
        this.totalCount = res.total_items;
        this.tableData = res.books
      });
    },

    // 查询方法
    onSubmit() {
      this.currentPage = 1;
      this.page();
    },
    clear() {
      this.searchInfo = ''
      this.page();
    },


    //分页
    handleSizeChange(val) {
      // 重新设置每页显示的条数
      this.pageSize = val;
      this.page();
    },

    handleCurrentChange(val) {
      // 重新设置当前页码
      this.currentPage = val;
      this.page();
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
