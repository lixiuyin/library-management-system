<template>
  <div class="app-container-publish" >

    <el-breadcrumb separator="/" style="font-size: 90%;margin-left: 1%">
      <el-breadcrumb-item :to="{path:'../bookManage'}">图书首页</el-breadcrumb-item>
      <el-breadcrumb-item>读者管理</el-breadcrumb-item>
    </el-breadcrumb>
    <!--搜索表单-->
    <div style="transform: scale(1.3);width: 60%;margin-left: 12%;margin-top: 4%">
      <el-form :inline="true" :model="searchInfo" class="demo-form-inline">
        <el-form-item label="读者">
          <el-input v-model="searchInfo" placeholder="请输入读者信息以查找" ></el-input>
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
        <el-button type="danger" size="medium" @click="deleteByIds()">批量删除</el-button>
        <el-button type="primary" size="medium" @click="dialogVisible = true; newUser = { };">添加读者</el-button>
      </div>

      <!--添加数据对话框表单-->
      <el-dialog class="el_dialog_publish" ref="form" title="读者信息" :visible.sync="dialogVisible" width="30%">
        <el-form ref="form" :model="newUser" label-width="80px" size="mini">
          <el-form-item label="读者姓名">
            <el-input v-model="newUser.name" placeholder="请输入读者姓名"></el-input>
          </el-form-item>
          <el-form-item prop="gender" label="性别">
            <el-select v-model="newUser.gender" filterabl placeholder="请选择" style="margin-left: 0">
              <i slot="prefix" class="el-input__icon el-icon-male signIn-input-icon"></i>
              <el-option
                  v-for="item in genders"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="类型" prop="type">
            <el-select v-model="newUser.type" aria-placeholder="请选择人员类型" >
              <i slot="prefix" class="el-input__icon el-icon-box signIn-input-icon"></i>
              <el-option
                  v-for="item in types"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="联系方式">
            <el-input v-model="newUser.contact" placeholder="请输入联系方式"></el-input>
          </el-form-item>
          <el-form-item label="余额">
            <el-input v-model="newUser.balance" placeholder="请输入余额"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="add" style="margin-left: 0vw">提交</el-button>
            <el-button @click="dialogVisible = false">取消</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>

      <!--删除读者原因的表单-->
      <el-dialog class="el_dialog_publish" ref="form" title="删除原因" :visible.sync="deleteDialogVisible" width="30%">
        <el-form ref="form" :model="operation_reason" label-width="80px" size="mini">
          <el-form-item label="图书名称">
            <el-input v-model="operation_reason" placeholder="请输入删除读者原因" ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="deleteById()" style="margin-left: 0vw">提交</el-button>
            <el-button @click="deleteDialogVisible = false">取消</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>

      <!--充值金额的表单-->
      <el-dialog class="el_dialog_publish" ref="form" title="充值扣款" :visible.sync="rechargeDialogVisible" width="30%">
        <el-form ref="form" :model="charge" label-width="80px" size="mini">
          <el-form-item label="变动金额">
            <el-input v-model="charge" placeholder="请输入变动金额" ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="rechargecById()" style="margin-left: 0vw">提交</el-button>
            <el-button @click="rechargeDialogVisible = false">取消</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>

      <!--修改密码对话框表单-->
      <el-dialog class="el_dialog_publish" ref="form" title="修改密码" :visible.sync="passwordDialogVisible" width="30%">
        <el-form ref="User" :model="Pass" label-width="80px" size="mini" :rules="rules">
          <el-form-item label="新密码" prop="newPassword">
            <el-input v-model="Pass.newPassword" aria-placeholder="输入新密码" ></el-input>
          </el-form-item>
          <el-form-item label="再输一次" prop="againPassword">
            <el-input v-model="Pass.againPassword" aria-placeholder="再次输入新密码" ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button  @click="changePassword" >确认修改</el-button>
            <el-button @click="passwordDialogVisible = false">取消修改</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
      <br>
      <!--表格-->
      <template>
        <el-table :data="tableData" style="width: 100%"  max-height="540.6px" max-width @selection-change="handleSelectionChange">
          <!--  复选框       -->
          <el-table-column type="selection" width="55" align="center"></el-table-column>
          <el-table-column prop="user_id" label="读者编号" align="center" width="110"></el-table-column>
          <el-table-column prop="name" label="姓名" align="center" min-width="80"></el-table-column>
          <el-table-column prop="gender" label="性别" align="center" width="70"></el-table-column>
          <el-table-column prop="type" label="类型" align="center" width="80"></el-table-column>
          <el-table-column prop="contact" label="联系方式" align="center" width="120"></el-table-column>
          <el-table-column prop="balance" label="余额" align="center" width="90"></el-table-column>
          <el-table-column prop="count" label="未归还本数" align="center" width="95"></el-table-column>
          <el-table-column align="center" label="操作" min-width="240" fixed="right">
            <template slot-scope="scope">
              <div class="table-operation-btns">
                <el-button type="primary" size="small" @click="update(scope.row.user_id)">编辑</el-button>
                <el-button type="warning" size="small" @click="recharge(scope.row.user_id)">充值</el-button>
                <el-button type="info" size="small" @click="password(scope.row.user_id)">改密</el-button>
                <el-button type="danger" size="small" @click="deleteOne(scope.row.user_id)">删除</el-button>
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
  register as add,
  deleteById,
  update,
  password_update, user_page, getInfo
} from "@/api/getUser.js";
import {add as recharge} from "@/api/getCharge.js"
import {getCount} from "@/api/getBorrow";
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
      genders: [ // 下拉框选项数据
        { label: '男', value: '男' },
        { label: '女', value: '女' },
      ],
      types: [ // 下拉框选项数据
        { label: '教师', value: '教师' },
        { label: '研究生', value: '研究生' },
        { label: '本科生', value: '本科生' },
        { label: '其他', value: '其他' },
      ],
      //修改密码话框是否展示的标记
      passwordDialogVisible:false,
      //密码相关信息
      Pass:{
        password: "",
        newPassword:"",
        againPassword:"",
      },
      //充值对话框是否展示的标记
      rechargeDialogVisible:false,
      //充值金额
      charge:"",
      // 添加数据对话框是否展示的标记
      dialogVisible: false,
      //删除原因对话框是否展示的标记
      deleteDialogVisible:false,
      //是否批量删除
      isMany:"",
      //选中的id
      selected_id:"",
      // 搜索读者信息
      searchInfo: "",
      //新增读者信息
      newUser:{},
      //删除读者的原因
      operation_reason:"",
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
      user_page(
          this.searchInfo,
          this.currentPage,
          this.pageSize
      ).then((res) => {
        this.totalCount = res.total_items
        this.tableData = res.users
      }).catch(err=>{
        this.$alert(err.message)
      })
    },
    // 添加数据
    add() {
      let operator;
      if (this.newUser.user_id) {
        //修改
        operator = update(this.newUser);
      } else {
        operator = add(this.newUser);
      }
      operator.then((resp) => {
        if (resp.code === 200) {
          // this.dialogVisible = false;
          this.page();
          this.dialogVisible=false
          this.$message({
            message: "恭喜你，保存成功",
            type: "success"
          });
          this.$confirm("是否继续添加读者?", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "info",
          }).then(()=>{
            this.newUser = {};
            this.dialogVisible=true
          }).catch(()=>{
            this.newUser = {};
            this.dialogVisible=false
          })
        } else {
          this.$message.error(resp.message);
        }
      }).catch(err=>{
        this.$message.error(err);
      });
    },
    //修改
    update(user_id) {
      //1. 打开窗口
      this.dialogVisible = true;
      console.log(user_id)
      //2. 发送请求,获取原信息
      getInfo(user_id).then((res) => {
        if (res.code === 200) {
          this.newUser = res.data;
        }
      }).catch((res)=>{
        this.$message.error(res.message);
      })
      this.page();
    },
    //充值
    recharge(user_id){
      this.selected_id=user_id
      this.rechargeDialogVisible=true
    },
    rechargecById(){
      this.$confirm("您确定进行充值吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(()=>{
        recharge(this.selected_id,this.charge,"充值").then((res) => {
        if (res.code === 200) {
          this.$message.success("充值成功")
          this.page()
          this.rechargeDialogVisible=false
        }
        else{
          this.$message.info(res.message)
        }
      }).catch((res)=>{
        this.$message.error(res.message);
      })
      this.page();
      }).catch(()=>{
        this.$message.info("已取消充值")
      })
    },
    //修改密码
    password(user_id){
      this.selected_id=user_id
      this.passwordDialogVisible=true
    },
    //打开借阅对话框
    deleteOne(user_id) {
      this.isMany=false
      this.deleteDialogVisible=true
      this.selected_id=user_id
    },
    //批量借阅时打开对话框进行填写
    deleteByIds(){
      // 弹出确认提示框
      this.isMany=true
      this.deleteDialogVisible=true
      //获取多选的全部书的id
      for (let i = 0; i < this.multipleSelection.length; i++) {
        this.selectedIds[i] = this.multipleSelection[i].user_id;
      }
    },
    //进行删除请求
    deleteById(){
      if(this.isMany===false){
        this.$confirm("您确定删除这位读者吗?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }).then(() => {
          //2. 发送AJAX请求
          deleteById(this.selected_id,this.operation_reason).then((res) => {
            if (res.code === 200) {
              //删除成功
              this.$message.success("删除成功");
              this.page();
              this.operation_reason=""
              this.deleteDialogVisible=false
            } else {
              this.operation_reason=""
              this.deleteDialogVisible=false
              this.$message.error(res.message);
            }
          }).catch(err=>{
            this.$alert(err.message)
            this.$confirm("是否重新删除", "提示", {
              confirmButtonText: "确定",
              cancelButtonText: "取消",
              type: "warning",
            }).then(()=>{
              this.operation_reason=""
              this.deleteDialogVisible=true
            }).catch(()=>{
              this.operation_reason=""
              this.deleteDialogVisible=false
            })
          })
        }).catch(() => {
          //用户点击取消按钮
          this.operation_reason=""
          this.$message.info("已取消删除");
        });
      }
      else{
        this.$confirm("此操作将批量删除这些读者, 是否继续?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }).then(() => {
          //发送请求
          for(let i = 0; i < this.selectedIds.length; i++){
            deleteById(this.selectedIds[i],this.operation_reason).then((res) => {
              if (res.code === 200) {
                //删除成功
                this.$message.success("删除成功");
                this.page();
                this.operation_reason=""
                this.deleteDialogVisible=false
              } else {
                this.operation_reason=""
                this.deleteDialogVisible=false
                this.$message.info(res.message);
              }
            }).catch(err=>{
              this.$alert(err.message)
              this.$confirm("是否重新删除", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
              }).then(()=>{
                this.operation_reason=""
              }).catch(()=>{
                this.operation_reason=""
                this.deleteDialogVisible=false
              })
            })
          }
        }).catch(() => {
          //用户点击取消按钮
          this.$message.info("已取消删除");
        });
      }
    },


    //修改操作
    checkRight() {
      password_update(this.selected_id,this.Pass.newPassword).then((res)=>{
        if(res.code!==200){
          this.$alert(res.message, '警告', {
            confirmButtonText: '确定',
            callback: action => {
              this.Pass.newPassword = ''; // 清空输入框的值
              this.Pass.againPassword = ''; // 清空输入框的值
            }
          })
        }
        else{
          this.$message.success(res.message)
        }
      }).catch(err=>{
        this.$alert(err.message)
      })
    },
    //是否符合格式
    checkFormat() {
      return new Promise((resolve, reject) => {
        const pattern = /^(?=.*[a-z\d])(?=.*[A-Z\d])(?=.*[a-zA-Z]).+/;
        if (this.Pass.newPassword.length > 20 || this.Pass.newPassword.length < 8) {
          this.$alert('密码长度范围为8到20', '警告', {
            confirmButtonText: '确定',
            callback: action => {
              this.Pass.newPassword = ''; // 清空输入框的值
              this.Pass.againPassword = '';
            }
          });
          reject('密码长度不符合要求');
        }
        if (!pattern.test(this.Pass.newPassword)) {
          this.$alert('大写小写字母、数字中至少包含两种', '警告', {
            confirmButtonText: '确定',
            callback: action => {
              this.Pass.newPassword = ''; // 清空输入框的值
              this.Pass.againPassword = '';
            }
          });
          reject('密码格式不符合要求');
        }
        resolve();
      });
    },
    //是否与新密码相等
    checkSame() {
      return new Promise((resolve, reject) => {
        if (!(this.Pass.againPassword === this.Pass.newPassword)) {
          this.$alert('两次输入新密码不相同', '警告', {
            confirmButtonText: '确定',
            callback: action => {
              this.Pass.newPassword = ''; // 清空输入框的值
              this.Pass.againPassword = '';
            }
          });
          reject('两次输入密码不相同');
        }
        resolve();
      });
    },
    //更改密码，执行系列检测
    changePassword() {
      this.checkPassword()
          .then(() => {

          })
          .catch(error => {
            this.$message.info(error.message);
            console.error(error.message);
          });
    },
    //检查密码正确性
    checkPassword() {
      return new Promise((resolve, reject) => {
        this.checkSame();
        this.checkFormat()
            .then(() => this.checkRight())
            .then(() => {
              resolve();
            })
            .catch(error => {
              reject(error);
            });
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
  //left: 15%;

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
