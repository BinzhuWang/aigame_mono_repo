const getters = {
  token: (state) => state.user.token,
  isCollapse: (state) => state.user.isCollapse,
  UserInfo: (state) => state.user.UserInfo,
  themeConfig: (state) => state.user.themeConfig,
  pptList: (state) => state.user.pptList,
  selectPptItem: (state) => state.user.selectPptItem,
  tabsMenuList: (state) => state.tabs.tabsMenuList,
};

export default getters;
