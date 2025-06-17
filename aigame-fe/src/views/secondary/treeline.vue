<template>
  <div class="plan-tree-component">
    <el-tree
      :data="outline"
      node-key="id"
      :props="defaultProps"
      default-expand-all
      :expand-on-click-node="false"
      :allow-drop="allowDrop"
      :allow-drag="allowDrag"
      @node-drop="handleDrop"
    >
      <template #default="{ node, data }">
        <div class="slotContentBox">
          <div
            :class="[
              'custom-tree-node',
              { 'dynamic-class': data && data.level === 1 },
            ]"
          >
            <!-- 111 {{ data.game_goal }} -->
            <div class="inputBoxMain">
              <div class="pageSource">
                <span v-if="data && data.level === 1">
                  <!-- 第{{ numberToChinese(data.index) }}章 -->
                  game_goal：
                </span>
                <span v-else>text_excerpt</span>
              </div>
              <input
                v-if="data && data.game_goal"
                ref="input"
                v-model="data.game_goal"
                class="ownInput"
                rows="1"
                placeholder="请输入您对应的标题或点击AI帮写..."
                size="mini"
                @blur="() => submitEdit(node, data)"
              />
              <input
                v-else
                ref="input"
                v-model="data.text_excerpt"
                class="ownInput"
                rows="1"
                placeholder="请输入您对应的标题或点击AI帮写..."
                size="mini"
                @blur="() => submitEdit(node, data)"
              />
            </div>
          </div>
          <div v-if="data && !data.game_goal" class="contentInput">
            <span class="pageSource">image_summary</span>
            <input
              ref="myTextarea"
              v-model="data.image_summary"
              class="ownInput"
              rows="1"
              placeholder="请输入您对应的游戏内容"
              @blur.native="saveSummary"
            />
          </div>
          <div v-if="data && data?.start_page" class="contentInput">
            <span class="pageSource">start_page</span>
            <input
              ref="myTextarea"
              v-model="data.start_page"
              class="ownInput"
              rows="1"
              placeholder="请输入您对应的开始页码"
              @blur.native="saveSummary"
            />
          </div>
          <div v-if="data && data?.end_page" class="contentInput">
            <span class="pageSource">end_page</span>
            <input
              ref="myTextarea"
              v-model="data.end_page"
              class="ownInput"
              rows="1"
              placeholder="请输入您对应的结束页码"
              @blur.native="saveSummary"
            />
          </div>
          <div v-if="data && data?.module_id" class="contentInput">
            <span class="pageSource">module_id</span>
            <input
              ref="myTextarea"
              v-model="data.module_id"
              :disabled="true"
              class="ownInput"
              rows="1"
              placeholder="请输入您对应的游戏Id"
              @blur.native="saveSummary"
            />
          </div>
          <div class="prototype-flow-section">
            <label>knowledge_list: </label>
            <div
              v-for="(knowledgeItem, knowledgeItemIndex) in data.knowledge_list"
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
                @click="removeKnowledge(data, knowledgeItemIndex)"
              >
                <el-icon><CircleClose /></el-icon>
              </div>
            </div>

            <div class="asset-item">
              <div class="asset-content">
                <div
                  class="asset-image-wrapper"
                  style="cursor: pointer"
                  title="添加素材"
                  @click="addKnowledge(data)"
                >
                  <el-icon style="width: 100px; height: 100px"
                    ><Plus
                  /></el-icon>
                </div>
              </div>
            </div>
          </div>

          <div class="img-list">
            <label v-if="data && data?.asset_list?.length > 0"
              >asset_list：</label
            >
            <div
              class="img-item"
              v-for="(imgItem, imgIndex) in data.asset_list"
              :key="imgIndex"
            >
              <!-- 图片展示，支持预览 -->
              <el-image
                class="image"
                :src="imgItem.reference"
                :preview-src-list="[imgItem.reference]"
                fit="cover"
                v-if="imgItem.type === 'image' || imgItem.type === 'background'"
              />
              <audio controls v-if="imgItem.type === 'audio'">
                <source :src="imgItem.reference" type="audio/mp4" />
                <source
                  :src="imgItem.reference"
                  type="audio/ogg; codecs=opus"
                />
                <source
                  :src="imgItem.reference"
                  type="audio/ogg; codecs=vorbis"
                />
                <source :src="imgItem.reference" type="audio/mpeg" />
              </audio>
              <video
                class="image"
                v-if="imgItem.type === 'vedio'"
                :src="imgItem.reference"
              ></video>
              <!-- 图片描述展示 -->
              <div class="description">
                <p class="tag">
                  <strong>asset_name:</strong>
                  <el-input
                    v-model="imgItem.asset_name"
                    style="min-width: max-content; max-width: 80%"
                    placeholder="请输入内容"
                  />
                </p>
                <p class="desp">
                  <strong>resolution:</strong>
                  {{ imgItem.resolution }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </template>
    </el-tree>
  </div>
</template>

<script>
import { ref, onMounted, computed, inject, watch } from "vue";
import { useStore } from "vuex";
import {
  gameModule,
  gameModuleEdit,
  gameGerate,
  regenModule,
  gameQuery,
} from "@/api/modules/index";
import { ElMessage } from "element-plus";
export default {
  name: "PlanTreeComponent",

  setup() {
    const outline = ref([]);
    const defaultProps = {
      children: "evidence",
      label: "label",
    };
    let idCount = ref(1);
    const store = useStore();
    const selectPptItem = computed(() => store.getters.selectPptItem);

    const getGameId = async () => {
      const data = {
        attach_id: selectPptItem.value.id ? selectPptItem.value.id : 3,
      };
      gameQuery(data).then((res) => {
        const gameIdList = (res?.result || []).map((item) => item.id);
        // const gameId = gameIdList[gameIdList.length - 1 || 0];
        const gameId = gameIdList[0];
        store.dispatch("user/setPPTItem", {
          ...selectPptItem.value,
          gameId: gameId,
          gameInfoList: res?.result,
          gameStatus: res?.result[0]?.status,
          gameIdList: gameIdList,
        });
        getDetail(gameId);
      });
    };
    const getDetail = (gameId) => {
      const data = {
        id: gameId ? gameId : 3,
        module_type: "goal",
      };
      gameModule(data).then((res) => {
        console.log("gameDetail", res);
        outline.value = [res.result];
        console.log(outline.value, "outline");
        store.dispatch("user/setPPTItem", {
          ...selectPptItem.value,
          gameStatus,

          gameId: gameId || selectPptItem.value.gameId,
        });
        generateIndexes(outline.value);
      });
    };

    const onSaveLoadingChange = inject("onSaveLoadingChange");
    const saveData = async () => {
      console.log("子组件方法被调用保存方法", outline.value);
      try {
        onSaveLoadingChange(true);
        const data = {
          id: selectPptItem.value.gameId ? selectPptItem.value.gameId : 3,
          module_type: "goal",
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
      }
    };

    const stepValue = inject("stepValue");
    const gameStatus = computed(() => {
      const gameItem = selectPptItem.value.gameInfoList.find(
        (item) => Number(item.id) === Number(stepValue.value)
      );
      return gameItem?.status;
    });
    watch(
      () => stepValue.value,
      (newValue) => {
        getDetail(newValue);
      }
    );

    const onGenetareLoadingChange = inject("onGenetareLoadingChange");
    const onPlanGenerate = async () => {
      try {
        onGenetareLoadingChange(true);

        const data = {
          id: selectPptItem.value.id ? selectPptItem.value.id : 3,
          module_type: "goal",
        };
        gameQuery(data).then((res) => {
          const gameIsGoaling = (res?.result || []).some(
            (item) => item.status === "planing"
          );
          const regenStatusList = [
            "coding",
            "planing",
            "plan",
            "code",
            "fplan",
            "fcode",
          ];
          if (gameIsGoaling || regenStatusList.includes(gameStatus.value)) {
            // ElMessage.warning("正在生成plan.json中，请耐心等候...");
            // onGenetareLoadingChange(false);
            regenModule({
              id: selectPptItem.value.gameId ? selectPptItem.value.gameId : 3,
              module_type: "plan",
            })
              .then((res) => {
                if (res.code === 200) {
                  ElMessage.success("重新生成请求发送成功, 请稍后查看");
                  getGameId();
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
              getGameId();
            } else {
              ElMessage.error("生成请求发送失败，请重试");
            }
          });
        });
      } finally {
        onGenetareLoadingChange(false);
      }
    };

    const generateIndexes = (nodes, parentIndex = "", level = 1) => {
      console.log(nodes, "nodes");
      let counter = 1;
      nodes.forEach((node) => {
        const index = parentIndex
          ? `${parentIndex}-${counter++}`
          : `${counter++}`;
        node.index = index;
        node.level = level;
        if (!node.id) {
          const uniqueId = "node" + idCount.value++;
          node.id = uniqueId;
        }

        if (node.evidence && Array.isArray(node.evidence)) {
          generateIndexes(node.evidence, index, level + 1);
        }
        // if (node.evidence && node.evidence.length > 0) {
        //   generateIndexes(node.evidence, index, level + 1);
        // }
      });
    };

    const numberToChinese = (num) => {
      const chineseNums = [
        "零",
        "一",
        "二",
        "三",
        "四",
        "五",
        "六",
        "七",
        "八",
        "九",
      ];
      const units = ["", "十", "百", "千", "万", "十", "百", "千", "亿"];

      let result = "";
      let strNum = num.toString();
      let len = strNum.length;

      for (let i = 0; i < len; i++) {
        let digit = parseInt(strNum[i]);
        if (digit !== 0) {
          result += chineseNums[digit] + units[len - i - 1];
        } else if (result && result[result.length - 1] !== "零") {
          result += chineseNums[digit];
        }
      }

      result = result.replace(/零+/g, "零");
      result = result.replace(/零([十百千])/, "$1");
      result = result.replace(/零+$/, "");

      if (result === "十") {
        result = "十";
      } else if (result.startsWith("一十")) {
        result = result.replace("一十", "十");
      }

      return result;
    };

    const handleDrop = (draggingNode, dropNode, dropType, ev) => {
      console.log("tree drop: ", dropNode.label, dropType);
      generateIndexes(outline.value);
    };

    const allowDrop = (draggingNode, dropNode, type) => true;

    const allowDrag = (draggingNode) => {
      return draggingNode.data.game_goal.indexOf("hahah") === -1;
    };
    let newlabel = ref("");

    const submitEdit = (node, data) => {
      if (data.game_goal === newlabel.value) {
        newlabel.value = "";
        data.isEdit = 0;
      } else {
        data.label = newlabel.value;
        newlabel.value = "";
        data.isEdit = 0;
        onlySave();
      }
    };

    const saveSummary = () => {
      onlySave();
    };

    const onlySave = () => {
      // Implement save logic here
    };

    onMounted(() => {
      // getDetail();
      getGameId();
    });

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

    return {
      outline,
      defaultProps,
      onSaveLoadingChange,
      selectPptItem,
      saveData,
      onGenetareLoadingChange,
      onPlanGenerate,
      numberToChinese,
      handleDrop,
      allowDrop,
      allowDrag,
      submitEdit,
      addKnowledge,
      removeKnowledge,
      saveSummary,
    };
  },
};
</script>

<style lang="scss" scoped>
@import "./index.scss";

:deep(.el-loading-spinner) {
  top: 20% !important;
}
.el-loading-spinner {
  top: 20% !important;
}
:deep(.el-tree-node__children) {
  background: #f7f9fa;
}
.prototype-flow-section {
  border: 1px solid #ddd;
  padding: 12px;
  border-radius: 8px;
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
  }
}

.prototype-card p {
  margin: 5px 0;
}
.img-list {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  gap: 20px;

  .img-item {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    padding: 10px;
    border: 1px solid #ebeef5;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

    .image {
      width: 200px;
      height: 200px;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid #dcdfe6;
    }
    .autio {
      width: 300px;
      height: 100px;
    }

    .description {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 10px;

      .tag {
        font-size: 14px;
        color: #333;
      }

      .desp {
        font-size: 14px;
        color: #606266;
        line-height: 1.5;
      }

      .el-checkbox {
        margin-top: 10px;
      }
    }
  }
}
.btnList {
  display: flex;
}
.btnStarDe {
  width: 20px;
  height: 20px;
  position: relative;
  top: -6px;
  img {
    width: 100%;
    height: 100%;
  }
}
.btnStarBorder {
  color: #0066ff;
  background: linear-gradient(#fff, #fff) padding-box,
    linear-gradient(45deg, #e0b0ff, #00feff, #90ff7b, #e0b0ff) border-box;
  border: 2px solid transparent;
  border-radius: 30px;
  cursor: pointer;
  text-decoration: none;
  position: relative;
}
.bgDeBtn {
  background-image: linear-gradient(180deg, #009fff 11%, #0066ff 89%);
  box-shadow: inset 0 2px 4px 0 #6cb6ff, inset 0 6px 5px 0 #ffffffa6,
    inset 0 -2px 3px 0 #7eb2ff, inset 0 -3px 6px 0 #0052cc;
  border-radius: 20px;
  color: #fff;
  font-weight: bold;
}
</style>
