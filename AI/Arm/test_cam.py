import torch
import torchvision.transforms as transforms
from PIL import Image
from arm import CustomDataset

# Load the saved model
model_path = 'Models/0002.model'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device ="cpu"
model = torch.jit.load(model_path).to(device)
model.eval()
transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
])

print(model)
exit(0)

dataset = CustomDataset("Learning Data/test", transform=transform)
data_loader = torch.utils.data.DataLoader(dataset=dataset, batch_size=50, shuffle=False)
# Define the image preprocessing transformations


with torch.no_grad():
        correct = 0
        total = 0
        i = 0
        for images, labels in data_loader:
            i += 1
            correct = 0
            total = 0
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            print('{} - {}:  Accuracy of the model on the test images: {} %'.format(i*50-50,i*50, 100 * correct / total))

# Load and preprocess the image
"""image_path = 'Learning Data/frames/r0-0001.jpg'
image = Image.open(image_path).convert('RGB')
input_tensor = transform(image).unsqueeze(0).to(device)  # Add a batch dimension

# Make predictions
with torch.no_grad():
    output = model(input_tensor)

# Get the predicted class
_, predicted_class = torch.max(output, 1)

# Print the predicted class
print("Predicted class:", predicted_class.item())"""
