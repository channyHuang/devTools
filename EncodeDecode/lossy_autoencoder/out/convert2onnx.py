import torch
import onnx 

model = torch.load('main.tar')

model.eval()

input_shape = (1, 3, 224, 224)
dummy_input = torch.randn(*input_shape)

onnx_path = "your_model.onnx"
torch.onnx.export(model, dummy_input, onnx_path)

print(f"模型已成功转换为ONNX格式，保存在 {onnx_path}")

