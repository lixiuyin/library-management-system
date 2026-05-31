<template>
  <div class="login">
    <el-carousel  indicator-position="outside" style="height: 100%;width: 100%" interval="7000" >
      <el-carousel-item v-for="item in imagesBox" :key="item.id" style="height: 100vh;width: 100vw">
        <img :src="item.idView" class="image">
      </el-carousel-item>
    </el-carousel>
    <div class="login-mian">
      <div class="login-title">欢迎登录</div>
      <div class="login-form">
        <el-form :model="loginForm" :rules="rules" ref="loginForm">
          <el-form-item prop="user_id">
            <el-input v-model="loginForm.user_id" aria-placeholder="请输入账号"><i slot="prefix"
                                                                                    class="el-input__icon el-icon-user-solid login-input-icon"></i>
            </el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input v-model="loginForm.password" aria-placeholder="请输入密码" show-password><i slot="prefix"
                                                                                                  class="el-input__icon el-icon-lock login-input-icon"></i>
            </el-input>
          </el-form-item>
          <el-form-item class="login-button-item">
            <el-button :loading="isLoading" class="login-button" type="primary" @click="loginUser('loginForm')">登录
            </el-button>
          </el-form-item>
          <el-form-item class="login-button-item">
            <el-button :loading="onLoading" class="login-button" type="success" @click="signIn()">注册
            </el-button>
          </el-form-item>
          <el-form-item class="login-button-item">
            <el-button :loading="onLoading" class="login-button" type="warning" @click="visit">游客访问
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import {login} from '@/api/getUser.js';
import {getExpire} from '@/api/getBorrow.js'
import {getToken, setToken} from "@/utils/auth.js";
export default {
  data() {
    return {
      //登录数据
      loginForm: {
        user_id: "B000000001",
        password: "password05"
      },
      //验证规则
      rules: {
        user_id: [
          {required: true, message: '请输入用户名', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '请输入密码', trigger: 'blur'}
        ]
      },
      //按钮加载中
      isLoading: false,
      onLoading: false,

      //轮播图图片
      imagesBox:[{id:0,idView:require("../../public/images/img.png")}],

      // fiveNews: []
    }
  },
  methods: {
    signIn(){
      this.onLoading = true;
      let context = this;
      window.location.replace('/signIn').then(() => {
        context.onLoading = false;
      })
    },
    //登录
    loginUser(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          //改变按钮的加载状态
          this.isLoading = true;
          //验证通过,发起请求进行登录
          login(this.loginForm).then(res => {
            if (res !== -1 && res.code === 200) {//登录成功
              this.isLoading = false;
              setToken(res.token);
              //跳转至主页
              this.$router.push("/home");
              //提示
              this.$message.success("登录成功");
              this.checkBorrow()

            } else {
              this.isLoading = false;
              this.$message.error(res.message);       // 从后端获取的错误信息，提示给用户
            }
            //2秒关闭按钮的加载状态
            setTimeout(() => {
              this.isLoading = false;
            }, 2000)
          }).catch(err=>{
            this.$alert(err.message)
          })
        } else {
          this.$message.error("请输入账号或密码")
          return false;
        }
      });
    },
    visit(){
      this.$router.push('/visitor');
    },
    //检查是否有图书5天之内将逾期
    checkBorrow(){
      getExpire().then(res=>{
        if(res.code===200){
          if(res.total_items>0){
            this.$confirm(`您有${res.total_items}本图书借阅即将到期`, {
              confirmButtonText: "确定",
              type: "warning",
            }).then(()=>{
              this.$message.success("已确认")
            })
          }
          else {
            this.$confirm(`您没有图书借阅即将到期`, {
              confirmButtonText: "确定",
              type: "success",
            }).then(()=>{
              this.$message.success("已确认")
            }).catch(()=>{
              this.$message.success("已确认")
            })
          }
        }
        else{
          this.$message.warning(res.message)
        }
      }).catch(err=>{
        this.$alert(err.message)
      })
    }
  },

  mounted() {
    //removeStorage("user");
    let Authorization = getToken();
    console.log(Authorization)
    if (Authorization) {
      //跳转至主页
      this.$router.push({name: "home"});
    }
  }
}
</script>

<style>
body {
  margin: 0px;
}

.login {
  background-image: linear-gradient(to right, #fbc2eb, #a6c1ee);
  height: 98vh;
  display: flex;
  position: relative;
  justify-content: center;
}
img{
  width: 100%;
  height: 100%;
}

.login-mian {
  background-color: #fff;
  width: 358px;
  height: 560px;
  border-radius: 15px;
  padding: 0 50px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  opacity:0.9;
  z-index: 9999;
}

.login-title {
  font-size: 38px;
  font-weight: bold;
  text-align: center;
  line-height: 200px;
}

.login-form {
  margin-top: 50px;
}

.login-button-item {
  margin-top: 13px;
}

.login-button {
  width: 358px;
}

.login-input-icon {
  font-size: 20px;
}
</style>
