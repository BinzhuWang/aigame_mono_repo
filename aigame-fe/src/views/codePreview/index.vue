<template>
  <div class="app">
    <!-- <div class="navTop">
      <div />
      <RightMenu />
    </div> -->
    <div class="btn-group">
      <span style="margin-right: 12px"
        >pptId：<span style="color: #777777">{{ selectPptItem.id }}</span></span
      >
      <span style="margin-right: 12px"
        >pptName：<span style="color: #777777">{{
          selectPptItem.name
        }}</span></span
      >
      <el-button type="primary" @click="onPrePage">上一页</el-button>
      当前关卡:
      <el-select v-model="stepValue" size="large" style="width: 120px">
        <el-option
          v-for="(item, index) in gameIdList"
          :key="item"
          :label="`关卡${index + 1}`"
          :value="item"
        />
      </el-select>

      <el-button type="primary" @click="onSave">保存修改</el-button>
    </div>
    <div class="code-preview-page">
      <div class="left-chat">
        <!-- <ChatCom /> -->
        <chat @send-message="handleSendMessage"></chat>
      </div>
      <div class="right-code">
        <div class="code-header">
          <div class="tab-btn-right" v-if="!activeEditTab">
            <el-switch
              v-model="activePreviewTab"
              size="large"
              active-text="Preview"
              inactive-text="Code"
            />
          </div>
          <div v-if="accessUrl" style="margin-left: 24px">
            <a :href="accessUrl" target="_blank"> 点击查看html版本效果 </a>
          </div>
          <div class="tab-btn-right">
            <el-button type="primary" @click="onEditModeChange">{{
              activeEditTab ? "退出编辑模式" : "进入编辑模式"
            }}</el-button>
          </div>
        </div>
        <div class="rightBtnBox" v-if="activeEditTab">
          <div v-if="activeEditTab" style="width: 100%; height: 100%">
            <SandpackProvider
              key="sandpackKey"
              template="react-ts"
              ref="sandpackRef"
              className="code-edit-page"
              :previewStyle="{ height: '100%' }"
              :editor-props="{ style: { height: '100%' } }"
              :preview-props="{ style: { height: '100%' } }"
              :showRefreshButton="true"
              :showLineNumbers="true"
              :files="{
                '/App.tsx': editCodeMessage,
                ...shadcnFiles,
              }"
              :customSetup="customSetup"
              :options="{
                externalResources: [
                  'https://unpkg.com/@tailwindcss/ui/dist/tailwind-ui.min.css',
                ],
                editorHeight: 650,
                editorWidth: 400,
                showLineNumbers: true,
              }"
              style="width: 100%; height: 100%; display: flex"
            >
              <CodeEditor
                style="width: 50%; height: 100%; border-right: 1px solid #ccc"
                :code="editCodeMessage"
                :onCodeUpdate="handleEditorChange"
              />
              <SandpackPreview
                :showNavigator="false"
                :showOpenInCodeSandbox="false"
                :showRefreshButton="false"
                :showRestartButton="false"
                :showOpenNewtab="false"
                class="h-full w-full"
                style="width: 50%; height: 100%; overflow: scroll"
              />
            </SandpackProvider>
          </div>
          <div
            v-if="activePreviewTab && codeMessage"
            class="preview-container"
            id="capture"
          >
            <SandpackProvider
              key="preView"
              template="react-ts"
              :files="{
                '/App.tsx': codeMessage,
                ...shadcnFiles,
              }"
              :customSetup="customSetup"
              :options="{
                externalResources: [
                  'https://unpkg.com/@tailwindcss/ui/dist/tailwind-ui.min.css',
                ],
              }"
              style="
                position: absolute;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
              "
            >
              <SandpackPreview
                :showNavigator="false"
                :showOpenInCodeSandbox="false"
                :showRefreshButton="false"
                :showRestartButton="false"
                :showOpenNewtab="false"
                class="h-full w-full"
                style="width: 100%; height: 100%"
              />
            </SandpackProvider>
          </div>
        </div>
        <div class="rightBtnBox" v-if="!activeEditTab">
          <div
            v-if="!activePreviewTab && codeMessage"
            style="width: 100%; height: 100%"
          >
            <SandpackProvider
              key="code"
              template="react-ts"
              :files="{
                '/App.tsx': codeMessage,
              }"
              :customSetup="customSetup"
            >
              <SandpackCodeEditor
                :showNavigator="false"
                :showOpenInCodeSandbox="false"
                :showRefreshButton="false"
                :showRestartButton="false"
                :showOpenNewtab="false"
                class="h-full w-full"
              />
            </SandpackProvider>
          </div>
          <div
            v-if="activePreviewTab && codeMessage"
            class="preview-container"
            id="capture"
          >
            <SandpackProvider
              key="preView"
              template="react-ts"
              :files="{
                '/App.tsx': codeMessage,
                ...shadcnFiles,
              }"
              :customSetup="customSetup"
              :options="{
                externalResources: [
                  'https://unpkg.com/@tailwindcss/ui/dist/tailwind-ui.min.css',
                ],
              }"
              style="
                position: absolute;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
              "
            >
              <SandpackPreview
                :showNavigator="false"
                :showOpenInCodeSandbox="false"
                :showRefreshButton="false"
                :showRestartButton="false"
                :showOpenNewtab="false"
                class="h-full w-full"
                style="width: 100%; height: 100%"
              />
            </SandpackProvider>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed, watch, provide, nextTick } from "vue";

import {
  Sandpack,
  SandpackProvider,
  SandpackCodeEditor,
  CodeEditor,
  SandpackPreview,
} from "sandpack-vue3";

import html2canvas from "html2canvas";

import dedent from "dedent";
// import ChatCom from "./components/chat/index.vue";
import RightMenu from "@/components/RightMenu.vue"; // 引入 RightMenu 组件
import chat from "./components/index.vue"; // 引入 RightMenu 组件
import {
  gameModule,
  gameModuleEdit,
  gameGerateByChat,
} from "@/api/modules/index";
import { ElLoading } from "element-plus";

import { useStore } from "vuex";
import { useRouter } from "vue-router";

const router = useRouter();

const store = useStore();

import * as shadcnComponents from "@/lib/shadcn.js";

const shadcnFiles = {
  "/lib/utils.ts": shadcnComponents.utils,
  "/components/ui/accordion.tsx": shadcnComponents.accordian,
  "/components/ui/alert-dialog.tsx": shadcnComponents.alertDialog,
  "/components/ui/alert.tsx": shadcnComponents.alert,
  "/components/ui/avatar.tsx": shadcnComponents.avatar,
  "/components/ui/badge.tsx": shadcnComponents.badge,
  "/components/ui/breadcrumb.tsx": shadcnComponents.breadcrumb,
  "/components/ui/button.tsx": shadcnComponents.button,
  "/components/ui/calendar.tsx": shadcnComponents.calendar,
  "/components/ui/card.tsx": shadcnComponents.card,
  "/components/ui/carousel.tsx": shadcnComponents.carousel,
  "/components/ui/checkbox.tsx": shadcnComponents.checkbox,
  "/components/ui/collapsible.tsx": shadcnComponents.collapsible,
  "/components/ui/dialog.tsx": shadcnComponents.dialog,
  "/components/ui/drawer.tsx": shadcnComponents.drawer,
  "/components/ui/dropdown-menu.tsx": shadcnComponents.dropdownMenu,
  "/components/ui/input.tsx": shadcnComponents.input,
  "/components/ui/label.tsx": shadcnComponents.label,
  "/components/ui/menubar.tsx": shadcnComponents.menuBar,
  "/components/ui/navigation-menu.tsx": shadcnComponents.navigationMenu,
  "/components/ui/pagination.tsx": shadcnComponents.pagination,
  "/components/ui/popover.tsx": shadcnComponents.popover,
  "/components/ui/progress.tsx": shadcnComponents.progress,
  "/components/ui/radio-group.tsx": shadcnComponents.radioGroup,
  "/components/ui/select.tsx": shadcnComponents.select,
  "/components/ui/separator.tsx": shadcnComponents.separator,
  "/components/ui/skeleton.tsx": shadcnComponents.skeleton,
  "/components/ui/slider.tsx": shadcnComponents.slider,
  "/components/ui/switch.tsx": shadcnComponents.switchComponent,
  "/components/ui/table.tsx": shadcnComponents.table,
  "/components/ui/tabs.tsx": shadcnComponents.tabs,
  "/components/ui/textarea.tsx": shadcnComponents.textarea,
  "/components/ui/toast.tsx": shadcnComponents.toast,
  "/components/ui/toaster.tsx": shadcnComponents.toaster,
  "/components/ui/toggle-group.tsx": shadcnComponents.toggleGroup,
  "/components/ui/toggle.tsx": shadcnComponents.toggle,
  "/components/ui/tooltip.tsx": shadcnComponents.tooltip,
  "/components/ui/use-toast.tsx": shadcnComponents.useToast,
  "/components/ui/index.tsx": `
  export * from "./button"
  export * from "./card"
  export * from "./input"
  export * from "./label"
  export * from "./select"
  export * from "./textarea"
  export * from "./avatar"
  export * from "./radio-group"
  `,
  "/public/index.html": dedent`
  <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Document</title>
      </head>
      <body>
        <div id="root">
        </div>
      </body>
      
    </html>`,
};

const selectPptItem = computed(() => store.getters.selectPptItem);
const gameIdList = computed(() => store.getters.selectPptItem.gameIdList || []);
const gameInfoList = computed(
  () => store.getters.selectPptItem.gameInfoList || []
);

const messageObj = ref({
  "/App.tsx":
    'import { useState } from \'react\';\nimport { motion } from \'framer-motion\';\n\nconst gameData1 = {\n  gameName: "Animal Rhymes Adventure",\n  backgroundImage: "http://api.gamecreator.online/data/upload/assets/image/d13dc0d3-d4b9-4e19-a5f1-5cffb9c074d5/0.jpg",\n  animals: [\n    { id: 1, name: "Bee", home: "Beehive" },\n    { id: 2, name: "Bat", home: "Cave" },\n    { id: 3, name: "Bird", home: "Nest" },\n    { id: 4, name: "Frog", home: "Pond" }\n  ],\n  questions: [\n    { id: 1, word: "cat", correctRhyme: "hat", wrongRhyme: "dog", animalId: 1 },\n    { id: 2, word: "log", correctRhyme: "frog", wrongRhyme: "tree", animalId: 1 },\n    { id: 3, word: "moon", correctRhyme: "spoon", wrongRhyme: "star", animalId: 2 },\n    { id: 4, word: "fall", correctRhyme: "ball", wrongRhyme: "jump", animalId: 2 },\n    { id: 5, word: "red", correctRhyme: "bed", wrongRhyme: "blue", animalId: 3 },\n    { id: 6, word: "light", correctRhyme: "kite", wrongRhyme: "dark", animalId: 3 },\n    { id: 7, word: "rain", correctRhyme: "train", wrongRhyme: "sun", animalId: 4 },\n    { id: 8, word: "boat", correctRhyme: "goat", wrongRhyme: "car", animalId: 4 }\n  ],\n  estimatedDuration: 300,\n  core_gameplay_summary: "Guide each animal to their home by answering questions and selecting correct rhyming words."\n};\n\nconst gameData2 = {\n  boardGameBackground: "http://api.gamecreator.online/data/upload/assets/image/d305d8e4-059b-44d0-bc42-23ce866535ef/0.jpg"\n};\n\n// Animal emoji mapping\nconst animalEmojis = {\n  Bee: \'🐝\',\n  Bat: \'🦇\',\n  Bird: \'🐦\',\n  Frog: \'🐸\'\n};\n\ntype GameLevel = \'level1\' | \'level2\' | \'end\';\n\nexport default function App() {\n  const [currentLevel, setCurrentLevel] = useState<GameLevel>(\'level1\');\n\n  return (\n    <div>\n      {currentLevel === \'level1\' && (\n        <AnimalRhymesGame onComplete={() => setCurrentLevel(\'level2\')} />\n      )}\n      {currentLevel === \'level2\' && (\n        <RhymingWordsGame onComplete={() => setCurrentLevel(\'end\')} />\n      )}\n      {currentLevel === \'end\' && (\n        <div className="flex justify-center items-center min-h-screen bg-gray-100">\n          <div className="bg-white p-8 rounded shadow">\n            <h1 className="text-3xl font-bold mb-4">Congratulations!</h1>\n            <p className="text-lg">You completed all levels!</p>\n            <button\n              onClick={() => setCurrentLevel(\'level1\')}\n              className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"\n            >\n              Restart Game\n            </button>\n          </div>\n        </div>\n      )}\n    </div>\n  );\n}\n\nfunction AnimalRhymesGame({ onComplete }: { onComplete: () => void }) {\n  const [currentScreen, setCurrentScreen] = useState(\'start\');\n  const [currentAnimalIndex, setCurrentAnimalIndex] = useState(0);\n  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);\n  const [score, setScore] = useState(0);\n  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);\n  const [completedAnimals, setCompletedAnimals] = useState<number[]>([]);\n\n  // Get the current animal\n  const currentAnimal = gameData1.animals[currentAnimalIndex];\n  // Get current animal\'s questions\n  const animalQuestions = gameData1.questions.filter(q => q.animalId === currentAnimal?.id);\n  const currentQuestion = animalQuestions[currentQuestionIndex];\n\n  // Start the game\n  const startGame = (animalIndex: number) => {\n    setCurrentAnimalIndex(animalIndex);\n    setCurrentQuestionIndex(0);\n    setCurrentScreen(\'game\');\n  };\n\n  // Check the answer\n  const checkAnswer = (answer: string) => {\n    setSelectedAnswer(answer);\n    const isCorrect = answer === currentQuestion.correctRhyme;\n    \n    if (isCorrect) {\n      setScore(score + 1);\n      \n      // Check if all questions for the current animal are complete\n      if (currentQuestionIndex === animalQuestions.length - 1) {\n        setCompletedAnimals([...completedAnimals, currentAnimal.id]);\n        \n        // Check if all animals are completed\n        if (completedAnimals.length === gameData1.animals.length - 1) {\n          setTimeout(() => {\n            setCurrentScreen(\'end\');\n            onComplete();\n          }, 1000);\n          return;\n        }\n      }\n    }\n    \n    setTimeout(() => {\n      setSelectedAnswer(null);\n      if (isCorrect) {\n        if (currentQuestionIndex < animalQuestions.length - 1) {\n          setCurrentQuestionIndex(currentQuestionIndex + 1);\n        } else {\n          setCurrentScreen(\'animal-select\');\n        }\n      }\n    }, 1000);\n  };\n\n  // Reset the game\n  const resetGame = () => {\n    setCurrentScreen(\'start\');\n    setCurrentAnimalIndex(0);\n    setCurrentQuestionIndex(0);\n    setScore(0);\n    setCompletedAnimals([]);\n    setSelectedAnswer(null);\n  };\n\n  // Render start screen\n  if (currentScreen === \'start\') {\n    return (\n      <div className="fixed inset-0 flex items-center justify-center bg-cover bg-center"\n          style={{ backgroundImage: `url(${gameData1.backgroundImage})` }}>\n        <div className="absolute inset-0 bg-black bg-opacity-50"></div>\n        <div className="relative z-10 text-center p-8 max-w-md w-full">\n          <h1 className="text-4xl font-bold text-white mb-6">{gameData1.gameName}</h1>\n          <p className="text-xl text-white mb-8">{gameData1.core_gameplay_summary}</p>\n          <button \n            onClick={() => setCurrentScreen(\'animal-select\')}\n            className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-6 rounded-full text-xl shadow-lg transition"\n          >\n            Start Game\n          </button>\n        </div>\n      </div>\n    );\n  }\n\n  // Render animal selection screen\n  if (currentScreen === \'animal-select\') {\n    return (\n      <div className="fixed inset-0 flex items-center justify-center bg-cover bg-center"\n          style={{ backgroundImage: `url(${gameData1.backgroundImage})` }}>\n        <div className="absolute inset-0 bg-black bg-opacity-50"></div>\n        <div className="relative z-10 text-center p-4 w-full max-w-2xl">\n          <h2 className="text-3xl font-bold text-white mb-8">Choose an Animal to Help</h2>\n          <div className="grid grid-cols-2 gap-4">\n            {gameData1.animals.map((animal, index) => (\n              <div \n                key={animal.id}\n                onClick={() => startGame(index)}\n                className={`p-6 rounded-xl backdrop-blur-sm bg-white/10 border-2 ${completedAnimals.includes(animal.id) ? \'border-green-500\' : \'border-white/30\'} flex flex-col items-center justify-center cursor-pointer hover:bg-white/20 transition`}\n              >\n                <span className="text-5xl mb-2">{animalEmojis[animal.name as keyof typeof animalEmojis]}</span>\n                <h3 className="text-xl font-bold text-white">{animal.name}</h3>\n                <p className="text-white/80">Home: {animal.home}</p>\n                {completedAnimals.includes(animal.id) && (\n                  <div className="mt-2 text-green-500 font-bold">Completed!</div>\n                )}\n              </div>\n            ))}\n          </div>\n          <div className="mt-8 text-white">\n            Score: {score} | Completed: {completedAnimals.length}/{gameData1.animals.length}\n          </div>\n        </div>\n      </div>\n    );\n  }\n\n  // Render game screen\n  if (currentScreen === \'game\' && currentAnimal && currentQuestion) {\n    return (\n      <div className="fixed inset-0 flex items-center justify-center bg-cover bg-center"\n          style={{ backgroundImage: `url(${gameData1.backgroundImage})` }}>\n        <div className="absolute inset-0 bg-black bg-opacity-50"></div>\n        <div className="relative z-10 text-center p-4 w-full max-w-md">\n          <div className="flex justify-between items-center mb-8">\n            <div className="text-4xl">\n              {animalEmojis[currentAnimal.name as keyof typeof animalEmojis]}\n            </div>\n            <div className="text-white">\n              Question {currentQuestionIndex + 1}/{animalQuestions.length}\n            </div>\n          </div>\n          \n          <div className="bg-white/90 rounded-xl p-6 mb-8 shadow-lg">\n            <h3 className="text-2xl font-bold mb-4">Which word rhymes with:</h3>\n            <div className="text-4xl font-bold text-blue-600 mb-6">{currentQuestion.word}</div>\n            \n            <div className="grid grid-cols-1 gap-3">\n              {[currentQuestion.correctRhyme, currentQuestion.wrongRhyme]\n                .sort(() => Math.random() - 0.5)\n                .map((option, i) => (\n                  <button\n                    key={i}\n                    onClick={() => !selectedAnswer && checkAnswer(option)}\n                    disabled={!!selectedAnswer}\n                    className={`py-4 px-6 rounded-lg text-xl font-bold transition-all ${\n                      !selectedAnswer \n                        ? \'bg-blue-500 hover:bg-blue-600 text-white\'\n                        : option === currentQuestion.correctRhyme\n                          ? \'bg-green-500 text-white\'\n                          : option === selectedAnswer\n                            ? \'bg-red-500 text-white\'\n                            : \'bg-gray-300 text-gray-700\'\n                    }`}\n                  >\n                    {option}\n                  </button>\n                ))}\n            </div>\n          </div>\n          \n          <div className="text-white text-lg">\n            Score: {score} | {currentAnimal.name}\'s Progress: {currentQuestionIndex + 1}/{animalQuestions.length}\n          </div>\n        </div>\n      </div>\n    );\n  }\n\n  // Render end screen\n  if (currentScreen === \'end\') {\n    return (\n      <div className="fixed inset-0 flex items-center justify-center bg-cover bg-center"\n          style={{ backgroundImage: `url(${gameData1.backgroundImage})` }}>\n        <div className="absolute inset-0 bg-black bg-opacity-50"></div>\n        <div className="relative z-10 text-center p-8 max-w-md w-full">\n          <h1 className="text-4xl font-bold text-white mb-6">Congratulations!</h1>\n          <p className="text-2xl text-white mb-8">You helped all animals find their homes!</p>\n          \n          <div className="bg-white/90 rounded-xl p-6 mb-8">\n            <h3 className="text-xl font-bold mb-4">Your Results:</h3>\n            <div className="text-3xl font-bold text-blue-600 mb-2">{score} Correct Answers</div>\n            <p className="text-gray-700">You completed all {gameData1.animals.length} animals!</p>\n          </div>\n          \n          <div className="flex justify-center gap-4">\n            <button \n              onClick={resetGame}\n              className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-6 rounded-full text-lg shadow-lg transition"\n            >\n              Play Again\n            </button>\n            <button \n              onClick={() => setCurrentScreen(\'animal-select\')}\n              className="bg-gray-500 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-full text-lg shadow-lg transition"\n            >\n              Animal Select\n            </button>\n          </div>\n          <button\n            onClick={onComplete}\n            className="bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-full text-lg mt-4 shadow-lg transition"\n          >\n            Next Level\n          </button>\n        </div>\n      </div>\n    );\n  }\n\n  return (\n    <div className="fixed inset-0 flex items-center justify-center bg-gray-100">\n      <div className="text-2xl">Loading game...</div>\n    </div>\n  );\n}\n\nfunction RhymingWordsGame({ onComplete }: { onComplete: () => void }) {\n  const [gameState, setGameState] = useState<\'start\' | \'roll_result\' | \'name_rhyme\' | \'check\'>(\'start\');\n  const [diceValue, setDiceValue] = useState<number | null>(null);\n  const [userRhymeWord, setUserRhymeWord] = useState<string>(\'\');\n\n  const handleDiceRoll = () => {\n    const result = Math.floor(Math.random() * 6) + 1;\n    setDiceValue(result);\n    setGameState(\'roll_result\');\n    console.log("Dice rolling... Sound effect!");\n  };\n\n  const handleNextState = () => {\n    if (gameState === \'roll_result\') {\n      setGameState(\'name_rhyme\');\n    } else if (gameState === \'check\') {\n      setGameState(\'start\');\n      setUserRhymeWord(\'\');\n      onComplete();\n    }\n  };\n\n  const handleRhymeCheck = () => {\n    if (userRhymeWord.length > 0) {\n      console.log("Victory sound effect!");\n      setGameState(\'check\');\n    }\n  };\n\n  return (\n    <div className="min-h-screen flex items-center justify-center bg-cover" style={{ backgroundImage: `url(${gameData2.boardGameBackground})` }}>\n      <div className="bg-white rounded-lg shadow-lg p-6 w-[320px] md:w-[400px]">\n        {gameState === \'start\' && (\n          <div className="text-center">\n            <h1 className="text-2xl font-bold mb-4">Rhyming Words Board Race</h1>\n            <button onClick={handleDiceRoll} className="bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-600 mt-4">\n              Roll Dice\n            </button>\n          </div>\n        )}\n        \n        {gameState === \'roll_result\' && diceValue && (\n          <div className="text-center">\n            <motion.div\n              animate={{ rotate: 360 }}\n              transition={{ duration: 1 }}\n              className="text-4xl font-bold mb-2"\n            >\n              🎲 {diceValue}\n            </motion.div>\n            <button onClick={handleNextState} className="bg-green-500 text-white font-bold py-2 px-4 rounded hover:bg-green-600 mt-4">\n              Next\n            </button>\n          </div>\n        )}\n\n        {gameState === \'name_rhyme\' && (\n          <div className="text-center">\n            <h2 className="text-xl font-bold mb-2">Provide a rhyming word</h2>\n            <input\n              type="text"\n              value={userRhymeWord}\n              onChange={(e) => setUserRhymeWord(e.target.value)}\n              className="border border-gray-300 p-2 rounded mb-4"\n            />\n            <button onClick={handleRhymeCheck} className="bg-yellow-500 text-white font-bold py-2 px-4 rounded hover:bg-yellow-600">\n              Submit\n            </button>\n          </div>\n        )}\n\n        {gameState === \'check\' && (\n          <div className="text-center">\n            <h2 className="text-xl font-bold mb-4">Correct! Move forward!</h2>\n            <button onClick={handleNextState} className="bg-purple-500 text-white font-bold py-2 px-4 rounded hover:bg-purple-600">\n              Continue\n            </button>\n          </div>\n        )}\n      </div>\n    </div>\n  );\n}\n',
});

const codeMessage = ref("");

const customSetup = ref({
  dependencies: {
    "lucide-react": "latest",
    recharts: "2.9.0",
    "react-router-dom": "latest",
    "@radix-ui/react-accordion": "^1.2.0",
    "@radix-ui/react-alert-dialog": "^1.1.1",
    "@radix-ui/react-aspect-ratio": "^1.1.0",
    "@radix-ui/react-avatar": "^1.1.0",
    "@radix-ui/react-checkbox": "^1.1.1",
    "@radix-ui/react-collapsible": "^1.1.0",
    "@radix-ui/react-dialog": "^1.1.1",
    "@radix-ui/react-dropdown-menu": "^2.1.1",
    "@radix-ui/react-hover-card": "^1.1.1",
    "@radix-ui/react-label": "^2.1.0",
    "@radix-ui/react-menubar": "^1.1.1",
    "@radix-ui/react-navigation-menu": "^1.2.0",
    "@radix-ui/react-popover": "^1.1.1",
    "@radix-ui/react-progress": "^1.1.0",
    "@radix-ui/react-radio-group": "^1.2.0",
    "@radix-ui/react-select": "^2.1.1",
    "@radix-ui/react-separator": "^1.1.0",
    "@radix-ui/react-slider": "^1.2.0",
    "@radix-ui/react-slot": "^1.1.0",
    "@radix-ui/react-switch": "^1.1.0",
    "@radix-ui/react-tabs": "^1.1.0",
    "@radix-ui/react-toast": "^1.2.1",
    "@radix-ui/react-toggle": "^1.1.0",
    "@radix-ui/react-toggle-group": "^1.1.0",
    "@radix-ui/react-tooltip": "^1.1.2",
    "class-variance-authority": "^0.7.0",
    clsx: "^2.1.1",
    "date-fns": "^3.6.0",
    "embla-carousel-react": "^8.1.8",
    "react-day-picker": "^8.10.1",
    "tailwind-merge": "^2.4.0",
    "tailwindcss-animate": "^1.0.7",
    "framer-motion": "^11.15.0",
    vaul: "^0.9.1",
  },
});

const activeEditTab = ref(false);
const onEditModeChange = () => {
  activeEditTab.value = !activeEditTab.value;
  if (activeEditTab.value) {
    editCodeMessage.value = codeMessage.value;
  }
};

// 来个粗略的防抖吧
let timer = null;
const editCodeMessage = ref("");
const handleEditorChange = (e) => {
  timer && clearTimeout(timer);
  timer = setTimeout(() => {
    editCodeMessage.value = e;
  }, 3000);
};

const chatMessages = ref([]);
provide("chatMessages", chatMessages);

const activePreviewTab = ref(false);
const getCodeStr = (codeId) => {
  const data = {
    id: codeId ? codeId : selectPptItem.value.gameId || 3,
    module_type: "code",
  };
  codeMessage.value = "";
  chatMessages.value = [];
  gameModule(data).then((res) => {
    messageObj.value = {
      "/App.tsx": res.result.code,
    };
    if (res.result.code) {
      codeMessage.value = res.result.code;
    }
  });
};
const accessUrl = ref("");
const stepValue = ref(selectPptItem.value.gameId);
watch(
  stepValue,
  (newValue) => {
    const currentGameItem =
      gameInfoList.value.find((item) => item.id === newValue) || {};
    accessUrl.value = currentGameItem.access_url;
    getCodeStr(newValue);
  },
  { immediate: true }
);
const onPrePage = () => {
  router.back();
};

const sandpackRef = ref(null);
const onSave = async () => {
  // 方法1：直接获取特定文件内容

  const loading = ElLoading.service({
    lock: true,
    text: "加载中...",
    background: "rgba(0, 0, 0, 0.7)",
  });
  let updateCodeStr = codeMessage.value;

  if (activeEditTab.value) {
    updateCodeStr = editCodeMessage.value;
  }

  try {
    gameModuleEdit(
      {
        id: stepValue.value,
        module_type: "code",
      },
      updateCodeStr
    ).then(() => {
      updateCode(updateCodeStr);
    });
  } finally {
    loading.close();
  }
};

onMounted(async () => {
  await getCodeStr();
});

const sendMessageToOrigin = async (contentArr) => {
  // const loading = ElLoading.service({
  //   lock: true,
  //   text: "加载中...",
  //   background: "rgba(0, 0, 0, 0.7)",
  // });
  chatMessages.value.push(
    {
      role: "user",
      type: "text",
      content: [{ type: "text", text: contentArr[0].content }],
    },
    {
      role: "assistant",
      type: "text",
      content: [{ type: "text", text: "正在生成代码，请稍后..." }],
    }
  );
  try {
    sendLoading.value = true;
    const res = await gameGerateByChat({
      game_id: stepValue.value,
      content: contentArr,
    });
    chatMessages.value.splice(-1, 2, {
      role: "assistant",
      type: "text",
      content: [{ type: "text", text: "代码生成成功，请查看..." }],
    });
    updateCode(res.result.code);
    if (res.code !== 200) {
      ElMessage.error("代码生成失败，请重试，详细错误请打开控制台查看");
      console.log(JSON.stringify(res.data));
    }
  } catch (error) {
    chatMessages.value.splice(-1, 2, {
      role: "assistant",
      type: "text",
      content: [{ type: "text", text: "生成失败，请重新提问..." }],
    });
    console.log(error);
  } finally {
    sendLoading.value = false;
    // loading.close();
  }
};

const sendLoading = ref(false);
const handleSendMessage = async (message) => {
  if (activePreviewTab.value) {
    const element = document.getElementById("capture");

    html2canvas(element).then((canvas) => {
      const imageUrl = canvas.toDataURL("image/png");
      const contentArr = [
        {
          feedback_type: "user_ask",
          content: message,
        },
        {
          feedback_type: "screenshot",
          content: imageUrl,
        },
      ];
      sendMessageToOrigin(contentArr);
    });
  } else {
    sendMessageToOrigin([
      {
        feedback_type: "user_ask",
        content: message,
      },
    ]);
  }
};

const updateCode = async (askStr) => {
  if (askStr) {
    codeMessage.value = askStr;
  }
};
provide("sendLoading", sendLoading);
</script>

<style lang="scss" scoped>
@import "./index.scss";
</style>
