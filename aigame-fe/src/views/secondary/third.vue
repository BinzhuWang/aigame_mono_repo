<template>
  <div class="app-container">
    <div class="secondMain">
      <div class="treeBox">
        <treeline />
      </div>
      <div class="bottomBtnGrounp">
        <el-button type="primary" plain> 保存修改 </el-button>
        <el-button type="primary" plain> 下一步 </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { getList } from "@/api/table";
import treeline from "./treeline";
export default {
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
  components: {
    treeline,
  },
  data() {
    return {
      list: null,
      listLoading: true,
    };
  },
  created() {
    // this.fetchData();
  },
  methods: {
    fetchData() {
      this.listLoading = true;
      getList().then((response) => {
        this.list = response.data.items;
        this.listLoading = false;
      });
    },
  },
};
</script>
<style lang="scss" scoped>
.secondMain {
  position: relative;
}
.bottomBtnGrounp {
  position: absolute;
  height: 50px;
  bottom: 0;
  background: #fff;
  width: 100%;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 20px;
  // height: ;
}
.treeBox {
  overflow-y: auto;
  height: calc(100vh - 110px);
}
</style>
