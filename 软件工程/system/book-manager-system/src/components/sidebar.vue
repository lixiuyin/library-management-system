<template>
      <el-row class="tac">
				<el-col :span="24" class="tac1">
          <el-menu :default-active="activeIndex || '1'" class="el-menu-vertical-demo" background-color="#307a93"
                   text-color="#fff" active-text-color="#ffd04b">
						<router-link to="/bookManage">
							<el-menu-item index="1">
								<i class="el-icon-s-home"></i>
								<span slot="title">图书管理</span>
							</el-menu-item>
						</router-link>
						<router-link to="/userManage">
							<el-menu-item index="2">
								<i class="el-icon-reading"></i>
								<span slot="title">读者管理</span>
							</el-menu-item>
						</router-link>


            <el-submenu index="3">
              <template slot="title">
                <i class="el-icon-box"></i>
                <span>借阅</span>
              </template>
              <el-menu-item-group>

                <router-link to="/borrowManage">
                  <el-menu-item index="3-1">
                    <i class="el-icon-reading"></i>
                    <span slot="title">借阅管理</span>
                  </el-menu-item>
                </router-link>

                <router-link to="/borrowNow">
                  <el-menu-item index="3-2">
                    <template slot="title">
                      <i class="el-icon-notebook-1"></i>
                      <span>当前借阅</span>
                    </template>
                  </el-menu-item>
                </router-link>

                <router-link to="/borrowHistory">
                  <el-menu-item index="3-3">
                    <template slot="title">
                      <i class="el-icon-notebook-2"></i>
                      <span>历史借阅</span>
                    </template>
                  </el-menu-item>
                </router-link>

                <router-link to="/borrowRank">
                  <el-menu-item index="3-4">
                    <template slot="title">
                      <i class="el-icon-notebook-2"></i>
                      <span>借阅排行</span>
                    </template>
                  </el-menu-item>
                </router-link>
              </el-menu-item-group>
            </el-submenu>

            <router-link to="/importantRecordManage">
              <el-menu-item index="4">
                <i class="el-icon-money"></i>
                <span slot="title">重要操作记录</span>
              </el-menu-item>
            </router-link>

            <router-link to="/systemManage">
              <el-menu-item index="5">
                <i class="el-icon-warning-outline"></i>
                <span slot="title">系统管理</span>
              </el-menu-item>
            </router-link>

					</el-menu>
				</el-col>
			</el-row>
</template>
<script>
	export default {
    // data(){
    //   return{
    //     activeIndex: null,
    //   }
    // },
    // methods:{
    //   handleMenuClick(index) {
    //     this.activeIndex = index;
    //     // Save the selected index to local storage
    //     localStorage.setItem('activeIndex', index);
    //   }
    // },
    // mounted() {
    //   this.handleMenuClick(this.activeIndex)
    // },
    // updated() {
    //   this.activeIndex = localStorage.getItem('activeIndex');
    //
    // }
  };
</script>
<style scoped>
	a {
		text-decoration: none;
	}

	* {
		padding: 0px;
		margin: 0px;
	}
  span:hover{
    color: yellow;
  }
	.tac1 {
		text-align: left;
    height: 100%;
        width: 100%;
		background: #307a93;

	}
  span{
    font-size:large;
  }

	.tac {
		width: 100%;
	}
    .el-menu-item{
        min-width: 12%!important;
        font-size: 1%;
    }
</style>
