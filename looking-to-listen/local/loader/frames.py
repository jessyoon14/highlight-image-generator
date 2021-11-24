from PIL import Image
import torch
import numpy as np
from typing import Union, List
from facenet_pytorch import MTCNN, InceptionResnetV1, extract_face

cpu_device = torch.device("cpu")


def input_face_embeddings(
    frames: Union[List[str], np.ndarray],
    is_path: bool,
    mtcnn: MTCNN,
    resnet: InceptionResnetV1,
    face_embed_cuda: bool,
    use_half: bool,
    coord: List,
    name: str = None,
    save_frames: bool = False,
) -> torch.Tensor:
    """
    Get the face embedding

    NOTE: If a face is not detected by the detector,
    instead of throwing an error it zeros the input
    for embedder.

    NOTE: Memory hungry function, hence the profiler.

    Args:
        frames: Frames from the video
        is_path: Whether to read from filesystem or memory
        mtcnn: face detector
        resnet: face embedder
        face_embed_cuda: use cuda for model
        use_half: use half precision

    Returns:
        emb: Embedding for all input frames
    """
    if face_embed_cuda and torch.cuda.is_available():
        device = torch.device("cuda:0")
    else:
        device = torch.device("cpu")
    result_cropped_tensors1 = []
    result_cropped_tensors2 = []
    no_face_indices1 = []
    no_face_indices2 = []
    
    # detect initial face position in first frame
    first_frame = frames[0]
    bounding_box, prob = mtcnn.detect(first_frame)
    
    if len(prob) < 2:
        print("ERR: Can't detect two face from first frame")
        return (None, None)

    # detect face 1
    box1 = bounding_box[0, :]
    face1_x, face1_y = ((box1[0] + box1[2])//2, (box1[1] + box1[3])//2)

    # detect face 2
    box2 = bounding_box[1, :]
    face2_x, face2_y = ((box2[0] + box2[2])//2, (box2[1] + box2[3])//2)


    for i, f in enumerate(frames):
        if is_path:
            frame = Image.open(f)
        else:
            frame = Image.fromarray(f.astype("uint8"))

        with torch.no_grad():
            cropped_tensors = None
            height, width, c = f.shape
            bounding_box, prob = mtcnn.detect(frame)

            if len(prob) < 2:
                print("ERR: Can't detect two face")
                return (None, None)
            
            if bounding_box is not None:
                face1_found = False
                face2_found = False
                for box in bounding_box:
                    x1, y1, x2, y2 = box
                    if x1 > x2:
                        x1, x2 = x2, x1
                    if y1 > y2:
                        y1, y2 = y2, y1

                    if face1_x >= x1 and face1_y >= y1 and face1_x <= x2 and face1_y <= y2:
                        cropped_tensors1 = extract_face(frame, box)
                        face1_found = True
                        # print("found", box, x, y, end='\r')

                    if face2_x >= x1 and face2_y >= y1 and face2_x <= x2 and face2_y <= y2:
                        cropped_tensors2 = extract_face(frame, box)
                        face2_found = True
                        # print("found", box, x, y, end='\r')
                    
                    if face1_found and face2_found:
                        break
        
        # if face1 not found
        if cropped_tensors1 is None:
            cropped_tensors1 = torch.zeros((3, 160, 160))
            no_face_indices1.append(i)

        # if face2 not found
        if cropped_tensors2 is None:
            cropped_tensors2 = torch.zeros((3, 160, 160))
            no_face_indices2.append(i)

        
        if save_frames:
            name = name.replace(".mp4", "")
            saveimg = cropped_tensors.detach().cpu().numpy().astype("uint8")
            saveimg = np.squeeze(saveimg.transpose(1, 2, 0))
            Image.fromarray(saveimg).save(f"{name}_{i}_face1.png")

            name = name.replace(".mp4", "")
            saveimg = cropped_tensors.detach().cpu().numpy().astype("uint8")
            saveimg = np.squeeze(saveimg.transpose(1, 2, 0))
            Image.fromarray(saveimg).save(f"{name}_{i}_face2.png")

        result_cropped_tensors1.append(cropped_tensors1.to(device))
        result_cropped_tensors2.append(cropped_tensors2.to(device))

    if len(no_face_indices1) > 20 or len(no_face_indices2) > 20:
        # few videos start with silence, allow 0.5 seconds of silence else remove
        return (None, None)
    del frames

    # Stack all frames
    result_cropped_tensors1 = torch.stack(result_cropped_tensors1)
    result_cropped_tensors2 = torch.stack(result_cropped_tensors2)

    # Embed all frames
    result_cropped_tensors1 = result_cropped_tensors1.to(device)
    result_cropped_tensors2 = result_cropped_tensors2.to(device)
    
    if use_half:
        result_cropped_tensors1 = result_cropped_tensors1.half()
        result_cropped_tensors2 = result_cropped_tensors2.half()

    with torch.no_grad():
        emb1 = resnet(result_cropped_tensors1)
        emb2 = resnet(result_cropped_tensors2)
    if use_half:
        emb1 = emb1.float()
        emb2 = emb2.float()
    
    result1 = emb1.to(cpu_device)
    result2 = emb2.to(cpu_device)
    
    
    return result1, result2

if __name__ == "__main__":
    mtcnn = MTCNN(keep_all=True).eval()
    resnet = InceptionResnetV1(pretrained="vggface2").eval()
    device = torch.device("cpu")
    res = input_face_embeddings(["a.jpg", "b.jpg"], True, mtcnn, resnet, device)
    print(res.shape)  # 512D
    print("Passed")
