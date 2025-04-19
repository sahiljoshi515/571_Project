from Project import *
def get_compression(file_name):
    with open(file_name, "r") as file:
        sum = 0
        for line in file:
            # Process each line here
            compressed = run_length_encode(bwt_transform(line))
            compressed_bytes = compressed.encode("utf-8")
            sum +=len(compressed_bytes)
    return sum/21.0

def get_pcd(file1, file2):
    with open(file1, "r") as file1, open(file2, "r") as file2:
        sum = 0
        for line1, line2 in zip(file1, file2):
            # Process each line here
            compressed1 = run_length_encode(bwt_transform(line1))
            compressed2 = run_length_encode(bwt_transform(line2))
            Cx = compressed1.encode("utf-8")
            Cy = compressed2.encode("utf-8")
            sum += (abs(len(Cx) - len(Cy))/max(len(Cx), len(Cy)))
    return sum/21.0

HM = get_pcd("human.txt", "mouse.txt")
MF = get_pcd("mouse.txt", "frog.txt")
HF = get_pcd("human.txt", "frog.txt")

print("Human-Mouse:", HM)
print("Mouse-Frog:", MF)
print("Human-Frog:", HF)
