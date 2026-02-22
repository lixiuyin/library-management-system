<template>
  <div class="signIn">
    <el-carousel  indicator-position="outside" style="height: 100%;width: 100% ;background-size: 100% 100%;" interval="7000" >
      <el-carousel-item v-for="item in imagesBox" :key="item.id" style="height: 100vh;width: 100vw">
        <img :src="item.idView" class="image">
      </el-carousel-item>
    </el-carousel>
    <div class="signIn-mian">
      <div class="signIn-title">欢迎注册</div>
      <div class="signIn-form">
        <el-form :model="signInForm" ref="signInForm" :rules="rules">
          <el-form-item prop="name" label="真实姓名">
            <el-input v-model="signInForm.name" aria-placeholder="请输入真实姓名">
              <i slot="prefix" class="el-input__icon el-icon-user signIn-input-icon"></i></el-input>
          </el-form-item>
          <el-form-item prop="password" label="密码">
            <el-input v-model="signInForm.password" aria-placeholder="请输入密码" show-password>
              <i slot="prefix" class="el-input__icon el-icon-lock signIn-input-icon"></i>
            </el-input>
          </el-form-item>
          <el-form-item prop="checkPassword" label="重复密码">
            <el-input v-model="signInForm.checkPassword" aria-placeholder="请重复输入密码" show-password
            >
              <i slot="prefix" class="el-input__icon el-icon-lock signIn-input-icon"></i>
            </el-input>
          </el-form-item>
          <el-form-item prop="contact" label="手机号码">
            <el-input v-model="signInForm.contact" aria-placeholder="请输入手机号码" show-password>
              <i slot="prefix" class="el-input__icon el-icon-lock signIn-input-icon"></i>
            </el-input>
          </el-form-item>
          <el-form-item prop="gender" label="性别">
            <el-select v-model="signInForm.gender" filterabl placeholder="请选择" style="margin-left: 2%">
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
            <el-select v-model="signInForm.type" aria-placeholder="请选择人员类型" >
              <i slot="prefix" class="el-input__icon el-icon-box signIn-input-icon"></i>
              <el-option
                  v-for="item in types"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item class="signIn-button-item">
            <el-button :loading="isLoading" class="signIn-button" type="primary" @click="register()">注册</el-button>
          </el-form-item>
          <el-form-item class="signIn-button-item">
            <el-button :loading="isLoading" class="signIn-button" type="info" @click="back">取消</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import {register, login, getId} from '@/api/getUser.js';
import {getToken, setToken} from "@/utils/auth.js";
export default {
  data() {
    return {
      //登录数据
      signInForm: {
        name: "",
        password: "",
        checkPassword: "",
        gender:"男",
        type:"本科生",
        contact:""
      },
      loginForm: {
        user_id: "",
        password: "",

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
      //验证规则
      rules: {
        name: [
          {required: true, message: '请输入真实姓名', trigger: 'blur'},
          {
            validator: (rule, value, callback) => {
              if (value.length >10) {
                callback(new Error('姓名必须小于10个字符'));
              } else {
                callback();
              }
            },
            trigger: 'blur'
          }
        ],
        password: [
          {required: true, message: '请输入密码', trigger: 'blur'}
        ],
        checkPassword: [
          {required: true, message: '请重复密码', trigger: 'blur'}
        ],
        gender: [
          {required: true, message: '请选择性别', trigger: 'blur'}
        ],
        type: [
          {required: true, message: '请选择类型', trigger: 'blur'}
        ],
        contact: [
          {required: true, message: '请输入手机号码', trigger: 'blur'},
          {
            validator: (rule, value, callback) => {
              if (value.length !== 11) {
                callback(new Error('电话号码为11位'));
              } else {
                callback();
              }
            },
            trigger: 'blur'
          }
        ],
      },
      //按钮加载中
      isLoading: false,
      //轮播图图片
      imagesBox:[{id:0,idView:require("../../public/images/img.png")}],
      //请求图
      headers: {
        Authorization: `Bearer ${getToken()}`
      }
    }
  },
  methods: {

    back() {
      window.location.replace('/')
    },
    register() {
      let flag = 1;
      // this.checkNull();
      // this.checkFormat();
      // this.checkSame();
      // if (!this.checkNull() && !this.checkFormat() && !this.checkSame())
      //   flag = 0;
      if (flag === 1) {

        register(this.signInForm).then(res => {
          if (res !== -1 && res.code === 200) {
            this.$message.success("注册成功");
            this.loginForm.user_id=res.user_id
            this.loginForm.password=this.signInForm.password
            login(this.loginForm).then(res1 => {
              if (res1.code === 200) {//登录成功
                  setToken(res1.token)
                //保存user信息到localStorage
                    //跳转至主页
                    this.$router.push("/home");
                    //提示
                    this.$message.success("登录成功");

              } else if(res1.code===400){
                this.$message.error(res1.msg);       // 从后端获取的错误信息，提示给用户
              }
            });
          } else {
            this.$message.error(res.msg);
          }
        }).catch(err => {
          this.$message.info(err);
        });
      }

    },
  },
  checkNull() {
    if (this.signInForm.name === '' || this.signInForm.username === '' || this.signInForm.password === '' || this.signInForm.checkPassword === '' || this.signInForm.gender === '') {
      this.$alert('请填入所有信息', '警告', {
        confirmButtonText: '确定',
        callback: action => {
        }
      });
      return false;
    }
    return true;
  },
  checkChinese() {
    const pattern = /[\u4e00-\u9fa5]/; // 使用正则表达式匹配中文字符
    if (pattern.test(this.signInForm.username)) {
      this.$alert('输入内容不能包含中文', '警告', {
        confirmButtonText: '确定',
        callback: action => {
          this.signInForm.username = ''; // 清空输入框的值
        }
      });
    }
  },
  //是否符合格式
  checkFormat() {
    const pattern = /^(?=.*[a-z\d])(?=.*[A-Z\d])(?=.*[a-zA-Z]).+/;
    if (this.signInForm.password.length > 18 || (this.signInForm.password.length < 6 && this.signInForm.password.length > 0)) {
      this.$alert('密码长度范围为6到18', '警告', {
        confirmButtonText: '确定',
        callback: action => {
          this.signInForm.password = ''; // 清空输入框的值
          this.signInForm.checkPassword = '';
        }
      });
      return false;
    }
    if (!pattern.test(this.signInForm.password) && !(this.signInForm.password === '')) {
      this.$alert('大写小写字母、数字中至少包含两种', '警告', {
        confirmButtonText: '确定',
        callback: action => {
          this.signInForm.password = ''; // 清空输入框的值
          this.signInForm.checkPassword = '';
        }
      });
      return false;
    }
    return true;
  },
  //是否与新密码相等
  checkSame() {
    if (!(this.signInForm.checkPassword === this.signInForm.password)) {
      this.$alert('两次输入新密码不相同', '警告', {
        confirmButtonText: '确定',
        callback: action => {
          this.signInForm.checkPassword = ''; // 清空输入框的值
        }
      });
      return false;
    }
    return true;
  },
  mounted() {

  }
}
</script>

<style scoped>
body {
  margin: 0px;
}

.signIn {
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
.signIn-mian {
  background-color: #fff;
  width: 358px;
  height: 790px;
  border-radius: 15px;
  padding: 0 50px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  opacity:1;
  z-index: 2;

}

.signIn-title {
  font-size: 38px;
  font-weight: bold;
  text-align: center;
  line-height: 100px;
}

.signIn-form {
  margin-top: 2px;
}

.signIn-button-item {
  margin-top: 30px;
}

.signIn-button {
  width: 358px;
}

.signIn-input-icon {
  font-size: 20px;
}
.el-option /deep/{
  background-color: blue !important; /* 修改背景颜色为蓝色 */
  color: white !important; /* 修改文字颜色为白色 */
}

</style>
