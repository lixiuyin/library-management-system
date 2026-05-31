import request from '../utils/request.js'
import {getToken} from "@/utils/auth";
export	function login(data){
	return request({
		url: '/api/user/login',//请求接口
		method: 'post',//请求方式
		data//请求参数
	})
}
export function getInfo() {
	return request({
		url: '/api/user/getInfo',
		method: 'post',
		data: {},
	})
}
export function getById(id) {
	return request({
		url: '/api/user/'+id,//请求接口
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
export	function update_password(old_password,new_password){
	const data = {
		old_password: old_password,
		new_password: new_password,
	};
	return request({
		url: '/api/user/update_password',//请求接口
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

export function getId(user_id) {
	return request({
		url: '/api/user/getId?user_id='+user_id,
		method: 'get',
	})
}
