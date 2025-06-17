<template>
  <div class="app-container">
    <!-- <div class="json-header-link">
      <a href="">parse.json</a>
    </div> -->
    <div class="leftImgBox">
      <LeftImg />
    </div>

    <div class="content">
      <div class="tree-box">
        <div v-for="(item, index) in list" :key="item.page" class="tree-item">
          <h5>
            <span
              >Page: {{ item.page }}
              <!-- <el-input style="display: inline;" v-model="item.title" placeholder="请输入内容"/> -->
            </span>
            <span
              >所属模块:
              <el-input-number v-model="item.module_id" :step="1" step-strictly
            /></span>
          </h5>
          <div class="text-list">
            <div
              class="text-item"
              v-for="(textItem, textIndex) in item.text"
              :key="textIndex"
            >
              {{ textItem }}
              <!-- <el-input v-model="textItem" placeholder="请输入内容" /> -->
            </div>
          </div>
          <div class="img-list">
            <div
              class="img-item"
              v-for="(imgItem, imgIndex) in item.images"
              :key="imgIndex"
            >
              <!-- 图片展示，支持预览 -->
              <el-image
                class="image"
                :src="addImagePrefix(imgItem.path)"
                :preview-src-list="[addImagePrefix(imgItem.path)]"
                fit="cover"
              />
              <!-- 图片描述展示 -->
              <div class="description">
                <p class="tag">
                  <strong>标签:</strong>
                  <el-input v-model="imgItem.tag" placeholder="请输入内容" />
                </p>
                <p class="desp">
                  <strong>描述:</strong>
                  <el-input v-model="imgItem.desp" placeholder="请输入内容" />
                </p>
                <el-checkbox
                  v-model="imgItem.use_in_game"
                  label="使用为素材"
                ></el-checkbox>
              </div>
            </div>
          </div>
          <!-- 音频 -->
          <div class="img-list">
            <div
              class="img-item"
              v-for="(autioItem, autioIndex) in item.audios"
              :key="autioIndex"
            >
              <div class="autio">
                <audio controls>
                  <source :src="autioItem.path" type="audio/mp4" />
                  <source :src="autioItem.path" type="audio/ogg; codecs=opus" />
                  <source
                    :src="autioItem.path"
                    type="audio/ogg; codecs=vorbis"
                  />
                  <source :src="autioItem.path" type="audio/mpeg" />
                </audio>
              </div>
              <!-- 音频描述展示 -->
              <div class="description">
                <p class="tag">
                  <strong>标签:</strong>
                  <el-input v-model="autioItem.tag" placeholder="请输入内容" />
                </p>
                <p class="desp">
                  <strong>描述:</strong>
                  <el-input v-model="autioItem.desp" placeholder="请输入内容" />
                </p>
                <el-checkbox
                  v-model="autioItem.use_in_game"
                  label="使用为素材"
                ></el-checkbox>
              </div>
            </div>
          </div>
          <!-- 视频 -->
          <div class="img-list">
            <div
              class="img-item"
              v-for="(vedioItem, vedioIndex) in item.videos"
              :key="vedioIndex"
            >
              <video class="image" :src="vedioItem.path"></video>
              <!-- 音频描述展示 -->
              <div class="description">
                <p class="tag">
                  <strong>标签:</strong>
                  <el-input v-model="autioItem.tag" placeholder="请输入内容" />
                </p>
                <p class="desp">
                  <strong>描述:</strong>
                  <el-input v-model="autioItem.desp" placeholder="请输入内容" />
                </p>
                <el-checkbox
                  v-model="vedioItem.use_in_game"
                  label="使用为素材"
                ></el-checkbox>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="btn-group">
        <span style="margin-right: auto; white-space: nowrap"
          >pptId: {{ selectPptItem.id }}</span
        >
        <el-button type="primary" @click="onPrePage">上一页</el-button>
        <el-button type="primary" @click="sendSave">保存修改</el-button>
        <el-button type="primary" @click="sendGener" :loading="generateLoading"
          >生成goal</el-button
        >
        <el-button type="primary" @click="jumpNext">下一页</el-button>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import RightMenu from "@/components/RightMenu.vue";
import LeftImg from "@/components/leftImgs.vue";
import {
  getPptParseInfo,
  editPptParseInfo,
} from "@/api/modules/codePreview.js";
import { goalGerate, gameQuery } from "@/api/modules/index.js";
import { ElMessage } from "element-plus";

const router = useRouter();
const store = useStore();
const list = ref([]);

const selectPptItem = computed(() => store?.getters?.selectPptItem);

// 图片地址前缀
const IMAGE_PREFIX = "https://api.gamecreator.online";

// 为图片路径添加前缀
const addImagePrefix = (path) => {
  if (!path.startsWith("http")) {
    return `${IMAGE_PREFIX}${path}`;
  }
  return path;
};

// 获取解析列表
const getParseList = async () => {
  try {
    const pptId = store.getters.selectPptItem?.id;
    if (!pptId) return;

    const response = await getPptParseInfo({
      id: pptId,
      module_type: "parse",
    });
    list.value = response.result?.document_info || [];
  } catch (error) {
    console.error("获取解析数据失败：", error);
  }
};

const saveLoading = ref(false);
// 保存修改
const saveParseList = async () => {
  try {
    const pptId = store.getters.selectPptItem?.id;
    if (!pptId) return;
    saveLoading.value = true;
    const res = await editPptParseInfo(
      { id: pptId || 3, module_type: "parse" },
      { document_info: list.value }
    );
    if (res.code === 200) {
      ElMessage.success("保存成功");
    }
  } catch (error) {
    console.error("保存失败：", error);
    ElMessage.error("保存失败，请重试");
  } finally {
    saveLoading.value = false;
  }
};

const generateLoading = ref(false);
const sendGener = async () => {
  try {
    const pptId = store.getters.selectPptItem?.id;
    if (!pptId) {
      return;
    }
    generateLoading.value = true;
    const data = {
      id: pptId ? pptId : 3,
      module_type: "goal",
    };
    gameQuery(data).then(async (res) => {
      const gameIsGoaling = (res?.result || []).some(
        (item) => item.status === "goaling"
      );
      if (gameIsGoaling) {
        ElMessage.warning("正在生成goal.json中，请耐心等候...");
        onGenetareLoadingChange(false);
        return;
      }
      const resGoal = await goalGerate({ attach_id: pptId });
      if (resGoal.code === 200) {
        ElMessage.success("生成goal成功");
      }
    });
  } catch (error) {
    console.error("生成goal失败：", error);
    ElMessage.error("生成goal失败，请重试");
  } finally {
    generateLoading.value = false;
  }
};

// 保存按钮
const sendSave = () => {
  saveParseList();
};
const onPrePage = () => {
  router.back();
};
// 跳转下一页
const jumpNext = () => {
  const status =
    store.getters.selectPptItem?.gameStatus ||
    store.getters.selectPptItem?.status;
  const canJumpStatus = ["goal", "fplan", "plan", "coding", "fcode", "code"];
  if (canJumpStatus.includes(status)) {
    router.push("/secondary");
  } else {
    ElMessage.error("该模块尚未成功生成goal，请等待goal生成成功");
  }
};

onMounted(getParseList);
</script>
<style scoped>
@import "./index.scss";
</style>
