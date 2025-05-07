from flask import Flask, request, jsonify
from flask_cors import CORS
from modelscope import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)
CORS(app)

# 初始化模型和分词器
# model_path = "/home/zhiqiang/test/ai_demo/models/Qwen1.5-0.5B-Chat" 
model_path = "./models/Qwen1.5-0.5B-Chat"  # 更新为完整的模型路径
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True)
model = model.eval()

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': '消息不能为空'}), 400

        messages = [{"role": "user", "content": user_message}]
        input_ids = tokenizer.apply_chat_template(
            messages,
            return_tensors="pt"
        ).to(model.device)

        # 生成回复
        with torch.no_grad():
            outputs = model.generate(
                input_ids,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
            )
        
        response = tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)
        
        return jsonify({
            'status': 'success',
            'response': response,
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 