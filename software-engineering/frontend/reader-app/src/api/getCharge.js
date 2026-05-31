import request from '../utils/request.js'
export function page(page,pageSize) {
    return request({
        url: '/api/recharge/page?page='+page+'&pageSize='+pageSize,
        method: 'get',
    })
}
