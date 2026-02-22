<template>
  <div class="app-container-publish" >

    <el-breadcrumb separator="/" style="font-size: 90%;margin-left: 1%">
      <el-breadcrumb-item :to="{path:'../bookManage'}">图书首页</el-breadcrumb-item>
      <el-breadcrumb-item>操作记录</el-breadcrumb-item>
    </el-breadcrumb>
    <!--搜索表单-->
    <div style="transform: scale(1.3);width: 60%;margin-left: 12%;margin-top: 4%">
      <el-form :inline="true" :model="searchInfo" class="demo-form-inline">
        <el-form-item label="记录信息">
          <el-input v-model="searchInfo" placeholder="请输入重要操作信息以查找" ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">查询</el-button>
          <el-button type="info" @click="clear">清空</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="page-content">
      <br>
      <!--表格-->
      <template>
        <el-table :data="tableData" style="width: 100%" max-height="540" @selection-change="handleSelectionChange">
          <el-table-column prop="record_id" label="记录编号" align="center" width="90"></el-table-column>
          <el-table-column prop="admin_id" label="管理员账号" align="center" width="100"></el-table-column>
          <el-table-column prop="affected_user_id" label="受影响的读者编号" width="120" align="center">
            <template slot-scope="scope">
              {{ scope.row.affected_user_id || '无' }}
            </template>
          </el-table-column>
          <el-table-column prop="affected_admin_id" label="受影响的管理员账号" width="130" align="center">
            <template slot-scope="scope">
              {{ scope.row.affected_admin_id || '无' }}
            </template>
          </el-table-column>
          <el-table-column prop="date_time" label="操作时间" align="center" min-width="150"></el-table-column>
          <el-table-column prop="content" label="操作内容" align="center" min-width="100"></el-table-column>
          <el-table-column prop="reason" label="操作原因" align="center" min-width="120"></el-table-column>
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
  page,
} from "@/api/getImportantOperation.js";
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

    page() {
      page(
          this.searchInfo,
          this.currentPage,
          this.pageSize
      ).then((res) => {
        this.totalCount = res.total_items;
        this.tableData = res.records
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
    // 复选框选中后执行的方法
    handleSelectionChange(val) {
      this.multipleSelection = val;
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
<style scoped>
.app-container-publish {
  margin-top: 1%;
}

.page-content {
  margin-left: 3%;
  margin-right: 3%;
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
