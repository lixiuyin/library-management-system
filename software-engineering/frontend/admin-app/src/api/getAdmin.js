import request from "@/utils/request";

export function deleteAdminById(admin_id) {
    const data = {
        admin_id: admin_id,
    };
    return request({
        url: '/api/admin/admin_delete' ,
        method: 'delete',
        data
    })
}
export function add(password) {
    const data = {
        password: password,
    };
    return request({
        url: '/api/admin/admin_add',
        method: 'post',
        data
    })
}

export function update(admin_id,password) {
    const data = {
        admin_id: admin_id,
        password: password,
    };
    return request({
        url: '/api/admin/admin_update',
        method: 'post',
        data
    })
}
export function page(keyword,page,pageSize) {
    return request({
        url: '/api/admin/admin_page?keyword='+keyword+'&page='+page+'&pageSize='+pageSize,
        method: 'get',
    })
}

