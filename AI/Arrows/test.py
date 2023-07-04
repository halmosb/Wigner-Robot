import torch
import torchvision.transforms as transforms
from PIL import Image
from arrow import Net, CustomDataset
import os
import glob
"""# Load the saved model
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

"""
model_path = 'Models/0012.model'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device ="cpu"
model = torch.jit.load(model_path).to(device)
model.eval()

transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])

dataset = CustomDataset("D:/ROBOTSTUFF/Data/AI/Arrow/test", transform=transform)

test_mode = "copy_wrong"

if test_mode == "normal":
    data_loader = torch.utils.data.DataLoader(dataset=dataset, batch_size=100, shuffle=False)
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


elif test_mode == "print_wrong":
    data_loader = torch.utils.data.DataLoader(dataset=dataset, batch_size=1, shuffle=False)
    # Define the image preprocessing transformations
    i = 0
    with torch.no_grad():
        correct = 0
        total = 0
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
            #print('Accuracy of the model on the test images: {} %'.format(100 * correct / total))
            if correct == 0:
                print(i, end=", ")


elif test_mode == "copy_wrong":
    labels = {0: "u", 1: "d", 2: "l", 3: "r"}
    dir = os.listdir("D:/ROBOTSTUFF/Data/AI/Arrow/test")

    files = glob.glob("D:/ROBOTSTUFF/Data/AI/Arrow/missed/*")
    for f in files:
        os.remove(f)

    #print(dir)
    for img_name in dir:
        image_path = f'D:/ROBOTSTUFF/Data/AI/Arrow/test/{img_name}'
        image = Image.open(image_path).convert('L')
        input_tensor = transform(image.resize((64,48))).unsqueeze(0).to(device)  # Add a batch dimension

        # Make predictions
        with torch.no_grad():
            output = model(input_tensor)

        # Get the predicted class
        _, predicted_class = torch.max(output, 1)
        if labels[predicted_class.item()] not in img_name:
            print(f"File: {img_name} -- Predicted class: {predicted_class.item()}={labels[predicted_class.item()]}", end="")
            os.system(f'copy D:\\ROBOTSTUFF\\Data\\AI\\Arrow\\test\\{img_name} D:\\ROBOTSTUFF\\Data\\AI\\Arrow\\missed\\{img_name}')
    exit(0)

    data_loader = torch.utils.data.DataLoader(dataset=dataset, batch_size=1, shuffle=False)
    # Define the image preprocessing transformations
    i = 0
    with torch.no_grad():
        correct = 0
        total = 0
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
            #print('Accuracy of the model on the test images: {} %'.format(100 * correct / total))
            if correct == 0:
                print(dir[i], end=", ")
                os.system(f'copy D:\\ROBOTSTUFF\\Data\\AI\\Arrow\\test\\{dir[i]} D:\\ROBOTSTUFF\\Data\\AI\\Arrow\\missed\\{dir[i]}')

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
