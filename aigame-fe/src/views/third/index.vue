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
          >当前module状态:{{ selectPptItem.gameStatus }}</span
        >
        <el-button type="primary" @click="onPrePage" style="margin-left: auto"
          >上一页</el-button
        >
        <el-button type="primary" @click="sendSave" :loading="saveLoading"
          >保存修改</el-button
        >
        <el-button type="primary" @click="sendGener" :loading="generateLoading"
          >生成游戏</el-button
        >
        <el-button type="primary" @click="jumpThird"> 下一页 </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, defineComponent, provide, computed } from "vue";
import { useRouter } from "vue-router";
import treeline from "./treeline.vue";
import LeftImg from "@/components/leftImgs.vue";
import { ElMessage } from "element-plus";
import { useStore } from "vuex";
import { gameQuery } from "@/api/modules/index";

export default defineComponent({
  components: {
    treeline,
  },
  setup() {
    const list = ref(null);
    const listLoading = ref(true);
    const router = useRouter();
    const store = useStore();
    const treelineComponent = ref(null);

    const selectPptItem = computed(() => store?.getters?.selectPptItem);
    const gameIdList = computed(
      () => store?.getters?.selectPptItem?.gameIdList || []
    );

    const stepValue = ref(selectPptItem.value.gameId);
    provide("stepValue", stepValue);
    // console.log(selectPptItem.value, "=======");

    const saveLoading = ref(false);
    const onSaveLoadingChange = (val) => {
      saveLoading.value = val;
    };
    provide("onSaveLoadingChange", onSaveLoadingChange);

    const sendSave = () => {
      console.log("dddd");
      if (treelineComponent.value) {
        treelineComponent.value.saveData();
      }
    };

    const generateLoading = ref(false);
    const onGenetareLoadingChange = (val) => {
      generateLoading.value = val;
    };
    provide("onGenetareLoadingChange", onGenetareLoadingChange);

    const sendGener = async () => {
      console.log("dddd");
      if (treelineComponent.value) {
        await treelineComponent.value.onGameGerate();
      }
    };
    const onPrePage = () => {
      router.back();
    };

    const jumpThird = () => {
      const status =
        store.getters.selectPptItem?.gameStatus ||
        store.getters.selectPptItem?.status;
      const canJumpStatus = ["code"];
      const data = {
        attach_id: store.getters.selectPptItem?.id
          ? store.getters.selectPptItem?.id
          : 3,
      };
      if (canJumpStatus.includes(status)) {
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
          router.push("/codePreview/previewMain");
        });
      } else {
        ElMessage.error("该模块尚未成功生成code.json，请等待code.json生成成功");
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
      gameIdList,
      stepValue,
      generateLoading,
      onPrePage,
      sendSave,
      jumpThird,
      sendGener,
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
  // bottom: 0;
  // background: #fff;
  // width: 100%;
  // left: 0;
  // right: 0;
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
