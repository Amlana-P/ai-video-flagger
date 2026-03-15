import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import cv2
from frequency_detector import frequency_score

model = models.resnet18(weights="DEFAULT")

model.fc = torch.nn.Linear(512,1)

model.eval()

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

def analyze_video(frames):

    cnn_scores = []
    freq_scores = []

    for frame in frames:

        img = Image.open(frame).convert("RGB")

        tensor = transform(img).unsqueeze(0)

        with torch.no_grad():

            output = torch.sigmoid(model(tensor))

        cnn_scores.append(output.item())

        freq_scores.append(
            frequency_score(
                cv2.imread(frame)
            )
        )

    cnn_avg = sum(cnn_scores)/len(cnn_scores)

    freq_avg = sum(freq_scores)/len(freq_scores)

    probability = (0.7 * cnn_avg) + (0.3 * freq_avg)

    probability = max(0, min(probability, 1))

    return {
        "ai_probability": probability
    }