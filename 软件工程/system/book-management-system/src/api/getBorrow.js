import request from '../utils/request.js'
export function page(page,pageSize) {
    return request({
        url: '/api/borrow/page?page='+page+'&pageSize='+pageSize,
        method: 'get',
    })
}
export function getExpire() {
    return request({
        url: '/api/borrow/expire',
        method: 'get',
    })
}
