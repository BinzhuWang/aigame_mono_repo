<template>
  <div v-if="true">
    <div class="flex-div">
      <div class="left-div">
        <SandpackProvider>
          <Sandpack
            template="react-ts"
            :files="messageObj"
            :customSetup="customSetup"
          />
          <!-- <SandpackPreview
            showNavigator="{false}"
            showOpenInCodeSandbox="{false}"
            showRefreshButton="{false}"
            showRestartButton="{false}"
            showOpenNewtab="{false}"
            className="h-full w-full"
          /> -->
        </SandpackProvider>
      </div>
    </div>
  </div>
  <div v-else>
    <el-row class="data-lists">
      <el-col :span="9" :class="{ shake: disabled }"
        ><div class="data-item-one flx-row">
          <div class="item-left">
            <img src="../../assets/home.png" alt="" srcset="" />
          </div>
          <div class="item-right">
            <div class="item-right-top">
              <div class="tit">本期活动GMX</div>
              <div class="num">1523.53w</div>
            </div>
            <div class="line"></div>
            <div class="item-right-bottom flx-row">
              <div class="item">
                <div class="tit">类目一</div>
                <div class="num">53w</div>
              </div>
              <div class="item">
                <div class="tit">类目一</div>
                <div class="num">53w</div>
              </div>
              <div class="item">
                <div class="tit">类目一</div>
                <div class="num">53w</div>
              </div>
            </div>
          </div>
        </div></el-col
      >
      <el-col :span="9" :class="{ shake: disabled }"
        ><div class="data-item-two">
          <div class="item">
            <div class="item-des flx-row">
              <img src="../../assets/icon1.png" alt="" />
              <div class="right">
                <div class="num">934.7w <span>29.74</span></div>
                <div class="txt">今日DAU</div>
              </div>
            </div>
          </div>
          <div class="item">
            <div class="item-des flx-row" style="margin-right: 0px">
              <img src="../../assets/icon2.png" alt="" />
              <div class="right">
                <div class="num">264.7w <span>29.74</span></div>
                <div class="txt">今日DAU</div>
              </div>
            </div>
          </div>
          <div class="item">
            <div class="item-des flx-row">
              <div class="right border-right-1px">
                <div class="num">24.93w</div>
                <div class="txt">今日DAU</div>
              </div>
              <div class="right">
                <div class="num">984.52w</div>
                <div class="txt">总用户数</div>
              </div>
            </div>
          </div>
          <div class="item">
            <div class="item-des flx-row" style="margin-right: 0px">
              <div class="right border-right-1px">
                <div class="num">84.52w</div>
                <div class="txt">GPS</div>
              </div>
              <div class="right">
                <div class="num">84.52w</div>
                <div class="txt">特权</div>
              </div>
            </div>
          </div>
        </div></el-col
      >
      <el-col :span="6" :class="{ shakeRight: disabled }">
        <div class="data-item-three">
          <div class="tit">待处理</div>
          <div class="content">
            <div class="item">
              <div class="item-data">
                <div class="tit">退款申请</div>
                <div class="num">89 <span>条</span></div>
                <el-icon class="icon"><ArrowRight /></el-icon>
              </div>
            </div>
            <div class="item">
              <div class="item-data">
                <div class="tit">退款申请</div>
                <div class="num">89 <span>条</span></div>
                <el-icon class="icon"><ArrowRight /></el-icon>
              </div>
            </div>
            <div class="item">
              <div class="item-data">
                <div class="tit">退款申请</div>
                <div class="num">89 <span>条</span></div>
                <el-icon class="icon"><ArrowRight /></el-icon>
              </div>
            </div>
            <div class="item">
              <div class="item-data">
                <div class="tit">退款申请</div>
                <div class="num">89 <span>条</span></div>
                <el-icon class="icon"><ArrowRight /></el-icon>
              </div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
    <el-row class="dataLayer">
      <el-col :span="18">
        <div class="flx-row">
          <div class="datalayer-echarts" :class="{ shake: disabled }">
            <GMVnearly></GMVnearly>
          </div>
          <div class="datalayer-echarts" :class="{ shake: disabled }">
            <linenearly></linenearly>
          </div>
        </div>
        <div class="table-data" :class="{ shake: disabled }">
          <div class="tit">主题页列表</div>
          <div class="table-box">
            <el-table
              :data="tableData"
              :header-cell-style="{
                background: '#FAFBFDFF',
                fontWeight: '400',
                fontSize: '14px',
                padding: '0',
                fontHeight: '36px',
                height: '36px',
              }"
              :row-style="{
                fontWeight: '400',
                fontSize: '14px',
                padding: '0',
                fontHeight: '44px',
                height: '44px',
              }"
            >
              <el-table-column
                v-for="item in options"
                :key="item.type"
                :prop="item.props"
                :label="item.label"
                :width="item.width"
                :align="item.align"
                show-overflow-tooltip
                :fixed="item.fixed"
              >
                <template v-slot:default="scope" v-if="item.props === 'type'">
                  <span class="type" v-if="scope.row[item.props] == true"
                    >外部链接</span
                  >
                  <span
                    class="type error-type"
                    v-if="scope.row[item.props] == false"
                    >内部链接</span
                  >
                </template>
                <template v-slot:default="scope" v-if="item.props === 'state'">
                  <span v-if="scope.row[item.props] == true">
                    <i class="state"></i>已上线</span
                  >
                  <span v-if="scope.row[item.props] == false">
                    <i class="state error-state"></i>已下线</span
                  >
                </template>
                <template
                  v-slot:default="scope"
                  v-if="item.props === 'actions'"
                >
                  <el-icon class="icon-edit" @click="editorClick(scope.row)"
                    ><Edit
                  /></el-icon>
                  <el-popconfirm
                    confirm-button-text="确认"
                    cancel-button-text="取消"
                    :icon="InfoFilled"
                    icon-color="#626AEF"
                    title="确认删除该主题?"
                    @confirm="DeleteItem(index)"
                  >
                    <template #reference>
                      <el-icon class="icon-dele"><Delete /></el-icon>
                    </template>
                  </el-popconfirm>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="data-item-three" :class="{ shakeRight: disabled }">
          <div class="tit">常用功能</div>
          <div class="content">
            <div class="item">
              <div class="item-data flx-row">
                <div class="tit">
                  <el-icon><Histogram /></el-icon>订单列表
                </div>
                <el-icon class="icon"><ArrowRight /></el-icon>
              </div>
            </div>
            <div class="item">
              <div class="item-data flx-row">
                <div class="tit">
                  <el-icon><Avatar /></el-icon>用户列表
                </div>
                <el-icon class="icon"><ArrowRight /></el-icon>
              </div>
            </div>
            <div class="item">
              <div class="item-data">
                <div class="tit">
                  <el-icon><HomeFilled /></el-icon>首页配置
                </div>
                <el-icon class="icon"><ArrowRight /></el-icon>
              </div>
            </div>
            <div class="item">
              <div class="item-data">
                <div class="tit">
                  <el-icon><PictureFilled /></el-icon>主题配置
                </div>
                <el-icon class="icon"><ArrowRight /></el-icon>
              </div>
            </div>
            <div class="item">
              <div class="item-data">
                <div class="tit">
                  <el-icon><Menu /></el-icon>活动管理
                </div>
                <el-icon class="icon"><ArrowRight /></el-icon>
              </div>
            </div>
            <div class="item">
              <div class="item-data">
                <div class="tit">
                  <el-icon><Tools /></el-icon>退款申请
                </div>
                <el-icon class="icon"><ArrowRight /></el-icon>
              </div>
            </div>
          </div>
        </div>
        <div class="notice">
          <div class="notice-news">
            <img src="../../assets/homebg.jpeg" alt="" />
            <div class="txt one-cut-txt">
              查看更多查看更多查看更多查看更查看更多查看更多查看更多查看更
            </div>
          </div>
        </div>
        <div class="data-item-three" :class="{ shakeRight: disabled }">
          <div class="tit">公告栏</div>
          <div class="notice-lists">
            <div
              class="item one-cut-txt"
              v-for="item in notList"
              :key="item.id"
            >
              <span class="type">通知</span> {{ item.text }}
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import GMVnearly from "./components/GMVnearly.vue";
import linenearly from "./components/linenearly.vue";
import { options } from "./options.js";
import { homeList, noticeLists } from "../../api/modules/index.js";
import Sandpacks, {
  Sandpack,
  SandpackProvider,
  ErrorOverlay,
  SandpackCodeViewer,
  SandpackCodeEditor,
} from "sandpack-vue3";
// e.component("Sandpack", Fr), e.component("SandpackLayout", Bt), e.component("SandpackProvider", Lt), e.component("ErrorOverlay", Xe2), e.component("LoadingOverlay", Ze), e.component("CodeEditor", Ee), e.component("SandpackCodeEditor", zt), e.component("SandpackCodeViewer", Jt2),

console.log(Sandpacks, "Sandpacks======");
const messageObj = ref({
  "/App.tsx":
    'import { useState } from \'react\';\nimport { motion } from \'framer-motion\';\n\nconst gameData1 = {\n  gameName: "Animal Rhymes Adventure",\n  backgroundImage: "http://api.gamecreator.online/data/upload/assets/image/d13dc0d3-d4b9-4e19-a5f1-5cffb9c074d5/0.jpg",\n  animals: [\n    { id: 1, name: "Bee", home: "Beehive" },\n    { id: 2, name: "Bat", home: "Cave" },\n    { id: 3, name: "Bird", home: "Nest" },\n    { id: 4, name: "Frog", home: "Pond" }\n  ],\n  questions: [\n    { id: 1, word: "cat", correctRhyme: "hat", wrongRhyme: "dog", animalId: 1 },\n    { id: 2, word: "log", correctRhyme: "frog", wrongRhyme: "tree", animalId: 1 },\n    { id: 3, word: "moon", correctRhyme: "spoon", wrongRhyme: "star", animalId: 2 },\n    { id: 4, word: "fall", correctRhyme: "ball", wrongRhyme: "jump", animalId: 2 },\n    { id: 5, word: "red", correctRhyme: "bed", wrongRhyme: "blue", animalId: 3 },\n    { id: 6, word: "light", correctRhyme: "kite", wrongRhyme: "dark", animalId: 3 },\n    { id: 7, word: "rain", correctRhyme: "train", wrongRhyme: "sun", animalId: 4 },\n    { id: 8, word: "boat", correctRhyme: "goat", wrongRhyme: "car", animalId: 4 }\n  ],\n  estimatedDuration: 300,\n  core_gameplay_summary: "Guide each animal to their home by answering questions and selecting correct rhyming words."\n};\n\nconst gameData2 = {\n  boardGameBackground: "http://api.gamecreator.online/data/upload/assets/image/d305d8e4-059b-44d0-bc42-23ce866535ef/0.jpg"\n};\n\n// Animal emoji mapping\nconst animalEmojis = {\n  Bee: \'🐝\',\n  Bat: \'🦇\',\n  Bird: \'🐦\',\n  Frog: \'🐸\'\n};\n\ntype GameLevel = \'level1\' | \'level2\' | \'end\';\n\nexport default function App() {\n  const [currentLevel, setCurrentLevel] = useState<GameLevel>(\'level1\');\n\n  return (\n    <div>\n      {currentLevel === \'level1\' && (\n        <AnimalRhymesGame onComplete={() => setCurrentLevel(\'level2\')} />\n      )}\n      {currentLevel === \'level2\' && (\n        <RhymingWordsGame onComplete={() => setCurrentLevel(\'end\')} />\n      )}\n      {currentLevel === \'end\' && (\n        <div className="flex justify-center items-center min-h-screen bg-gray-100">\n          <div className="bg-white p-8 rounded shadow">\n            <h1 className="text-3xl font-bold mb-4">Congratulations!</h1>\n            <p className="text-lg">You completed all levels!</p>\n            <button\n              onClick={() => setCurrentLevel(\'level1\')}\n              className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"\n            >\n              Restart Game\n            </button>\n          </div>\n        </div>\n      )}\n    </div>\n  );\n}\n\nfunction AnimalRhymesGame({ onComplete }: { onComplete: () => void }) {\n  const [currentScreen, setCurrentScreen] = useState(\'start\');\n  const [currentAnimalIndex, setCurrentAnimalIndex] = useState(0);\n  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);\n  const [score, setScore] = useState(0);\n  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);\n  const [completedAnimals, setCompletedAnimals] = useState<number[]>([]);\n\n  // Get the current animal\n  const currentAnimal = gameData1.animals[currentAnimalIndex];\n  // Get current animal\'s questions\n  const animalQuestions = gameData1.questions.filter(q => q.animalId === currentAnimal?.id);\n  const currentQuestion = animalQuestions[currentQuestionIndex];\n\n  // Start the game\n  const startGame = (animalIndex: number) => {\n    setCurrentAnimalIndex(animalIndex);\n    setCurrentQuestionIndex(0);\n    setCurrentScreen(\'game\');\n  };\n\n  // Check the answer\n  const checkAnswer = (answer: string) => {\n    setSelectedAnswer(answer);\n    const isCorrect = answer === currentQuestion.correctRhyme;\n    \n    if (isCorrect) {\n      setScore(score + 1);\n      \n      // Check if all questions for the current animal are complete\n      if (currentQuestionIndex === animalQuestions.length - 1) {\n        setCompletedAnimals([...completedAnimals, currentAnimal.id]);\n        \n        // Check if all animals are completed\n        if (completedAnimals.length === gameData1.animals.length - 1) {\n          setTimeout(() => {\n            setCurrentScreen(\'end\');\n            onComplete();\n          }, 1000);\n          return;\n        }\n      }\n    }\n    \n    setTimeout(() => {\n      setSelectedAnswer(null);\n      if (isCorrect) {\n        if (currentQuestionIndex < animalQuestions.length - 1) {\n          setCurrentQuestionIndex(currentQuestionIndex + 1);\n        } else {\n          setCurrentScreen(\'animal-select\');\n        }\n      }\n    }, 1000);\n  };\n\n  // Reset the game\n  const resetGame = () => {\n    setCurrentScreen(\'start\');\n    setCurrentAnimalIndex(0);\n    setCurrentQuestionIndex(0);\n    setScore(0);\n    setCompletedAnimals([]);\n    setSelectedAnswer(null);\n  };\n\n  // Render start screen\n  if (currentScreen === \'start\') {\n    return (\n      <div className="fixed inset-0 flex items-center justify-center bg-cover bg-center"\n          style={{ backgroundImage: `url(${gameData1.backgroundImage})` }}>\n        <div className="absolute inset-0 bg-black bg-opacity-50"></div>\n        <div className="relative z-10 text-center p-8 max-w-md w-full">\n          <h1 className="text-4xl font-bold text-white mb-6">{gameData1.gameName}</h1>\n          <p className="text-xl text-white mb-8">{gameData1.core_gameplay_summary}</p>\n          <button \n            onClick={() => setCurrentScreen(\'animal-select\')}\n            className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-6 rounded-full text-xl shadow-lg transition"\n          >\n            Start Game\n          </button>\n        </div>\n      </div>\n    );\n  }\n\n  // Render animal selection screen\n  if (currentScreen === \'animal-select\') {\n    return (\n      <div className="fixed inset-0 flex items-center justify-center bg-cover bg-center"\n          style={{ backgroundImage: `url(${gameData1.backgroundImage})` }}>\n        <div className="absolute inset-0 bg-black bg-opacity-50"></div>\n        <div className="relative z-10 text-center p-4 w-full max-w-2xl">\n          <h2 className="text-3xl font-bold text-white mb-8">Choose an Animal to Help</h2>\n          <div className="grid grid-cols-2 gap-4">\n            {gameData1.animals.map((animal, index) => (\n              <div \n                key={animal.id}\n                onClick={() => startGame(index)}\n                className={`p-6 rounded-xl backdrop-blur-sm bg-white/10 border-2 ${completedAnimals.includes(animal.id) ? \'border-green-500\' : \'border-white/30\'} flex flex-col items-center justify-center cursor-pointer hover:bg-white/20 transition`}\n              >\n                <span className="text-5xl mb-2">{animalEmojis[animal.name as keyof typeof animalEmojis]}</span>\n                <h3 className="text-xl font-bold text-white">{animal.name}</h3>\n                <p className="text-white/80">Home: {animal.home}</p>\n                {completedAnimals.includes(animal.id) && (\n                  <div className="mt-2 text-green-500 font-bold">Completed!</div>\n                )}\n              </div>\n            ))}\n          </div>\n          <div className="mt-8 text-white">\n            Score: {score} | Completed: {completedAnimals.length}/{gameData1.animals.length}\n          </div>\n        </div>\n      </div>\n    );\n  }\n\n  // Render game screen\n  if (currentScreen === \'game\' && currentAnimal && currentQuestion) {\n    return (\n      <div className="fixed inset-0 flex items-center justify-center bg-cover bg-center"\n          style={{ backgroundImage: `url(${gameData1.backgroundImage})` }}>\n        <div className="absolute inset-0 bg-black bg-opacity-50"></div>\n        <div className="relative z-10 text-center p-4 w-full max-w-md">\n          <div className="flex justify-between items-center mb-8">\n            <div className="text-4xl">\n              {animalEmojis[currentAnimal.name as keyof typeof animalEmojis]}\n            </div>\n            <div className="text-white">\n              Question {currentQuestionIndex + 1}/{animalQuestions.length}\n            </div>\n          </div>\n          \n          <div className="bg-white/90 rounded-xl p-6 mb-8 shadow-lg">\n            <h3 className="text-2xl font-bold mb-4">Which word rhymes with:</h3>\n            <div className="text-4xl font-bold text-blue-600 mb-6">{currentQuestion.word}</div>\n            \n            <div className="grid grid-cols-1 gap-3">\n              {[currentQuestion.correctRhyme, currentQuestion.wrongRhyme]\n                .sort(() => Math.random() - 0.5)\n                .map((option, i) => (\n                  <button\n                    key={i}\n                    onClick={() => !selectedAnswer && checkAnswer(option)}\n                    disabled={!!selectedAnswer}\n                    className={`py-4 px-6 rounded-lg text-xl font-bold transition-all ${\n                      !selectedAnswer \n                        ? \'bg-blue-500 hover:bg-blue-600 text-white\'\n                        : option === currentQuestion.correctRhyme\n                          ? \'bg-green-500 text-white\'\n                          : option === selectedAnswer\n                            ? \'bg-red-500 text-white\'\n                            : \'bg-gray-300 text-gray-700\'\n                    }`}\n                  >\n                    {option}\n                  </button>\n                ))}\n            </div>\n          </div>\n          \n          <div className="text-white text-lg">\n            Score: {score} | {currentAnimal.name}\'s Progress: {currentQuestionIndex + 1}/{animalQuestions.length}\n          </div>\n        </div>\n      </div>\n    );\n  }\n\n  // Render end screen\n  if (currentScreen === \'end\') {\n    return (\n      <div className="fixed inset-0 flex items-center justify-center bg-cover bg-center"\n          style={{ backgroundImage: `url(${gameData1.backgroundImage})` }}>\n        <div className="absolute inset-0 bg-black bg-opacity-50"></div>\n        <div className="relative z-10 text-center p-8 max-w-md w-full">\n          <h1 className="text-4xl font-bold text-white mb-6">Congratulations!</h1>\n          <p className="text-2xl text-white mb-8">You helped all animals find their homes!</p>\n          \n          <div className="bg-white/90 rounded-xl p-6 mb-8">\n            <h3 className="text-xl font-bold mb-4">Your Results:</h3>\n            <div className="text-3xl font-bold text-blue-600 mb-2">{score} Correct Answers</div>\n            <p className="text-gray-700">You completed all {gameData1.animals.length} animals!</p>\n          </div>\n          \n          <div className="flex justify-center gap-4">\n            <button \n              onClick={resetGame}\n              className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-6 rounded-full text-lg shadow-lg transition"\n            >\n              Play Again\n            </button>\n            <button \n              onClick={() => setCurrentScreen(\'animal-select\')}\n              className="bg-gray-500 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-full text-lg shadow-lg transition"\n            >\n              Animal Select\n            </button>\n          </div>\n          <button\n            onClick={onComplete}\n            className="bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-full text-lg mt-4 shadow-lg transition"\n          >\n            Next Level\n          </button>\n        </div>\n      </div>\n    );\n  }\n\n  return (\n    <div className="fixed inset-0 flex items-center justify-center bg-gray-100">\n      <div className="text-2xl">Loading game...</div>\n    </div>\n  );\n}\n\nfunction RhymingWordsGame({ onComplete }: { onComplete: () => void }) {\n  const [gameState, setGameState] = useState<\'start\' | \'roll_result\' | \'name_rhyme\' | \'check\'>(\'start\');\n  const [diceValue, setDiceValue] = useState<number | null>(null);\n  const [userRhymeWord, setUserRhymeWord] = useState<string>(\'\');\n\n  const handleDiceRoll = () => {\n    const result = Math.floor(Math.random() * 6) + 1;\n    setDiceValue(result);\n    setGameState(\'roll_result\');\n    console.log("Dice rolling... Sound effect!");\n  };\n\n  const handleNextState = () => {\n    if (gameState === \'roll_result\') {\n      setGameState(\'name_rhyme\');\n    } else if (gameState === \'check\') {\n      setGameState(\'start\');\n      setUserRhymeWord(\'\');\n      onComplete();\n    }\n  };\n\n  const handleRhymeCheck = () => {\n    if (userRhymeWord.length > 0) {\n      console.log("Victory sound effect!");\n      setGameState(\'check\');\n    }\n  };\n\n  return (\n    <div className="min-h-screen flex items-center justify-center bg-cover" style={{ backgroundImage: `url(${gameData2.boardGameBackground})` }}>\n      <div className="bg-white rounded-lg shadow-lg p-6 w-[320px] md:w-[400px]">\n        {gameState === \'start\' && (\n          <div className="text-center">\n            <h1 className="text-2xl font-bold mb-4">Rhyming Words Board Race</h1>\n            <button onClick={handleDiceRoll} className="bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-600 mt-4">\n              Roll Dice\n            </button>\n          </div>\n        )}\n        \n        {gameState === \'roll_result\' && diceValue && (\n          <div className="text-center">\n            <motion.div\n              animate={{ rotate: 360 }}\n              transition={{ duration: 1 }}\n              className="text-4xl font-bold mb-2"\n            >\n              🎲 {diceValue}\n            </motion.div>\n            <button onClick={handleNextState} className="bg-green-500 text-white font-bold py-2 px-4 rounded hover:bg-green-600 mt-4">\n              Next\n            </button>\n          </div>\n        )}\n\n        {gameState === \'name_rhyme\' && (\n          <div className="text-center">\n            <h2 className="text-xl font-bold mb-2">Provide a rhyming word</h2>\n            <input\n              type="text"\n              value={userRhymeWord}\n              onChange={(e) => setUserRhymeWord(e.target.value)}\n              className="border border-gray-300 p-2 rounded mb-4"\n            />\n            <button onClick={handleRhymeCheck} className="bg-yellow-500 text-white font-bold py-2 px-4 rounded hover:bg-yellow-600">\n              Submit\n            </button>\n          </div>\n        )}\n\n        {gameState === \'check\' && (\n          <div className="text-center">\n            <h2 className="text-xl font-bold mb-4">Correct! Move forward!</h2>\n            <button onClick={handleNextState} className="bg-purple-500 text-white font-bold py-2 px-4 rounded hover:bg-purple-600">\n              Continue\n            </button>\n          </div>\n        )}\n      </div>\n    </div>\n  );\n}\n',
});

const customSetup = ref({
  dependencies: {
    "framer-motion": "^11.15.0",
  },
});

const tableData = ref([]);
const notList = ref([]);
const disabled = ref(false);

const DeleteItem = (index) => {
  tableData.value.splice(index, 1);
};

const initData = () => {
  homeList().then((res) => {
    tableData.value = res.data.data;
  });

  noticeLists().then((res) => {
    notList.value = res.data.data;
  });
};

onMounted(() => {
  initData();
  disabled.value = true;
  setTimeout(() => {
    disabled.value = false;
  }, 1500);
});
</script>

<style lang="scss" scoped>
@import "./index.scss";
</style>
