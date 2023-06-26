import torch
import torchvision.transforms as transforms
from PIL import Image
from arrow import ConvNet

# Load the saved model
model_path = 'model.ckpt'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = ConvNet(4).to(device)
model.load_state_dict(torch.load(model_path))
#exit(0)
model.eval()  # Set the model to evaluation mode

# Define the image preprocessing transformations
transform = transforms.Compose([
    transforms.Resize((32, 32)),  # Resize images to a consistent size
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # normalize inputs
])

# Load and preprocess the image
image_path = 'Learning Data/up/r0-0001.jpg'
image = Image.open(image_path).convert('RGB')
input_tensor = transform(image).unsqueeze(0).to(device)  # Add a batch dimension

# Make predictions
with torch.no_grad():
    output = model(input_tensor)

# Get the predicted class
_, predicted_class = torch.max(output, 1)

# Print the predicted class
print("Predicted class:", predicted_class.item())
