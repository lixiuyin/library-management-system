<template>
  <div class="app-container-publish" >

    <el-breadcrumb separator="/" style="font-size: 90%;margin-left: 1%">
      <el-breadcrumb-item :to="{path:'../bookManage'}">图书首页</el-breadcrumb-item>
      <el-breadcrumb-item>借阅管理</el-breadcrumb-item>
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
    <div class="page-content">
      <!--按钮-->
      <div class="action-buttons">
        <el-button type="success" size="medium" @click="borrowByIds()">批量借阅</el-button>
        <el-button type="warning" size="medium" @click="returnByIds()">批量归还</el-button>
        <el-button type="info" size="medium" @click="continueByIds()">批量续借</el-button>
      </div>

      <!--选择借阅人表单-->
      <el-dialog class="el_dialog_publish" ref="form" title="上架图书信息" :visible.sync="dialogVisible" width="30%">
        <el-form ref="form" :model="borrower" label-width="80px" size="mini">
          <el-form-item label="输入借阅人">
            <el-input v-model="borrower.user_id" placeholder="请输入借阅人id" @input="checkLength"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="borrowById()" style="margin-left: 0vw">提交</el-button>
            <el-button @click="dialogVisible = false">取消</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
      <br>
      <!--表格-->
      <template>
        <el-table :data="tableData" style="width: 100%"  @selection-change="handleSelectionChange" max-height="540"  >
          <!--  复选框       -->
          <el-table-column type="selection" width="55" align="center"></el-table-column>
          <el-table-column prop="title" label="图书名称" align="center" width="130%"></el-table-column>
          <el-table-column prop="book_id" label="图书编号" align="center" width="150%"></el-table-column>
          <el-table-column prop="category_code" label="分类编码" align="center"></el-table-column>
          <el-table-column prop="isbn" label="ISBN" align="center" width="130%"></el-table-column>
          <el-table-column prop="author" label="作者" align="center" width="150%"></el-table-column>
          <el-table-column prop="publisher" label="出版社" align="center" width="150%"></el-table-column>
          <el-table-column prop="publish_date" label="出版日期" align="center" width="150%"></el-table-column>
          <el-table-column prop="intro" label="简介" align="center" width="100px"></el-table-column>
          <el-table-column prop="status" label="当前状态" align="center" width="100px"></el-table-column>
          <el-table-column align="center" label="操作">
            <template slot-scope="scope">
              <el-row>
                <el-col :span="12">
                  <el-button  type="success" size="small" @click="borrow(scope.row.book_id)">借阅</el-button>
                </el-col>
                <el-col :span="12">
                  <el-button  type="warning" size="small" @click="returnById(scope.row.book_id)">归还</el-button>
                </el-col>
                <el-col :span="12">
                  <el-button  type="info" size="small" @click="continueById(scope.row.book_id)">续借</el-button>
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
  page,
} from "@/api/getBook.js";
import {
    borrow,
    borrow_continue,
    borrow_return,
    // getById
} from "@/api/getBorrow";
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
      // 添加数据对话框是否展示的标记
      dialogVisible: false,
      // 搜索图书信息
      searchInfo: "",
      //借书人的id
      borrower:{
        user_id:""
      },
      //被借的书的id
      selected_id:"",
      // 被选中的id数组
      selectedIds: [],
      //是否是批量删除
      isMany:false,
      // 复选框选中数据集合
      multipleSelection: [],
      // 表格数据
      tableData: [],
      headers: {
        Authorization: getToken(),
      }
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
          this.searchInfo,
          this.currentPage,
          this.pageSize
      ).then((res) => {
        this.totalCount = res.total_items;
        this.tableData = res.books
      });
    },
    //打开借阅对话框
    borrow(book_id){
      this.isMany=false
      this.dialogVisible=true
      this.selected_id=book_id
    },
    //批量借阅时打开对话框进行填写
    borrowByIds(){
      // 弹出确认提示框
      this.isMany=true
      this.dialogVisible=true
      //获取多选的全部书的id
      for (let i = 0; i < this.multipleSelection.length; i++) {
        this.selectedIds[i] = this.multipleSelection[i].book_id;
      }
    },
    //进行借阅请求
    borrowById(){
      if(this.isMany===false){
        this.$confirm("您确定借阅这本书吗?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }).then(() => {
          //2. 发送AJAX请求
          borrow(this.selected_id,this.borrower.user_id).then((res) => {
            if (res.code === 200) {
              //删除成功
              this.$message.success("恭喜你，借阅成功");
              this.page();
            } else {
              this.$message.error(res.message);
            }
          }).catch(err=>{
            this.$alert(err.message)
            this.$confirm("是否重新借阅", "提示", {
              confirmButtonText: "确定",
              cancelButtonText: "取消",
              type: "warning",
            }).then(()=>{
              this.borrower.user_id=""
            }).catch(()=>{
              this.borrower.user_id=""
              this.dialogVisible=false
            })
          })
        }).catch(() => {
          //用户点击取消按钮
          this.borrower.user_id=""
          this.$message.info("已取消借阅");
        });
      }
      else{
        this.$confirm("此操作将批量借阅这些图书, 是否继续?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }).then(() => {
          //发送请求
          for(let i = 0; i < this.selectedIds.length; i++){
            borrow(this.selectedIds[i],this.borrower.user_id).then((res) => {
              if (res.code === 200) {
                //删除成功
                this.$message.success("借阅成功");
                this.page();
              } else {
                this.$message.error(res.message);
              }
            }).catch(err=>{
              this.$alert(err.message)
            })
          }
        }).catch(() => {
          //用户点击取消按钮
          this.borrower.user_id=""
          this.$message.info("已取消借阅");
        });
      }
    },
    //单独进行归还
    returnById(book_id){
      borrow_return(book_id).then(res=>{
        if(res.code===200){
          this.$message.success("归还成功")
          this.page()
        }
        else{
          this.$message.error(res.message);
        }
      }).catch(err=>{
        this.$alert(err.message)
      })
    },
    //批量归还
    returnByIds(){
      //获取多选的全部书的id
      for (let i = 0; i < this.multipleSelection.length; i++) {
        this.selectedIds[i] = this.multipleSelection[i].book_id;
      }
      this.$confirm("此操作将批量归还这些图书, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
        //发送请求
        for(let i = 0; i < this.selectedIds.length; i++){
          borrow_return(this.selectedIds[i]).then((res) => {
            if (res.code === 200) {
              //删除成功
              this.$message.success("归还成功");
              this.page();
            } else {
              this.$message.error(res.message);
            }
          }).catch(err=>{
            this.$alert(err.message)
          })
        }
      }).catch(() => {
        //用户点击取消按钮
        this.$message.info("已取消归还");
      });

    },
    //续借
    continueById(book_id){
      borrow_continue(book_id).then(res=>{
        if(res.code===200){
          this.$message.success("续借成功")
        }
        else{
          this.$message.error(res.message);
        }
      }).catch(err=>{
        this.$alert(err.message)
      })
    },
    //批量续借
    continueByIds(){
      //获取多选的全部书的id
      for (let i = 0; i < this.multipleSelection.length; i++) {
        this.selectedIds[i] = this.multipleSelection[i].book_id;
      }
      this.$confirm("此操作将批量续借这些图书, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
        //发送请求
        for(let i = 0; i < this.selectedIds.length; i++){
          borrow_continue(this.selectedIds[i]).then((res) => {
            if (res.code === 200) {
              //删除成功
              this.$message.success("续借成功");
              this.page();
            } else {
              this.$message.error(res.message);
            }
          }).catch(err=>{
            this.$alert(err.message)
          })
        }
      }).catch(() => {
        //用户点击取消按钮
        this.$message.info("已取消续借");
      });
    },
    // 复选框选中后执行的方法
    handleSelectionChange(val) {
      this.multipleSelection = val;
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
