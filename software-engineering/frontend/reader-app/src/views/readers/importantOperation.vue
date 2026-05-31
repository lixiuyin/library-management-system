<template>
  <div class="app-container-publish" >

    <el-breadcrumb separator="/" style="font-size: 90%;margin-left: 1%">
      <el-breadcrumb-item :to="{path:'../home'}">首页</el-breadcrumb-item>
      <el-breadcrumb-item>重要操作记录</el-breadcrumb-item>
    </el-breadcrumb>
    <div style="margin-left: 3%;margin-right: 3%;margin-top: 3%">
      <br>
      <!--表格-->
      <template>
        <el-table :data="tableData" style="width: 100%"  max-height="540" >
          <el-table-column prop="record_id" label="记录编号" align="center" width="150%"></el-table-column>
          <el-table-column prop="date_time" label="操作时间" align="center"></el-table-column>
          <el-table-column prop="content" label="操作内容" align="center"></el-table-column>
          <el-table-column prop="reason" label="操作原因" align="center" width="150%"></el-table-column>
        </el-table>

      </template>
      <!--分页工具条-->
      <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :background="background"
                     :current-page="currentPage" :page-sizes="[5, 10, 15, 20]" :page-size="5"
                     layout="total, sizes, prev, pager, next, jumper" :total="totalCount" style="margin-top: 10px;text-align: center">
      </el-pagination>

    </div>

  </div>
</template>

<script>
import {
  page,
} from "@/api/getImportantOperation.js";
export default {
  data() {
    return {
      background: true,
      // 每页显示的条数
      pageSize: 5,
      // 总记录数
      totalCount: 100,
      // 当前页码
      currentPage: 1,

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
          this.currentPage,
          this.pageSize
      ).then((res) => {
        this.totalCount = res.total_items;
        this.tableData = res.records;
      });
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
