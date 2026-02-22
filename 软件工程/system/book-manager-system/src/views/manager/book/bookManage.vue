<template>
  <div class="app-container-publish" >

    <el-breadcrumb separator="/" style="font-size: 90%;margin-left: 1%">
      <el-breadcrumb-item>图书首页</el-breadcrumb-item>
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
        <el-button type="danger" size="medium" @click="deleteByIds()">批量下架</el-button>
        <el-button type="primary" size="medium" @click="dialogVisible = true; newBook = { };">上架图书</el-button>
      </div>

      <!--添加数据对话框表单-->
      <el-dialog class="el_dialog_publish" ref="form" title="上架图书信息" :visible.sync="dialogVisible" width="30%">
        <el-form ref="form" :model="newBook" label-width="80px" size="mini">
          <el-form-item label="图书名称">
            <el-input v-model="newBook.title" placeholder="请输入图书名称" @input="checkLength"></el-input>
          </el-form-item>
          <el-form-item label="分类编码">
            <el-select v-model="newBook.category_code" filterabl placeholder="请选择分类" >
              <i slot="prefix" class="el-input__icon el-icon-male signIn-input-icon"></i>
              <el-option
                  v-for="item in category_codes"
                  :key="item.code"
                  :label="item.name"
                  :value="item.code"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="ISBN">
            <el-input v-model="newBook.isbn" placeholder="请输入ISBN"></el-input>
          </el-form-item>
          <el-form-item label="作者">
            <el-input v-model="newBook.author" placeholder="请输入作者"></el-input>
          </el-form-item>
          <el-form-item label="出版社">
            <el-input v-model="newBook.publisher" placeholder="请输入出版社"></el-input>
          </el-form-item>
          <el-form-item label="出版日期">
            <el-date-picker
                v-model="newBook.publish_date"
                align="right"
                type="date"
                placeholder="选择日期"
                :picker-options="pickerOptions">
            </el-date-picker>
          </el-form-item>
          <el-form-item label="价格">
            <el-input v-model="newBook.price" placeholder="请输入价格"></el-input>
          </el-form-item>
          <el-form-item label="简介">
            <el-input v-model="newBook.intro" placeholder="请输入图书简介"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="add" style="margin-left: 0vw">提交</el-button>
            <el-button @click="dialogVisible = false">取消</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
<!--      下架图书表单-->
      <el-dialog class="el_dialog_publish" ref="form" title="下架原因" :visible.sync="deleteDialogVisible" width="30%">
        <el-form ref="form" :model="operation_reason" label-width="80px" size="mini">
          <el-form-item label="下架原因">
            <el-input v-model="operation_reason" placeholder="请输入下架原因" ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="deleteById()" style="margin-left: 0vw">提交</el-button>
            <el-button @click="deleteDialogVisible = false">取消</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
      <br>
      <!--表格-->
      <template>
        <el-table :data="tableData" style="width: 100%"  max-height="540"  @selection-change="handleSelectionChange">
          <!--  复选框       -->
          <el-table-column type="selection" width="55" align="center"></el-table-column>
          <el-table-column prop="title" label="图书名称" align="center" min-width="140"></el-table-column>
          <el-table-column prop="book_id" label="图书编号" align="center" width="90"></el-table-column>
          <el-table-column prop="category_code" label="分类编码" align="center" width="90"></el-table-column>
          <el-table-column prop="isbn" label="ISBN" align="center" width="120"></el-table-column>
          <el-table-column prop="author" label="作者" align="center" min-width="100"></el-table-column>
          <el-table-column prop="publisher" label="出版社" align="center" min-width="110"></el-table-column>
          <el-table-column prop="publish_date" label="出版日期" align="center" width="110"></el-table-column>
          <el-table-column prop="intro" label="简介" align="center" min-width="120"></el-table-column>
          <el-table-column prop="status" label="当前状态" align="center" width="80"></el-table-column>
          <el-table-column align="center" label="操作" width="140" fixed="right">
            <template slot-scope="scope">
              <div class="table-operation-btns">
                <el-button type="primary" size="small" @click="update(scope.row.book_id)">编辑</el-button>
                <el-button type="danger" size="small" @click="deleteBook(scope.row.book_id)">下架</el-button>
              </div>
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
  add,
  deleteById,
  page,
  update,
  getById,
  getCategory
} from "@/api/getBook.js";
export default {
  data() {
    return {
      activeIndex: null,
      //日期快捷选择
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now();
        },
        shortcuts: [{
          text: '今天',
          onClick(picker) {
            picker.$emit('pick', new Date());
          }
        }, {
          text: '昨天',
          onClick(picker) {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24);
            picker.$emit('pick', date);
          }
        }, {
          text: '一周前',
          onClick(picker) {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
            picker.$emit('pick', date);
          }
        }]
      },
      //类型选择
      category_codes:[],
      background: true,
      // 每页显示的条数
      pageSize: 5,
      // 总记录数
      totalCount: 0,
      // 当前页码
      currentPage: 1,
      // 添加数据对话框是否展示的标记
      dialogVisible: false,
      //删除原因对话框是否展示的标记
      deleteDialogVisible:false,
      // 搜索图书信息
      searchInfo: "",
      //新增图书信息
      newBook:{},
      //下架图书原因
      operation_reason:"",
      //被选中的下架图书id
      selected_id:"",
      // 被选中的id数组
      selectedIds: [],
      // 复选框选中数据集合
      multipleSelection: [],
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
          this.searchInfo,
          this.currentPage,
          this.pageSize
      ).then((res) => {
        this.totalCount = res.total_items;
        this.tableData = res.books
      }).catch(err=>{
        this.$alert(err.message)
      })
      getCategory().then(res=>{
        this.category_codes=res.categorys
      })
    },
    // 添加数据
    add() {
      const originalDate = new Date(this.newBook.publish_date)
      originalDate.setDate(originalDate.getDate() + 1)
      this.newBook.publish_date = originalDate.toISOString().split("T")[0];
      let operator;
      if (this.newBook.book_id) {
        //修改
        operator = update(this.newBook);
      } else {
        operator = add(this.newBook);
      }
      operator.then((resp) => {
        if (resp.code === 200) {
          // this.dialogVisible = false;
          this.page();
          this.dialogVisible=false
          this.$message.success({
            message: "恭喜你，保存成功",
          });
          this.$confirm("是否继续操作?", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "info",
          }).then(()=>{
            this.dialogVisible=true
          }).catch(()=>{
            this.newBook = {};
            this.dialogVisible=false
          })
        } else {
          this.$message.info(resp.message);
        }
      }).catch(err=>{
        this.$message.error(err);
      });
    },
    update(book_id) {
      //1. 打开窗口
      this.dialogVisible = true;
      console.log(book_id)
      //2. 发送请求,获取原信息
      getById(book_id).then((res) => {
        if (res.code === 200) {
          this.newBook = res.book;
        }
      }).catch((res)=>{
        this.$message.error(res.message);
      })
      this.page();
    },
    deleteBook(book_id){
      this.deleteDialogVisible=true
      this.selected_id=book_id
    },
    //删除信息
    deleteById() {
      this.$confirm("此操作将下架此图书, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
        //2. 发送AJAX请求
        deleteById(this.selected_id,this.operation_reason).then((res) => {
          if (res.code === 200) {
            //删除成功
            this.$message.success("恭喜你，下架成功");
            this.operation_reason=""
            this.deleteDialogVisible=false
            this.page();
          } else {
            this.operation_reason=""
            this.$message.error(res.message);
            this.page();
            this.$confirm("是否重新下架?", "提示", {
              confirmButtonText: "确定",
              cancelButtonText: "取消",
              type: "warning",
            }).then(()=>{
              this.deleteDialogVisible=true
            }).catch(()=>{
              this.deleteDialogVisible=false
            })
          }
        }).catch(err=>{
          this.$message.error(err.message)
        })
      }).catch(() => {
        //用户点击取消按钮
        this.$message.info("已取消删除");
      });
    },


    // 批量下架图书信息
    deleteByIds() {
      // 弹出确认提示框
      this.$confirm("此操作将下架这些书籍, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
        //用户点击确认按钮
        //1. 创建id数组, 从 this.multipleSelection 获取即可
        for (let i = 0; i < this.multipleSelection.length; i++) {
          this.selectedIds[i] = this.multipleSelection[i].book_id;
        }
        //2. 发送AJAX请求
        for(let i = 0; i < this.selectedIds.length; i++){
          deleteById(this.selectedIds[i],"批量下架").then((resp) => {
            if (resp.code === 200) {
              //删除成功
              this.$message.success("恭喜你，下架成功");
              this.page();
            } else {
              this.$message.error(resp.msg);
              this.page();
            }
          }).catch(err=>{
            this.$alert(err.message)
          })
        }
      }).catch(() => {
        //用户点击取消按钮
        this.$message.info("已取消下架");
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
  left: 15%;
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

.el_dialog_publish {
  margin-top: 7vw;
  margin-left: 7vw;
}
</style>
