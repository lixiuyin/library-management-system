<template>
  <div class="app-container-publish" >

    <el-breadcrumb separator="/" style="font-size: 90%;margin-left: 1%">
      <el-breadcrumb-item :to="{path:'../bookManage'}">图书首页</el-breadcrumb-item>
      <el-breadcrumb-item>管理员管理</el-breadcrumb-item>
    </el-breadcrumb>
    <!--搜索表单-->
    <div style="transform: scale(1.3);width: 60%;margin-left: 12%;margin-top: 4%">
      <el-form :inline="true" :model="searchInfo" class="demo-form-inline">
        <el-form-item label="管理员">
          <el-input v-model="searchInfo" placeholder="请输入管理员信息以查找" ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">查询</el-button>
          <el-button type="info" @click="clear">清空</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="page-content">
      <!--按钮-->
      <div class="action-buttons">
        <el-button type="primary" size="medium" @click="passwordDialogVisible = true; Pass = { };">添加管理员</el-button>
      </div>
      <!--修改密码对话框表单-->
      <el-dialog class="el_dialog_publish" ref="form" title="修改密码" :visible.sync="passwordDialogVisible" width="30%">
        <el-form ref="User" :model="Pass" label-width="80px" size="mini" >
          <el-form-item label="新密码" prop="newPassword">
            <el-input v-model="Pass.newPassword" aria-placeholder="输入新密码" ></el-input>
          </el-form-item>
          <el-form-item label="再输一次" prop="againPassword">
            <el-input v-model="Pass.againPassword" aria-placeholder="再次输入新密码" ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button  @click="add" >确认修改</el-button>
            <el-button @click="passwordDialogVisible = false">取消修改</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
      <br>
      <!--表格-->
      <template>
        <el-table :data="tableData" style="width: 100%" border max-height="540.6px" max-width @selection-change="handleSelectionChange">
          <!--  复选框       -->
          <el-table-column prop="admin_id" label="管理员编号" align="center" width="130%"></el-table-column>
          <el-table-column prop="password" label="管理员密码" align="center"></el-table-column>
          <el-table-column align="center" label="操作">
            <template slot-scope="scope">
              <el-row>
                <el-col :span="12">
                  <el-button  type="primary" size="small" @click="update(scope.row.admin_id)">改密</el-button>
                </el-col>
                <el-col :span="12">
                  <el-button  type="danger" size="small" @click="deleteById(scope.row.admin_id)">删除</el-button>
                </el-col>

              </el-row>
            </template>
          </el-table-column>
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
  add ,
  deleteAdminById as deleteById,
  update,
  page
} from "@/api/getAdmin.js";
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
      //修改密码话框是否展示的标记
      passwordDialogVisible:false,
      //密码相关信息
      Pass:{
        newPassword:"",
        againPassword:"",
      },
      //选中的id
      selected_id:"",
      // 搜索信息
      searchInfo: "",
      //新增读者信息
      newAdmin:{},
      // 表格数据
      tableData: [],

    };
  },

  mounted() {
    this.page();
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
        this.tableData = res.admins
      }).catch(err=>{
        this.$alert(err.message)
      })

    },
    // 添加数据
    add() {
      let operator;
      if (this.selected_id) {
        //修改
          operator = update(this.selected_id,this.Pass.newPassword);
      } else {
        operator = add(this.Pass.newPassword);
      }
      operator.then((resp) => {
        if (resp.code === 200) {
          // this.dialogVisible = false;
          this.page();
          this.passwordDialogVisible=false
          this.$message({
            message: "保存成功",
            type: "success"
          })
        } else {
          this.$message.error(resp.message);
        }
      }).catch(err=>{
        this.$message.error(err.message);
      });
    },
    //打开修改窗口
    update(admin_id) {
      //1. 打开窗口
      this.passwordDialogVisible= true;
      this.selected_id=admin_id
    },
    //删除
    deleteById(admin_id){
      this.$confirm("是否继续删除?", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(()=>{
        deleteById(admin_id).then(res=>{
          if(res.code===200){
            this.$message.success(res.message)
            this.page()
          }
          else {
            this.$message.warning(res.message)
          }
        }).catch(err=>{
          this.$message.error(err.message)
        })
      }).catch(()=>{
        this.$message.success("已取消")
      })
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

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 12px;
  margin-bottom: 8px;
}

.table-operation-btns {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  align-items: center;
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
