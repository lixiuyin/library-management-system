<template>
	<div class="header">
		<el-container id="top">
			<h2>图书管理系统</h2>
			<span class="el-menu-item header-welcome" @click="logOut"><i class="el-icon-s-unfold"></i> 退出登录</span>
		</el-container>
	</div>
</template>

<script>
	import {removeToken} from "@/utils/auth.js";
	export default{
		data(){
			return{}
		},
		methods:{
			//退出登录
				logOut(){
					this.$confirm('请问是否退出登录', '提示', {
						confirmButtonText: '确定',
						cancelButtonText: '点错了',
						type: 'warning'
					}).then(() => {
						removeToken();
						//返回登录页面
						this.$router.push({name: "login"});
						//提示
						this.$message.success("退出系统");

					}).catch(() => {

					});
				},


			}

	}
</script>

<style scoped>
	*{
		/* padding:0px; */
		margin: 0px;
	}
	.header{
		width: 100%;
		height:8vh;
		background: #266a7e;
	}
	.el-menu-item.header-welcome:hover{
		background: #bcd7d3;
		color:yellow;
		height: 100%;
	}
	h2{
		line-height: 8vh;
		color:white;
		margin-left: 30px;
	}
	.el-menu-item.header-welcome {
		color: white;
		margin-left: auto;
		line-height: 8vh;
	}
</style>
