import torch
import torchvision.transforms as transforms
from PIL import Image
from arrow import Net


model_path = 'newer_arrow.pt'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
])
model = Net().to(device)
model.load_state_dict(torch.load(model_path))
#exit(0)
model.eval()  # Set the model to evaluation mode


# Load and preprocess the image
image_path = 'Learning Data/frames/r0-0001.jpg'
image = Image.open(image_path).convert('RGB')
input_tensor = transform(image.resize((64,48))).unsqueeze(0).to(device)  # Add a batch dimension

# Make predictions
with torch.no_grad():
    output = model(input_tensor)

# Get the predicted class
_, predicted_class = torch.max(output, 1)

# Print the predicted class
print("Predicted class:", predicted_class.item())
