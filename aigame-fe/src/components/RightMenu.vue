<template>
  <div class="right-menu">
    <el-dropdown class="avatar-container" trigger="click">
      <div class="avatar-wrapper">
        <!-- <img
          :src="avatarImage + '?imageView2/1/w/80/h/80'"
          class="user-avatar"
        /> -->
        <el-icon :size="24"><Avatar /></el-icon>
        <i class="el-icon-caret-bottom" />
      </div>
      <template #dropdown>
        <el-dropdown-menu class="user-dropdown">
          <!-- <router-link to="/home">
            <el-dropdown-item> 回到首页 </el-dropdown-item>
          </router-link> -->
          <!-- <el-dropdown-item @click="dialogVisible = true"
            >生成列表</el-dropdown-item
          >
          <el-dropdown-item>
            <a target="_blank" href="">操作流程</a>
          </el-dropdown-item> -->
          <el-dropdown-item divided @click="logout"> Log Out </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>

    <el-dialog
      append-to-body
      title="生成列表"
      v-model="dialogVisible"
      width="60%"
      :before-close="handleClose"
    >
      <div>
        <el-table :data="tableData" style="width: 100%">
          <el-table-column prop="date" label="日期" width="180" />
          <el-table-column prop="name" label="姓名" width="180" />
          <el-table-column prop="address" label="地址" />
          <el-table-column fixed="right" label="操作" width="100">
            <template #default="{ row }">
              <el-button type="text" size="small" @click="handleClick(row)">
                查看
              </el-button>
              <el-button type="text" size="small">编辑</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="dialogVisible = false"
          >确定</el-button
        >
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "vuex";
import avatarImage from "@/assets/images/avatar.png"; // 使用 import 语法
import { ElMessageBox } from "element-plus"; // 导入 ElMessageBox

const dialogVisible = ref(false);
const tableData = ref([
  {
    date: "2016-05-02",
    name: "王小虎",
    address: "上海市普陀区金沙江路 1518 弄",
  },
  {
    date: "2016-05-04",
    name: "王小虎",
    address: "上海市普陀区金沙江路 1517 弄",
  },
  {
    date: "2016-05-01",
    name: "王小虎",
    address: "上海市普陀区金沙江路 1519 弄",
  },
  {
    date: "2016-05-03",
    name: "王小虎",
    address: "上海市普陀区金沙江路 1516 弄",
  },
]);

const router = useRouter();
const route = useRoute();
const store = useStore();

const userName = computed(() => store.getters.userName);

function handleClose(done) {
  ElMessageBox.confirm("确认关闭？")
    .then(() => {
      done();
    })
    .catch(() => {});
}

async function logout() {
  await store.dispatch("user/logout");
  router.push(`/login?redirect=${route.fullPath}`);
}

function handleClick(row) {
  console.log("查看", row);
}
</script>

<style lang="scss" scoped>
.right-menu {
  float: right;
  height: 100%;
  width: 40px;
  line-height: 50px;
  margin-right: 20px;
  &:focus {
    outline: none;
  }

  .avatar-container {
    margin-right: 30px;

    .avatar-wrapper {
      margin-top: 12px;
      position: relative;

      .user-avatar {
        cursor: pointer;
        width: 40px;
        height: 40px;
        border-radius: 10px;
      }

      .el-icon-caret-bottom {
        cursor: pointer;
        position: absolute;
        right: -20px;
        top: 25px;
        font-size: 12px;
      }
    }
  }
}
</style>
