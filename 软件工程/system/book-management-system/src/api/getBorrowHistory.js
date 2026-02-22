import request from '../utils/request.js'
export function HistoricalPage(page,pageSize) {
    return request({
        url: '/api/borrow/HistoricalPage?page='+page+'&pageSize='+pageSize,
        method: 'get',
    })
}
