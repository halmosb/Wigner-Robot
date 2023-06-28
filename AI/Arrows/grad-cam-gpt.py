import torch
from torch.autograd import Function
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from arrow import Net

class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradient = None

        self.model.eval()
        self._register_hooks()

    def _register_hooks(self):
        def backward_hook(module, grad_input, grad_output):
            self.gradient = grad_output[0]

        target_layer = self.target_layer
        if isinstance(target_layer, str):
            target_layer = dict(self.model.named_modules())[target_layer]

        target_layer.register_backward_hook(backward_hook)

    def _forward_pass(self, x):
        self.model.zero_grad()
        return self.model(x)

    def _backward_pass(self, outputs):
        one_hot = torch.zeros_like(outputs)
        one_hot[0, outputs.argmax()] = 1
        outputs.backward(gradient=one_hot, retain_graph=True)

    def generate_heatmap(self, input_image):
        input_image = input_image.float().unsqueeze(0)
        output = self._forward_pass(input_image)
        self._backward_pass(output)
    
        gradient = self.gradient.detach().squeeze(0)
        activations = self.target_layer_output.detach().squeeze(0)
    
        weights = torch.mean(gradient, dim=(1, 2), keepdim=True)
        cam = torch.sum(weights * activations, dim=0)
        cam = np.maximum(cam, 0)  # ReLU
    
        # Normalize the heatmap between 0 and 1
        cam = cam - torch.min(cam)
        cam = cam / torch.max(cam)
    
        cam = cam.numpy()
        cam = cv2.resize(cam, input_image.shape[2:][::-1])
        cam = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    
        # Overlay the heatmap on the input image
        output_image = np.float32(cam) + np.float32(input_image.squeeze(0).permute(1, 2, 0))
        output_image = output_image / np.max(output_image)
    
        return np.uint8(255 * output_image)


# Usage example
net = Net()
grad_cam = GradCAM(net, target_layer=net.conv3)  # Choose the target layer for visualization

# Assuming you have an input image file called "input_image.jpg"
input_image_path = "Learning Data/frames/u0-0132.jpg"
input_image = Image.open(input_image_path).convert("L").resize((64,48))  # Read and convert to grayscale
input_image = np.array(input_image)  # Convert to numpy array
input_image = torch.from_numpy(input_image).unsqueeze(0)  # Convert to tensor and add batch dimension

heatmap_image = grad_cam.generate_heatmap(input_image)

# Display the input image and heatmap side by side
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].imshow(input_image.squeeze(0), cmap='gray')
axes[0].axis('off')
axes[0].set_title('Input Image')
axes[1].imshow(heatmap_image)
axes[1].axis('off')
axes[1].set_title('Heatmap')

plt.show()
