<template>
  <div class="app">
    <div class="navTop">
      <div />
      <RightMenu />
    </div>
    <div class="app-bg">
      <img src="@/assets/images/halo.png" alt="" />
      <!-- <img src="@/assets/images/circle.webp" alt=""> -->
    </div>
    <div class="app-content">
      <header class="header">
        <div class="logo">
          <img src="../../../public/logo.webp" alt="Logo" />
        </div>
        <div class="user-info">
          <span>Powered by <b>AI Game Generator</b></span>
        </div>
      </header>

      <main class="main-content">
        <h1>
          Turn your <span class="highlight">PowerPoint</span> <br />
          into an <span class="highlight">app</span>
        </h1>
        <div class="input-container">
          <span class="i-box"><i class="el-icon-upload" /></span>
          <label for="ppt">Upload Your PowerPoint Here</label>
          <input
            id="ppt"
            type="file"
            accept=".ppt,.pptx"
            class="hidden"
            @change="handleFileChange"
          />
        </div>
        <div v-show="true" class="upload-list">
          <table class="ppt-list-table">
            <thead>
              <tr>
                <th class="col1">id</th>
                <th class="col2">name</th>
                <th class="col3">url</th>
                <th class="col4">status</th>
                <th class="col5">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(ppt, i) in pptList" :key="'ppt' + i">
                <td>{{ ppt.id }}</td>
                <td>{{ ppt.name }}</td>
                <td>
                  <!-- <a :href="ppt.url">Link</a> -->
                  <img
                    style="width: 80px; height: 80px"
                    :src="ppt.cover"
                    alt="cover"
                  />
                </td>
                <td>{{ ppt.status }}</td>
                <td>
                  <div class="generate">
                    <el-dropdown style="width: 100px">
                      <el-button
                        type="primary"
                        @click="onLeftBtnClick(ppt.status)"
                      >
                        Enter<el-icon class="el-icon--right"
                          ><arrow-down
                        /></el-icon>
                      </el-button>
                      <template #dropdown>
                        <el-dropdown-menu>
                          <el-dropdown-item
                            v-for="(item, index) in dropDownMap[ppt.status]"
                            :key="index"
                            @click="jumpUrl(ppt, item)"
                            >{{ item }}</el-dropdown-item
                          >
                        </el-dropdown-menu>
                      </template>
                    </el-dropdown>

                    <el-popconfirm
                      title="确定删除"
                      placement="top"
                      @confirm="deleteItem(ppt)"
                    >
                      <template #reference>
                        <el-button style="width: 60px" type="danger">
                          删除
                        </el-button>
                      </template>
                    </el-popconfirm>
                    <el-button style="width: 120px" @click="updateStatus(ppt, 'uploaded')">
                      回退至uploaded
                    </el-button>
                    <el-button style="width: 80px" @click="reParse(ppt)">
                      重新解析
                    </el-button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </main>

      <footer class="footer">
        <p>Built with AI Game Generator.</p>
      </footer>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import RightMenu from "@/components/RightMenu.vue"; // 引入 RightMenu 组件
import {
  attach,
  attachList,
  gameQuery,
  deleteAttach,
  updateAttachStatus,
  reParseAttach,
} from "@/api/modules/index";
import { useStore } from "vuex"; // 如果你使用 Vuex 4
// import { useStore } from 'pinia'; // 如果你使用 Pinia
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
const dropDownList = ["parse.json", "goal.json", "plan.json", "game view"];
const dropDownMap = {
  parse: dropDownList.slice(0, 1),
  goaling: dropDownList.slice(0, 1),
  fgoal: dropDownList.slice(0, 1),
  goal: dropDownList.slice(0, 2),
  planing: dropDownList.slice(0, 2),
  fplan: dropDownList.slice(0, 2),
  plan: dropDownList.slice(0, 3),
  coding: dropDownList.slice(0, 3),
  fode: dropDownList.slice(0, 3),
  code: dropDownList.slice(0, 4),
};
export default {
  components: {
    RightMenu, // 注册 RightMenu 组件
  },
  setup() {
    const store = useStore();
    const pptList = computed(() => store.getters.pptList);
    const router = useRouter();

    const getList = () => {
      const data = {
        file_type: "ppt",
      };
      attachList(data).then((res) => {
        console.log(res.result, "rrres");
        store.dispatch("user/setPPT", res.result);
      });
    };

    const handleFileChange = (event) => {
      const file = event.target.files[0];
      if (!file) return;

      const validTypes = [
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
      ];
      if (!validTypes.includes(file.type)) {
        alert("只能上传PPT文件");
        return;
      }

      const maxSize = 30 * 1024 * 1024; // 30 MB
      if (file.size > maxSize) {
        alert("文件大小不能超过30MB");
        return;
      }

      const formData = new FormData();
      formData.append("files", file);

      attach(formData)
        .then((response) => {
          console.log("上传成功:", response);
          // 这里可以更新pptList，假设服务器返回了更新后的列表
          // pptList.value = response.data;
        })
        .catch((error) => {
          console.error("上传失败:", error);
        });
    };

    const onLeftBtnClick = (status) => {
      const list = dropDownMap[status];
      if (!list?.length) {
        ElMessage.warning("正在解析中，请耐心等待...");
      }
    };
    const jumpUrl = async (item, type) => {
      const data = {
        attach_id: item.id,
      };
      gameQuery(data).then((res) => {
        const gameIdList = (res?.result || []).map((item) => item.id);
        // const gameId = gameIdList[gameIdList.length - 1 || 0];
        const gameId = gameIdList[0];

        store.dispatch("user/setPPTItem", {
          ...item,
          gameId: gameId,
          gameStatus: res.result[0]?.status,
          gameInfoList: res.result,
          gameIdList: gameIdList,
        });
        if (type === "parse.json") {
          router.push({
            path: "/parseJson",
          });
          return;
        }
        if (type === "goal.json") {
          router.push({
            path: "/secondary/main",
          });
          return;
        }
        if (type === "plan.json") {
          router.push({
            path: "/third/main1",
          });
          return;
        }
        if (type === "code.json") {
          router.push({
            path: "/codePreview",
          });
          return;
        }
      });
      // store.dispatch("user/setPPTItem", item);
      // router.push({
      //   path: "/parseJson",
      // })
    };

    const deleteItem = async (item) => {
      try {
        const res = await deleteAttach({
          id: item.id,
          file_type: "ppt",
        });
        if (res.code === 200) {
          ElMessage.success("删除成功");
        } else {
          ElMessage.error("删除失败");
        }
      } finally {
        getList();
      }
    };

    const updateStatus = async (item, status) => {
      try {
        const res = await updateAttachStatus({
          id: item.id,
          status,
        });
        if (res.code === 200) {
          ElMessage.success("状态修改成功");
        } else {
          ElMessage.error("状态修改失败");
        }
      } finally {
        getList();
      }
    };
    const reParse = async (item) => {
      try {
        const res = await reParseAttach({
          attach_id: item.id,
        });
        if (res.code === 200) {
          ElMessage.success("重新解析成功");
        } else {
          ElMessage.error("重新解析失败");
        }
      } finally {
        getList();
      }
    };

    onMounted(() => {
      getList();
    });

    return {
      dropDownMap,
      pptList,
      deleteItem,
      updateStatus,
      reParse,
      handleFileChange,
      onLeftBtnClick,
      jumpUrl,
    };
  },
};
</script>

<style scoped lang="scss">
.app {
  position: relative;
  background: #f4f4f5;
  * {
    box-sizing: border-box;
    overflow: hidden;
  }
}

.app-bg {
  display: flex;
  justify-content: center;
  max-width: 1200px;
  height: 100%;
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  background: inherit;
}

.app-bg img {
  mix-blend-mode: screen;
  width: 1200px;
}

.app-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  text-align: center;
  position: relative;
}

p {
  margin: 0px;
}

.header {
  width: 100%;
  padding: 20px;
  text-align: center;
  flex-shrink: 0;
}

.logo img {
  height: 40px;
  margin-right: 10px;
}

.user-info {
  font-size: 0.9em;
  color: #666;
  margin-top: 50px;

  span {
    display: inline-block;
    border-radius: 99px;
    padding: 0 20px;
    height: 3em;
    line-height: 3em;
    border: 1px solid #e4e4e7;
    background-color: rgb(255 255 255 / var(--tw-bg-opacity, 1));
    box-shadow: 0px 1px 1px 0px rgba(0, 0, 0, 0.25);
  }
}

.main-content {
  max-width: 66rem;
  margin-top: 40px;
  flex-grow: 1;

  h1 {
    font-size: 64px;
    font-weight: 400;
  }

  .ppt-list-table {
    table-layout: fixed;
    width: 100%;
    border-collapse: collapse;
    border: 1px solid #d5d5d5;

    th,
    td {
      border: 1px solid #d5d5d5;
      padding: 10px;

      a {
        color: #007bff;
        text-decoration: underline;
      }
    }

    .col1 {
      width: 4em;
    }

    .col2 {
      width: 12em;
    }

    .col3 {
      width: 6em;
    }

    .col4 {
      width: 6em;
    }

    .col5 {
      width: 24em;
    }

    .generate {
      border-radius: 5px;
      line-height: 1.5em;
      font-size: inherit;
      color: #fff;
      // background: #007bff;
      padding: 5px 5px;
      cursor: pointer;
      user-select: none;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
  }
}

.highlight {
  color: #007bff;
}

.input-container {
  margin: 20px 0;
  display: flex;
  align-items: center;
  border-radius: 12px;
  background: #fff;
  padding: 10px;
  border: 4px solid #d4d4d8;

  .i-box {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    background: #000;
    border-radius: 4px;
    color: #fff;
    font-size: 14px;
    margin-right: 5px;
  }

  #ppt {
    display: none;
  }
}

input[type="text"] {
  width: 300px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  margin-left: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.example-apps {
  margin-top: 20px;
}

.example-apps button {
  margin: 5px;
  padding: 8px 16px;
  background-color: #e0e0e0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.footer {
  padding: 8px 20px 12px;
  width: 100%;
  text-align: left;
  font-weight: bold;
  flex-shrink: 0;
}

.social-icons img {
  height: 30px;
  margin: 0 10px;
}
.navTop {
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: fixed;
  top: 0;
  width: 100%;
}
</style>
