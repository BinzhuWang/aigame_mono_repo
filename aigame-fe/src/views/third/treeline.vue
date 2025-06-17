<template>
  <div class="plan-tree-component">
    <div v-for="(item, index) in outline" :key="index" class="outline-module">
      <div class="module-header" @click="toggleModule(index)">
        <i
          :class="
            isModuleCollapsed[index]
              ? 'el-icon-caret-right'
              : 'el-icon-caret-bottom'
          "
        />
        <span class="game-name">{{ item.game_name }}</span>
        <i class="toggle-icon">
          <i
            :class="
              isModuleCollapsed[index]
                ? 'el-icon-circle-plus-outline'
                : 'el-icon-remove-outline'
            "
          />
        </i>
      </div>

      <transition name="collapse">
        <div v-show="!isModuleCollapsed[index]" class="module-body">
          <div class="module-content">
            <div class="left-module">
              <div class="field-group">
                <label>core_gameplay_summary: </label>
                <textarea
                  v-model="item.core_gameplay_summary"
                  style="min-height: 100px"
                  minRow="5"
                  maxRow="10"
                  class="ownInput"
                  placeholder="请输入核心玩法摘要"
                />
              </div>
              <div class="field-group">
                <label>estimated_duration_seconds: </label>
                <input
                  v-model="item.estimated_duration_seconds"
                  type="number"
                  class="ownInput"
                  placeholder="请输入预计时长"
                />
              </div>
              <div class="prototype-flow-section">
                <label>prototype_flow: </label>
                <div
                  v-for="(flow, flowIndex) in item.prototype_flow"
                  :key="flowIndex"
                  class="prototype-card"
                >
                  <p>
                    <strong>flow_description: </strong>
                    <input
                      v-model="flow.description"
                      type="text"
                      class="ownInput"
                      placeholder="请输入流程描述"
                    />
                  </p>
                  <p>
                    <strong>current_state: </strong>
                    <input
                      v-model="flow.state"
                      type="text"
                      class="ownInput"
                      placeholder="请输入当前状态"
                    />
                  </p>
                  <p>
                    <strong>next_state: </strong>
                    <input
                      v-model="flow.next_state"
                      type="text"
                      class="ownInput"
                      placeholder="请输入下一状态"
                    />
                  </p>
                  <p>
                    <strong>user_input: </strong>
                    <input
                      v-model="flow.user_input"
                      type="text"
                      class="ownInput"
                      placeholder="请输入用户输入"
                    />
                  </p>
                  <div
                    class="close-icon-box"
                    @click="removeFlowItem(item, flowIndex)"
                  >
                    <el-icon><CircleClose /></el-icon>
                  </div>
                </div>
                <div class="asset-item">
                  <div class="asset-content">
                    <div
                      class="asset-image-wrapper"
                      style="cursor: pointer"
                      title="添加prototype_flow"
                      @click="addFlowItem(item.prototype_flow)"
                    >
                      <el-icon style="width: 100px; height: 100px"
                        ><Plus
                      /></el-icon>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="right-module">
              <div class="field-group">
                <label>features: </label>
                <div
                  v-for="(featureList, featureKey) in item.features"
                  :key="featureKey"
                >
                  <label>{{ featureKey }}: </label>
                  <div
                    v-for="(feature, featureIndex) in featureList"
                    :key="featureIndex"
                    style="position: relative"
                  >
                    <input
                      v-model="item.features[featureKey][featureIndex]"
                      class="ownInput"
                      placeholder="编辑特性内容"
                    />
                    <div
                      class="close-icon-box"
                      style="position: absolute; right: -20px; top: -10px; cursor: pointer"
                      @click="removeFeatureItem(featureList, flowIndex)"
                    >
                      <el-icon><CircleClose /></el-icon>
                    </div>
                  </div>
                  <div>
                    <div
                      class="asset-image-wrapper"
                      style="
                        cursor: pointer;
                        width: 40px;
                        height: 40px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                      "
                      :title="`添加${featureKey}`"
                      @click="addFeatureItem(featureList)"
                    >
                      <el-icon style="width: 20px; height: 20px"
                        ><Plus
                      /></el-icon>
                    </div>
                  </div>
                </div>
              </div>
              <div class="prototype-flow-section">
                <label>knowledge_list: </label>
                <div
                  v-for="(
                    knowledgeItem, knowledgeItemIndex
                  ) in item.knowledge_list"
                  :key="knowledgeItemIndex"
                  class="prototype-card"
                >
                  <p>
                    <strong>content: </strong>
                    <input
                      v-model="knowledgeItem.content"
                      style="min-width: max-content; max-width: 80%"
                      type="text"
                      class="ownInput"
                      placeholder="请输入内容"
                    />
                  </p>
                  <p>
                    <strong>context: </strong>
                    <input
                      v-model="knowledgeItem.context"
                      type="text"
                      style="min-width: max-content; max-width: 80%"
                      class="ownInput"
                      placeholder="请输入内容"
                    />
                  </p>
                  <p>
                    <strong>page: </strong>
                    <input
                      v-model="knowledgeItem.page"
                      type="text"
                      style="min-width: max-content; max-width: 80%"
                      class="ownInput"
                      placeholder="请输入内容"
                    />
                  </p>
                  <div
                    class="close-icon-box"
                    @click="removeKnowledge(item, knowledgeItemIndex)"
                  >
                    <el-icon><CircleClose /></el-icon>
                  </div>
                </div>
                <div class="asset-item">
                  <div class="asset-content">
                    <div
                      class="asset-image-wrapper"
                      style="cursor: pointer"
                      title="添加知识点"
                      @click="addKnowledge(item)"
                    >
                      <el-icon style="width: 100px; height: 100px"
                        ><Plus
                      /></el-icon>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="assets-section">
            <label>static_assets: </label>
            <div
              v-for="(asset, assetIndex) in item.asset_list"
              :key="assetIndex"
              class="asset-item"
            >
              <div class="asset-content">
                <div
                  :class="{
                    'asset-image-wrapper': true,
                    'audio-type': asset.type === 'audio',
                  }"
                >
                  <img
                    :src="asset.reference"
                    alt="静态资源图片"
                    class="asset-image"
                    v-if="
                      (asset.type === 'image' || asset.type === 'background') &&
                      asset.reference
                    "
                  />
                  <audio
                    controls
                    v-if="asset.type === 'audio'"
                    class="asset-audio"
                    :src="asset.reference"
                  ></audio>
                  <video
                    class="asset-video"
                    v-if="asset.type === 'video'"
                    :src="asset.reference"
                  ></video>
                </div>
                <div class="asset-details">
                  <p>
                    <strong>asset_name: </strong>
                    <input
                      v-model="asset.asset_name"
                      type="text"
                      style="min-width: max-content; max-width: 80%"
                      class="ownInput"
                      placeholder="请输入内容"
                    />
                  </p>
                  <p>
                    <strong>type: </strong>
                    <select
                      v-if="asset.editType === 'add'"
                      v-model="asset.type"
                      class="ownInput"
                    >
                      <option value="image">image</option>
                      <option value="background">background</option>
                      <option value="audio">audio</option>
                      <option value="video">video</option>
                    </select>
                    <span v-else>
                      {{ asset.type }}
                    </span>
                  </p>
                  <p
                    v-if="asset.type === 'image' || asset.type === 'background'"
                  >
                    <strong>resolution: </strong>
                    <input
                      v-model="asset.resolution"
                      type="text"
                      style="min-width: max-content; max-width: 80%"
                      class="ownInput"
                      placeholder="请输入内容"
                    />
                  </p>
                  <p v-if="asset.type !== 'video'">
                    <strong>prompt: </strong>
                    <input
                      v-model="asset.prompt"
                      type="text"
                      style="min-width: max-content; max-width: 80%"
                      class="ownInput"
                      placeholder="请输入内容"
                    />
                  </p>
                  <p v-if="asset.type === 'video'">
                    <strong>image_prompt: </strong>
                    <input
                      v-model="asset.image_prompt"
                      type="text"
                      style="min-width: max-content; max-width: 80%"
                      class="ownInput"
                      placeholder="请输入内容"
                    />
                  </p>
                  <p v-if="asset.type === 'video'">
                    <strong>video_prompt: </strong>
                    <input
                      v-model="asset.prompt"
                      type="text"
                      style="min-width: max-content; max-width: 80%"
                      class="ownInput"
                      placeholder="请输入内容"
                    />
                  </p>
                  <p>
                    <strong>reference: </strong>
                    <!-- <input
                      v-model="asset.reference"
                      v-if="asset.editType === 'add'"
                      type="text"
                      style="min-width: max-content; max-width: 80%"
                      class="ownInput"
                      placeholder="请输入内容"
                    /> -->
                    <a :href="asset.reference" target="_blank">{{
                      asset.reference
                    }}</a>
                  </p>
                  <el-button
                    v-if="asset.editType !== 'add'"
                    :loading="asset.editLoading"
                    type="primary"
                    @click="regenAsset(asset)"
                  >
                    重新生成
                  </el-button>
                  <el-button
                    v-if="asset.editType === 'add'"
                    :loading="asset.editLoading"
                    type="primary"
                    @click="generateAddAsset(asset)"
                  >
                    {{ asset.type === "video" ? "生成图片" : "确定生成" }}
                  </el-button>
                  <el-button
                    v-if="asset.editType === 'add' && asset.type === 'video'"
                    :loading="asset.editLoading"
                    type="primary"
                    @click="generateAddAsset(asset, true)"
                  >
                    生成视频
                  </el-button>

                  <span class="upload-btn" v-if="asset.editType === 'add'">
                    <el-button :loading="asset.uploadLoading" type="primary">
                      <label :for="`ppt${assetIndex}`"> 手动上传 </label>
                    </el-button>
                    <input
                      :id="`ppt${assetIndex}`"
                      type="file"
                      class="hidden upload-file-input"
                      @change="(e) => handleFileChange(e, asset)"
                    />
                  </span>
                </div>
              </div>
              <div
                class="close-icon-box"
                @click="removeAsset(item, assetIndex)"
              >
                <el-icon><CircleClose /></el-icon>
              </div>
            </div>
          </div>
          <div class="asset-item">
            <div class="asset-content">
              <div
                class="asset-image-wrapper"
                style="cursor: pointer"
                title="添加素材"
                @click="addAsset(item.asset_list)"
              >
                <el-icon style="width: 100px; height: 100px"><Plus /></el-icon>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <div class="save-button-container">
      <!-- <el-button type="primary" @click="saveData"> 保存 </el-button> -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, inject, watch } from "vue";
import {
  gameModule,
  attachMedia,
  gameModuleEdit,
  gameGerate,
  regenModule,
  textToSound,
  textToImage,
  runwayVideo,
  gameQuery,
} from "@/api/modules/index";
import { useStore } from "vuex";
import { ElMessage } from "element-plus";

const store = useStore();
const outline = ref([]);
const isModuleCollapsed = ref([]);

const selectPptItem = computed(() => store.getters.selectPptItem);

const addFeatureItem = (featureList) => {
  featureList.push("");
};

const removeFeatureItem = (featureList, index) => {
  featureList.splice(index, 1);
};

const addFlowItem = (flowList) => {
  flowList.push({
    description: "",
    current_state: "",
    next_state: "",
    user_input: "",
  });
};

const removeFlowItem = (item, index) => {
  item.prototype_flow.splice(index, 1);
};
const addAsset = (assetsList) => {
  assetsList.push({
    asset_name: "",
    duration: "",
    fps: null,
    prompt: "",
    editType: "add",
    reference: "",
    resolution: "",
    type: "image",
  });
};

const removeAsset = (item, index) => {
  item.asset_list.splice(index, 1);
};

const regenAsset = async (item) => {
  item.editLoading = true;
  try {
    if (item.type === "image" || item.type === "background") {
      const res = await textToImage({
        prompt: item.prompt,
      });
      if (res.code === 200) {
        item.reference = res.result[0];
      } else {
        ElMessage.error(res.msg);
      }
    }
    if (item.type === "audio") {
      const res = await textToSound({
        content: item.prompt,
      });
      if (res.code === 200) {
        item.reference = res.result.audio;
      } else {
        ElMessage.error(res.msg);
      }
    }
    if (item.type === "video") {
      const videoRes = await runwayVideo({
        image_url: item.image_url,
        prompt_text: item.prompt,
      });
      if (videoRes.code === 200) {
        item.reference = videoRes.result[0];
        // item.editType = "view";
      } else {
        ElMessage.error(res.msg);
      }
    }
  } finally {
    item.editLoading = false;
  }
};

const generateAddAsset = async (item, isGenerateVideo = false) => {
  try {
    if (isGenerateVideo) {
      if (!item.image_url) {
        ElMessage.error("请先生成图片");
        return;
      }
      if (!item.prompt) {
        ElMessage.error("请输入prompt");
        return;
      }
      const videoRes = await runwayVideo({
        image_url: item.image_url,
        prompt_text: item.prompt,
      });
      if (videoRes.code === 200) {
        item.reference = videoRes.result[0];
        // item.editType = "view";
      } else {
        ElMessage.error(res.msg);
      }
    }
    item.editLoading = true;
    if (item.type === "image" || item.type === "background") {
      const res = await textToImage({
        prompt: item.prompt,
      });
      if (res.code === 200) {
        item.reference = res.result[0];
        item.editType = "view";
      } else {
        ElMessage.error(res.msg);
      }
    }
    if (item.type === "audio") {
      const res = await textToSound({
        content: item.prompt,
      });
      if (res.code === 200) {
        item.reference = res.result.audio;
        item.editType = "view";
      } else {
        ElMessage.error(res.msg);
      }
    }

    if (item.type === "video") {
      const res = await textToImage({
        prompt: item.image_prompt,
      }).then(async (res) => {
        item.image_url = res.result[0];
        // const videoRes = await runwayVideo({
        //   image_url: res.result[0],
        //   prompt_text: item.prompt,
        // });
        // if (videoRes.code === 200) {
        //   item.reference = videoRes.result[0];
        //   item.editType = "view";
        // } else {
        //   ElMessage.error(res.msg);
        // }
      });
    }
  } finally {
    item.editLoading = false;
  }
};
const handleFileChange = (event, asset) => {
  const file = event.target.files[0];
  if (!file) return;

  const imgTypeList = [
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "image/svg+xml",
  ];

  const audioTypeList = [
    "audio/mpeg",
    "audio/wav",
    "audio/ogg",
    "audio/mp3",
    "audio/m4a",
  ];
  const videoTypeList = [
    "video/mp4",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-flv",
    "video/webm",
  ];
  const allTypeList = [...imgTypeList, ...audioTypeList, ...videoTypeList];
  if (!allTypeList.includes(file.type)) {
    ElMessage.error("只能上传图片、音频、视频文件");
    return;
  }

  const maxSize = 30 * 1024 * 1024; // 30 MB
  if (file.size > maxSize) {
    alert("文件大小不能超过30MB");
    return;
  }

  let fileType = "";
  if (imgTypeList.includes(file.type)) {
    fileType = "image";
  }
  if (audioTypeList.includes(file.type)) {
    fileType = "audio";
  }
  if (videoTypeList.includes(file.type)) {
    fileType = "video";
  }

  const formData = new FormData();
  formData.append("files", file);
  asset.uploadLoading = true;

  attachMedia(formData, fileType, selectPptItem.value.id)
    .then((response) => {
      console.log("上传成功:", response);
      // 这里可以更新pptList，假设服务器返回了更新后的列表
      // pptList.value = response.data;
      asset.reference = response.result[0].url;
      asset.type = fileType;
    })
    .catch((error) => {
      console.error("上传失败:", error);
    })
    .finally(() => {
      asset.uploadLoading = false;
    });
};

const getDetail = (gameId) => {
  const data = {
    id: gameId ? gameId : selectPptItem.value.gameId || 3,
    module_type: "plan",
  };
  gameModule(data).then((res) => {
    console.log("gameDetail", res);
    outline.value = [res.result];
    isModuleCollapsed.value = new Array(outline.value.length).fill(false);
    store.dispatch("user/setPPTItem", {
      ...selectPptItem.value,
      gameStatus,
      gameId: gameId || selectPptItem.value.gameId,
    });
  });
};

const stepValue = inject("stepValue");
const gameStatus = computed(() => {
  const gameItem = selectPptItem.value.gameInfoList.find(
    (item) => item.id === stepValue.value
  );
  return gameItem?.status;
});
watch(
  () => stepValue.value,
  (newValue) => {
    getDetail(newValue);
  }
);

const toggleModule = (index) => {
  isModuleCollapsed.value[index] = !isModuleCollapsed.value[index];
};

const onSaveLoadingChange = inject("onSaveLoadingChange");
const saveData = async () => {
  console.log("保存的数据：", outline.value);
  const isAllComplete = outline.value[0].asset_list.every(
    (item) => item.reference
  );
  if (!isAllComplete) {
    ElMessage.error("请完成素材模块填写");
    return;
  }
  outline.value[0].asset_list.forEach((item) => {
    item.editType = "view";
  });
  // 实现保存逻辑，例如调用API
  try {
    onSaveLoadingChange(true);
    const data = {
      id: selectPptItem.value.gameId ? selectPptItem.value.gameId : 3,
      module_type: "plan",
    };
    gameModuleEdit(data, outline.value[0]).then((res) => {
      if (res.code === 200) {
        ElMessage.success("保存成功");
      } else {
        ElMessage.error("保存失败，请重试");
      }
    });
  } finally {
    onSaveLoadingChange(false);
    this.getDetail();
  }
};
const onGenetareLoadingChange = inject("onGenetareLoadingChange");
const onGameGerate = async () => {
  try {
    onGenetareLoadingChange(true);
    const data = {
      id: selectPptItem.value.gameId ? selectPptItem.value.gameId : 3,
    };
    gameQuery(data).then((res) => {
      const gameIsGoaling = (res?.result || []).some(
        (item) => item.status === "coding"
      );
      const regenStatusList = ["coding", "code", "fcode"];
      if (gameIsGoaling || regenStatusList.includes(gameStatus.value)) {
        // ElMessage.warning("正在生成code.json中，请耐心等候...");
        // onGenetareLoadingChange(false);
        regenModule({
          id: selectPptItem.value.gameId ? selectPptItem.value.gameId : 3,
          module_type: "code",
        })
          .then((res) => {
            if (res.code === 200) {
              ElMessage.success("重新生成请求发送成功, 请稍后查看");
            } else {
              ElMessage.error("重新生成请求发送失败，请重试");
            }
          })
          .finally(() => {
            onGenetareLoadingChange(false);
          });
        return;
      }
      gameGerate({
        id: selectPptItem.value.gameId ? selectPptItem.value.gameId : 3,
      }).then((generRes) => {
        if (generRes.code === 200) {
          ElMessage.success("生成请求发送成功, 请稍后查看");
        } else {
          ElMessage.error("生成请求发送失败，请重试");
        }
      });
    });
  } finally {
    onGenetareLoadingChange(false);
  }
};

const addKnowledge = (node) => {
  if (!Array.isArray(node?.knowledge_list)) {
    node.knowledge_list = [];
  }
  node.knowledge_list.push({
    content: "",
    context: "",
    page: "",
  });
};

const removeKnowledge = (node, index) => {
  node.knowledge_list.splice(index, 1);
};

defineExpose({
  saveData,
  onGameGerate,
});

onMounted(() => {
  getDetail();
});
</script>

<style lang="scss" scoped>
@import "./index.scss";

/* 样式保持不变 */
.plan-tree-component {
  padding: 20px;
}

.outline-module {
  background: #f9f9f9;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.module-header {
  display: flex;
  align-items: center;
  cursor: pointer;
  background: #e9f5ff;
  padding: 10px;
  border-bottom: 1px solid #ddd;
  border-radius: 8px 8px 0 0;
}

.tree-icon {
  margin-right: 10px;
  font-size: 20px;
}

.game-name {
  font-size: 16px;
  font-weight: bold;
  flex-grow: 1;
}

.toggle-icon {
  font-size: 16px;
  color: #666;
}

.module-body {
  padding: 20px;
}

.module-content {
  display: flex;
  justify-content: space-between;
  gap: 40px;
}

.left-module,
.right-module {
  flex: 1;
}

.field-group {
  margin-bottom: 15px;
}

.field-group label {
  font-weight: bold;
  margin-right: 10px;
  margin-bottom: 5px;
}

.ownInput {
  width: 100%;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.assets-section {
  margin-top: 20px;
}

.asset-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  position: relative;
  .close-icon-box {
    position: absolute;
    top: 8px;
    right: 8px;
    cursor: pointer;
  }
  .upload-btn {
    display: inline-block;
    width: fit-content;
    height: fit-content;
    margin-left: 12px;
    vertical-align: middle;
    color: #ffffff;
    cursor: pointer;
    > label {
      display: inline-block;
      box-sizing: border-box;
      width: 100%;
      height: 100%;
      // width: 80px;
      // height: 32px;
      // padding: 8px 16px;
      // text-align: center;
      // line-height: 16px;
      // border-radius: 4px;
      color: #ffffff;
      cursor: pointer;
      background-color: #4060c7;
      // &:hover {
      //   background-color: rgb(85, 85, 85);
      // }
    }
  }
  .upload-file-input {
    display: none;
  }
}

.asset-content {
  display: flex;
  gap: 20px;
}

.asset-image-wrapper {
  width: 100px;
  height: 100px;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
  &.audio-type {
    width: 300px;
    height: 100px;
  }
}

.asset-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.asset-audio {
  width: 300px;
  height: 100px;
}
.asset-video {
  width: 100px;
  height: 100px;
}

.asset-details {
  flex: 1;
}

.prototype-flow-section {
  margin-top: 20px;
}

.prototype-card {
  background: #f3f3f3;
  padding: 15px;
  padding-top: 5px;
  padding-bottom: 5px;
  margin-top: 10px;
  border-radius: 8px;
  border: 1px solid #ddd;
  position: relative;
  .close-icon-box {
    position: absolute;
    top: 8px;
    right: 8px;
    cursor: pointer;
  }
}

.prototype-card p {
  margin: 5px 0;
}

.save-button-container {
  margin-top: 20px;
  text-align: center;
}

.collapse-enter-active,
.collapse-leave-active {
  transition: height 0.3s ease, opacity 0.3s ease;
}

.collapse-enter,
.collapse-leave-to {
  height: 0;
  opacity: 0;
}
</style>
