
import service from "../request.js";
export function LoginInfo(query) {
  return service({
    method: "POST",
    url: "/user/login",
    data: query,
  });
}

// 获取ppt列表
export function attachList(params) {
  return service({
    url: "/attach",
    method: "get",
    params,
  });
}

// 获取parseJson内容
export function getPptParseInfo(params) {
    return service({
      url: "/attach/module",
      method: "get",
      params,
    });
  }

  // 修改parseJson内容
export function editPptParseInfo(params, data) {
    return service({
      url: `/attach/module?id=${params.id}&module_type=${params.module_type}`,
      method: "POST",
      data,
    });
  }
