<template>
  <el-card class="clo-center">
    <div class="p10">验证组件🍨🍨🍨🍧🍧🍧</div>
    <el-form
      label-position="left"
      inline
      label-width="100px"
      :model="formLabelAlign"
    >
      <el-form-item label="请输入验证码" style="margin-right: 0">
        <el-input v-model="formLabelAlign.code" />
      </el-form-item>
      <el-form-item>
        <div class="s-canvas">
          <canvas
            @click="upDataCode"
            ref="canvasRef"
            :width="contentWidth"
            :height="contentHeight"
          ></canvas></div
      ></el-form-item>
    </el-form>
    <div className="sliderContent">
      <div className="imgDev" style="width: 500px">
        <canvas id="canvasImg" width="500" height="auto"></canvas>
        <canvas
          className="slider"
          id="sliderBlock"
          :width="500"
          :height="280"
          :style="{ left: sildLeft + 'px' }"
        ></canvas>
        <!-- <el-slider class="moveSlider" @change="changeValue1" v-model="value1" /> -->
      </div>
    </div>
    <div
      class="moveSlider"
      :style="{
        background: verifyResult ? '#859baa' : '#f7f8fa',
        color: verifyResult ? '#fff' : '606266',
      }"
    >
      {{ verifyResult ? "解锁成功" : "滑动解锁" }}
      <div class="slider" @mousedown="sliderMove" ref="slider">
        <el-icon v-if="verifyResult" class="icon-style" style="color: #859baa"
          ><Select
        /></el-icon>
        <el-icon v-else class="icon-style"><DArrowRight /></el-icon>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { DArrowRight, Select } from "@element-plus/icons-vue";
import { onMounted, reactive, ref } from "vue";
const contentWidth = ref(100);
const contentHeight = ref(32);
const sliderWidth = ref();
const sliderHeight = ref();
const sildLeft = ref(0);
const value1 = ref(0);
const sildY = ref();
const sildX = ref();
const verifyResult = ref(false);
const formLabelAlign = reactive({
  code: "",
});
const identifyCodes = ref("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890");
const identifyCode = ref("1234");
const canvasRef = ref(null);

// 生成随机数
const randomNum = (min, max) => {
  return Math.floor(Math.random() * (max - min) + min);
};

const randomColor = (min, max) => {
  var r = randomNum(min, max);
  var g = randomNum(min, max);
  var b = randomNum(min, max);
  return "rgb(" + r + "," + g + "," + b + ")";
};

const drawPic = () => {
  let ctx = canvasRef.value.getContext("2d");
  ctx.fillStyle = randomColor(180, 230); //填充颜色
  ctx.fillRect(0, 0, contentWidth.value, contentHeight.value); //填充位置
  // drawLine(ctx);

  let imgCode = "";
  // 随机产生字符串，并且随机旋转
  for (let i = 0; i < 4; i++) {
    const text = identifyCodes.value[randomNum(0, identifyCodes.value.length)];
    const deg = randomNum(-30, 30);
    imgCode += text;
    ctx.font = randomNum(18, 40) + "px Simhei"; //填充字体
    ctx.textBaseline = "top";
    ctx.fillStyle = randomColor(80, 150);
    drawDot(ctx);
    ctx.save(); //保存
    ctx.translate(30 * i + 15, 15);
    ctx.rotate((deg * Math.PI) / 180); //随机的旋转
    ctx.fillText(text, -15 + 5, -15); //
    ctx.restore(); //清除
  }
  drawLine(ctx);
  return imgCode;
};

const drawLine = (ctx) => {
  for (let i = 0; i < 5; i++) {
    ctx.strokeStyle = randomColor(0, 255);
    ctx.beginPath();
    ctx.moveTo(
      randomNum(0, contentWidth.value),
      randomNum(0, contentHeight.value)
    );
    ctx.lineTo(
      randomNum(0, contentWidth.value),
      randomNum(0, contentHeight.value)
    );
    ctx.stroke();
  }
};
const drawDot = (ctx) => {
  for (let i = 0; i < 20; i++) {
    ctx.fillStyle = randomColor(0, 255);
    ctx.beginPath();
    ctx.arc(
      randomNum(0, contentWidth.value),
      randomNum(0, contentHeight.value),
      1,
      0,
      2 * Math.PI
    );
    ctx.fill();
  }
};

onMounted(() => {
  drawPic();
  loadImage();
});

const upDataCode = () => {
  identifyCode.value = "";
  makeCode(identifyCodes.value, 4);
};
const makeCode = (val, l) => {
  for (let i = 1; i < val.length && i <= l; i++) {
    identifyCode.value +=
      identifyCodes.value[
        Math.floor(Math.random() * (identifyCodes.value.length - 0) + 0)
      ];
  }
  console.log(identifyCode.value);
  drawPic();
};

// 拼图
const loadImage = () => {
  //加载图片
  let mainDom = document.getElementById("canvasImg");
  let bg = mainDom.getContext("2d");
  let imgSrc = "";
  let img = document.createElement("img");
  img.src = imgSrc;
  img.onload = () => {
    mainDom.height = (img.height / img.width) * mainDom.width;
    bg.drawImage(img, 0, 0, mainDom.width, mainDom.height);
    let r = 10; //半圆的半径
    let w = 60; //滑块的宽度
    let x = randomNum(85, mainDom.width - w - r - 2); //保证缺口完全展示，不会隐藏
    let y = randomNum(16, mainDom.height - w - r - 2);
    sildY.value = y;
    sildX.value = x;
    bg.lineWidth = 1;
    bg.strokeStyle = "white";
    bg.beginPath();
    bg.moveTo(x, y);
    //top
    bg.arc(x + w / 2, y, r, -Math.PI, 0, true);
    bg.lineTo(x + w, y);
    //right
    bg.arc(x + w, y + w / 2, r, 1.5 * Math.PI, 0.5 * Math.PI, false);
    bg.lineTo(x + w, y + w);
    //bottom
    bg.arc(x + w / 2, y + w, r, 0, Math.PI, false);
    bg.lineTo(x, y + w);
    //left
    bg.arc(x, y + w / 2, r, 0.5 * Math.PI, 1.5 * Math.PI, true);
    bg.lineTo(x, y);
    bg.stroke();
    bg.fillStyle = "rgba(0, 0, 0, 0.4)"; //设置背景颜色
    bg.fill();
    sliderContent(img);
  };
};

const sliderContent = (img) => {
  let r = 10; //半圆的半径
  let w = 60; //滑块的宽度
  let mainDom = document.getElementById("sliderBlock");
  let ctx = mainDom.getContext("2d");
  //index.store.ts
  let x = sildLeft.value;
  let y = sildY.value;
  let PI = Math.PI;
  ctx.lineWidth = 1;
  //绘制
  ctx.beginPath();
  //left
  ctx.moveTo(x, y);
  //top
  ctx.arc(x + w / 2, y, r, -PI, 0, true);
  ctx.lineTo(x + w, y);
  //right
  ctx.arc(x + w, y + w / 2, r, 1.5 * PI, 0.5 * PI, false);
  ctx.lineTo(x + w, y + w);
  //bottom
  ctx.arc(x + w / 2, y + w, r, 0, PI, false);
  ctx.lineTo(x, y + w);
  //left
  ctx.arc(x, y + w / 2, r, 0.5 * PI, 1.5 * PI, true);
  ctx.lineTo(x, y);
  ctx.shadowBlur = 10;
  ctx.shadowColor = "black";
  ctx.stroke();
  ctx.clip();
  console.log(img);
  ctx.drawImage(img, -sildX.value + sildLeft.value, 0, 500, 280);
  // console.log(ctx)
};

const sliderMove = (event) => {
  let disX = 0;
  const iconWidth = 60;
  const ele = document.querySelector(".moveSlider .slider");
  const startX = event.clientX || event.touches[0].pageX;
  const MaxX = 500 - iconWidth;
  if (verifyResult.value) {
    return false;
  }
  // 开始移动
  const onMove = (e) => {
    const endX = e.clientX || e.touches[0].pageX;
    disX = endX - startX;
    if (disX <= 0) {
      disX = 0;
    }
    if (disX >= MaxX - iconWidth) {
      disX = MaxX;
    }
    sildLeft.value = disX;
    ele.style.transition = ".1s all";
    ele.style.transform = `translateX(${disX}px)`;
    console.log(ele.style.transform);
  };

  const onEnd = () => {
    if (disX > sildX.value - 5 && disX < sildX.value + 5) {
      verifyResult.value = true;
    } else {
      ele.style.transition = ".5s all";
      ele.style.transform = "translateX(0)";
    }
    document.removeEventListener("mousemove", onMove);
    document.removeEventListener("mouseup", onEnd);
  };
  document.addEventListener("mousemove", onMove);
  document.addEventListener("mouseup", onEnd);
};
</script>

<style lang="scss" scoped>
.s-canvas {
  height: 38px;
}
.s-canvas canvas {
  margin-top: 1px;
  margin-left: 8px;
}
.sliderContent {
  margin-top: 20px;
  position: relative;
  .slider {
    position: absolute;
  }
}
.moveSlider {
  width: 500px;
  height: 32px;
  background-color: #f7f8fa;
  font-size: 14px;
  line-height: 32px;
  text-align: center;
  color: #606266;
  position: relative;
  border: 1px solid #e4e7ed;
  .slider {
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    width: 32px;
    background-color: #fff;
    cursor: pointer;
    .icon-style {
      margin-top: 6px;
      font-size: 20px;
      text-align: center;
    }
  }
}
</style>
