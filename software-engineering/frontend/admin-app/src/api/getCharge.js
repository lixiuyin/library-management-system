import request from '../utils/request.js'
export function page(user_id,page,pageSize) {
    return request({
        url: '/api/borrow/page?user_id='+user_id+'&page='+page+'&pageSize='+pageSize,
        method: 'get',
    })
}
export function add(user_id,value,reason) {
    const data = {
        user_id: user_id,
        value: value,
        reason:reason,
    };
    return request({
        url: '/api/recharge/add',
        method: 'post',
        data
    })
}
