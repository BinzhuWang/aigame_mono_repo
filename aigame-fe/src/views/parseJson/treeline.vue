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
                <input
                  v-model="item.core_gameplay_summary"
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
                  >
                    <input
                      v-model="item.features[featureKey][featureIndex]"
                      class="ownInput"
                      placeholder="编辑特性内容"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="assets-section">
            <label>static_assets: </label>
            <div
              v-for="(asset, assetIndex) in item.asset"
              :key="assetIndex"
              class="asset-item"
            >
              <div class="asset-content">
                <div class="asset-image-wrapper">
                  <img
                    :src="asset.reference"
                    alt="静态资源图片"
                    class="asset-image"
                  />
                </div>
                <div class="asset-details">
                  <p><strong>asset_name: </strong>{{ asset.asset_name }}</p>
                  <p><strong>type: </strong>{{ asset.type }}</p>
                  <p><strong>resolution: </strong>{{ asset.resolution }}</p>
                  <p><strong>prompt: </strong>{{ asset.prompt }}</p>
                  <p>
                    <strong>reference: </strong
                    ><a :href="asset.reference" target="_blank">{{
                      asset.reference
                    }}</a>
                  </p>
                </div>
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
import { ref, onMounted, computed } from "vue";
import { gameModule } from "@/api/modules/index";
import { useStore } from "vuex";

const store = useStore();
const outline = ref([]);
const isModuleCollapsed = ref([]);

const selectPptItem = computed(() => store.getters.selectPptItem);

const getDetail = () => {
  const data = {
    id: selectPptItem.value.id ? selectPptItem.value.id : 3,
    module_type: "plan",
  };
  gameModule(data).then((res) => {
    console.log("gameDetail", res);
    outline.value = res.result;
    isModuleCollapsed.value = new Array(outline.value.length).fill(false);
  });
};

const toggleModule = (index) => {
  isModuleCollapsed.value[index] = !isModuleCollapsed.value[index];
};

const saveData = () => {
  console.log("保存的数据：", outline.value);
  // 实现保存逻辑，例如调用API
};

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
}

.asset-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
