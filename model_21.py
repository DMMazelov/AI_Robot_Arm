import torch
from torch.utils.data import Dataset, DataLoader
import cv2
import os
import numpy as np

class HandDataset(Dataset):
    def init(self, images_folder, annotations_file, transform=None):
        self.images_folder = images_folder
        self.transform = transform
        
        self.annotations = np.load(annotations_file)  
        self.image_files = sorted(os.listdir(images_folder))

    def len(self):
        return len(self.image_files)

    def getitem(self, idx):
        img_path = os.path.join(self.images_folder, self.image_files[idx])
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (256, 256))
        keypoints = self.annotations[idx]  
        keypoints = keypoints.flatten()    

        image = image / 255.0  
        image = torch.tensor(image, dtype=torch.float32).permute(2, 0, 1)         keypoints = torch.tensor(keypoints, dtype=torch.float32)

        return image, keypointsimport torch.nn as nn

class HandPoseNet(nn.Module):
    def init(self):
        super().init()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 3, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d(1)
        )
        self.fc = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 42) 
        )

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)

import torch.optim as optim
train_dataset = HandDataset("train_images", "train_annotations.npy")
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = HandPoseNet().to(device)
criterion = nn.MSELoss()  
optimizer = optim.Adam(model.parameters(), lr=1e-3)
num_epochs = 50
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    for images, keypoints in train_loader:
        images = images.to(device)
        keypoints = keypoints.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, keypoints)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {total_loss/len(train_loader):.4f}")
torch.save(model.state_dict(), "hand_pose_model.pth")
def predict_hand(image, model):
    model.eval()
    img = cv2.resize(image, (256,256))
    img_tensor = torch.tensor(img/255.0, dtype=torch.float32).permute(2,0,1).unsqueeze(0).to(device)
    with torch.no_grad():
        keypoints = model(img_tensor).cpu().numpy().reshape(-1,2)
    h, w = image.shape[:2]
    keypoints[:,0] *= w
    keypoints[:,1] *= h
    return keypoints
