import request from '../utils/request.js'
export	function login(data){
	return request({
		url: '/api/user/login',//请求接口
		method: 'post',//请求方式
		data//请求参数
	})
}
export function getInfo(user_id) {
	const data = {
		user_id: user_id,
	};
	return request({
		url: '/api/user/getInfo?user_id='+user_id,//请求接口
		method: 'post',//请求方式
		data
	})
}
export function getById(user_id) {
	return request({
		url: '/api/user/getById?user_id='+user_id,//请求接口
		method: 'get',//请求方式
	})
}
export	function register(data){
	return request({
		url: '/api/user/register',//请求接口
		method: 'post',//请求方式
		data//请求参数
	})
}
export function password_update(user_id,new_password){
	const data = {
		user_id: user_id,
		new_password:new_password,
	};
	return request({
		url: '/api/admin/password_update' ,//请求接口
		method: 'post',//请求方式
		data,
	})
}


export function update(user) {
	return request({
		url: '/api/user/update',
		method: 'post',
		data: user
	})
}

export function deleteById(user_id,operation_reason) {
	const data = {
		user_id: user_id,
		operation_reason: operation_reason,
	};
	return request({
		url: '/api/admin/user_delete' ,
		method: 'delete',
		data
	})
}

export function user_page(keyword,page,pageSize) {
	return request({
		url: '/api/admin/user_page?keyword='+keyword+'&page='+page+'&pageSize='+pageSize,
		method: 'get',
	})
}
