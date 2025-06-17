import { LoginInfo } from "../../api/modules/index.js";
import router from "../../router/router.js";
import { mix } from "../../utils/color.js";
import { ElMessage } from "element-plus";

// 假设 removeToken 和 resetRouter 在某个工具文件中定义

export default {
  namespaced: true,
  state: {
    UserInfo: {},
    token: sessionStorage.getItem("token") || "",
    isCollapse: true,
    themeConfig: {
      primary: "#4060c7",
      tabColor: "#FFFFFF",
      footColor: "#606266",
      backgroundColor: "#FFFFFF",
      textColor: "#00000099",
      istags: true,
    },
    pptList: [],
    selectPptItem: {},
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
    },
    setUserInfo(state, userinfo) {
      state.UserInfo = userinfo;
    },
    SetIsCollapse(state, isCollapse) {
      state.isCollapse = isCollapse;
    },
    SET_PPT: (state, pptList) => {
      console.log("Mutating pptList with:", pptList); // 日志
      state.pptList = pptList;
    },
    SET_PPTITEM: (state, selectPptItem) => {
      state.selectPptItem = selectPptItem;
    },
    setThemeConfig(state, primary) {
      state.themeConfig.primary = primary;
    },
    setThemeConfigTbaColor(state, primary) {
      state.themeConfig.tabColor = primary;
      if (primary == "#FFFFFF") {
        state.themeConfig.footColor = "#606266";
      } else {
        state.themeConfig.footColor = "#ffffff";
      }
    },
    setThemeConfigMenuColor(state, primary) {
      if (primary) {
        state.themeConfig.backgroundColor = "#FFFFFF";
        state.themeConfig.textColor = "#00000099";
      } else {
        state.themeConfig.backgroundColor = "#1d2129";
        state.themeConfig.textColor = "#bdbdc0";
      }
    },
    setThemeConfigchangeTags(state, primary) {
      if (primary) {
        state.themeConfig.istags = true;
      } else {
        state.themeConfig.istags = false;
      }
    },
    RESET_STATE(state) {
      state.UserInfo = {};
      state.token = "";
      sessionStorage.removeItem("token");
    },
  },

  actions: {
    login({ commit }, userInfo) {
      return new Promise((resolve, reject) => {
        LoginInfo(userInfo)
          .then((res) => {
            console.log(res);
            let token = res.result;
            sessionStorage.setItem("token", token);
            commit("setToken", token);
            router.replace("/");
            ElMessage({
              message: "登录成功",
              type: "success",
            });
            resolve();
          })
          .catch((err) => {
            reject(err);
          });
      });
    },
    logout({ commit }) {
      return new Promise((resolve) => {
        ElMessage({
          type: "success",
          message: "退出登录!",
        });
        // removeToken(); // must remove token first
        sessionStorage.removeItem("token");

        // resetRouter();
        commit("RESET_STATE");
        resolve();
      });
    },
    changeIsCollapse({ commit }, str) {
      console.log(str);
      commit("SetIsCollapse", str);
    },
    changeThem({ commit }, str) {
      commit("setThemeConfig", str);
      const pre = "--el-color-primary";
      const mixWhite = "#ffffff";
      const mixBlack = "#4060c7";
      const el = document.documentElement;
      el.style.setProperty(pre, str);
      for (let i = 1; i < 10; i += 1) {
        el.style.setProperty(`${pre}-light-${i}`, mix(str, mixWhite, i * 0.7));
      }
      el.style.setProperty("--el-color-primary-dark", mix(str, mixBlack, 0.1));
    },
    setPPTItem({ commit }, selectPptItem) {
      commit("SET_PPTITEM", selectPptItem);
    },
    setPPT({ commit }, pptList) {
      console.log("Dispatching SET_PPT with:", pptList); // 日志
      commit("SET_PPT", pptList);
    },
    changeTabColor({ commit }, val) {
      commit("setThemeConfigTbaColor", val);
    },
    changeMenuColor({ commit }, val) {
      commit("setThemeConfigMenuColor", val);
    },
    changeTags({ commit }, val) {
      commit("setThemeConfigchangeTags", val);
    },
  },
};
