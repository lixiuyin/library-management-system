<template>
	<div>
		<div class="box">
			<topbar class="top"></topbar>
			<sidebar class="side"></sidebar>
			<router-view class="main"/>
		</div>
	</div>
</template>
<script>
	import sidebar from '../components/sidebar.vue'
	import topbar from '../components/topbar.vue'
  import bookManage from "@/views/manager/book/bookManage.vue";
	export default {
		components: {
			sidebar,
			topbar,
      bookManage,
		}
	};
</script>
<style scoped>
	*{
		padding:0px;
		margin: 0px;
	}
	a {
		text-decoration: none;
	}
	.top{
		position: absolute;
		left: 0px;
		top:0px;
	}
	.side{
		position: absolute;
		left: 0px;
		top:8vh;
		width: 12%;
		height:92vh;
		overflow-y: auto;
	}
	.main{
		position: absolute;
		top:8vh;
		left:12%;
		width: 88%;
		height:90vh;
		overflow-y: auto;
	}
	.box {
		position: relative;
		display: flex;
	}
</style>
