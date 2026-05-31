import request from "@/utils/request";

export function page(admin_id,page,pageSize) {
    return request({
        url: '/api/operation/admin_record?admin_id='+admin_id+'&page='+page+'&pageSize='+pageSize,
        method: 'get',
    })
}
