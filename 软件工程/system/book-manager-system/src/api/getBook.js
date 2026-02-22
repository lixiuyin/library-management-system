import request from '../utils/request.js'
//分页查询 模糊查询
export function page(keyword,page,pageSize) {
    return request({
        url: '/api/book/page?keyword='+keyword+'&page='+page+'&pageSize='+pageSize,
        method: 'get',
    })
}
export function add(newBook) {
    return request({
        url: '/api/book/add',
        method: 'post',
        data: newBook
    })
}

export function update(book) {
    return request({
        url: '/api/book/update',
        method: 'put',
        data: book
    })
}


export function deleteById(book_id,operation_reason) {
    const data = {
        book_id: book_id,
        operation_reason: operation_reason,
    };
    return request({
        url: '/api/book/delete' ,
        method: 'delete',
        data
    })
}


export function getById(book_id) {
    return request({
        url: '/api/book/getById?book_id='+book_id,
        method: 'get',
    })
}

export function getCategory() {
    return request({
        url: '/api/book/category',
        method: 'get',
    })
}
export function getTop() {
    return request({
        url: '/api/book/top',
        method: 'get',
    })
}
