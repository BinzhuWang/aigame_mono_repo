<template>
  <div class="leftImg">
    <el-badge
      :max="99"
      v-for="(url, index) in srcList"
      :value="index + 1"
      :offset="[16, 16]"
      :key="url"
      style="width: 188px; height: 188px"
    >
      <el-image
        :key="url"
        :src="url"
        style="width: 188px; height: 188px"
        :initial-index="index"
        :preview-src-list="srcList"
        fit="contain"
      />
    </el-badge>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useStore } from "vuex";
import { screenshot } from "@/api/modules/index";

const store = useStore();

const srcList = ref([]);
const selectPptItem = computed(() => store.getters.selectPptItem);

const getScreenshot = () => {
  const data = {
    attach_id: selectPptItem.value.id ? selectPptItem.value.id : 3,
  };
  screenshot(data).then((res) => {
    srcList.value = res.result;
  });
};
onMounted(() => {
  getScreenshot();
});
</script>

<style lang="scss" scoped>
.leftImg {
  width: 208px;
  overflow: hidden;
  box-sizing: border-box;
  *  {
    box-sizing: border-box;
  }
}
::v-deep(.el-badge) {
  .el-badge__content.is-fixed {
    top: 16px;
    right: 24px;
  }
}
</style>
