import Together from "together-ai";

// 创建一个 Together API 客户端实例
const client = new Together({
  apiKey: "BB77WM98VGMSTxAW", // 确保在你的环境变量中设置了 TOGETHER_API_KEY
});

// 定义一个异步函数用于发送消息并获取响应
export async function getChatCompletion(messages) {
  try {
    const chatCompletion = await client.chat.completions.create({
      messages: messages,
      model: "mistralai/Mixtral-8x7B-Instruct-v0.1", // 根据需要选择模型
    });

    return chatCompletion.choices;
  } catch (err) {
    if (err instanceof Together.APIError) {
      console.error("API Error:", err.status, err.name, err.headers);
    } else {
      console.error("Unexpected Error:", err);
    }
    throw err;
  }
}
