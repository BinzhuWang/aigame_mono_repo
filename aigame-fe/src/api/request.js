import axios from "axios";
import { ElMessage, ElMessageBox } from "element-plus"; // 确保引入ElMessageBox用于进一步的错误处理

const service = axios.create({
  baseURL: import.meta.env.VITE_BASE_API, // 使用 Vite 的环境变量
  timeout: 15 * 1000 * 60, // 15 分钟超时,
});

// Request interceptors
service.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem("token");
    console.log("Token:", token); // 添加日志查看token
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
      console.log("Authorization Header:", config.headers["Authorization"]); // 检查请求头是否正确设置
    }
    return config;
  },
  (error) => {
    console.error("Request error: ", error);
    return Promise.reject(error);
  }
);

// Response interceptors
service.interceptors.response.use(
  (response) => {
    if (response.status !== 200) {
      ElMessage({
        type: "error",
        message: "服务器忙，请稍后再试~",
      });
      return Promise.reject(new Error("非预期的响应状态"));
    }
    const res = response.data;
    if (res.code !== 200) {
      ElMessage({
        message: res.message || "Error",
        type: "error",
        duration: 5000,
      });

      if (res.code === 50008 || res.code === 50012 || res.code === 50014) {
        ElMessageBox.confirm(
          "您已被登出，可以取消以停留在此页面，或重新登录",
          "确认登出",
          {
            confirmButtonText: "重新登录",
            cancelButtonText: "取消",
            type: "warning",
          }
        ).then(() => {
          // 假设有一个 Vuex store 用于处理 token 重置
          store.dispatch("user/resetToken").then(() => {
            location.reload();
          });
        });
      }
      return Promise.reject(new Error(res.message || "Error"));
    }

    return res;
  },
  (error) => {
    console.error("Response error: ", error);
    ElMessage({
      message: error.message,
      type: "error",
      duration: 5000,
    });
    return Promise.reject(error);
  }
);

export default service;
