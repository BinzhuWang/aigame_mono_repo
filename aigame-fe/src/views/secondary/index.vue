<template>
  <div class="app-container">
    <div class="leftImgBox">
      <LeftImg />
    </div>
    <div class="secondMain">
      <div class="treeBox">
        <treeline ref="treelineComponent" />
      </div>
      <div class="bottomBtnGrounp">
        <span style="margin-right: 12px; white-space: nowrap"
          >pptId: {{ selectPptItem.id }}</span
        >
        <span style="white-space: nowrap">
          当前module:
          <el-select v-model="stepValue" size="large" style="width: 120px">
            <el-option
              v-for="(item, index) in gameIdList"
              :key="item"
              :label="`module${index + 1}`"
              :value="item"
            />
          </el-select>
        </span>
        <span style="margin: 0 12px; white-space: nowrap"
          >当前module状态：{{ selectPptItem.gameStatus }}</span
        >
        <el-button type="primary" @click="onPrePage" style="margin-left: auto"
          >上一页</el-button
        >
        <el-button type="primary" @click="sendSave" :loading="saveLoading"
          >保存修改</el-button
        >
        <el-button type="primary" @click="sendGener" :loading="generateLoading"
          >生成plan</el-button
        >
        <el-button type="primary" @click="jumpThird"> 下一页 </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, defineComponent, provide, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import treeline from "./treeline.vue";
import LeftImg from "@/components/leftImgs.vue";
import { ElMessage } from "element-plus";

export default defineComponent({
  components: {
    treeline,
    LeftImg,
  },
  setup() {
    const list = ref(null);
    const listLoading = ref(true);
    const router = useRouter();
    const treelineComponent = ref(null);

    const store = useStore();
    const selectPptItem = computed(() => store.getters.selectPptItem);
    const gameIdList = computed(
      () => store.getters.selectPptItem?.gameIdList || []
    );

    const stepValue = ref(selectPptItem.value.gameId);
    provide("stepValue", stepValue);

    const saveLoading = ref(false);
    const onSaveLoadingChange = (val) => {
      saveLoading.value = val;
    };
    provide("onSaveLoadingChange", onSaveLoadingChange);
    const sendSave = async () => {
      console.log("dddd");
      if (treelineComponent.value) {
        await treelineComponent.value.saveData();
      }
    };
    const onPrePage = () => {
      router.back();
    };

    const generateLoading = ref(false);
    const onGenetareLoadingChange = (val) => {
      generateLoading.value = val;
    };
    provide("onGenetareLoadingChange", onGenetareLoadingChange);
    const sendGener = async () => {
      console.log("dddd");
      if (treelineComponent.value) {
        await treelineComponent.value.onPlanGenerate();
      }
    };

    const jumpThird = () => {
      const status =
        store.getters.selectPptItem?.gameStatus ||
        store.getters.selectPptItem?.status;
      const canJumpStatus = ["plan", "coding", "fcode", "code"];
      if (canJumpStatus.includes(status)) {
        router.push("/third/main1");
      } else {
        ElMessage.error("该模块尚未成功生成plan.json，请等待plan.json生成成功");
      }
    };

    // const fetchData = async () => {
    //   listLoading.value = true;
    //   try {
    //     const response = await getList();
    //     list.value = response.data.items;
    //   } finally {
    //     listLoading.value = false;
    //   }
    // };

    return {
      list,
      listLoading,
      selectPptItem,
      stepValue,
      gameIdList,
      sendSave,
      onPrePage,
      sendGener,
      jumpThird,
      treelineComponent,
    };
  },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: "success",
        draft: "gray",
        deleted: "danger",
      };
      return statusMap[status];
    },
  },
});
</script>

<style lang="scss" scoped>
.app-container {
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  overflow: hidden;
  .leftImgBox {
    width: 200px;
    height: calc(100vh - 70px);
    overflow: auto;
  }
}
.secondMain {
  position: relative;
  flex: 1;
}
.bottomBtnGrounp {
  position: fixed;
  top: 8px;
  left: 50%;
  transform: translateX(-50%);
  // position: absolute;
  // height: 50px;
  // background: #fff;
  // width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  // padding-top: 20px;
}
.treeBox {
  overflow-y: auto;
  height: calc(100vh - 70px);
}
</style>
