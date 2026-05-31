import request from '../utils/request.js'
//分页查询 模糊查询
export function page(keyword,page,pageSize) {
    return request({
        url: '/api/book/page?keyword='+keyword+'&page='+page+'&pageSize='+pageSize,
        method: 'get',
    })
}
