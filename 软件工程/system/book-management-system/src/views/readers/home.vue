<template>
  <div class="app-container-home">
    <!--个人信息表单-->
    <div class="title" style="margin-top: 1%;margin-bottom: -2%">
      <h1 >个人信息</h1>
      <br>
    </div>
    <el-form ref="User" :model="User" label-width="80px" size="small" class="form-container" :rules="rules">
      <el-form-item label="真实姓名" prop="name">
        <el-input v-model="User.name" aria-placeholder="请输入新的姓名" :readonly="!isEditing">{{User.name}}</el-input>
      </el-form-item>
      <el-form-item label="电话号码" prop="contact">
        <el-input v-model="User.contact" aria-placeholder="请输入您的电话号码" :readonly="!isEditing">{{User.contact}}</el-input>
      </el-form-item>
      <el-form-item label="性别" prop="gender">
        <el-select v-model="User.gender" aria-placeholder="请选择" :readonly="!isEditing" style="margin-left: -50%">
          <el-option
              v-for="item in genders"
              :key="item.value"
              :label="item.label"
              :value="item.value"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="类型" prop="type">
        <el-select v-model="User.type" aria-placeholder="请选择" :readonly="!isEditing" style="margin-left: -50%">
          <el-option
              v-for="item in types"
              :key="item.value"
              :label="item.label"
              :value="item.value"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="isEditing=true" style="background: #ffffff;color: black;margin-left: -30%">编辑信息</el-button>
        <el-button type="primary" @click="save" v-if="isEditing" style="background: #ffffff;color: black">保存修改</el-button>
        <el-button @click="dialogVisible = true">修改密码</el-button>
      </el-form-item>
    </el-form>
    <br>
    <!--修改密码对话框表单-->
    <el-dialog class="el_dialog" ref="form" title="修改密码" :visible.sync="dialogVisible" width="30%">
      <el-form ref="User" :model="Pass" label-width="80px" size="mini" :rules="rules">
        <el-form-item label="旧密码" prop="password">
          <el-input v-model="Pass.password" aria-placeholder="输入旧密码" ></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="Pass.newPassword" aria-placeholder="输入新密码" ></el-input>
        </el-form-item>
        <el-form-item label="再输一次" prop="againPassword">
          <el-input v-model="Pass.againPassword" aria-placeholder="再次输入新密码" ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button  @click="changePassword" >确认修改</el-button>
          <el-button @click="dialogVisible = false">取消修改</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
    <hr>
    <div style="margin-top: 2%">
      <h1 class="title" style="margin-top: 0%">快捷入口</h1>
      <el-row>
        <el-button @click="goToPage1" style="margin-top: 5%;margin-left: 12%;margin-right: 10%" icon="el-icon-reading">浏览图书</el-button>
        <el-button @click="goToPage2" style="margin-left: 10%;margin-right: 10%" icon="el-icon-notebook-1">当前借阅</el-button>
        <el-button @click="goToPage3" style="margin-left: 10%;margin-right: 10%" icon="el-icon-notebook-2">历史借阅</el-button>
      </el-row>
      <el-row>
        <el-button @click="goToPage4" style="margin-top: 5%;margin-left: 12%;margin-right: 10%" icon="el-icon-money">充值记录</el-button>
        <el-button @click="goToPage5" style="margin-left: 10%;margin-right: 10%" icon="el-icon-warning-outline">重要操作</el-button>
      </el-row>
    </div>

  </div>
</template>

<script>
import {
  getToken
} from '@/utils/auth';
import {
  update,
  update_password,
  getInfo,
} from "@/api/getUser.js";
import axios from "axios";

export default {
  data() {
    return {
      // 添加数据对话框是否展示的标记
      id:'',
      dialogVisible: false,
      isEditing:false,
      User: {
        name: "",
        gender: "",
        type:"",
        contact:""
      },
      Pass:{
        password: "",
        newPassword:"",
        againPassword:"",
      },
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

      rules: {
        name: [
          {required: true, message: '请输入真实姓名', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '输入旧密码', trigger: 'blur'}
        ],
        newPassword: [
          {required: true, message: '输入新密码', trigger: 'blur'}
        ],
        againPassword: [
          {required: true, message: '再次输入新密码', trigger: 'blur'}
        ],
        gender:[
          {required: true, message: '请选择性别', trigger: 'blur'}
        ]
      },
    };
  },

  mounted() {

    getInfo().then(res=>{
      this.User.name=res.data.name
      this.User.type=res.data.type
      this.User.gender=res.data.gender
      this.User.contact=res.data.contact
    }).catch(err=>{
      this.$alert(err.message)
    })
  },

  methods: {

    //是否为旧密码
    checkRight() {
      update_password(this.Pass.password,this.Pass.newPassword).then((res)=>{
        if(res.code!==200){
          this.$alert(res.message, '警告', {
            confirmButtonText: '确定',
            callback: action => {
              this.Pass.password = ''; // 清空输入框的值
            }
          })
        }
        else{
          this.$message(res.message)
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
    goToPage1(){
      this.$router.push('/browBooks');
    },
    goToPage2(){
      this.$router.push('/borrowNow');
    },
    goToPage3(){
      this.$router.push('/borrowHistory');

    },
    goToPage4(){
      this.$router.push('/rechargeRecord');

    },
    goToPage5(){
      this.$router.push('/importantRecord');

    },


    save(){
		  let user = {...this.User};
      update(user).then(res => {
        if (res.code === 200) {
          this.isEditing=false;
          this.dialogVisible = false;
          this.$message.success("修改成功");
        }
        else {
          this.$message.error("修改失败");
        }
      }).catch(err => {
        this.$message.error(err.message);
      })
    },
    changePassword() {
      this.checkPassword()
          .then(() => {
            this.User.password = this.Pass.newPassword;

          })
          .catch(error => {
            this.$message.info(error.message);
            console.error(error.message);
          });
    },

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
    }
  },
};
</script>
<style scoped>
.title{
  margin-left: 50px;
  margin-top: 50px;
}
.form-container{
  margin-top: 30px;
  font-size: 20px;
  text-align: center;
  width: 500px;
  margin-left: 50px;
}
.app-container-home {
  width: 100%;
  display: flex;
  flex-direction: column;

.el-button {
  background: #ffffff ;
  border: 2px solid #2487b0 !important;
}
/* 悬停样式 */
.el-button:hover {
  background: #2487b0 !important;
  text-decoration: none;
  color: #ffffff !important;
}

}




</style>
