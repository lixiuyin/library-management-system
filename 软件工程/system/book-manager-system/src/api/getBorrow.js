import request from '../utils/request.js'
export function page(keyword,page,pageSize) {
    return request({
        url: '/api/borrow/page?keyword='+keyword+'&page='+page+'&pageSize='+pageSize,
        method: 'get',
    })
}
export function borrow(book_id,user_id) {
    const data = {
        book_id: book_id,
        user_id: user_id,
    };
    return request({
        url: '/api/borrow/borrow',
        method: 'post',
        data
    })
}
export function borrow_return(book_id) {
    const data = {
        book_id: book_id,
    };
    return request({
        url: '/api/borrow/return',
        method: 'post',
        data
    })
}
export function borrow_continue(book_id) {
    const data = {
        book_id: book_id,
    };
    return request({
        url: '/api/borrow/renew',
        method: 'post',
        data
    })
}
export function getById(borrow_id) {
    return request({
        url: '/api/borrow/getById?borrow_id='+borrow_id,
        method: 'get',
    })
}

export function getCount(user_id) {
    return request({
        url: '/api/borrow/count?user_id='+user_id,
        method: 'get',
    })
}
