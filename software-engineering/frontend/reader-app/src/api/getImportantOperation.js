import request from "@/utils/request";

export function page(page,pageSize) {
    return request({
        url: '/api/operation/user_record?page='+page+'&pageSize='+pageSize,
        method: 'get',
    })
}
