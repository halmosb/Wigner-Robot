import torch
import torchvision.transforms as transforms
from PIL import Image
from arrow import Net, CustomDataset

# Load the saved model
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

dataset = CustomDataset("Learning Data/test3", transform=transform)
data_loader = torch.utils.data.DataLoader(dataset=dataset, batch_size=50, shuffle=False)
# Define the image preprocessing transformations


with torch.no_grad():
        correct = 0
        total = 0
        for images, labels in data_loader:
            correct = 0
            total = 0
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            print('Accuracy of the model on the test images: {} %'.format(100 * correct / total))

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
