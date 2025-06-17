<template>
  <div class="chatMain">
    <div class="chat-container">
      <div v-show="chatMessages.length <= 0" class="defaultText">
        <p>
          <!-- <span><img src="@/assets/images/logoMax.png" alt="" /></span> -->
         请输入你的建议，生成更优代码
        </p>
      </div>
      <div class="chat-messages">
        <div v-for="(msg, index) in chatMessages" :key="index" class="flexChat">
          <div :class="['messageBox', msg.role]">
            <div :class="['message', msg.type]">
              <!-- 问 user -->
              <template v-if="msg.role === 'user'">
                <div
                  v-for="(item, index) in msg.content"
                  :key="'wen' + index"
                  class="userTitle infoList"
                >
                  <div v-if="item.type === 'text'" class="textBox">
                    {{ item.text }}
                  </div>
                  <div v-if="item.type === 'image_url'" class="imgBox">
                    <img :src="item.image_url.url" alt="" />
                  </div>
                  <div v-if="item.type === 'file'" class="fileAnBox">
                    <el-tag type="success">{{ item.file_detail.name }}</el-tag>
                  </div>
                </div>
                <div class="userImg">
                  <!-- <img :src="avatar" alt="" /> -->
                  <el-icon color="#4060c7"><Avatar /></el-icon>
                </div>
              </template>
              <!-- 答 user -->
              <template v-if="msg.role === 'assistant'">
                <div class="userInfo">
                  <!-- <img :src="logoMax" alt="" class="logoMax" /> -->
                  <el-icon color="#4060c7"><Headset /></el-icon>
                </div>
                <div
                  v-for="(item, index) in msg.content"
                  :key="'wen' + index"
                  class="answerTitle infoList"
                >
                  <div class="textBox">
                    <div v-html="item.text"></div>
                  </div>
                </div>
              </template>
            </div>
            <button
              v-if="msg.type === 'user'"
              @click="openEditDialog(index)"
              class="edit-icon"
            >
              <svg class="icon svg-icon" aria-hidden="true">
                <use xlink:href="#icon-edit"></use>
              </svg>
            </button>
          </div>
        </div>
      </div>
      <div class="chatBottom GH">
        <div v-if="false" class="chatBottomHeader">
          <div style="display: flex; align-items: center">
            <el-tooltip
              class="item"
              effect="dark"
              content="上传图片"
              placement="top"
            >
              <div class="workItem upload-button">
                <input
                  class="file-input"
                  ref="fileInput"
                  type="file"
                  @change="onFileChange"
                  accept="image/*"
                />
                <i class="el-icon-picture-outline-round"></i>
              </div>
            </el-tooltip>

            <el-tooltip
              class="item"
              effect="dark"
              content="上传文件"
              placement="top"
            >
              <file-select @changeFile="changeFile"></file-select>
            </el-tooltip>
            <div class="workItem">
              <el-tooltip
                class="item"
                effect="dark"
                content="新建对话"
                placement="top"
              >
                <i
                  @click="setNewDialog"
                  class="el-icon-circle-plus-outline"
                ></i>
              </el-tooltip>
            </div>
          </div>
          <div>
            <el-tooltip
              class="item"
              effect="dark"
              content="切换模型"
              placement="top"
            >
              <module-select
                v-model="modelName"
                :model_list="model_list"
              ></module-select>
            </el-tooltip>
          </div>
        </div>

        <div class="chatBoxInput">
          <el-input
            type="textarea"
            :autosize="{ minRows: 6, maxRows: 6 }"
            placeholder="请输入您的问题"
            v-model="inputMessage"
            @keydown="handleKeydown"
          >
          </el-input>
        </div>
        <div class="tipBottom">
          <div class="bottomLeft">
            <el-button
              :icon="Position"
              type="primary"
              @click="clearHistory"
              >清除历史对话</el-button
            >
          </div>
          <div class="bottomRight">
            <el-button
              :icon="Position"
              type="primary"
              :loading="sendLoading"
              @click="establishConnection"
              >发送</el-button
            >
          </div>
        </div>
        <div v-if="imgBoxList.length > 0" class="fileBottom">
          <div v-for="(item, index) in imgBoxList" :key="'file' + index">
            <template v-if="item.type === 'image_url'">
              <div class="fileBox">
                <div class="delImgBtn red" @click="resetImgList">
                  <i class="el-icon-delete"></i>
                </div>
                <img :src="item.image_url.url" alt="" />
              </div>
            </template>
            <template v-if="item.type === 'file'">
              <div>
                <el-tag closable type="success" @close="resetImgList">
                  {{ item.file_detail.name }}
                </el-tag>
              </div>
            </template>
          </div>
        </div>
      </div>
      <el-dialog title="编辑消息" v-model:visible="dialogVisible" width="30%">
        <el-input type="textarea" v-model="editMessageText" rows="5"></el-input>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmEdit">确认</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, defineEmits, computed, inject } from "vue";
const emit = defineEmits(['send-message']);
// import axios from "axios";
// import { getToken } from "@/utils/auth";
// import { chatApi, chatAllInfo, closeSession } from "@/api/gpt";
// import { marked } from "marked";
// import hljs from "highlight.js";
import "highlight.js/styles/atom-one-dark.css";
import { useStore } from "vuex";
import { gameGerateByChat } from "@/api/modules/index";
import { ElLoading, ElMessage } from 'element-plus'

// 引入组件并注释掉
// import moduleSelect from './component/moduleSelect.vue';
// import FileSelect from './component/FileSelect.vue';
// import SidebarChatList from './component/SidebarChatList.vue';

// 数据
const store = useStore();
const avatar = computed(() => store.getters.avatar);
const dialogVisible = ref(false);
const inputMessage = ref("");
const imgBoxList = reactive([]);
const chatMessages = inject("chatMessages");
const localChatList = reactive([]);
const chatBaseApi = ref(process.env.VUE_APP_CHAT_BASE_API);
const editMessageIndex = ref(null);
const editMessageText = ref("");
// const token = ref(getToken());
const sseSource = ref(null);

// 方法和生命周期钩子
const resetImgList = () => {
  imgBoxList.value = [];
};

const updateCode = inject("updateCode");
const gameId = inject("gameId");
const sendLoading = inject("sendLoading");
const establishConnection = async () => {
  if (!inputMessage.value) {
    ElMessage.error("请输入内容");
    return
  }
  emit('send-message', inputMessage.value);
  inputMessage.value = ''
};

const clearHistory = () => {
  if (sendLoading.value) {
    ElMessage.warning("存在请求中对话，请等待完成后再试");
    return;
  }
  if (chatMessages.value.length > 0) {
    chatMessages.value = [];
  } else {
    ElMessage.warning("没有历史对话可以清除");
  }
  
};


// 其他逻辑同 Vue 2.0，只需将数据和方法绑定到 `ref` 和 `reactive`。
</script>

<style lang="scss" scoped>
@import "./index.scss";
</style>
