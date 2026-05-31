<template>
  <div class="app-container-publish" >

    <el-breadcrumb separator="/" style="font-size: 90%;margin-left: 1%">
      <el-breadcrumb-item :to="{path:'../home'}">首页</el-breadcrumb-item>
      <el-breadcrumb-item>充值记录</el-breadcrumb-item>
    </el-breadcrumb>
    <div style="margin-left: 3%;margin-right: 3%;margin-top: 3%">

      <br>
      <!--表格-->
      <template>
        <el-table :data="tableData" style="width: 100%"  max-height="540" >
          <!--  这个是复选框，这个部分不需要        -->
          <!--          <el-table-column type="selection" width="55" align="center"></el-table-column>-->
          <el-table-column prop="record_id" label="记录编号" align="center" width="150%"></el-table-column>
          <el-table-column prop="value" label="变动金额" align="center"></el-table-column>
          <el-table-column prop="date" label="变动日期" align="center"></el-table-column>
          <el-table-column prop="reason" label="变动原因" align="center" width="150%"></el-table-column>
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
} from "@/api/getCharge.js";
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
      // 添加数据对话框是否展示的标记
      dialogVisible: false,
      // 表格数据
      tableData: [],

    };
  },

  mounted() {
    this.page(); //当页面加载完成后，发送异步请求，获取数据

  },

  methods: {
    // checkLength() {
    //   if (this.information.hotelName.length>20 ) {
    //     this.$alert('标题长度不能大于20', '警告', {
    //       confirmButtonText: '确定',
    //       callback: action => {
    //         this.information.hotelName = ''; // 清空输入框的值
    //       }
    //     });
    //   }
    // },
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
    // 复选框选中后执行的方法
    // handleSelectionChange(val) {
    //   this.multipleSelection = val;
    // },
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
