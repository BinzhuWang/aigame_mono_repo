shadcn_examples = {
    "mini game": {
        "prompt": "Generate a **fully functional educational memory matching game** that is **interactive, engaging, and suitable for children**. The game should be designed to help children improve their memory skills",
        "response": """
      ```tsx
      import { useState } from 'react';

      // 原始JSON数据
      const gameData = {
        gameName: "Animal Rhymes Adventure",
        backgroundImage: "http://api.gamecreator.online/data/upload/assets/image/d13dc0d3-d4b9-4e19-a5f1-5cffb9c074d5/0.jpg",
        animals: [
          { id: 1, name: "Bee", home: "Beehive" },
          { id: 2, name: "Bat", home: "Cave" },
          { id: 3, name: "Bird", home: "Nest" },
          { id: 4, name: "Frog", home: "Pond" }
        ],
        questions: [
          { id: 1, word: "cat", correctRhyme: "hat", wrongRhyme: "dog", animalId: 1 },
          { id: 2, word: "log", correctRhyme: "frog", wrongRhyme: "tree", animalId: 1 },
          { id: 3, word: "moon", correctRhyme: "spoon", wrongRhyme: "star", animalId: 2 },
          { id: 4, word: "fall", correctRhyme: "ball", wrongRhyme: "jump", animalId: 2 },
          { id: 5, word: "red", correctRhyme: "bed", wrongRhyme: "blue", animalId: 3 },
          { id: 6, word: "light", correctRhyme: "kite", wrongRhyme: "dark", animalId: 3 },
          { id: 7, word: "rain", correctRhyme: "train", wrongRhyme: "sun", animalId: 4 },
          { id: 8, word: "boat", correctRhyme: "goat", wrongRhyme: "car", animalId: 4 }
        ],
        estimatedDuration: 300,
        core_gameplay_summary: "Guide each animal to their home by answering questions and selecting correct rhyming words."
      };
      
      // 动物表情映射
      const animalEmojis = {
        Bee: '🐝',
        Bat: '🦇',
        Bird: '🐦',
        Frog: '🐸'
      };
      
      export default function AnimalRhymesGame() {
        const [currentScreen, setCurrentScreen] = useState('start');
        const [currentAnimalIndex, setCurrentAnimalIndex] = useState(0);
        const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
        const [score, setScore] = useState(0);
        const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
        const [completedAnimals, setCompletedAnimals] = useState<number[]>([]);
      
        // 获取当前动物
        const currentAnimal = gameData.animals[currentAnimalIndex];
        // 获取当前动物的问题
        const animalQuestions = gameData.questions.filter(q => q.animalId === currentAnimal?.id);
        const currentQuestion = animalQuestions[currentQuestionIndex];
      
        // 开始游戏
        const startGame = (animalIndex: number) => {
          setCurrentAnimalIndex(animalIndex);
          setCurrentQuestionIndex(0);
          setCurrentScreen('game');
        };
      
        // 检查答案
        const checkAnswer = (answer: string) => {
          setSelectedAnswer(answer);
          const isCorrect = answer === currentQuestion.correctRhyme;
          
          if (isCorrect) {
            setScore(score + 1);
            
            // 检查是否完成当前动物的所有问题
            if (currentQuestionIndex === animalQuestions.length - 1) {
              setCompletedAnimals([...completedAnimals, currentAnimal.id]);
              
              // 检查是否所有动物都已完成
              if (completedAnimals.length === gameData.animals.length - 1) {
                setTimeout(() => setCurrentScreen('end'), 1000);
                return;
              }
            }
          }
          
          setTimeout(() => {
            setSelectedAnswer(null);
            if (isCorrect) {
              if (currentQuestionIndex < animalQuestions.length - 1) {
                setCurrentQuestionIndex(currentQuestionIndex + 1);
              } else {
                setCurrentScreen('animal-select');
              }
            }
          }, 1000);
        };
      
        // 重置游戏
        const resetGame = () => {
          setCurrentScreen('start');
          setCurrentAnimalIndex(0);
          setCurrentQuestionIndex(0);
          setScore(0);
          setCompletedAnimals([]);
          setSelectedAnswer(null);
        };
      
        // 渲染开始屏幕
        if (currentScreen === 'start') {
          return (
            <div className="fixed inset-0 flex items-center justify-center bg-cover bg-center"
                 style={{ backgroundImage: `url(${gameData.backgroundImage})` }}>
              <div className="absolute inset-0 bg-black bg-opacity-50"></div>
              <div className="relative z-10 text-center p-8 max-w-md w-full">
                <h1 className="text-4xl font-bold text-white mb-6">{gameData.gameName}</h1>
                <p className="text-xl text-white mb-8">{gameData.core_gameplay_summary}</p>
                <button 
                  onClick={() => setCurrentScreen('animal-select')}
                  className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-6 rounded-full text-xl shadow-lg transition"
                >
                  Start Game
                </button>
              </div>
            </div>
          );
        }
      
        // 渲染动物选择屏幕
        if (currentScreen === 'animal-select') {
          return (
            <div className="fixed inset-0 flex items-center justify-center bg-cover bg-center"
                 style={{ backgroundImage: `url(${gameData.backgroundImage})` }}>
              <div className="absolute inset-0 bg-black bg-opacity-50"></div>
              <div className="relative z-10 text-center p-4 w-full max-w-2xl">
                <h2 className="text-3xl font-bold text-white mb-8">Choose an Animal to Help</h2>
                <div className="grid grid-cols-2 gap-4">
                  {gameData.animals.map((animal, index) => (
                    <div 
                      key={animal.id}
                      onClick={() => startGame(index)}
                      className={`p-6 rounded-xl backdrop-blur-sm bg-white/10 border-2 ${completedAnimals.includes(animal.id) ? 'border-green-500' : 'border-white/30'} flex flex-col items-center justify-center cursor-pointer hover:bg-white/20 transition`}
                    >
                      <span className="text-5xl mb-2">{animalEmojis[animal.name as keyof typeof animalEmojis]}</span>
                      <h3 className="text-xl font-bold text-white">{animal.name}</h3>
                      <p className="text-white/80">Home: {animal.home}</p>
                      {completedAnimals.includes(animal.id) && (
                        <div className="mt-2 text-green-500 font-bold">Completed!</div>
                      )}
                    </div>
                  ))}
                </div>
                <div className="mt-8 text-white">
                  Score: {score} | Completed: {completedAnimals.length}/{gameData.animals.length}
                </div>
              </div>
            </div>
          );
        }
      
        // 渲染游戏屏幕
        if (currentScreen === 'game' && currentAnimal && currentQuestion) {
          return (
            <div className="fixed inset-0 flex items-center justify-center bg-cover bg-center"
                 style={{ backgroundImage: `url(${gameData.backgroundImage})` }}>
              <div className="absolute inset-0 bg-black bg-opacity-50"></div>
              <div className="relative z-10 text-center p-4 w-full max-w-md">
                {/* 动物和进度指示器 */}
                <div className="flex justify-between items-center mb-8">
                  <div className="text-4xl">
                    {animalEmojis[currentAnimal.name as keyof typeof animalEmojis]}
                  </div>
                  <div className="text-white">
                    Question {currentQuestionIndex + 1}/{animalQuestions.length}
                  </div>
                </div>
                
                {/* 问题区域 */}
                <div className="bg-white/90 rounded-xl p-6 mb-8 shadow-lg">
                  <h3 className="text-2xl font-bold mb-4">Which word rhymes with:</h3>
                  <div className="text-4xl font-bold text-blue-600 mb-6">{currentQuestion.word}</div>
                  
                  {/* 答案选项 */}
                  <div className="grid grid-cols-1 gap-3">
                    {[currentQuestion.correctRhyme, currentQuestion.wrongRhyme]
                      .sort(() => Math.random() - 0.5) // 随机排序选项
                      .map((option, i) => (
                        <button
                          key={i}
                          onClick={() => !selectedAnswer && checkAnswer(option)}
                          disabled={!!selectedAnswer}
                          className={`py-4 px-6 rounded-lg text-xl font-bold transition-all ${
                            !selectedAnswer 
                              ? 'bg-blue-500 hover:bg-blue-600 text-white'
                              : option === currentQuestion.correctRhyme
                                ? 'bg-green-500 text-white'
                                : option === selectedAnswer
                                  ? 'bg-red-500 text-white'
                                  : 'bg-gray-300 text-gray-700'
                          }`}
                        >
                          {option}
                        </button>
                      ))}
                  </div>
                </div>
                
                {/* 分数显示 */}
                <div className="text-white text-lg">
                  Score: {score} | {currentAnimal.name}'s Progress: {currentQuestionIndex + 1}/{animalQuestions.length}
                </div>
              </div>
            </div>
          );
        }
      
        // 渲染结束屏幕
        if (currentScreen === 'end') {
          return (
            <div className="fixed inset-0 flex items-center justify-center bg-cover bg-center"
                 style={{ backgroundImage: `url(${gameData.backgroundImage})` }}>
              <div className="absolute inset-0 bg-black bg-opacity-50"></div>
              <div className="relative z-10 text-center p-8 max-w-md w-full">
                <h1 className="text-4xl font-bold text-white mb-6">Congratulations!</h1>
                <p className="text-2xl text-white mb-8">You helped all animals find their homes!</p>
                
                <div className="bg-white/90 rounded-xl p-6 mb-8">
                  <h3 className="text-xl font-bold mb-4">Your Results:</h3>
                  <div className="text-3xl font-bold text-blue-600 mb-2">{score} Correct Answers</div>
                  <p className="text-gray-700">You completed all {gameData.animals.length} animals!</p>
                </div>
                
                <div className="flex justify-center gap-4">
                  <button 
                    onClick={resetGame}
                    className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-6 rounded-full text-lg shadow-lg transition"
                  >
                    Play Again
                  </button>
                  <button 
                    onClick={() => setCurrentScreen('animal-select')}
                    className="bg-gray-500 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-full text-lg shadow-lg transition"
                  >
                    Animal Select
                  </button>
                </div>
              </div>
            </div>
          );
        }
      
        // 默认返回加载状态
        return (
          <div className="fixed inset-0 flex items-center justify-center bg-gray-100">
            <div className="text-2xl">Loading game...</div>
          </div>
        );
      }
      ```
 children     """,
    },
    "landing page": {
        "prompt": "Build a landing page for a healthcare company",
        "response": """
        ```tsx
                import React from 'react';
            import { Button } from "/components/ui/button"
            import { Card, CardContent } from "/components/ui/card"
            import { Heart, Shield, Clock, Users } from "lucide-react"

            export default function HealthcareLandingPage() {
          return (
        <div className="flex flex-col min-h-screen">
          <header className="px-4 lg:px-6 h-14 flex items-center">
            <a className="flex items-center justify-center" href="#">
              <Heart className="h-6 w-6 text-primary" />
                  <span className="sr-only">HealthCare Co.</span>
            </a>
            <nav className="ml-auto flex gap-4 sm:gap-6">
              <a className="text-sm font-medium hover:underline underline-offset-4" href="#">
                Services
                  </a>
              <a className="text-sm font-medium hover:underline underline-offset-4" href="#">
                About
                  </a>
              <a className="text-sm font-medium hover:underline underline-offset-4" href="#">
                Contact
                  </a>
            </nav>
          </header>
          <main className="flex-1">
            <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48">
              <div className="container px-4 md:px-6">
                <div className="flex flex-col items-center space-y-4 text-center">
                  <div className="space-y-2">
                    <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
                      Your Health, Our Priority
                        </h1>
                        <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl dark:text-gray-400">
                          Providing compassionate care and cutting-edge medical solutions to improve your quality of life.
                            </p>
                      </div>
                      <div className="space-x-4">
                        <Button>Book Appointment</Button>
                        <Button variant="outline">Learn More</Button>
                      </div>
                    </div>
                  </div>
                </section>
                <section className="w-full py-12 md:py-24 lg:py-32 bg-gray-100 dark:bg-gray-800">
                  <div className="container px-4 md:px-6">
                    <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl text-center mb-8">Our Services</h2>
                    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
                      <Card>
                        <CardContent className="p-6 flex flex-col items-center text-center space-y-2">
                          <Shield className="h-12 w-12 text-primary" />
                              <h3 className="text-xl font-bold">Preventive Care</h3>
                          <p className="text-gray-500 dark:text-gray-400">Regular check-ups and screenings to keep you healthy.</p>
                        </CardContent>
                      </Card>
                      <Card>
                        <CardContent className="p-6 flex flex-col items-center text-center space-y-2">
                          <Users className="h-12 w-12 text-primary" />
                              <h3 className="text-xl font-bold">Family Medicine</h3>
                          <p className="text-gray-500 dark:text-gray-400">Comprehensive care for patients of all ages.</p>
                        </CardContent>
                      </Card>
                      <Card>
                        <CardContent className="p-6 flex flex-col items-center text-center space-y-2">
                          <Clock className="h-12 w-12 text-primary" />
                              <h3 className="text-xl font-bold">24/7 Emergency</h3>
                          <p className="text-gray-500 dark:text-gray-400">Round-the-clock care for urgent medical needs.</p>
                        </CardContent>
                      </Card>
                      <Card>
                        <CardContent className="p-6 flex flex-col items-center text-center space-y-2">
                          <Heart className="h-12 w-12 text-primary" />
                              <h3 className="text-xl font-bold">Specialized Care</h3>
                          <p className="text-gray-500 dark:text-gray-400">Expert treatment for complex health conditions.</p>
                        </CardContent>
                      </Card>
                    </div>
                  </div>
                </section>
                <section className="w-full py-12 md:py-24 lg:py-32">
                  <div className="container px-4 md:px-6">
                    <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl text-center mb-8">What Our Patients Say</h2>
                    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                      {[1, 2, 3].map((i) => (
                    <Card key={i}>
                      <CardContent className="p-6 space-y-2">
                        <p className="text-gray-500 dark:text-gray-400">
                          "The care I received was exceptional. The staff was friendly and professional, and the doctors took the time to listen to my concerns."
                        </p>
                        <div className="flex items-center space-x-2">
                          <img
                                src="github.com/nutlope.png"
                                alt="Patient"
                                    className="rounded-full"
                                    width={40}
                                                                   height={40}
                                                                                                 />
                                  <div>
                            <p className="font-medium">Jane Doe</p>
                            <p className="text-sm text-gray-500 dark:text-gray-400">Patient</p>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                    </div>
                  </div>
                </section>
                <section className="w-full py-12 md:py-24 lg:py-32 bg-gray-100 dark:bg-gray-800">
                  <div className="container px-4 md:px-6">
                    <div className="flex flex-col items-center space-y-4 text-center">
                      <div className="space-y-2">
                        <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">Ready to Prioritize Your Health?</h2>
                        <p className="mx-auto max-w-[600px] text-gray-500 md:text-xl dark:text-gray-400">
                          Book an appointment today and take the first step towards a healthier you.
                            </p>
                      </div>
                      <Button size="lg">Book Appointment Now</Button>
                    </div>
                  </div>
                </section>
              </main>
              <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t">
                <p className="text-xs text-gray-500 dark:text-gray-400">© 2023 HealthCare Co. All rights reserved.</p>
                <nav className="sm:ml-auto flex gap-4 sm:gap-6">
                  <a className="text-xs hover:underline underline-offset-4" href="#">
                    Terms of Service
                      </a>
                  <a className="text-xs hover:underline underline-offset-4" href="#">
                    Privacy
                  </a>
                </nav>
              </footer>
            </div>
          )
            }
            ```
                """,
    },
    "blog app": {
        "prompt": "make me a personal blog",
        "response": """
        ```tsx
                import { useState } from 'react'
            import Link from 'next/link'
            import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "/components/ui/card"
            import { Button } from "/components/ui/button"
            import { ArrowLeft } from 'lucide-react'

            // Sample blog post data with full content
                    const blogPosts = [
      {
        id: 1,
        title: "Getting Started with Next.js",
        excerpt: "Learn how to build modern web applications with Next.js",
        date: "2023-06-01",
        readTime: "5 min read",
        content: "Next.js is a powerful React framework that makes it easy to build fast, SEO-friendly web applications.
        Here are some key features of Next.js:

          1. Server-Side Rendering (SSR): Next.js can render React components on the server, which improves initial load time and SEO.
          2. Static Site Generation (SSG): You can generate static HTML files at build time for even faster loading.
              3. API Routes: Next.js allows you to create API endpoints as part of your application.
                  4. File-based Routing: Simply create files in the 'pages' directory to define routes.
              5. Built-in CSS Support: Next.js supports CSS Modules, Sass, and other styling options out of the box.

          To get started with Next.js, you can use the following command: npx create-next-app@latest my-next-app"
          },
      {
        id: 2,
        title: "The Power of Tailwind CSS",
        excerpt: "Discover how Tailwind CSS can streamline your styling workflow",
        date: "2023-06-05",
        readTime: "4 min read",
        content: `
              Tailwind CSS is a utility-first CSS framework that can significantly speed up your development process.
                  Instead of writing custom CSS, you apply pre-existing classes directly in your HTML.

          Key benefits of Tailwind CSS include:

          1. Rapid Development: With utility classes, you can quickly style elements without switching between HTML and CSS files.
          2. Consistency: Tailwind provides a set of pre-defined design tokens, ensuring consistency across your project.
          3. Customization: You can easily customize the default configuration to match your design system.
              4. Responsive Design: Tailwind includes responsive utility variants, making it simple to create responsive layouts.
          5. Smaller File Sizes: When properly configured, Tailwind can eliminate unused CSS, resulting in smaller file sizes.

          To start using Tailwind CSS in your project, you can install it with npm: npm install tailwindcss

              Then, add the Tailwind directives to your CSS file and start using the utility classes in your HTML. Enjoy the power of Tailwind!
            `


          },
      {
        id: 3,
        title: "React Hooks Explained",
        excerpt: "Dive deep into React Hooks and how they can simplify your components",
        date: "2023-06-10",
        readTime: "6 min read",
        content: `
              React Hooks are functions that allow you to use state and other React features in functional components.
              They were introduced in React 16.8 and have revolutionized how we write React components.

                  Some of the most commonly used hooks are:

                  1. useState: Allows you to add state to functional components.
                  2. useEffect: Lets you perform side effects in functional components.
              3. useContext: Provides a way to pass data through the component tree without manually passing props.
              4. useReducer: An alternative to useState for managing complex state logic.
                  5. useCallback and useMemo: Help optimize performance by memoizing functions and values.

                  Here's a simple example using useState and useEffect:

              Hooks simplify your components and make it easier to reuse stateful logic between components.
                `
              },
      {
        id: 4,
        title: "Building Accessible Web Apps",
        excerpt: "Learn best practices for creating inclusive and accessible web applications",
        date: "2023-06-15",
        readTime: "7 min read",
        content: `
              Creating accessible web applications is crucial for ensuring that all users, including those with disabilities,
          can use your website effectively. Here are some key principles to follow:

          1. Semantic HTML: Use appropriate HTML elements for their intended purpose. For example, use <button> for buttons and <a> for links.
          2. ARIA attributes: When necessary, use ARIA (Accessible Rich Internet Applications) attributes to provide additional context to screen readers.
          3. Keyboard Navigation: Ensure that all interactive elements can be accessed and operated using only a keyboard.
              4. Color Contrast: Make sure there's sufficient color contrast between text and background for readability.
                  5. Alternative Text: Provide alt text for images to describe their content to users who can't see them.
                  6. Focus Management: Properly manage focus, especially in single-page applications and dynamic content.
          7. Responsive Design: Create layouts that adapt to different screen sizes and orientations.

              Remember, accessibility is not just about complying with guidelines—it's about creating a better user experience for everyone.
        `
          }
    ]

        export default function Blog() {
      const [selectedPost, setSelectedPost] = useState(null);

              return (
                <div className="min-h-screen flex flex-col">
          {/* Header */}
                  <header className="bg-primary text-primary-foreground shadow-lg">
            <div className="container mx-auto px-4 py-6 flex justify-between items-center">
              <h1 className="text-2xl font-bold">My Awesome Blog</h1>
              <nav>
                <ul className="flex space-x-4">
                  <li><Link href="/" className="hover:underline">Home</Link></li>
                  <li><Link href="/about" className="hover:underline">About</Link></li>
                  <li><Link href="/contact" className="hover:underline">Contact</Link></li>
                </ul>
              </nav>
            </div>
          </header>

          {/* Main Content */}
              <main className="flex-grow container mx-auto px-4 py-8">
            {selectedPost ? (
                      <div>
                <Button
                  variant="outline"
                      onClick={() => setSelectedPost(null)}
                                             className="mb-4"
                    >
                  <ArrowLeft className="mr-2 h-4 w-4" /> Back to all posts
                    </Button>
                <h2 className="text-3xl font-bold mb-2">{selectedPost.title}</h2>
                <p className="text-muted-foreground mb-4">{selectedPost.date} · {selectedPost.readTime}</p>
                <div className="prose max-w-none">
                  {selectedPost.content.split('\n').map((paragraph, index) => (
                    <p key={index} className="mb-4">{paragraph}</p>
                  ))}
                </div>
              </div>
            ) : (
              <>
                    <h2 className="text-3xl font-bold mb-6">Latest Posts</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {blogPosts.map((post) => (
                    <Card key={post.id}>
                      <CardHeader>
                        <CardTitle>{post.title}</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <p className="text-muted-foreground">{post.excerpt}</p>
                      </CardContent>
                      <CardFooter className="flex justify-between items-center">
                        <div className="text-sm text-muted-foreground">
                          {post.date} · {post.readTime}
                                                              </div>
                        <Button variant="outline" onClick={() => setSelectedPost(post)}>Read More</Button>
                      </CardFooter>
                    </Card>
                  ))}
                </div>
                  </>
                    )}
          </main>

          {/* Footer */}
              <footer className="bg-muted mt-8">
            <div className="container mx-auto px-4 py-6 text-center">
              <p>&copy; 2023 My Awesome Blog. All rights reserved.</p>
              <div className="mt-2">
                <Link href="/privacy" className="text-sm text-muted-foreground hover:underline mr-4">Privacy Policy</Link>
                <Link href="/terms" className="text-sm text-muted-foreground hover:underline">Terms of Service</Link>
              </div>
            </div>
          </footer>
        </div>
      )
    }
    ```
            """,
    },
    "calculator app": {
        "prompt": "make me a calculator app",
        "response": """
            I'll create a calculator app using React. This calculator will support basic arithmetic operations: addition, subtraction, multiplication, and division. Let's break it down into components and implement the functionality.

            ```tsx{filename=calculator.tsx}
            import { useState } from 'react'
                import { Button } from "/components/ui/button"
            import { Card, CardContent, CardHeader, CardTitle } from "/components/ui/card"

            export default function Calculator() {
          const [display, setDisplay] = useState('0')
                                                       const [firstOperand, setFirstOperand] = useState<number | null>(null)
                                                                                                                             const [operator, setOperator] = useState<string | null>(null)
                                                                                                                                                                                           const [waitingForSecondOperand, setWaitingForSecondOperand] = useState(false)

                                                                                                                                                                                                                                                                        const inputDigit = (digit: string) => {
            if (waitingForSecondOperand) {
              setDisplay(digit)
              setWaitingForSecondOperand(false)
                } else {
              setDisplay(display === '0' ? digit : display + digit)
                                 }
              }

          const inputDecimal = () => {
            if (waitingForSecondOperand) {
              setDisplay('0.')
              setWaitingForSecondOperand(false)
                  return
                }

            if (!display.includes('.')) {
              setDisplay(display + '.')
            }
          }

              const clear = () => {
            setDisplay('0')
            setFirstOperand(null)
                setOperator(null)
                setWaitingForSecondOperand(false)
              }

              const performOperation = (nextOperator: string) => {
            const inputValue = parseFloat(display)

                if (firstOperand === null) {
              setFirstOperand(inputValue)
            } else if (operator) {
              const result = calculate(firstOperand, inputValue, operator)
                  setDisplay(String(result))
                  setFirstOperand(result)
                }

            setWaitingForSecondOperand(true)
                                               setOperator(nextOperator)
              }

              const calculate = (firstOperand: number, secondOperand: number, operator: string) => {
                    switch (operator) {
                                      case '+':
                                        return firstOperand + secondOperand
                                      case '-':
                                        return firstOperand - secondOperand
                                      case '*':
                                        return firstOperand * secondOperand
                                      case '/':
                                        return firstOperand / secondOperand
                                      default:
                                        return secondOperand
                                    }
                             ">Calculator</CardTitle>
                                      </CardHeader>
                                      <Caro give the user an explanation on each question whether they go, setSelectedAnswer] = useState<string | null>(null)

                                                                                                                                                          const q    {
          question: "Which war was fought between the North and the South United States?",
          options: ["Revolutionary Wation abolished slavery?",
          options: ["13th", "14th", "15thn + 1} of {questions.length}</p>
                <p className="text-gra   }
                          disabled={showExplanation}
                                                  clag features:

        1. Five questions about American history
        2. Multipns cover various important aspects of American history, from the founding of the nation to constitutional amendments, making iault function PomodoroTimer() {
      const [mode, setMode] = useSt() => {
          if (interval) clearInterval(interval)
            }
      }, kBS+Jhi+EAuu+lKAkYUEIsmEAEoMeDmCETMvfSHTGkF5RWH7kz/ESHWPAq/kcCRpFBSLG9MCQALgAIgQs2YunOszLSAyQYPVC2YdGGeHD2dTdJk1pAHGAWDjnkcLKFAAAA3CUgShLdGIxsY7AUABPRrgCABdDuQ5GC7DqPQCgbbJUAoRSUj+NIEig0YfyWUho1VBBBA//uQZB4ABZx5zfMakeAAAAmwAAAAF5F3P0w9GtAAACfAAAAAwLhMD).padStart(2, "0")}:${secs.toString().padStart(2, "0")}`
          }

          const adjustTime = (type: 'focus' | 'break', amount: number)sName="space-y-6">
                  <div className="flex justify-centet-6xl font-bold mb-8">{formatTime(timeLeft)}</div>

                                    +
                          </Button>
                        rdContent>
              </Card>
            </div>
            ```
                """,
    },
}
