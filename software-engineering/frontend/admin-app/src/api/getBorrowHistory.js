import request from '../utils/request.js'
export function HistoricalPage(keyword,page,pageSize) {
    return request({
        url: '/api/borrow/HistoricalPage?keyword='+keyword+'&page='+page+'&pageSize='+pageSize,
        method: 'get',
    })
}
