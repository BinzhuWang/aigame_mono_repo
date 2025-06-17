//src/api/user/index.js

import service from "../request.js";
// New functions: attach, attachList, gameQuery, screenshot, gameModule, getPlaData

export function LoginInfo(query) {
  return service({
    method: "POST",
    url: "/user/login",
    data: query,
  });
}

// 上传ppt
export function attach(data) {
  return service({
    url: "/attach?file_type=ppt",
    method: "post",
    data,
  });
}
// 上传ppt
export function attachMedia(data, fileType, id) {
  return service({
    url: `/attach?file_type=${fileType}&attach_id=${id}`,
    method: "post",
    data,
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
// 删除ppt
export function deleteAttach(params) {
  return service({
    url: "/attach",
    method: "delete",
    params,
  });
}

// 更新ppt状态
export function updateAttachStatus(data) {
  return service({
    url: `/attach/update_status`,
    method: "post",
    data,
  });
}
// 重新解析ppt
export function reParseAttach(params) {
  return service({
    url: `/attach/process`,
    method: "get",
    params,
  });
}

// 重新生成
export function regenModule(params) {
  return service({
    url: `/game/regen/${params.id}/${params.module_type}`,
    method: "get",
  });
}

// 文本转语音
export function textToSound(data) {
  return service({
    url: `/proxy/tts`,
    method: "post",
    data
  });
}
// 生成图片
export function textToImage(data) {
  return service({
    url: `/proxy/image/gen`,
    method: "post",
    data
  });
}
// 生成视频
export function runwayVideo(data) {
  return service({
    url: `/proxy/video/runway`,
    method: "post",
    data
  });
}

// 游戏查询
export function gameQuery(params) {
  return service({
    url: "/game/query",
    method: "get",
    params,
  });
}

// ppt截图查询
export function screenshot(params) {
  return service({
    url: "/attach/screenshot",
    method: "get",
    params,
  });
}

// 游戏模块查询
export function gameModule(params) {
  return service({
    url: "/game/module",
    method: "get",
    params,
  });
}

// 游戏模块修改
export function gameModuleEdit(params, data) {
  return service({
    url: `/game/module?id=${params.id}&module_type=${params.module_type}`,
    method: "post",
    data,
  });
}

// 点击生成goal
export function goalGerate(params) {
  return service({
    url: `/attach/process`,
    method: "get",
    params,
  });
}

// 点击生成游戏
export function gameGerate(data) {
  return service({
    url: `/game/generate`,
    method: "post",
    data,
  });
}

// 聊天生成游戏
export function gameGerateByChat(data) {
  return service({
    url: `/chat/code`,
    method: "post",
    data,
  });
}

// 获取平台数据
export function getPlaData(params) {
  return service({
    url: "/data",
    method: "get",
    params,
  });
}

// 结束

export function getMenuList(query) {
  return service({
    method: "get",
    url: "/permission/getMenuList",
    data: query,
  });
}
export function login(data) {
  return service({
    url: "/user/login",
    method: "post",
    data,
  });
}
export function getUserList(query) {
  return service({
    method: "get",
    url: "/permission/UserList",
    data: query,
  });
}
export function addUserList(query) {
  return service({
    method: "post",
    url: "/permission/addUserList",
    data: query,
  });
}
export function listUpdate(query) {
  return service({
    method: "post",
    url: "/permission/listUpdate",
    data: query,
  });
}
export function Newslist(query) {
  return service({
    method: "get",
    url: "/permission/Newslist",
    data: query,
  });
}
export function orderLists(query) {
  return service({
    method: "get",
    url: "/permission/orderLists",
    data: query,
  });
}
export function homeList(query) {
  return service({
    method: "get",
    url: "/permission/homeList",
    data: query,
  });
}
export function noticeLists(query) {
  return service({
    method: "get",
    url: "/permission/noticeLists",
    data: query,
  });
}
export function cardlists(query) {
  return service({
    method: "get",
    url: "/permission/cardlists",
    data: query,
  });
}
